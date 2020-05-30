# -*- coding: utf-8 -*-
"""
Coordinate Transformation Functions

This module contains the functions for converting one
`sunpy.coordinates.frames` object to another.

.. warning::

  The functions in this submodule should never be called directly, transforming
  between coordinate frames should be done using the ``.transform_to`` methods
  on `~astropy.coordinates.BaseCoordinateFrame` or
  `~astropy.coordinates.SkyCoord` instances.

"""
import logging
from copy import deepcopy
from functools import wraps

import numpy as np

import astropy.units as u
from astropy._erfa import obl06
from astropy.coordinates import (HCRS, ICRS, BaseCoordinateFrame, ConvertError,
                                 get_body_barycentric, get_body_barycentric_posvel)
from astropy.coordinates.baseframe import frame_transform_graph
from astropy.coordinates.builtin_frames.utils import get_jd12
from astropy.coordinates.matrix_utilities import matrix_product, matrix_transpose, rotation_matrix
from astropy.coordinates.representation import (CartesianDifferential, CartesianRepresentation,
                                                SphericalRepresentation,
                                                UnitSphericalRepresentation)
from astropy.coordinates.transformations import (AffineTransform, FunctionTransform,
                                                 FunctionTransformWithFiniteDifference)

from sunpy import log
from sunpy.sun import constants

from .frames import (_J2000, GeocentricEarthEquatorial, GeocentricSolarEcliptic,
                     Heliocentric, HeliocentricEarthEcliptic, HeliocentricInertial,
                     HeliographicCarrington, HeliographicStonyhurst, Helioprojective)

# Versions of Astropy that do not have HeliocentricMeanEcliptic have the same frame
# with the incorrect name HeliocentricTrueEcliptic
try:
    from astropy.coordinates import HeliocentricMeanEcliptic
except ImportError:
    from astropy.coordinates import HeliocentricTrueEcliptic as HeliocentricMeanEcliptic

try:
    from astropy.coordinates.builtin_frames import _make_transform_graph_docs as make_transform_graph_docs
except ImportError:
    from astropy.coordinates import make_transform_graph_docs as _make_transform_graph_docs
    make_transform_graph_docs = lambda: _make_transform_graph_docs(frame_transform_graph)


RSUN_METERS = constants.get('radius').si.to(u.m)

__all__ = ['hgs_to_hgc', 'hgc_to_hgs', 'hcc_to_hpc',
           'hpc_to_hcc', 'hcc_to_hgs', 'hgs_to_hcc',
           'hpc_to_hpc',
           'hcrs_to_hgs', 'hgs_to_hcrs',
           'hgs_to_hgs', 'hgc_to_hgc', 'hcc_to_hcc',
           'hme_to_hee', 'hee_to_hme', 'hee_to_hee',
           'hee_to_gse', 'gse_to_hee', 'gse_to_gse',
           'hgs_to_hci', 'hci_to_hgs', 'hci_to_hci',
           'hme_to_gei', 'gei_to_hme', 'gei_to_gei']


# Global counter to keep track of the layer of transformation
_layer_level = 0


