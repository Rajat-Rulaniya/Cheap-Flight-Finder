class FlightData:
    def __init__(self, price, from_city, to_city, out_date, return_date, origin_airport, destination_airport, stop_over_city, stop_over, origin_city_name):
        self.price = price
        self.departure_city = from_city
        self.destination_city = to_city
        self.departure_date = out_date
        self.return_date = return_date
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.stop_overs = stop_over
        self.stop_via_city = stop_over_city
        self.origin_city_name = origin_city_name
