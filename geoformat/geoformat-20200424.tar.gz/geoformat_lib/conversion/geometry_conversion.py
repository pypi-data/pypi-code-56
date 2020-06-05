import copy
import struct

import geoformat


def bbox_extent_to_2d_bbox_extent(bbox_extent):
    mid_idx = int(len(bbox_extent) / 2)
    bbox = (bbox_extent[0], bbox_extent[1], bbox_extent[mid_idx], bbox_extent[mid_idx + 1])

    return bbox


def geometry_type_to_2d_geometry_type(geometry_type):
    if 'POINT' in geometry_type.upper():
        new_geometry_type = 'Point'
    elif 'LINESTRING' in geometry_type.upper():
        new_geometry_type = 'Linestring'
    elif 'POLYGON' in geometry_type.upper():
        new_geometry_type = 'Polygon'
    elif 'GEOMETRY' in geometry_type.upper():
        new_geometry_type = 'Geometry'
    else:
        print("Geometry type unknown")

    if 'MULTI' in geometry_type.upper():
        new_geometry_type = 'Multi' + new_geometry_type

    return new_geometry_type


def coordinates_to_2d_coordinates(coordinates):
    def convert_to_2d(coordinates):

        if isinstance(coordinates[0][0], (int, float)):
            return tuple((coordinate[0], coordinate[1]) for coordinate in coordinates)
        elif isinstance(coordinates[0][0], (tuple, list)):
            new_coordinates = [None] * len(coordinates)
            for i_coord, under_coordinates in enumerate(coordinates):
                new_coordinates[i_coord] = convert_to_2d(under_coordinates)
            return new_coordinates
        else:
            print('error your geometry in input is not correct')

    return convert_to_2d(coordinates)


def geometry_to_2d_geometry(geometry, bbox=True):
    geometry_collection = geometry_to_geometry_collection(geometry, bbox=bbox,
                                                                    geometry_type_filter=geometry['type'])
    for i_geom, geom in enumerate(geometry_collection['geometries']):
        new_geometry_type = geometry_type_to_2d_geometry_type(geom['type'])
        new_geometry = {'type': new_geometry_type}
        new_geometry['coordinates'] = coordinates_to_2d_coordinates(geom['coordinates'])
        if bbox:
            if 'bbox' in geom:
                bbox = bbox_extent_to_2d_bbox_extent(geom['bbox'])
            else:
                bbox = geoformat.coordinates_to_bbox(new_geometry['coordinates'])

            new_geometry['bbox'] = bbox

        geometry_collection['geometries'][i_geom] = new_geometry

    if geometry['type'].upper() == 'GEOMETRYCOLLECTION':
        return geometry_collection
    else:
        return geometry_collection['geometries'][0]


def geolayer_to_2d_geolayer(input_geolayer):
    new_geolayer = {'features': {}, 'metadata': copy.deepcopy(input_geolayer['metadata'])}
    input_geometry_type = input_geolayer['metadata']['geometry_ref']['type']
    if isinstance(input_geometry_type, (list, tuple)):
        new_geometry_type = []
        for geom_type in input_geometry_type:
            new_geometry_type.append(geometry_type_to_2d_geometry_type(geom_type))
    else:
        new_geometry_type = geometry_type_to_2d_geometry_type(input_geometry_type)
    new_geolayer['metadata']['geometry_ref']['type'] = new_geometry_type

    if 'extent' in new_geolayer['metadata']['geometry_ref']:
        bbox_extent = True
    else:
        bbox_extent = False

    for i_feat in input_geolayer['features']:
        input_feature = input_geolayer['features'][i_feat]
        if 'feature_serialize' in input_geolayer['metadata']:
            if input_geolayer['metadata']['feature_serialize'] == True:
                input_feature = eval(input_feature)

        output_feature = copy.deepcopy(input_feature)

        if 'geometry' in input_feature:
            input_geometry = input_feature['geometry']
            new_geometry = geometry_to_2d_geometry(input_geometry, bbox=bbox_extent)
            output_feature['geometry'] = new_geometry

        if 'feature_serialize' in input_geolayer['metadata']:
            if input_geolayer['metadata']['feature_serialize'] == True:
                output_feature = str(output_feature)

        new_geolayer['features'][i_feat] = output_feature

    return new_geolayer


