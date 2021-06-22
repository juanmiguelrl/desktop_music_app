import urllib.request
import json

####################
# CONFIGURATION
####################
IP_ADDRESS = "http://127.0.0.1"
PORT = 5000
TIMEOUT_REQUEST = 5  # in seconds

####################
# CLIENT
####################
class MusicClient:
    
    def __do_request(self, method, dir):
        # Create the full address
        path = IP_ADDRESS + f":{str(PORT)}" + dir

        # Get data decoded
        response = urllib.request.urlopen(path, timeout=TIMEOUT_REQUEST)
        data = json.loads(response.read().decode("utf-8")).get("data")
        
        return data

    def get_avaliable_intervals(self):
        return self.__do_request("GET", "/intervals")

    def get_interval_info(self, key):
        intervals = self.get_avaliable_intervals()
        return intervals[key]

    def get_interval_songs(self, key, is_asc):
        mode = "asc" if is_asc else "des"
        dir = f"/songs/{key}/{mode}"

        return self.__do_request("GET", dir)