def _transformation_debug(description):
    """
    Decorator to produce debugging output for a transformation function: its description, inputs,
    and output.  Unicode box-drawing characters are used.
    """
    def decorator(func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            global _layer_level

            # Check if the logging level is at least DEBUG (for performance reasons)
            debug_output = log.getEffectiveLevel() <= logging.DEBUG

            if debug_output:
                # Indention for transformation layer
                indention = u"\u2502   " * _layer_level

                # For the input arguments, add indention to any lines after the first line
                from_str = str(args[0]).replace("\n", f"\n       {indention}\u2502       ")
                to_str = str(args[1]).replace("\n", f"\n       {indention}\u2502       ")

                # Log the description and the input arguments
                log.debug(f"{indention}{description}")
                log.debug(f"{indention}\u251c\u2500From: {from_str}")
                log.debug(f"{indention}\u251c\u2500To  : {to_str}")

                # Increment the layer level to increase the indention for nested transformations
                _layer_level += 1

            result = func(*args, **kwargs)

            if debug_output:
                # Decrement the layer level
                _layer_level -= 1

                # For the output, add intention to any lines after the first line
                out_str = str(result).replace("\n", f"\n       {indention}        ")

                # Log the output
                log.debug(f"{indention}\u2514\u2500Out : {out_str}")

            return result
        return wrapped_func
    return decorator


def _observers_are_equal(obs_1, obs_2):
    # Note that this also lets pass the situation where both observers are None
    if obs_1 is obs_2:
        return True

    # obs_1 != obs_2
    if obs_1 is None:
        raise ConvertError("The source observer is set to None, but the destination observer is "
                           f"{obs_2}.")
    if obs_2 is None:
        raise ConvertError("The destination observer is set to None, but the source observer is "
                           f"{obs_2}.")
    if isinstance(obs_1, str):
        raise ConvertError("The source observer needs to have `obstime` set because the "
                           "destination observer is different.")
    if isinstance(obs_2, str):
        raise ConvertError("The destination observer needs to have `obstime` set because the "
                           "source observer is different.")

    return np.atleast_1d((u.allclose(obs_1.lat, obs_2.lat) and
                          u.allclose(obs_1.lon, obs_2.lon) and
                          u.allclose(obs_1.radius, obs_2.radius) and
                          obs_1.obstime == obs_2.obstime)).all()


def _check_observer_defined(frame):
    if frame.observer is None:
        raise ConvertError("This transformation cannot be performed because the "
                           f"{frame.__class__.__name__} frame has observer=None.")
    elif isinstance(frame.observer, str):
        raise ConvertError("This transformation cannot be performed because the "
                           f"{frame.__class__.__name__} frame needs a specified obstime "
                           f"to fully resolve observer='{frame.observer}'.")


# =============================================================================
# ------------------------- Transformation Framework --------------------------
# =============================================================================


def _transform_obstime(frame, obstime):
    """
    Transform a frame to a new obstime using the appropriate loopback transformation.
    If the new obstime is None, no transformation is performed.
    If the frame's obstime is None, the frame is copied with the new obstime.
    """
    # If obstime is None or the obstime matches, nothing needs to be done
    if obstime is None or np.all(frame.obstime == obstime):
        return frame

    # Transform to the new obstime using the appropriate loopback transformation
    new_frame = frame.replicate(obstime=obstime)
    if frame.obstime is not None:
        return frame.transform_to(new_frame)
    else:
        return new_frame


def _rotation_matrix_hgs_to_hgc(obstime):
    """
    Return the rotation matrix from HGS to HGC at the same observation time
    """
    if obstime is None:
        raise ValueError("To perform this transformation the coordinate"
                         " Frame needs an obstime Attribute")

    # Import here to avoid a circular import
    from .sun import L0

    # Rotation is only in longitude, so only around the Z axis
    return rotation_matrix(-L0(obstime), 'z')


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference,
                                 HeliographicStonyhurst, HeliographicCarrington)
@_transformation_debug("HGS->HGC")
def hgs_to_hgc(hgscoord, hgcframe):
    """
    Convert from Heliographic Stonyhurst to Heliographic Carrington.
    """
    # First transform the HGS coord to the HGC obstime
    int_coord = _transform_obstime(hgscoord, hgcframe.obstime)

    # Rotate from HGS to HGC
    total_matrix = _rotation_matrix_hgs_to_hgc(int_coord.obstime)
    newrepr = int_coord.cartesian.transform(total_matrix)

    return hgcframe._replicate(newrepr, obstime=int_coord.obstime)


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference,
                                 HeliographicCarrington, HeliographicStonyhurst)
@_transformation_debug("HGC->HGS")
def hgc_to_hgs(hgccoord, hgsframe):
    """
    Convert from Heliographic Carrington to Heliographic Stonyhurst.
    """
    # First transform the HGC coord to the HGS obstime
    int_coord = _transform_obstime(hgccoord, hgsframe.obstime)

    # Rotate from HGC to HGS
    total_matrix = matrix_transpose(_rotation_matrix_hgs_to_hgc(int_coord.obstime))
    newrepr = int_coord.cartesian.transform(total_matrix)

    return hgsframe._replicate(newrepr, obstime=int_coord.obstime)


def _matrix_hcc_to_hpc():
    # Returns the transformation matrix that permutes/swaps axes from HCC to HPC

    # HPC spherical coordinates are a left-handed frame with these equivalent Cartesian axes:
    #   HPC_X = -HCC_Z
    #   HPC_Y = HCC_X
    #   HPC_Z = HCC_Y
    # (HPC_X and HPC_Y are not to be confused with HPC_Tx and HPC_Ty)
    return np.array([[0, 0, -1],
                     [1, 0, 0],
                     [0, 1, 0]])


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference,
                                 Heliocentric, Helioprojective)
@_transformation_debug("HCC->HPC")
def hcc_to_hpc(helioccoord, heliopframe):
    """
    Convert from Heliocentric Cartesian to Helioprojective Cartesian.
    """
    _check_observer_defined(helioccoord)
    _check_observer_defined(heliopframe)

    # Transform the HPC observer (in HGS) to the HPC obstime in case it's different
    observer = _transform_obstime(heliopframe.observer, heliopframe.obstime)

    # Loopback transform HCC coord to obstime and observer of HPC frame
    int_frame = Heliocentric(obstime=observer.obstime, observer=observer)
    int_coord = helioccoord.transform_to(int_frame)

    # Shift the origin from the Sun to the observer
    distance = int_coord.observer.radius
    newrepr = int_coord.cartesian - CartesianRepresentation(0*u.m, 0*u.m, distance)

    # Permute/swap axes from HCC to HPC equivalent Cartesian
    newrepr = newrepr.transform(_matrix_hcc_to_hpc())

    # Explicitly represent as spherical because external code (e.g., wcsaxes) expects it
    return heliopframe.realize_frame(newrepr.represent_as(SphericalRepresentation))


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference,
                                 Helioprojective, Heliocentric)
