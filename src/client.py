import urllib.request
from urllib import error
import json

class MusicClient:
    
    def __init__(self, address, port, timeout=5):
        self.ip_address = address
        self.port = port
        self.timeout = timeout  # in seconds

    def do_request(self, method, dir):
        path = self.ip_address + f":{str(self.port)}" + dir
        print(path)

        try:
            response = urllib.request.urlopen(path, timeout=self.timeout)
        except error.URLError as e:
            print(e)
            return None
        except ConnectionRefusedError as e:
            print(e)
            return None

        data = json.loads(response.read().decode("utf-8")).get("data")
        return data

    def get_avaliable_intervals(self):
        return self.do_request("GET", "/intervals")

    def get_interval_info(self, key):
        intervals = self.get_avaliable_intervals()

        if intervals == None:
            return None
        return intervals[key]

    def get_interval_songs(self, key, is_asc):
        dir = f"/songs/{key}/{is_asc}"
        return self.do_request("GET", dir)