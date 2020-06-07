"""Simple travelling salesman problem between cities."""

from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver.routing_enums_pb2 import (
    FirstSolutionStrategy,
    LocalSearchMetaheuristic,
)


class VrpSolver:
    """VrpSolver https://developers.google.com/optimization/routing/vrp"""

    def __init__(self, num_vehicles):
        self.num_vehicles = num_vehicles

    def create_data_model(self, distance_matrix):
        """Stores the data for the problem."""
        data = {}
        data["distance_matrix"] = distance_matrix
        data["num_vehicles"] = self.num_vehicles
        data["depot"] = 0
        return data

    def compute_total_distance(
        self, route, distance_matrix, unite_mesure="m", show_log=False
    ):
        """With a distance matrix compute the distance between nodes for routes
        """
        distance = distance_matrix[0][route[1]]
        for node in range(len(route) - 1):
            distance += distance_matrix[route[node]][route[node + 1]]
        if show_log:
            print(
                "\nFor route {} -- > distance {:.1f} {}".format(
                    route, distance, unite_mesure
                )
            )
        return distance

    def print_solution(self, manager, routing, solution):
        """Prints solution on console."""
        max_route_distance = 0
        for vehicle_id in range(self.num_vehicles):
            index = routing.Start(vehicle_id)
            plan_output = "Route for vehicle {}:\n".format(vehicle_id)
            route_distance = 0
            while not routing.IsEnd(index):
                plan_output += " {} -> ".format(manager.IndexToNode(index))
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(
                    previous_index, index, vehicle_id
                )
            plan_output += "{}\n".format(manager.IndexToNode(index))
            plan_output += "Distance of the route: {} m\n".format(route_distance)
            print(plan_output)
            max_route_distance = max(route_distance, max_route_distance)
        print("Maximum of the route distances: {} m".format(max_route_distance))

    def get_routes(self, manager, routing, solution):
        """Get vehicle routes from a solution and store them in an array."""
        # Get vehicle routes and store them in a two dimensional array whose
        # i,j entry is the jth location visited by vehicle i along its route.
        routes = []
        for route_nbr in range(self.num_vehicles):
            index = routing.Start(route_nbr)
            route = [manager.IndexToNode(index)]
            while not routing.IsEnd(index):
                index = solution.Value(routing.NextVar(index))
                route.append(manager.IndexToNode(index))
            routes.append(route)
        return routes

    def solver_guided_local_search(
        self,
        distance_matrix,
        time_max,
        heuristic_type="FirstSolutionStrategy",
        heuristic="PATH_CHEAPEST_ARC",
        max_travel_distance=False,
        show_log=False,
    ):
        """Solver fo for local heuristic search
        """
        # Instantiate the data problem.
        data = self.create_data_model(distance_matrix)

        # Create the routing index manager.
        manager = pywrapcp.RoutingIndexManager(
            len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
        )

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data["distance_matrix"][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        if not max_travel_distance:
            max_travel_distance = max(
                [int(sum(line)) * 2 for line in data["distance_matrix"]]
            )

        # Add Distance constraint.
        dimension_name = "Distance"
        routing.AddDimension(
            transit_callback_index,
            0,  # no slack
            max_travel_distance,  # vehicle maximum travel distance
            True,  # start cumul to zero
            dimension_name,
        )
        distance_dimension = routing.GetDimensionOrDie(dimension_name)
        distance_dimension.SetGlobalSpanCostCoefficient(100)

        # Setting guide local search solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        try:
            if heuristic_type == "FirstSolutionStrategy":
                search_parameters.local_search_metaheuristic = getattr(
                    FirstSolutionStrategy, heuristic
                )
            elif heuristic_type == "LocalSearchMetaheuristic":
                search_parameters.local_search_metaheuristic = getattr(
                    LocalSearchMetaheuristic, heuristic
                )
        except AttributeError as e:
            print("Heuristic is not in the available heuristic list\n")
            print(e)
            raise
        search_parameters.time_limit.seconds = time_max
        search_parameters.log_search = False

        # Solve the problem.
        assignment = routing.SolveWithParameters(search_parameters)

        route = False
        if assignment:
            route = self.get_routes(manager, routing, assignment)
            if show_log:
                # Print solution on console.
                self.print_solution(manager, routing, assignment)
        return route
