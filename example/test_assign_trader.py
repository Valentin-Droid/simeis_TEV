import unittest
import urllib.request
import urllib.parse
import json
import random, time

PORT=9345
URL=f"http://0.0.0.0:{PORT}"

class TestAssignTrader(unittest.TestCase):
    def setUp(self):
        unique = f"test-rich_{int(time.time())}_{random.randint(1000,9999)}"
        url = f"{URL}/player/new/{unique}"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            self.player = json.loads(response.read().decode())
        self.player_id = self.player["playerId"]
        self.player_key = self.player["key"]

    def test_assign_trader(self):
        url = f"{URL}/player/{self.player_id}?key={urllib.parse.quote(self.player_key)}"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            player_info = json.loads(response.read().decode())
        stations = player_info["stations"]
        station_id = list(stations.keys())[0]

        url = f"{URL}/station/{station_id}/crew/hire/trader?key={urllib.parse.quote(self.player_key)}"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            crew_result = json.loads(response.read().decode())
        crew_id = crew_result["id"]

        url = f"{URL}/station/{station_id}/crew/assign/{crew_id}/trading?key={urllib.parse.quote(self.player_key)}"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            assign_result = json.loads(response.read().decode())

if __name__ == "__main__":
    unittest.main()
