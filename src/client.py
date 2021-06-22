import urllib.request
from urllib import error
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
        path = IP_ADDRESS + f":{str(PORT)}" + dir
        print(path)

        try:
            response = urllib.request.urlopen(path, timeout=TIMEOUT_REQUEST)
        except error.URLError as e:
            print(e)
            return None
        except ConnectionRefusedError as e:
            print(e)
            return None

        data = json.loads(response.read().decode("utf-8")).get("data")
        return data

    def get_avaliable_intervals(self):
        return self.__do_request("GET", "/intervals")

    def get_interval_info(self, key):
        intervals = self.get_avaliable_intervals()

        if intervals == None:
            return None
        return intervals[key]

    def get_interval_songs(self, key, is_asc):
        dir = f"/songs/{key}/{is_asc}"

        return self.__do_request("GET", dir)