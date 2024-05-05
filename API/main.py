import SwiftToPython as STP
from secrets import API_KEY as api_key


def main():
    def print_routes(routes):
        for route in routes:
            print("route")
            on_route = STP.get_vehicles_with_locations(api_key, route.rt, completion=print_vehicles)
            print("on_route")

    def print_vehicles(vehicles):
        print("vehicles")

    def print_service_bulletins(bulletins):
        print(bulletins)

    STP.get_service_bulletins(api_key, "5", completion=print_service_bulletins)


if __name__ == "__main__":
    main()
