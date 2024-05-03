import busAPI


def main():
    api_key = "5hbdzrna2veCiFsynEW9ZTGWx"
    routes = busAPI.get_routes(api_key)
    route = routes[0]
    print(route)
    bus_ids = busAPI.get_vehicle_ids(api_key, route.rt)
    print(bus_ids[0])
    print(busAPI.get_vehicle_location(api_key, bus_ids[0]))


if __name__ == "__main__":
    main()