def envelope_to_bbox(envelope):
    """
    Convert envelope to bbox
        format (x_min, y_min, x_max, y_max)
    :param envelope:
    :return: (x_min, y_min, x_max, y_max)
    """

    return envelope[0], envelope[2], envelope[1], envelope[3]


def bbox_to_envelope(bbox):
    """
    Convert bbox to envelope
        format (x_min, x_max, y_min, y_max)
    :param bbox:
    :return: (x_min, x_max, y_min, y_max)
    """

    return bbox[0], bbox[2], bbox[1], bbox[3]


def geometry_to_geometry_collection(geometry, geometry_type_filter=None, bbox=True):
    """
    Transform a geometry to GeometryCollection
    """
    if geometry_type_filter:
        if isinstance(geometry_type_filter, str):
            geometry_type_filter = {geometry_type_filter.upper()}
        elif isinstance(geometry_type_filter, (list, tuple, set)):
            set_geom_type = set([])
            for geometry_type in geometry_type_filter:
                set_geom_type.update(set([geometry_type.upper()]))
            geometry_type_filter = set_geom_type
        else:
            print('geometry_type_filter must be a geometry type or a list of geometry type')
    else:
        geometry_type_filter = geoformat.GEOFORMAT_GEOMETRY_TYPE

    geometry_type = geometry['type']
    if geometry_type.upper() != 'GEOMETRYCOLLECTION':
        if geometry_type.upper() in geometry_type_filter:
            geometry_collection = {'type': 'GeometryCollection', 'geometries': [geometry]}
            if bbox:
                if 'bbox' in geometry:
                    bbox = geometry['bbox']
                else:
                    bbox = geoformat.coordinates_to_bbox(geometry['coordinates'])
                geometry_collection['bbox'] = bbox

            return geometry_collection
        else:
            print('geometry type non compatible with geometry in geoformat_lib :', geometry_type_filter )

    if geometry_type.upper() == 'GEOMETRYCOLLECTION':
        geometry_list = []
        if bbox:
            bbox_geometry_collection = None
        for geometry in geometry['geometries']:
            if geometry['type'].upper() in geometry_type_filter:
                if bbox:
                    if not 'bbox' in geometry:
                        bbox = geoformat.coordinates_to_bbox(geometry['coordinates'])
                        if not bbox_geometry_collection:
                            bbox_geometry_collection = bbox
                        else:
                            bbox_geometry_collection = geoformat.bbox_union(bbox_geometry_collection, bbox)
                        geometry['bbox'] = bbox

                geometry_list.append(geometry)
        geometry_collection = {'type': 'GeometryCollection', 'geometries': geometry_list}
        if bbox:
            geometry_collection['bbox'] = bbox_geometry_collection

        return geometry_collection


def format_coordinates(coordinates_list, format_type=None, precision=None):
    """convert list coordinates to tuple and change precision of coordinates"""
    tmp_list = [None] * len(coordinates_list)
    for i_coord, coordinates in enumerate(coordinates_list):
        if isinstance(coordinates, (int, float)):
            if isinstance(precision, int):
                # TODO if same coordinates that precedent then don't write coordinates
                coordinates = round(coordinates, precision)
            coord_tuple = coordinates
        elif isinstance(coordinates, (list, tuple)):
            coord_tuple = format_coordinates(coordinates)
            if format_type:
                coord_tuple = format_type(coord_tuple)
        else:
            raise TypeError('must be list or tuple containing int or float')
        tmp_list[i_coord] = coord_tuple

    if format_type:
        tmp_list = format_type(tmp_list)

    return tmp_list


def multi_geometry_to_single_geometry(geometry):
    """
    Iterator in given geometry and send single geometry (Point, LineString, Polygon) if geometry is a multigeometry.
    Works with GeometryCollection
    """

    if geometry['type'].upper() == 'GEOMETRYCOLLECTION':  # 'GeometryCollection'
        for inside_geometry in geometry['geometries']:
            for single_geom in multi_geometry_to_single_geometry(inside_geometry):
                yield single_geom

    elif geometry['type'].upper() in ['MULTIPOINT', 'MULTILINESTRING', 'MULTIPOLYGON']:
        if geometry['type'].upper() == 'MULTIPOINT':
            single_geometry_type = 'Point'
        elif geometry['type'].upper() == 'MULTILINESTRING':
            single_geometry_type = 'LineString'
        else:
            single_geometry_type = 'Polygon'

        multi_coordinates = geometry['coordinates']
        for coordinates in multi_coordinates:
            yield {'type': single_geometry_type, 'coordinates': coordinates}

    else:
        yield geometry


