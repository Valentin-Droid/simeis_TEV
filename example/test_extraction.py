import unittest
import urllib.request
import urllib.parse
import json
import random, time

PORT=9345
URL=f"http://0.0.0.0:{PORT}"

class TestExtraction(unittest.TestCase):
    def setUp(self):
        unique = f"test-rich_{int(time.time())}_{random.randint(1000,9999)}"
        url = f"{URL}/player/new/{unique}"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            self.player = json.loads(response.read().decode())
        self.player_id = self.player["playerId"]
        self.player_key = self.player["key"]

    def test_extraction(self):
        url = f"{URL}/player/{self.player_id}?key={urllib.parse.quote(self.player_key)}"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            player_info = json.loads(response.read().decode())
        stations = player_info["stations"]
        station_id = list(stations.keys())[0]
        ships = player_info["ships"]
        if not ships:
            self.skipTest("Aucun vaisseau disponible pour extraction.")
        ship_id = ships[0]["id"]

        url = f"{URL}/station/{station_id}/scan?key={urllib.parse.quote(self.player_key)}"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            scan_result = json.loads(response.read().decode())
        planets = scan_result["planets"]
        if not planets:
            self.skipTest("Aucune planète à proximité.")
        planet = planets[0]
        pos = planet["position"]

        url = f"{URL}/ship/{ship_id}/navigate/{pos[0]}/{pos[1]}/{pos[2]}?key={urllib.parse.quote(self.player_key)}"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)

        url = f"{URL}/ship/{ship_id}/extraction/start?key={urllib.parse.quote(self.player_key)}"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            extraction_result = json.loads(response.read().decode())

if __name__ == "__main__":
    unittest.main()
