from osrm import Point, RequestConfig, simple_route
from pynominatim import Nominatim


class RoutingDataMatrix(object):
    """From classical address create data matrix"""

    def __init__(self, host="localhost:5000"):
        self.host = host
        RequestConfig.host = self.host

    def coordinate_infos(self, locations):
        """With nominatim convert classic adress to geo_coordinates.
        """
        nominatim = Nominatim()
        geo_coordinates = []
        geo_points = []
        for loc in locations:
            address = nominatim.query(loc)
            if len(address) == 0:
                raise ValueError("Address dont match in nominatim", 0, loc)
            elif len(address) == 1:
                lat = float(address[0].get("lat"))
                lon = float(address[0].get("lon"))
            else:
                list_address = []
                for addres in address:
                    dict_address = {
                        "display_name": addres.get("display_name"),
                        "type": addres.get("type"),
                        "lat": addres.get("lat"),
                        "lon": addres.get("lon"),
                    }
                    list_address.append(dict_address)
                raise ValueError("To many address", len(address), list_address)

            geo_coordinates.append([lat, lon])
            point = Point(latitude=lat, longitude=lon)
            geo_points.append(point)
        return geo_coordinates, geo_points

    def distance_duration_matrix_simple_route(self, points):
        """Create distance matrix with OSRM point
        """
        distance_matrix = []
        duration_matrix = []

        for i in range(len(points)):
            dist_line_list = []
            dur_line_list = []
            for j in range(len(points)):
                result = simple_route(points[i], points[j])
                distance = result["routes"][0].get("distance")
                duration = result["routes"][0].get("duration")
                dist_line_list.append(distance)
                dur_line_list.append(duration)
            distance_matrix.append(dist_line_list)
            duration_matrix.append(dur_line_list)
        return distance_matrix, duration_matrix
