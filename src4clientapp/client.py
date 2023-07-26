import requests
import json

class Client():
    """
    usage:
    napkin_client = Client(HTTP, HOST, PATH, ways, periods,
                 data_type, PORT, API_KEY, DEVICE_ID)
    mean_val = napkin_client.get_mean()
    """
    def __init__(self, HTTP, HOST, PATH, ways, periods,
                 data_type, PORT, API_KEY, DEVICE_ID):
        self.http = HTTP
        self.host = HOST
        self.path = PATH
        self.ways = ways
        self.periods = periods
        self.data_type = data_type
        self.port = PORT
        self.api_key = API_KEY
        self.device_id = DEVICE_ID

        self.URL = self.http + self.host + self.path + "/" + str(self.device_id) + ways + periods + data_type
        
        self.headers = {
            "content-type": "application/json",
            "napkin-account-api-key": self.api_key
        }

    def get_mean(self):
        response = requests.get(self.URL,
                                headers=self.headers)
        json_dict = json.loads(response.text)
        mean_val = json_dict["mean"]
        return mean_val