def geometry_to_wkb(geometry, endian_big=True):
    """
    Transform geoformat geometry (or geojson like geometry) to wkb geometry.
    Optionally you can choose the output endian.

    :param geometry: geoformat geometry (or geojson like geometry)
    :param endian_big: True if output big endian / False if output little endian.
    :return: output bytes geometry in wkb format
    """

    def int_to_4_bytes_integer(integer_value, integer_endian_big=True):
        """
        make translation between int type value to 4 bytes value.
        Optionally you can choose output bytes endian

        :param integer_value: integer value
        :param integer_endian_big: True if output big endian / False if output little endian
        :return: input value in 4 bytes
        """
        if integer_endian_big is True:
            struct_format = ">i"
        else:
            struct_format = "<i"

        return bytearray(struct.pack(struct_format, integer_value))

    def float_to_double_8_bytes_array(float_value, float_big_endian=True):
        """
        Make translation between float type value to 8 bytes value.
        Optionally you can choose output bytes endian

        :param float_value: float value
        :param float_big_endian: True if output big endian / False if output little endian
        :return: input value in 8 bytes
        """
        if float_big_endian is True:
            struct_format = ">d"
        else:
            struct_format = "<d"

        return bytearray(struct.pack(struct_format, float_value))

    def coordinates_list_to_bytes(coordinates_list, coordinates_big_endian=True):
        """
        Transform a list of coordinates to bytes value.
        Optionally you can choose the output endian.

        :param coordinates_list: list of coordinates.
        :param coordinates_big_endian: True if output big endian / False if output little endian.
        :return: coordinates in bytes value.
        """

        def coordinates_to_bytes(coordinates, float_big_endian=True):
            """
            Transform coordinates to bytes.
            Optionally you can choose the output endian.

            :param coordinates:
            :param float_big_endian:
            :return: coordinates in bytes value.
            """
            (x, y) = coordinates
            x_bytes = float_to_double_8_bytes_array(float_value=x, float_big_endian=float_big_endian)
            y_bytes = float_to_double_8_bytes_array(float_value=y, float_big_endian=float_big_endian)

            return x_bytes + y_bytes

        first_coord = coordinates_list[0]
        if isinstance(first_coord, (list, tuple)):
            bytes_coordinates = int_to_4_bytes_integer(len(coordinates_list), integer_endian_big=coordinates_big_endian)
            for coord in coordinates_list:
                bytes_coordinates += coordinates_list_to_bytes(coordinates_list=coord,
                                                               coordinates_big_endian=coordinates_big_endian)
        elif isinstance(first_coord, (float, int)):
            bytes_coordinates = coordinates_to_bytes(coordinates=coordinates_list,
                                                     float_big_endian=coordinates_big_endian)
        else:
            raise ValueError

        return bytes_coordinates

    # START geometry_to_wkb
    geometry_type_to_wkb_geometry_type = {
        'POINT': b'\x00\x00\x00\x01',
        'LINESTRING': b'\x00\x00\x00\x02',
        'POLYGON': b'\x00\x00\x00\x03',
        'MULTIPOINT': b'\x00\x00\x00\x04',
        'MULTILINESTRING': b'\x00\x00\x00\x05',
        'MULTIPOLYGON': b'\x00\x00\x00\x06',
        'GEOMETRYCOLLECTION': b'\x00\x00\x00\x07',
    }

    if endian_big is True:
        b_endian = b'\x00'
    else:
        b_endian = b'\x01'

    geojson_type = geometry['type'].upper()
    multi = False
    if 'MULTI' in geojson_type:
        multi = True

    collection = False
    if geojson_type == 'GEOMETRYCOLLECTION':
        collection = True

    bytes_geo_type = bytearray(geometry_type_to_wkb_geometry_type[geojson_type])
    if endian_big is False:
        bytes_geo_type.reverse()

    if collection:
        wkb_coordinates = int_to_4_bytes_integer(integer_value=len(geometry['geometries']),
                                                 integer_endian_big=endian_big)
        for geometry_from_collection in geometry['geometries']:
            wkb_coordinates += geometry_to_wkb(geometry=geometry_from_collection, endian_big=endian_big)
    elif multi:
        wkb_coordinates = int_to_4_bytes_integer(integer_value=len(geometry['coordinates']),
                                                 integer_endian_big=endian_big)
        for single_geom in multi_geometry_to_single_geometry(geometry):
            wkb_coordinates += geometry_to_wkb(geometry=single_geom, endian_big=endian_big)
    else:
        wkb_coordinates = coordinates_list_to_bytes(geometry['coordinates'], coordinates_big_endian=endian_big)

    wkb_bytearray = b_endian + bytes_geo_type + wkb_coordinates

    return wkb_bytearray


