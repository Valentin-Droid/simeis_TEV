PORT=8080
URL=f"http://localhost:{PORT}"

import unittest
import urllib.request
import urllib.parse
import json
import random, time

class SimeisFunctionalTest(unittest.TestCase):
    def setUp(self):
        # Créer un nouveau joueur 
        unique = f"test-rich_{int(time.time())}_{random.randint(1000,9999)}"
        url = f"{URL}/player/new/{unique}"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            self.player = json.loads(response.read().decode())
        self.player_id = self.player["playerId"]
        self.player_key = self.player["key"]

    def test_scenario(self):
        # Vérifier l'argent de départ du joueur
        url = f"{URL}/player/{self.player_id}?key={urllib.parse.quote(self.player_key)}"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            player_info = json.loads(response.read().decode())
        player_money = player_info["money"]
        print("Argent de départ du joueur:", player_money)

        # Récupérer l'ID de la station du joueur
        stations = player_info["stations"]
        station_id = list(stations.keys())[0]

        # Lister les vaisseaux à l'achat sur la station
        url = f"{URL}/station/{station_id}/shipyard/list?key={urllib.parse.quote(self.player_key)}"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            ships_list = json.loads(response.read().decode())
        available_ships = ships_list["ships"]
        cheapest_ship = min(available_ships, key=lambda s: s["price"])
        ship_id = cheapest_ship["id"]

        # Acheter le vaisseau le moins cher
        url = f"{URL}/station/{station_id}/shipyard/buy/{ship_id}?key={urllib.parse.quote(self.player_key)}"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            buy_result = json.loads(response.read().decode())

        # Vérifier l'argent après achat du vaisseau
        url = f"{URL}/player/{self.player_id}?key={urllib.parse.quote(self.player_key)}"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            player_info = json.loads(response.read().decode())
        money_after_ship = player_info["money"]
        self.assertLess(money_after_ship, player_money)

        # Acheter un module Miner sur le vaisseau acheté
        url = f"{URL}/station/{station_id}/shop/modules"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            modules_list = json.loads(response.read().decode())

        url = f"{URL}/station/{station_id}/shop/modules/{ship_id}/buy/Miner?key={urllib.parse.quote(self.player_key)}"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            module_result = json.loads(response.read().decode())

        # Vérifier l'argent après achat du module
        url = f"{URL}/player/{self.player_id}?key={urllib.parse.quote(self.player_key)}"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            player_info = json.loads(response.read().decode())
        money_after_module = player_info["money"]
        self.assertLess(money_after_module, money_after_ship)

if __name__ == "__main__":
    unittest.main()
