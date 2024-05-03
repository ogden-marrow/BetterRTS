from dataclasses import dataclass

import requests


@dataclass
class Route:
    rt: str
    rtnm: str
    rtclr: str
    rtdd: str
    



def get_vehicle_ids(api_key, rt, rt_pid_data_feed=None):
    url = "http://riderts.app/bustime/api/v3/getvehicles"
    params = {
        "key": api_key,
        "format": "json",
        "rt": rt
    }

    if rt_pid_data_feed:
        params["rtpidatafeed"] = rt_pid_data_feed

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        if "bustime-response" in data:
            if "vehicle" in data["bustime-response"]:
                vehicles = data["bustime-response"]["vehicle"]
                vehicle_ids = [vehicle["vid"] for vehicle in vehicles]
                return vehicle_ids
            else:
                print("No 'vehicle' key found in the 'bustime-response'.")
        else:
            print("No 'bustime-response' key found in the API response.")
    else:
        print(f"Request failed with status code: {response.status_code}")

    return []


def get_routes(api_key, rt_pid_data_feed=None):
    url = "http://riderts.app/bustime/api/v3/getroutes"
    params = {
        "key": api_key,
        "format": "json"
    }

    if rt_pid_data_feed:
        params["rtpidatafeed"] = rt_pid_data_feed

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        if "bustime-response" in data:
            if "routes" in data["bustime-response"]:
                routes_data = data["bustime-response"]["routes"]
                routes = [Route(rt=route["rt"],
                                rtnm=route["rtnm"],
                                rtclr=route["rtclr"],
                                rtdd=route["rtdd"]) for route in routes_data]
                return routes
            else:
                print("No 'routes' key found in the 'bustime-response'.")
        else:
            print("No 'bustime-response' key found in the API response.")
    else:
        print(f"Request failed with status code: {response.status_code}")

    return []
