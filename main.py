import json
import requests
from datetime import datetime

BASE_URL = "https://gateway.apiportal.ns.nl/reisinformatie-api/api/v2/"
ARRIVALS_URL = "arrivals"
DEPARTURES_URL = "departures"
STATIONS_URL = "stations"


def load_config():
    with open('config.json', 'r') as config:
        data = json.load(config)
        return data


def api_call(url, params={}):
    config = load_config()
    headers = {
        "Ocp-Apim-Subscription-Key": config["api_key"]
    }
    response = requests.get(BASE_URL + url, params=params, headers=headers)
    if response.ok:
        return response.json()["payload"]
    return False


def get_station_code(station):
    payload = api_call(STATIONS_URL)
    if payload:
        station = next((item for item in payload if item["namen"]["lang"] == config["station"]), None)

        return station["code"]
    return None


def get_departing_trains(station):
    payload = api_call(DEPARTURES_URL, {"station": station, "maxJourneys": 5})
    if payload:
        for departure in payload["departures"]:
            print(departure["direction"], datetime.strptime(departure["actualDateTime"], "%Y-%m-%dT%H:%M:%S+0100"))

    return None


def time_since_last_check(last_check):
    return (datetime.now() - last_check).total_seconds()


if __name__ == "__main__":
    config = load_config()
    station = get_station_code(config["station"])
    if not station:
        print("Could not find station")

    last_check = datetime.utcfromtimestamp(0)

    while True:
        if time_since_last_check(last_check) > config["refresh_time"]:
            get_departing_trains(station)
            last_check = datetime.now()
