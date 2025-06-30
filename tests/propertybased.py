import os
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from example.client import Game

NB_ITERATIONS_TESTS = 1000000000

def create_property_based_test(f):
    regressions = []
    for i in range(0, NB_ITERATIONS_TESTS):
        if i < len(regressions):
            seed = regressions[i]
        else:
            seed = random.randrange(0, 2**64)
        random.seed(seed)
        try:
            f()
        except AssertionError as err:
            print(seed, "test failed")
            print(err)
            sys.exit(1)


def test_init_game():
    name = "testUser" + str(random.randint(1, 9999))
    game = Game(name)
    game.init_game()
    status = game.get("/player/{}".format(game.pid))
    assert status["money"] > 0, f"Le joueur {name} a une valeur de crédit invalide"
    assert game.sid is not None, "Le vaisseau n'est pas initialisé"
    assert game.sta is not None, "La station n'est pas initialisée"
    print("[*] test_init_game passed with:", name)


create_property_based_test(test_init_game)