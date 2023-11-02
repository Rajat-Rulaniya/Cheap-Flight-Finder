from data_manager import DataManager
from flight_search import FlightSearch
import datetime as dt
from email_manager import EmailManager
import os


FROM_CITY_CODE = os.environ["origin_city"]

date_from = (dt.datetime.now() + dt.timedelta(hours=24)).strftime("%d/%m/%Y")
date_to = (dt.datetime.now() + dt.timedelta(hours=24, weeks=26)).strftime("%d/%m/%Y")

email_manager = EmailManager()
data_manager = DataManager()
flight_search = FlightSearch()
sheet_data = data_manager.get_data()  # A List

for location_dict in sheet_data:
    location_name = location_dict["city"]
    location_id = location_dict["id"]
    location_lowest_price = location_dict["lowestPrice"]
    if len(location_dict["iataCode"]) == 0:
        location_dict["iataCode"] = flight_search.get_IATA_code(location_name)
        data_manager.update_data(location_dict, location_id)
    location_iata = location_dict["iataCode"]
    flight_details = flight_search.get_flight_details(FROM_CITY_CODE, location_iata, date_from, date_to)

    if flight_details.price < location_lowest_price:
        message = f"\n*Don't Miss Out*\n\nFlight from {flight_details.origin_city_name}(Airport: {flight_details.origin_airport}) --> {location_name}(Airport: {flight_details.destination_airport})\n\nAt just ₹{flight_details.price}\n\nOut Date: {flight_details.departure_date}\nReturn Date: {flight_details.return_date}"

        if flight_details.stop_overs > 0:
            message = f"\n*Don't Miss Out*\n\nFlight from {flight_details.origin_city_name}(Airport: {flight_details.origin_airport}) --> {location_name}(Airport: {flight_details.destination_airport})\n\nAt just ₹{flight_details.price}\n\nOut Date: {flight_details.departure_date}\nReturn Date: {flight_details.return_date}\nFlight has 1 stop over, via {flight_details.stop_via_city}"

        email_manager.send_mail(message)