@_transformation_debug("HPC->HCC")
def hpc_to_hcc(heliopcoord, heliocframe):
    """
    Convert from Helioprojective Cartesian to Heliocentric Cartesian.
    """
    _check_observer_defined(heliopcoord)
    _check_observer_defined(heliocframe)

    heliopcoord = heliopcoord.make_3d()

    # Permute/swap axes from HPC equivalent Cartesian to HCC
    newrepr = heliopcoord.cartesian.transform(matrix_transpose(_matrix_hcc_to_hpc()))

    # Transform the HPC observer (in HGS) to the HPC obstime in case it's different
    observer = _transform_obstime(heliopcoord.observer, heliopcoord.obstime)

    # Shift the origin from the observer to the Sun
    distance = observer.radius
    newrepr += CartesianRepresentation(0*u.m, 0*u.m, distance)

    # Complete the conversion of HPC to HCC at the obstime and observer of the HPC coord
    int_coord = Heliocentric(newrepr, obstime=observer.obstime, observer=observer)

    # Loopback transform HCC as needed
    return int_coord.transform_to(heliocframe)


def _rotation_matrix_hcc_to_hgs(longitude, latitude):
    # Returns the rotation matrix from HCC to HGS based on the observer longitude and latitude

    # Permute the axes of HCC to match HGS Cartesian equivalent
    #   HGS_X = HCC_Z
    #   HGS_Y = HCC_X
    #   HGS_Z = HCC_Y
    axes_matrix = np.array([[0, 0, 1],
                            [1, 0, 0],
                            [0, 1, 0]])

    # Rotate in latitude and longitude (sign difference because of direction difference)
    lat_matrix = rotation_matrix(latitude, 'y')
    lon_matrix = rotation_matrix(-longitude, 'z')

    return lon_matrix @ lat_matrix @ axes_matrix


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference,
                                 Heliocentric, HeliographicStonyhurst)
@_transformation_debug("HCC->HGS")
def hcc_to_hgs(helioccoord, heliogframe):
    """
    Convert from Heliocentric Cartesian to Heliographic Stonyhurst.
    """
    _check_observer_defined(helioccoord)

    # Transform the HCC observer (in HGS) to the HCC obstime in case it's different
    hcc_observer_at_hcc_obstime = _transform_obstime(helioccoord.observer, helioccoord.obstime)

    total_matrix = _rotation_matrix_hcc_to_hgs(hcc_observer_at_hcc_obstime.lon,
                                               hcc_observer_at_hcc_obstime.lat)

    # Transform from HCC to HGS at the HCC obstime
    newrepr = helioccoord.cartesian.transform(total_matrix)
    int_coord = HeliographicStonyhurst(newrepr, obstime=hcc_observer_at_hcc_obstime.obstime)

    # Loopback transform HGS if there is a change in obstime
    return _transform_obstime(int_coord, heliogframe.obstime)


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference,
                                 HeliographicStonyhurst, Heliocentric)
@_transformation_debug("HGS->HCC")
def hgs_to_hcc(heliogcoord, heliocframe):
    """
    Convert from Heliographic Stonyhurst to Heliocentric Cartesian.
    """
    _check_observer_defined(heliocframe)

    # Loopback transform HGS if there is a change in obstime
    int_coord = _transform_obstime(heliogcoord, heliocframe.obstime)

    # Transform the HCC observer (in HGS) to the HCC obstime in case it's different
    hcc_observer_at_hcc_obstime = _transform_obstime(heliocframe.observer, int_coord.obstime)

    total_matrix = matrix_transpose(_rotation_matrix_hcc_to_hgs(hcc_observer_at_hcc_obstime.lon,
                                                                hcc_observer_at_hcc_obstime.lat))

    # Transform from HGS to HCC at the same obstime
    newrepr = int_coord.cartesian.transform(total_matrix)
    return heliocframe.realize_frame(newrepr)


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference,
                                 Helioprojective, Helioprojective)
@_transformation_debug("HPC->HPC")
def hpc_to_hpc(from_coo, to_frame):
    """
    This converts from HPC to HPC, with different observer location parameters.
    It does this by transforming through HGS.
    """
    if _observers_are_equal(from_coo.observer, to_frame.observer) and \
       np.all(from_coo.obstime == to_frame.obstime):
        return to_frame.realize_frame(from_coo.data)

    _check_observer_defined(from_coo)
    _check_observer_defined(to_frame)

    hgs = from_coo.transform_to(HeliographicStonyhurst(obstime=to_frame.obstime))
    hpc = hgs.transform_to(to_frame)

    return hpc


