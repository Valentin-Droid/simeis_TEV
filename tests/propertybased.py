import os
import random
import sys
import time
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from example.client import Game

DEFAULT_TEST_DURATION = 30 
HEAVY_TEST_DURATION = 3600 

def create_property_based_test(f, duration_seconds=DEFAULT_TEST_DURATION):
    regressions = []
    start_time = time.time()
    iteration = 0
    
    print(f"[*] Running property-based test for {duration_seconds} seconds...")
    
    while time.time() - start_time < duration_seconds:
        if iteration < len(regressions):
            seed = regressions[iteration]
        else:
            seed = random.randrange(0, 2**64)
        random.seed(seed)
        try:
            f()
            iteration += 1
            if iteration % 100 == 0:
                elapsed = time.time() - start_time
                print(f"[*] Completed {iteration} iterations in {elapsed:.1f}s")
        except AssertionError as err:
            print(f"FAILURE: seed {seed}, iteration {iteration}, test failed")
            print(err)
            sys.exit(1)
    
    elapsed = time.time() - start_time
    print(f"[*] Property-based test completed: {iteration} iterations in {elapsed:.1f}s")


def test_init_game():
    name = "testUser" + str(random.randint(1, 9999))
    game = Game(name)
    game.init_game()
    status = game.get("/player/{}".format(game.pid))
    assert status["money"] > 0, f"Le joueur {name} a une valeur de crédit invalide"
    assert game.sid is not None, "Le vaisseau n'est pas initialisé"
    assert game.sta is not None, "La station n'est pas initialisée"
    print("[*] test_init_game passed with:", name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run property-based tests')
    parser.add_argument('--heavy', action='store_true', 
                        help='Run heavy tests (long duration)')
    parser.add_argument('--duration', type=int, 
                        help='Test duration in seconds')
    
    args = parser.parse_args()
    
    if args.duration:
        duration = args.duration
    elif args.heavy:
        duration = HEAVY_TEST_DURATION
    else:
        duration = DEFAULT_TEST_DURATION
    
    create_property_based_test(test_init_game, duration)