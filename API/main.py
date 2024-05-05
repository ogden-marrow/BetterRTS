import busAPI
from secrets import API_KEY as api_key


def main():
    routes = busAPI.get_routes(api_key)
    print(busAPI.get_service_bulletins(api_key, "5"))
    for route in routes:
        print(route)
        on_route = busAPI.get_vehicle_ids(api_key, route.rt)
        for vid in on_route.vids:
            vehicle = busAPI.get_vehicle_location(api_key, vid)
            print(vehicle)


if __name__ == "__main__":
    main()