def _rotation_matrix_reprs_to_reprs(start_representation, end_representation):
    """
    Return the matrix for the direct rotation from one representation to a second representation.
    The representations need not be normalized first, and can be arrays of representations.
    """
    A = start_representation.to_cartesian()
    B = end_representation.to_cartesian()
    rotation_axis = A.cross(B)
    rotation_angle = -np.arccos(A.dot(B) / (A.norm() * B.norm()))  # negation is required

    if rotation_angle.isscalar:
        # This line works around some input/output quirks of Astropy's rotation_matrix()
        matrix = np.array(rotation_matrix(rotation_angle, rotation_axis.xyz.value.tolist()))
    else:
        matrix_list = [np.array(rotation_matrix(angle, axis.xyz.value.tolist()))
                       for angle, axis in zip(rotation_angle, rotation_axis)]
        matrix = np.stack(matrix_list)

    return matrix


def _rotation_matrix_reprs_to_xz_about_z(representations):
    """
    Return one or more matrices for rotating one or more representations around the Z axis into the
    XZ plane.
    """
    A = representations.to_cartesian()

    # Zero out the Z components
    # (The additional transpose operations are to handle both scalar and array inputs)
    A_no_z = CartesianRepresentation((A.xyz.T * [1, 1, 0]).T)

    # Rotate the resulting vector to the X axis
    x_axis = CartesianRepresentation(1, 0, 0)
    matrix = _rotation_matrix_reprs_to_reprs(A_no_z, x_axis)

    return matrix


def _sun_earth_icrf(time):
    """
    Return the Sun-Earth vector for ICRF-based frames.
    """
    sun_pos_icrs = get_body_barycentric('sun', time)
    earth_pos_icrs = get_body_barycentric('earth', time)
    return earth_pos_icrs - sun_pos_icrs


# The Sun's north pole is oriented RA=286.13 deg, dec=63.87 deg in ICRS, and thus HCRS as well
# (See Archinal et al. 2011,
#   "Report of the IAU Working Group on Cartographic Coordinates and Rotational Elements: 2009")
# The orientation of the north pole in ICRS/HCRS is assumed to be constant in time
_SOLAR_NORTH_POLE_HCRS = UnitSphericalRepresentation(lon=286.13*u.deg, lat=63.87*u.deg)


# Calculate the rotation matrix to de-tilt the Sun's rotation axis to be parallel to the Z axis
_SUN_DETILT_MATRIX = _rotation_matrix_reprs_to_reprs(_SOLAR_NORTH_POLE_HCRS,
                                                     CartesianRepresentation(0, 0, 1))


@frame_transform_graph.transform(AffineTransform, HCRS, HeliographicStonyhurst)
@_transformation_debug("HCRS->HGS (affine transformation)")
def hcrs_to_hgs(hcrscoord, hgsframe):
    """
    Convert from HCRS to Heliographic Stonyhurst (HGS).

    HGS shares the same origin (the Sun) as HCRS, but has its Z axis aligned with the Sun's
    rotation axis and its X axis aligned with the projection of the Sun-Earth vector onto the Sun's
    equatorial plane (i.e., the component of the Sun-Earth vector perpendicular to the Z axis).
    Thus, the transformation matrix is the product of the matrix to align the Z axis (by de-tilting
    the Sun's rotation axis) and the matrix to align the X axis.  The first matrix is independent
    of time and is pre-computed, while the second matrix depends on the time-varying Sun-Earth
    vector.
    """
    if hgsframe.obstime is None:
        raise ValueError("To perform this transformation the coordinate"
                         " Frame needs an obstime Attribute")

    # Check whether differentials are involved on either end
    has_differentials = ((hcrscoord._data is not None and hcrscoord.data.differentials) or
                         (hgsframe._data is not None and hgsframe.data.differentials))

    # Determine the Sun-Earth vector in ICRS
    # Since HCRS is ICRS with an origin shift, this is also the Sun-Earth vector in HCRS
    # If differentials exist, also obtain Sun and Earth velocities
    if has_differentials:
        sun_pos_icrs, sun_vel = get_body_barycentric_posvel('sun', hgsframe.obstime)
        earth_pos_icrs, earth_vel = get_body_barycentric_posvel('earth', hgsframe.obstime)
    else:
        sun_pos_icrs = get_body_barycentric('sun', hgsframe.obstime)
        earth_pos_icrs = get_body_barycentric('earth', hgsframe.obstime)
    sun_earth = earth_pos_icrs - sun_pos_icrs

    # De-tilt the Sun-Earth vector to the frame with the Sun's rotation axis parallel to the Z axis
    sun_earth_detilt = sun_earth.transform(_SUN_DETILT_MATRIX)

    # Rotate the Sun-Earth vector about the Z axis so that it lies in the XZ plane
    rot_matrix = _rotation_matrix_reprs_to_xz_about_z(sun_earth_detilt)

    total_matrix = rot_matrix @ _SUN_DETILT_MATRIX

    # All of the above is calculated for the HGS observation time
    # If the HCRS observation time is different, calculate the translation in origin
    if np.any(hcrscoord.obstime != hgsframe.obstime):
        sun_pos_old_icrs = get_body_barycentric('sun', hcrscoord.obstime)
        offset_icrf = sun_pos_icrs - sun_pos_old_icrs
    else:
        offset_icrf = sun_pos_icrs * 0  # preserves obstime shape

    # Add velocity if needed (at the HGS observation time)
    if has_differentials:
        vel_icrf = (sun_vel - earth_vel).represent_as(CartesianDifferential)
        offset_icrf = offset_icrf.with_differentials(vel_icrf)

    offset = offset_icrf.transform(total_matrix)
    return total_matrix, offset


