import os

import requests

sheet_get_endpoint = os.environ["sheet_get_endpoint"]

sheet_header = {
    "Authorization": os.environ["Authorization"]
}


class DataManager:

    def get_data(self):
        response = requests.get(url=sheet_get_endpoint, headers=sheet_header)
        data = response.json()
        return data["locations"]

    def update_data(self, location_dict, city_id):
        sheet_put_endpoint = os.environ["sheet_put_endpoint"]
        new_data = {
            "location": location_dict
        }
        response = requests.put(url=sheet_put_endpoint, headers=sheet_header, json=new_data)
