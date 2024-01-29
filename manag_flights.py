from datetime import datetime, timedelta
from data_manager import Data_manager
import requests

TEQUILA_API = "qJkDFzpWbuqM23h3gO_HJMaWEQBGfgoF"
TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"

tequila_header = {
    "apikey": TEQUILA_API
}

MY_CT = "VIE" 
CITY_DICT = Data_manager().city_dict
TOMORROW = datetime.now().date() + timedelta(1)
TOMORROW = TOMORROW.strftime("%d/%m/%Y")
DATE_TO = datetime.now().date() + timedelta(days=(6 * 30))

class Find_flight:
    def __init__(self) -> None:
        self.destination_dict = []
      
        


    def search_flight(self):
        for x in CITY_DICT.values():
            self.params_tequila = {
                "fly_from": MY_CT,
                "fly_to": x[0],
                "date_from": TOMORROW,
                "date_to":DATE_TO,
                "one_for_city": 1,
                "max_stopovers": 0,
                "curr": "EUR",
                "price_from": 0,
                "price_to": x[1]

             }
            try:
                self.response_tequila = requests.get(f"{TEQUILA_ENDPOINT}/v2/search", params=self.params_tequila, headers=tequila_header)
                if self.response_tequila.json()["_results"] != 0 :
                    self.destination_dict = [{"cityFrom": x["cityFrom"],
                         "cityTo": x["cityTo"],
                         "countryFrom": x["countryFrom"]["name"],
                         "countryTo": x["countryTo"]["name"],
                         "local_departure": x["local_departure"],
                         "local_arrival": x["local_arrival"],
                         "price": x["price"],
                         "link":x["deep_link"]} for x in self.response_tequila.json()["data"]]

            except:
                print("There is no Flights that is in your requirements")    