@frame_transform_graph.transform(AffineTransform, HeliographicStonyhurst, HCRS)
@_transformation_debug("HGS->HCRS (affine transformation)")
def hgs_to_hcrs(hgscoord, hcrsframe):
    """
    Convert from Heliographic Stonyhurst to HCRS.
    """
    # Calculate the matrix and offset in the HCRS->HGS direction
    total_matrix, offset = hcrs_to_hgs(hcrsframe, hgscoord)

    # Invert the transformation to get the HGS->HCRS transformation
    reverse_matrix = matrix_transpose(total_matrix)
    # If differentials exist, properly negate the velocity
    if offset.differentials:
        pos = -offset.without_differentials()
        vel = -offset.differentials['s']
        offset = pos.with_differentials(vel)
    else:
        offset = -offset
    reverse_offset = offset.transform(reverse_matrix)

    return reverse_matrix, reverse_offset


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference,
                                 HeliographicStonyhurst, HeliographicStonyhurst)
@_transformation_debug("HGS->HGS")
def hgs_to_hgs(from_coo, to_frame):
    """
    Convert between two Heliographic Stonyhurst frames.
    """
    if to_frame.obstime is None:
        return from_coo.replicate()
    elif np.all(from_coo.obstime == to_frame.obstime):
        return to_frame.realize_frame(from_coo.data)
    else:
        return from_coo.transform_to(HCRS(obstime=from_coo.obstime)).transform_to(to_frame)


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference,
                                 HeliographicCarrington, HeliographicCarrington)
@_transformation_debug("HGC->HGC")
def hgc_to_hgc(from_coo, to_frame):
    """
    Convert between two Heliographic Carrington frames.
    """
    if np.all(from_coo.obstime == to_frame.obstime):
        return to_frame.realize_frame(from_coo.data)
    else:
        return from_coo.transform_to(HeliographicStonyhurst(obstime=from_coo.obstime)).\
               transform_to(to_frame)


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference,
                                 Heliocentric, Heliocentric)
@_transformation_debug("HCC->HCC")
def hcc_to_hcc(from_coo, to_frame):
    """
    Convert between two Heliocentric frames.
    """
    if _observers_are_equal(from_coo.observer, to_frame.observer) and \
       np.all(from_coo.obstime == to_frame.obstime):
        return to_frame.realize_frame(from_coo.data)

    _check_observer_defined(from_coo)
    _check_observer_defined(to_frame)

    # Convert through HGS
    hgscoord = from_coo.transform_to(HeliographicStonyhurst(obstime=to_frame.obstime))

    return hgscoord.transform_to(to_frame)


def _rotation_matrix_hme_to_hee(hmeframe):
    """
    Return the rotation matrix from HME to HEE at the same observation time
    """
    # Get the Sun-Earth vector
    sun_earth = HCRS(_sun_earth_icrf(hmeframe.obstime), obstime=hmeframe.obstime)
    sun_earth_hme = sun_earth.transform_to(hmeframe).cartesian

    # Rotate the Sun-Earth vector about the Z axis so that it lies in the XZ plane
    rot_matrix = _rotation_matrix_reprs_to_xz_about_z(sun_earth_hme)

    # Tilt the rotated Sun-Earth vector so that it is aligned with the X axis
    tilt_matrix = _rotation_matrix_reprs_to_reprs(sun_earth_hme.transform(rot_matrix),
                                                  CartesianRepresentation(1, 0, 0))

    return matrix_product(tilt_matrix, rot_matrix)


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference,
                                 HeliocentricMeanEcliptic, HeliocentricEarthEcliptic)
@_transformation_debug("HME->HEE")
def hme_to_hee(hmecoord, heeframe):
    """
    Convert from Heliocentric Mean Ecliptic to Heliocentric Earth Ecliptic
    """
    # Convert to the HME frame with mean equinox of date at the HEE obstime, through HCRS
    int_frame = HeliocentricMeanEcliptic(obstime=heeframe.obstime, equinox=heeframe.obstime)
    int_coord = hmecoord.transform_to(HCRS).transform_to(int_frame)

    # Rotate the intermediate coord to the HEE frame
    total_matrix = _rotation_matrix_hme_to_hee(int_frame)
    newrepr = int_coord.cartesian.transform(total_matrix)

    return heeframe.realize_frame(newrepr)


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference,
                                 HeliocentricEarthEcliptic, HeliocentricMeanEcliptic)
