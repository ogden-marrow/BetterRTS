import busAPI


def main():
    api_key = "5hbdzrna2veCiFsynEW9ZTGWx"
    routes = busAPI.get_routes(api_key)
    for route in routes:
        print(route)
        print(busAPI.get_vehicle_ids(api_key, route.rt))


if __name__ == "__main__":
    main()
