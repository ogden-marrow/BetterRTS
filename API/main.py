import busAPI


def main():
    api_key = "5hbdzrna2veCiFsynEW9ZTGWx"
    routes = busAPI.get_routes(api_key)
    for route in routes:
        print(route)
        on_route = busAPI.get_vehicle_ids(api_key, route.rt)
        for vid in on_route.vids:
            vehicle = busAPI.get_vehicle_location(api_key, vid)
            print(vehicle)


if __name__ == "__main__":
    main()