@_transformation_debug("HEE->HME")
def hee_to_hme(heecoord, hmeframe):
    """
    Convert from Heliocentric Earth Ecliptic to Heliocentric Mean Ecliptic
    """
    int_frame = HeliocentricMeanEcliptic(obstime=heecoord.obstime, equinox=heecoord.obstime)

    # Rotate the HEE coord to the intermediate frame
    total_matrix = matrix_transpose(_rotation_matrix_hme_to_hee(int_frame))
    int_repr = heecoord.cartesian.transform(total_matrix)
    int_coord = int_frame.realize_frame(int_repr)

    # Convert to the HME frame through HCRS
    return int_coord.transform_to(HCRS).transform_to(hmeframe)


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference,
                                 HeliocentricEarthEcliptic, HeliocentricEarthEcliptic)
@_transformation_debug("HEE->HEE")
def hee_to_hee(from_coo, to_frame):
    """
    Convert between two Heliocentric Earth Ecliptic frames.
    """
    if np.all(from_coo.obstime == to_frame.obstime):
        return to_frame.realize_frame(from_coo.data)
    else:
        return from_coo.transform_to(HCRS).transform_to(to_frame)


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference,
                                 HeliocentricEarthEcliptic, GeocentricSolarEcliptic)
@_transformation_debug("HEE->GSE")
def hee_to_gse(heecoord, gseframe):
    """
    Convert from Heliocentric Earth Ecliptic to Geocentric Solar Ecliptic
    """
    # Use an intermediate frame of HEE at the GSE observation time
    int_frame = HeliocentricEarthEcliptic(obstime=gseframe.obstime)
    int_coord = heecoord.transform_to(int_frame)

    # Get the Sun-Earth vector in the intermediate frame
    sun_earth = HCRS(_sun_earth_icrf(int_frame.obstime), obstime=int_frame.obstime)
    sun_earth_int = sun_earth.transform_to(int_frame).cartesian

    # Find the Earth-object vector in the intermediate frame
    earth_object_int = int_coord.cartesian - sun_earth_int

    # Flip the vector in X and Y, but leave Z untouched
    # (The additional transpose operations are to handle both scalar and array inputs)
    newrepr = CartesianRepresentation((earth_object_int.xyz.T * [-1, -1, 1]).T)

    return gseframe.realize_frame(newrepr)


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference,
                                 GeocentricSolarEcliptic, HeliocentricEarthEcliptic)
@_transformation_debug("GSE->HEE")
def gse_to_hee(gsecoord, heeframe):
    """
    Convert from Geocentric Solar Ecliptic to Heliocentric Earth Ecliptic
    """
    # Use an intermediate frame of HEE at the GSE observation time
    int_frame = HeliocentricEarthEcliptic(obstime=gsecoord.obstime)

    # Get the Sun-Earth vector in the intermediate frame
    sun_earth = HCRS(_sun_earth_icrf(int_frame.obstime), obstime=int_frame.obstime)
    sun_earth_int = sun_earth.transform_to(int_frame).cartesian

    # Find the Earth-object vector in the intermediate frame
    # Flip the vector in X and Y, but leave Z untouched
    # (The additional transpose operations are to handle both scalar and array inputs)
    earth_object_int = CartesianRepresentation((gsecoord.cartesian.xyz.T * [-1, -1, 1]).T)

    # Find the Sun-object vector in the intermediate frame
    sun_object_int = sun_earth_int + earth_object_int
    int_coord = int_frame.realize_frame(sun_object_int)

    return int_coord.transform_to(heeframe)


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference,
                                 GeocentricSolarEcliptic, GeocentricSolarEcliptic)
@_transformation_debug("GSE->GSE")
def gse_to_gse(from_coo, to_frame):
    """
    Convert between two Geocentric Solar Ecliptic frames.
    """
    if np.all(from_coo.obstime == to_frame.obstime):
        return to_frame.realize_frame(from_coo.data)
    else:
        return from_coo.transform_to(HeliocentricEarthEcliptic).transform_to(to_frame)


def _rotation_matrix_hgs_to_hci(obstime):
    """
    Return the rotation matrix from HGS to HCI at the same observation time
    """
    z_axis = CartesianRepresentation(0, 0, 1)*u.m
    if not obstime.isscalar:
        z_axis = z_axis._apply('repeat', obstime.size)

    # Get the ecliptic pole in HGS
    ecliptic_pole = HeliocentricMeanEcliptic(z_axis, obstime=obstime, equinox=_J2000)
    ecliptic_pole_hgs = ecliptic_pole.transform_to(HeliographicStonyhurst(obstime=obstime))

    # Rotate the ecliptic pole to the -YZ plane, which aligns the solar ascending node with the X
    # axis
    rot_matrix = _rotation_matrix_reprs_to_xz_about_z(ecliptic_pole_hgs.cartesian)
    xz_to_yz_matrix = rotation_matrix(-90*u.deg, 'z')

    return xz_to_yz_matrix @ rot_matrix


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference,
                                 HeliographicStonyhurst, HeliocentricInertial)
