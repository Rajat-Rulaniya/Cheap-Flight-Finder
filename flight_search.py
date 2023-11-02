import os

import requests
from flight_data import FlightData

api_key = os.environ["api_key"]
api_location_endpoint = "https://api.tequila.kiwi.com/locations/query"

api_search_endpoint = "https://api.tequila.kiwi.com/v2/search"

api_header = {
    "apikey": api_key
}

api_location_parameters = {
    "term": "",
    "location_types": "city"
}

api_search_parameters = {
    "fly_from": "",
    "fly_to": "",
    "date_from": "",
    "date_to": "",
    "curr": "INR",
    "nights_in_dst_from": 7,
    "nights_in_dst_to": 28,
    "flight_type": "round",
    "one_for_city": 1,
    "max_stopovers": 0,
}


class FlightSearch:
    def flight_data_pass(self, data, stop_overs, from_city_code, to_city_code):
        out_date = data["route"][0]["local_departure"].split("T")[0]
        return_date = data["route"][1]["local_departure"].split("T")[0]
        price = data["price"]
        origin_airport = data["route"][0]["flyFrom"]
        destination_airport = data["route"][0]["flyTo"]
        origin_city_name = data["route"][0]["cityFrom"]
        stop_over_city = None
        if stop_overs > 0:
            return_date = data["route"][3]["local_departure"].split("T")[0]
            stop_over_city = data["route"][0]["cityTo"]
        flight_data = FlightData(price,
                                 from_city_code,
                                 to_city_code,
                                 out_date,
                                 return_date,
                                 origin_airport,
                                 destination_airport,
                                 stop_over_city,
                                 stop_overs,
                                 origin_city_name
                                 )

        return flight_data

    def get_IATA_code(self, location_name):
        api_location_parameters["term"] = location_name
        response = requests.get(url=api_location_endpoint, params=api_location_parameters, headers=api_header)
        IATA_CODE = response.json()["locations"][0]["code"]
        return IATA_CODE

    def get_flight_details(self, from_city_code, to_city_code, date_from, date_to):
        stop_overs = 0
        api_search_parameters["max_stopovers"] = stop_overs
        api_search_parameters["fly_to"] = to_city_code
        api_search_parameters["date_from"] = date_from
        api_search_parameters["date_to"] = date_to
        api_search_parameters["fly_from"] = from_city_code

        response = requests.get(url=api_search_endpoint, headers=api_header, params=api_search_parameters)

        try:
            data = response.json()['data'][0]
        except IndexError:
            stop_overs = 2
            api_search_parameters["max_stopovers"] = stop_overs
            response = requests.get(url=api_search_endpoint, headers=api_header, params=api_search_parameters)
            data = response.json()['data'][0]
            return self.flight_data_pass(data, stop_overs, from_city_code, to_city_code)
        else:
            return self.flight_data_pass(data, stop_overs, from_city_code, to_city_code)