def wkb_to_geometry(wkb_geometry):
    """
    Transform wkb bytes geometry to geoformat (geojson like) geometry

    :param wkb_geometry: input wkb bytes
    :return: geoformat geometry (geojson like)
    """

    def double_8_bytes_to_float(double_8_bytes, double_big_endian, double_dimension=2):
        """
        Make translation between dimension * 8 bytes value to float type value.
        You have to give the endian of data and dimension of coordinates.

        :param double_8_bytes: coordinates value in 8 bytes
        :param double_big_endian: the endian order of your bytes
        :param double_dimension: number of dimension (default 2) for your coordinates
        :return: float tuple of coordinates
        """
        if double_big_endian is True:
            struct_format = ">{dim}d".format(dim=double_dimension)
        elif double_big_endian is False:
            struct_format = "<{dim}d".format(dim=double_dimension)
        else:
            raise ValueError('endian_big must be a bool type')

        return struct.unpack(struct_format, double_8_bytes)

    def integer_4_bytes_to_int(integer_4_bytes, integer_endian_big):
        """
        Make translation between integer 4 bytes value to integer type value.
        You have to give the endian of data and double_dimension of coordinates.

        :param integer_4_bytes: coordinates value in 8 bytes
        :param integer_endian_big: the endian of your bytes
        :return: float tuple of coordinates
        """
        if integer_endian_big is True:
            struct_format = ">i"
        elif integer_endian_big is False:
            struct_format = "<i"
        else:
            raise ValueError('endian_big must be a bool type')

        return struct.unpack(struct_format, integer_4_bytes)[0]

    def define_geometry_lenght_in_bytesarray(geometry_b, geometry_start_idx):
        """
        Return the geometry length (in number of bytes).

        :param geometry_b: geometry in wkb.
        :param geometry_start_idx: start index of geometrie in geometry_b.
        :return: length in integer.
        """
        # determine endian
        endian_b = geometry_b[geometry_start_idx]
        part_big_endian = True
        if endian_b == 1:
            part_big_endian = False
        geometry_start_idx += 1
        # determine geo type
        geometry_end_idx = geometry_start_idx + 4
        _geo_type_b = geometry_b[geometry_start_idx:geometry_end_idx]
        if part_big_endian is False:
            _geo_type_b = bytearray(_geo_type_b)
            _geo_type_b.reverse()
            _geo_type_b = bytes(_geo_type_b)
        _geo_type = big_endian_wkb_geometry_type_to_geometry_type[_geo_type_b]
        # deduce double_dimension
        _dimension = geo_type_to_dimension[_geo_type]
        geometry_start_idx = geometry_end_idx
        geometry_end_idx = geometry_end_idx + 4
        if 'Multi' in _geo_type:
            _geometry_idx_length = 9
            nb_part_b = geometry_b[geometry_start_idx:geometry_end_idx]
            nb_part = integer_4_bytes_to_int(integer_4_bytes=nb_part_b, integer_endian_big=part_big_endian)
            geometry_start_idx = geometry_end_idx
            for i_part in range(nb_part):
                length_part = define_geometry_lenght_in_bytesarray(geometry_b=geometry_b,
                                                                   geometry_start_idx=geometry_start_idx)
                _geometry_idx_length += length_part
                geometry_start_idx += length_part
        elif _geo_type == 'Point':
            _geometry_idx_length = 5 + _dimension * 8
        else:
            # determine nb coordinates or rings
            _nb_coordinates_or_rings_b = geometry_b[geometry_start_idx:geometry_end_idx]
            _nb_coordinates_or_rings = integer_4_bytes_to_int(integer_4_bytes=_nb_coordinates_or_rings_b,
                                                              integer_endian_big=part_big_endian)
            if 'LineString' in _geo_type:
                # deduce length of linestring part
                _geometry_idx_length = 9 + _dimension * 8 * _nb_coordinates_or_rings
            elif 'Polygon' in _geo_type:
                _geometry_idx_length = 9  # endian + _geo_type + nb_ring
                geometry_start_idx = geometry_end_idx
                # loop on each ring
                for ring in range(_nb_coordinates_or_rings):
                    # deduce nb coordinates by ring
                    geometry_end_idx = geometry_start_idx + 4
                    _nb_coordinates_b = geometry_b[geometry_start_idx:geometry_end_idx]
                    _nb_coordinates = integer_4_bytes_to_int(integer_4_bytes=_nb_coordinates_b,
                                                             integer_endian_big=part_big_endian)
                    # deduce ring length
                    ring_length = 4 + _dimension * 8 * _nb_coordinates  # nb coordinates + length of coordinates
                    _geometry_idx_length += ring_length
                    geometry_start_idx = geometry_start_idx + ring_length
            else:
                raise Exception('geo type not valid')

        return _geometry_idx_length

    def get_coordinates_list_from_wkb_geometry(wkb_coordinates, nb_coord, wkb_dimension, wkb_endian_big=True):
        """
        Determine coordinates list from wkb coordinates. To do that we need the wkb coordinates, the number of
        coordinates and their number of dimensions.
        Optionally you can choose the output endian.

        :param wkb_coordinates: coordinates in wkb
        :param nb_coord: number of coordinates
        :param wkb_dimension: number of dimensions in wkb coordinates
        :param wkb_endian_big: True if output big endian / False if output little endian.
        :return: coordinates list
        """
        _coordinates_list = [None] * nb_coord
        split_idx_list = range(0, nb_coord * wkb_dimension * 8, wkb_dimension * 8)
        for i_coord, _start_idx in enumerate(split_idx_list):
            _end_idx = _start_idx + 8 * wkb_dimension
            part_coordinates_b = wkb_coordinates[_start_idx:_end_idx]
            float_coordinates_list = list(double_8_bytes_to_float(double_8_bytes=part_coordinates_b,
                                                                  double_big_endian=wkb_endian_big,
                                                                  double_dimension=2))
            _coordinates_list[i_coord] = float_coordinates_list

        return _coordinates_list

    # START wkb_to_geometry
    big_endian_wkb_geometry_type_to_geometry_type = {
        b'\x00\x00\x00\x01': 'Point',
        b'\x00\x00\x00\x02': 'LineString',
        b'\x00\x00\x00\x03': 'Polygon',
        b'\x00\x00\x00\x04': 'MultiPoint',
        b'\x00\x00\x00\x05': 'MultiLineString',
        b'\x00\x00\x00\x06': 'MultiPolygon',
        b'\x00\x00\x00\x07': 'GeometryCollection',
    }
    geo_type_to_dimension = {
        'Point': 2,
        'LineString': 2,
        'Polygon': 2,
        'MultiPoint': 2,
        'MultiLineString': 2,
        'MultiPolygon': 2,
    }

    geometry_endian_b = wkb_geometry[0]
    if geometry_endian_b == 0:
        endian_big = True
    elif geometry_endian_b == 1:
        endian_big = False
    else:
        raise ValueError('wkb format must begin by \x00 for BIG or \x01 for LITTLE endian')

    geo_type_b = wkb_geometry[1:5]
    if endian_big is False:
        geo_type_b = bytearray(geo_type_b)
        geo_type_b.reverse()
        geo_type_b = bytes(geo_type_b)
    geo_type = big_endian_wkb_geometry_type_to_geometry_type[geo_type_b]

    return_geometry = {'type': geo_type}
    start_idx = 5
    end_idx = start_idx + 4
    if geo_type == 'GeometryCollection':
        nb_geometries_b = wkb_geometry[start_idx:end_idx]
        nb_geometries = integer_4_bytes_to_int(integer_4_bytes=nb_geometries_b, integer_endian_big=endian_big)
        start_idx = end_idx
        geometries_list = [None] * nb_geometries
        for idx_geometry in range(nb_geometries):
            # get length of geometry in collection (in bytes)
            geometry_in_collection_length = define_geometry_lenght_in_bytesarray(geometry_b=wkb_geometry,
                                                                                 geometry_start_idx=start_idx)
            end_idx = start_idx + geometry_in_collection_length
            # create geometry in collection
            geometry_in_collection_b = wkb_geometry[start_idx:end_idx]
            geometry_in_collection = wkb_to_geometry(geometry_in_collection_b)
            # add geometry in geometries_list
            geometries_list[idx_geometry] = geometry_in_collection
            # reset start idx
            start_idx = end_idx
        # add geometries
        return_geometry['geometries'] = geometries_list
    else:
        dimension = geo_type_to_dimension[geo_type]
        if 'Multi' in geo_type:
            # idx for nb geometries (4 bytes)
            end_idx = start_idx + 4
            nb_geometries_b = wkb_geometry[start_idx:end_idx]
            nb_geometries = integer_4_bytes_to_int(integer_4_bytes=nb_geometries_b, integer_endian_big=endian_big)
            start_idx = end_idx
            coordinates_list = [None] * nb_geometries
            for i_geometry in range(nb_geometries):
                # get length of geometry
                geometry_idx_length = define_geometry_lenght_in_bytesarray(geometry_b=wkb_geometry,
                                                                           geometry_start_idx=start_idx)
                end_idx = start_idx + geometry_idx_length
                slice_geom_b = wkb_geometry[start_idx:end_idx]
                slice_geom = wkb_to_geometry(slice_geom_b)
                coordinates_list[i_geometry] = slice_geom['coordinates']
                # reset start_idx for next geometry
                start_idx = end_idx
        elif geo_type == 'Point':
            x_y_b = wkb_geometry[start_idx:]
            coordinates = double_8_bytes_to_float(double_8_bytes=x_y_b,
                                                  double_big_endian=endian_big,
                                                  double_dimension=dimension)
            coordinates_list = list(coordinates)
        else:
            nb_coordinates_or_rings_b = wkb_geometry[start_idx:end_idx]
            nb_coordinates_or_rings = integer_4_bytes_to_int(integer_4_bytes=nb_coordinates_or_rings_b,
                                                             integer_endian_big=endian_big)
            if geo_type == 'LineString':
                len_bytes = nb_coordinates_or_rings * 8 * dimension
                start_idx = end_idx
                end_idx = start_idx + len_bytes
                coordinates_in_wkb = wkb_geometry[start_idx:end_idx]
                coordinates_list = get_coordinates_list_from_wkb_geometry(nb_coord=nb_coordinates_or_rings,
                                                                          wkb_coordinates=coordinates_in_wkb,
                                                                          wkb_dimension=dimension,
                                                                          wkb_endian_big=endian_big)
            elif geo_type == 'Polygon':
                ring_list = [None] * nb_coordinates_or_rings
                for i_ring in range(nb_coordinates_or_rings):
                    start_idx = end_idx
                    end_idx = start_idx + 4
                    nb_coordinates_b = wkb_geometry[start_idx:end_idx]
                    nb_coordinates = integer_4_bytes_to_int(integer_4_bytes=nb_coordinates_b,
                                                            integer_endian_big=endian_big)
                    len_bytes = nb_coordinates * 8 * dimension
                    start_idx = end_idx
                    end_idx = start_idx + len_bytes
                    coordinates_in_wkb = wkb_geometry[start_idx:end_idx]
                    coordinates_list = get_coordinates_list_from_wkb_geometry(nb_coord=nb_coordinates,
                                                                              wkb_coordinates=coordinates_in_wkb,
                                                                              wkb_dimension=dimension,
                                                                              wkb_endian_big=endian_big)
                    ring_list[i_ring] = coordinates_list

                coordinates_list = ring_list
            else:
                raise Exception('error on geometry type')

        # add coordines to geom
        return_geometry['coordinates'] = coordinates_list

    return return_geometry