@_transformation_debug("HGS->HCI")
def hgs_to_hci(hgscoord, hciframe):
    """
    Convert from Heliographic Stonyhurst to Heliocentric Inertial
    """
    # First transform the HGS coord to the HCI obstime
    int_coord = _transform_obstime(hgscoord, hciframe.obstime)

    # Rotate from HGS to HCI
    total_matrix = _rotation_matrix_hgs_to_hci(int_coord.obstime)
    newrepr = int_coord.cartesian.transform(total_matrix)

    return hciframe._replicate(newrepr, obstime=int_coord.obstime)


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference,
                                 HeliocentricInertial, HeliographicStonyhurst)
@_transformation_debug("HCI->HGS")
def hci_to_hgs(hcicoord, hgsframe):
    """
    Convert from Heliocentric Inertial to Heliographic Stonyhurst
    """
    # First transform the HCI coord to the HGS obstime
    int_coord = _transform_obstime(hcicoord, hgsframe.obstime)

    # Rotate from HCI to HGS
    total_matrix = matrix_transpose(_rotation_matrix_hgs_to_hci(int_coord.obstime))
    newrepr = int_coord.cartesian.transform(total_matrix)

    return hgsframe._replicate(newrepr, obstime=int_coord.obstime)


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference,
                                 HeliocentricInertial, HeliocentricInertial)
@_transformation_debug("HCI->HCI")
def hci_to_hci(from_coo, to_frame):
    """
    Convert between two Heliocentric Inertial frames.
    """
    if np.all(from_coo.obstime == to_frame.obstime):
        return to_frame.realize_frame(from_coo.data)
    else:
        return from_coo.transform_to(HeliographicStonyhurst(obstime=from_coo.obstime)).\
               transform_to(to_frame)


def _rotation_matrix_obliquity(time):
    """
    Return the rotation matrix from Earth equatorial to ecliptic coordinates
    """
    return rotation_matrix(obl06(*get_jd12(time, 'tt'))*u.radian, 'x')


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference,
                                 HeliocentricMeanEcliptic, GeocentricEarthEquatorial)
@_transformation_debug("HME->GEI")
def hme_to_gei(hmecoord, geiframe):
    """
    Convert from Heliocentric Mean Ecliptic to Geocentric Earth Equatorial
    """
    # Use an intermediate frame of HME at the GEI observation time, through HCRS
    int_frame = HeliocentricMeanEcliptic(obstime=geiframe.obstime, equinox=geiframe.equinox)
    int_coord = hmecoord.transform_to(HCRS).transform_to(int_frame)

    # Get the Sun-Earth vector in the intermediate frame
    sun_earth = HCRS(_sun_earth_icrf(int_frame.obstime), obstime=int_frame.obstime)
    sun_earth_int = sun_earth.transform_to(int_frame).cartesian

    # Find the Earth-object vector in the intermediate frame
    earth_object_int = int_coord.cartesian - sun_earth_int

    # Rotate from ecliptic to Earth equatorial
    rot_matrix = matrix_transpose(_rotation_matrix_obliquity(int_frame.equinox))
    newrepr = earth_object_int.transform(rot_matrix)

    return geiframe.realize_frame(newrepr)


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference,
                                 GeocentricEarthEquatorial, HeliocentricMeanEcliptic)
@_transformation_debug("GEI->HME")
def gei_to_hme(geicoord, hmeframe):
    """
    Convert from Geocentric Earth Equatorial to Heliocentric Mean Ecliptic
    """
    # Use an intermediate frame of HME at the GEI observation time
    int_frame = HeliocentricMeanEcliptic(obstime=geicoord.obstime, equinox=geicoord.equinox)

    # Get the Sun-Earth vector in the intermediate frame
    sun_earth = HCRS(_sun_earth_icrf(int_frame.obstime), obstime=int_frame.obstime)
    sun_earth_int = sun_earth.transform_to(int_frame).cartesian

    # Rotate from Earth equatorial to ecliptic
    rot_matrix = _rotation_matrix_obliquity(int_frame.equinox)
    earth_object_int = geicoord.cartesian.transform(rot_matrix)

    # Find the Sun-object vector in the intermediate frame
    sun_object_int = sun_earth_int + earth_object_int
    int_coord = int_frame.realize_frame(sun_object_int)

    # Convert to the final frame through HCRS
    return int_coord.transform_to(HCRS).transform_to(hmeframe)


@frame_transform_graph.transform(FunctionTransformWithFiniteDifference,
                                 GeocentricEarthEquatorial, GeocentricEarthEquatorial)
