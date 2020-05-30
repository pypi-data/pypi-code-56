# -*- coding: utf-8 -*-
"""
===========================================================
Identifying stars in a STEREO/SECCHI COR2 coronagraph image
===========================================================

How to use the `Vizier star catalog <https://vizier.u-strasbg.fr>`_ to
identify bright points in a STEREO/SECCHI COR 2 image as stars.
As a bonus, we also identify Mars.
"""
import matplotlib.pyplot as plt

# astroquery is not a dependency of SunPy so will need to be
# install this package separately.
from astroquery.vizier import Vizier
import astropy.units as u
from astropy.coordinates import Distance, SkyCoord
from astropy.time import Time

import sunpy.map
from sunpy.coordinates import get_body_heliographic_stonyhurst
from sunpy.net import helioviewer

###############################################################################
# Let's download a STEREO-A SECCHI COR2 image from Helioviewer which provide
# pre-processed images and load it into a Map.
hv = helioviewer.HelioviewerClient()
f = hv.download_jp2('2014/05/15 07:54', observatory='STEREO_A', instrument='SECCHI', detector='COR2')
cor2 = sunpy.map.Map(f)

###############################################################################
# To efficiently search the star field, we need to know what stars are near the
# Sun as observed by STEREO. We need the vector that points from STEREO to the Sun.
# The location of STEREO in HCRS provides the Sun-to-STEREO vector.

sun_to_stereo = cor2.observer_coordinate.transform_to('hcrs')

###############################################################################
# We next reflect the vector to get our search vector which points from STEREO
# to the Sun.

stereo_to_sun = SkyCoord(-sun_to_stereo.spherical, obstime=sun_to_stereo.obstime, frame='hcrs')

###############################################################################
# Let's look up bright stars using the Vizier search capability provided by
# astroquery.
# We will search the GAIA2 star catalog for stars with magnitude
# brighter than 7.

vv = Vizier(columns=['**'], row_limit=-1, column_filters={'Gmag': '<7'}, timeout=1200)
vv.ROW_LIMIT = -1
result = vv.query_region(stereo_to_sun, radius=4 * u.deg, catalog='I/345/gaia2')

###############################################################################
# Let's see how many stars we've found.
print(len(result[0]))

###############################################################################
# Now we load all stars into an array coordinate and transform it into the COR2
# image coordinates.  The reference epoch for the star positions is J2015.5,
# so we update these positions to the date of the COR2 observation using
# :meth:`astropy.coordinates.SkyCoord.apply_space_motion`.

tbl_crds = SkyCoord(ra=result[0]['RA_ICRS'],
                    dec=result[0]['DE_ICRS'],
                    distance=Distance(parallax=u.Quantity(result[0]['Plx'])),
                    pm_ra_cosdec=result[0]['pmRA'],
                    pm_dec=result[0]['pmDE'],
                    radial_velocity=result[0]['RV'],
                    frame='icrs',
                    obstime=Time(result[0]['Epoch'], format='jyear'))
tbl_crds = tbl_crds.apply_space_motion(new_obstime=cor2.date)
hpc_coords = tbl_crds.transform_to(cor2.coordinate_frame)

###############################################################################
# One of the bright features is actually Mars, so let's also get that coordinate.

mars = get_body_heliographic_stonyhurst('mars', cor2.date, observer=cor2.observer_coordinate)
mars_hpc = mars.transform_to(cor2.coordinate_frame)

###############################################################################
# Let's plot the results.
ax = plt.subplot(projection=cor2)

# Let's tweak the axis to show in degrees instead of arcsec
lon, lat = ax.coords
lon.set_major_formatter('d.dd')
lat.set_major_formatter('d.dd')

cor2.plot(axes=ax, vmin=0, vmax=600)
cor2.draw_limb()

# Plot the position of Mars
ax.plot_coord(mars_hpc, 's', color='white', fillstyle='none', markersize=12, label='Mars')
# Plot all of the stars
ax.plot_coord(hpc_coords, 'o', color='white', fillstyle='none')
plt.legend()
plt.show()
