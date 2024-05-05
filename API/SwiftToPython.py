import math
from dataclasses import dataclass
from typing import List, Optional

import requests


@dataclass
class Route:
    rt: str
    rtnm: str
    rtclr: str
    rtdd: str
    rtpidatafeed: Optional[str] = None


@dataclass
class VehicleLocation:
    vid: str
    tmstmp: str
    lat: str
    lon: str
    hdg: str
    pid: int
    rt: str
    des: str
    pdist: int
    dly: bool
    spd: int
    tatripid: str
    tablockid: str
    origtatripno: str
    zone: str
    mode: int
    psgld: str
    stst: int
    stsd: str
    rtpidatafeed: Optional[str] = None

@dataclass
class UserLocation:
    lat: float
    lon: float


@dataclass
class ServiceBulletinService:
    rt: str
    rtdir: str
    stpid: str
    stpnm: str


@dataclass
class ServiceBulletin:
    nm: str
    sbj: str
    cse: str
    dtl: str
    brf: str
    prty: str
    efct: str
    url: str
    srvc: List[ServiceBulletinService]
    mod: str
    rtpidatafeed: Optional[str] = None


@dataclass
class BusTimeResponseData:
    data: List


@dataclass
class BusTimeResponse:
    bustime_response: BusTimeResponseData


def find_closest_bus(user_location: UserLocation, rt: str, api_key: str, rt_pid_data_feed: Optional[str] = None,
                     completion=None):
    def callback(vehicle_locations):
        closest_bus = None
        min_distance = float('inf')

        for vehicle in vehicle_locations:
            try:
                lat = float(vehicle.lat)
                lon = float(vehicle.lon)
                vehicle_location = UserLocation(lat, lon)
                distance = calculate_distance(user_location, vehicle_location)
                if distance < min_distance:
                    min_distance = distance
                    closest_bus = vehicle
            except ValueError:
                pass

        if completion:
            completion(closest_bus)

    get_vehicles_with_locations(api_key, rt, rt_pid_data_feed, callback)


def calculate_distance(user_location: UserLocation, vehicle_location: UserLocation) -> float:
    earth_radius = 6371.0  # in kilometers
    lat1 = user_location.lat * math.pi / 180
    lon1 = user_location.lon * math.pi / 180
    lat2 = vehicle_location.lat * math.pi / 180
    lon2 = vehicle_location.lon * math.pi / 180

    d_lat = lat2 - lat1
    d_lon = lon2 - lon1

    a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = earth_radius * c
    return distance


def get_vehicles_with_locations(api_key: str, rt: str, rt_pid_data_feed: Optional[str] = None, completion=None):
    url = "https://riderts.app/bustime/api/v3/getvehicles"
    params = {
        "key": api_key,
        "format": "json",
        "rt": rt
    }

    if rt_pid_data_feed:
        params["rtpidatafeed"] = rt_pid_data_feed

    def callback(result):
        if isinstance(result, dict) and "bustime-response" in result:
            data = result["bustime-response"].get("vehicle", [])
            vehicle_locations = [VehicleLocation(**vehicle) for vehicle in data]
            if completion:
                completion(vehicle_locations)
        else:
            print("Failed to fetch vehicle locations")
            if completion:
                completion([])

    send_get_request(url, params, callback)


def get_routes(api_key: str, rt_pid_data_feed: Optional[str] = None, completion=None):
    url = "https://riderts.app/bustime/api/v3/getroutes"
    params = {
        "key": api_key,
        "format": "json"
    }

    if rt_pid_data_feed:
        params["rtpidatafeed"] = rt_pid_data_feed

    def callback(result):
        if isinstance(result, dict) and "bustime-response" in result:
            data = result["bustime-response"].get("routes", [])
            routes = [Route(**route) for route in data]
            if completion:
                completion(routes)
        else:
            print("Failed to fetch routes")
            if completion:
                completion([])

    send_get_request(url, params, callback)


def get_service_bulletins(api_key: str, rt: str, completion=None):
    url = "https://riderts.app/bustime/api/v3/getservicebulletins"
    params = {
        "key": api_key,
        "rt": rt,
        "format": "json"
    }

    def callback(result):
        if isinstance(result, dict) and "bustime-response" in result:
            data = result["bustime-response"].get("sb", [])
            service_bulletins = [ServiceBulletin(**bulletin) for bulletin in data]
            if completion:
                completion(service_bulletins)
        else:
            print("Failed to fetch service bulletins")
            if completion:
                completion([])

    send_get_request(url, params, callback)


def send_get_request(url: str, params: dict, completion=None):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        result = response.json()
        if completion:
            completion(result)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if completion:
            completion(None)
