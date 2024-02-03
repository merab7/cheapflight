import requests
import os

TEQUILA_API = os.environ.get("TEQUILA_API")
TEQUILA_ENDPOINT = os.environ.get("TEQUILA_ENDPOINT")
SHEETS_ENDPOINT_GET = os.environ.get("SHEETS_ENDPOINT_GET")
SHEETS_ENDPOINT_PUT = os.environ.get("SHEETS_ENDPOINT_PUT")
AUTOROTATION_SHEET =  os.environ.get("AUTOROTATION_SHEET")

sheet_header = {
    "Authorization": AUTOROTATION_SHEET
}

tequila_header = {
    "apikey": TEQUILA_API
}





class Data_manager:
    def __init__(self) -> None:
        self.city_dict = {}
        self.get_city_names()
        self.get_city_codes()
        self.updating_sheet()
        

    def get_city_names(self): #this function getting city names from my google sheet using sheety api and adding tem to city_dict as an key
        self.response_from_sheet = requests.get(SHEETS_ENDPOINT_GET, headers=sheet_header)
        self.sheet_data = self.response_from_sheet.json()
        self.city_dict ={x["city"]:x["lowestPrice"] for x in self.sheet_data['prices']}
    
    def get_city_codes(self): #this function getting city codes from tequila api using city names from city_dict as a "term" param and then updating city_dict
        for key, value in self.city_dict.items(): #adding codes for each city as a value. at the end i am getting dict with values as a code and keys as a city 
            self.params_tequila = { 
                "term":key,
                "location_types": "city",
                "limit": 1
                }

            self.response_tequila = requests.get(f"{TEQUILA_ENDPOINT}/locations/query", params=self.params_tequila, headers=tequila_header)
            self.data_tequila = self.response_tequila.json()
            self.city_dict[key] = [self.data_tequila["locations"][0]["code"], value]

    def updating_sheet(self): #with this function i am updating my sheet and adding codes to it. using x to handel the index of item in dict and then 
        #using that index in my put_url
        self.x = 0
        for key, value in self.city_dict.items():
            self.put_url = f"{SHEETS_ENDPOINT_PUT}{self.x+2}"
            self.params = {
                "price": {
                    "iataCode": value[0],
                      } 
            }
            self.x += 1
            self.response = requests.put(self.put_url, json=self.params, headers=sheet_header)
            
            

            