@_transformation_debug("GEI->GEI")
def gei_to_gei(from_coo, to_frame):
    """
    Convert between two Geocentric Earth Equatorial frames.
    """
    if np.all((from_coo.equinox == to_frame.equinox) and (from_coo.obstime == to_frame.obstime)):
        return to_frame.realize_frame(from_coo.data)
    else:
        return from_coo.transform_to(HCRS).transform_to(to_frame)


def _make_sunpy_graph():
    """
    Culls down the full transformation graph for SunPy purposes and returns the string version
    """
    # Frames to keep in the transformation graph
    keep_list = ['icrs', 'hcrs', 'heliocentrictrueecliptic', 'heliocentricmeanecliptic',
                 'heliographic_stonyhurst', 'heliographic_carrington',
                 'heliocentric', 'helioprojective',
                 'heliocentricearthecliptic', 'geocentricsolarecliptic',
                 'heliocentricinertial', 'geocentricearthequatorial',
                 'gcrs', 'precessedgeocentric', 'geocentrictrueecliptic', 'geocentricmeanecliptic',
                 'cirs', 'altaz', 'itrs']

    global frame_transform_graph
    backup_graph = frame_transform_graph

    small_graph = deepcopy(frame_transform_graph)
    cull_list = [name for name in small_graph.get_names() if name not in keep_list]
    cull_frames = [small_graph.lookup_name(name) for name in cull_list]

    for frame in cull_frames:
        # Remove the part of the graph where the unwanted frame is the source frame
        if frame in small_graph._graph:
            del small_graph._graph[frame]

        # Remove all instances of the unwanted frame as the destination frame
        for entry in small_graph._graph:
            if frame in small_graph._graph[entry]:
                del (small_graph._graph[entry])[frame]

    # Clean up the node list
    for name in cull_list:
        small_graph._cached_names.pop(name)

    _add_astropy_node(small_graph)

    # Overwrite the main transform graph
    frame_transform_graph = small_graph

    docstr = make_transform_graph_docs()

    # Restore the main transform graph
    frame_transform_graph = backup_graph

    # Make adjustments to the graph
    docstr = _tweak_graph(docstr)

    return docstr


def _add_astropy_node(graph):
    """
    Add an 'Astropy' node that links to an ICRS node in the graph
    """
    class Astropy(BaseCoordinateFrame):
        name = "REPLACE"

    @graph.transform(FunctionTransform, Astropy, ICRS)
    def fake_transform1():
        pass

    @graph.transform(FunctionTransform, ICRS, Astropy)
    def fake_transform2():
        pass


def _tweak_graph(docstr):
    # Remove Astropy's diagram description
    output = docstr[docstr.find('.. Wrap the graph'):]

    # Change the Astropy node
    output = output.replace('Astropy [shape=oval label="Astropy\\n`REPLACE`"]',
                            'Astropy [shape=box3d style=filled fillcolor=lightcyan '
                            'label="Other frames\\nin Astropy"]')

    # Change the Astropy<->ICRS links to black
    output = output.replace('ICRS -> Astropy[  color = "#783001" ]',
                            'ICRS -> Astropy[  color = "#000000" ]')
    output = output.replace('Astropy -> ICRS[  color = "#783001" ]',
                            'Astropy -> ICRS[  color = "#000000" ]')

    # Set the nodes to be filled and cyan by default
    output = output.replace('AstropyCoordinateTransformGraph {',
                            'AstropyCoordinateTransformGraph {\n'
                            '        node [style=filled fillcolor=lightcyan]')

    # Set the nodes for SunPy frames to be white
    sunpy_frames = ['HeliographicStonyhurst', 'HeliographicCarrington',
                    'Heliocentric', 'Helioprojective',
                    'HeliocentricEarthEcliptic', 'GeocentricSolarEcliptic',
                    'HeliocentricInertial', 'GeocentricEarthEquatorial']
    for frame in sunpy_frames:
        output = output.replace(frame + ' [', frame + ' [fillcolor=white ')

    # Set the rank direction to be left->right (as opposed to top->bottom)
    # Force nodes for ICRS, HCRS, and "Other frames in Astropy" to be at the same rank
    output = output.replace('        overlap=false',
                            '        overlap=false\n'
                            '        rankdir=LR\n'
                            '        {rank=same; ICRS; HCRS; Astropy}')

    output = output.replace('<ul>\n\n',
                            '<ul>\n\n' +
                            _add_legend_row('SunPy frames', 'white') +
                            _add_legend_row('Astropy frames', 'lightcyan'))

    return output


def _add_legend_row(label, color):
    row = '        <li style="list-style: none;">\n'\
          '            <p style="font-size: 12px;line-height: 24px;font-weight: normal;'\
          'color: #848484;padding: 0;margin: 0;">\n'\
          '                <b>' + label + ':</b>\n'\
          '                    <span class="dot" style="height: 20px;width: 40px;'\
          'background-color: ' + color + ';border-radius: 50%;border: 1px solid black;'\
          'display: inline-block;"></span>\n'\
          '            </p>\n'\
          '        </li>\n\n\n'
    return row
