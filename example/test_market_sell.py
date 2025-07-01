import unittest
import urllib.request
import urllib.parse
import json
import random, time

PORT=9345
URL=f"http://0.0.0.0:{PORT}"

class TestMarketSell(unittest.TestCase):
    def setUp(self):
        unique = f"test-rich_{int(time.time())}_{random.randint(1000,9999)}"
        url = f"{URL}/player/new/{unique}"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            self.player = json.loads(response.read().decode())
        self.player_id = self.player["playerId"]
        self.player_key = self.player["key"]

    def test_market_sell(self):
        url = f"{URL}/player/{self.player_id}?key={urllib.parse.quote(self.player_key)}"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            player_info = json.loads(response.read().decode())
        stations = player_info["stations"]
        station_id = list(stations.keys())[0]
        ships = player_info["ships"]
        if not ships:
            self.skipTest("Aucun vaisseau disponible pour vente.")
        ship_id = ships[0]["id"]

        url = f"{URL}/ship/{ship_id}?key={urllib.parse.quote(self.player_key)}"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            ship_info = json.loads(response.read().decode())
        cargo = ship_info.get("cargo", {}).get("resources", {})
        resource = None
        amount = 0
        for res, amnt in cargo.items():
            if amnt > 0:
                resource = res
                amount = amnt
                break
        if not resource:
            self.skipTest("Aucune ressource à vendre dans le cargo.")

        url = f"{URL}/ship/{ship_id}/unload/{resource}/{amount}?key={urllib.parse.quote(self.player_key)}"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)

        url = f"{URL}/market/{station_id}/sell/{resource}/{amount}?key={urllib.parse.quote(self.player_key)}"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            sell_result = json.loads(response.read().decode())

if __name__ == "__main__":
    unittest.main()
