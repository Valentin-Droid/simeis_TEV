import sys
import random
import time
import os

example_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'example')
sys.path.insert(0, example_path)

from watch_game import mkbar, WIDTH, SCORE, POTENTIAL, VOID

# Configuration de la durée selon l'environnement CI
DEFAULT_DURATION = 5
TEST_DURATION_SECONDS = int(os.environ.get('PROPERTY_TEST_DURATION', DEFAULT_DURATION))

print(f"🔄 Running property-based tests for {TEST_DURATION_SECONDS} seconds...")

def create_property_based_test(f):
    regressions = []  
    start_time = time.time()
    iteration = 0
    
    while time.time() - start_time < TEST_DURATION_SECONDS:
        if iteration < len(regressions):
            seed = regressions[iteration]
        else:
            seed = random.randrange(0, 2**64)
        random.seed(seed)
        try:
            f()
        except AssertionError as err:
            print(f"Seed {seed}, test failed after {iteration + 1} iterations")
            print(err)
            sys.exit(1)
        iteration += 1
    
    print(f"✅ Tests completed successfully after {iteration} iterations in {TEST_DURATION_SECONDS} seconds")


def test_mkbar():
    score = random.uniform(0, 100)
    pot = random.uniform(0, 100)
    maxs = random.uniform(1, 200) 
     
    result = mkbar(score, pot, maxs)
    
    #assert len(result) == WIDTH, f"La barre doit faire {WIDTH} caractères, mais elle en fait {len(result)}"
    
    for char in result:
        assert char in [SCORE, POTENTIAL, VOID], f"Caractère non autorisé: {char}"
    
    result_zero = mkbar(0, 0, maxs)
    assert result_zero == VOID * WIDTH, "Quand score et pot sont 0, la barre doit être vide"
    
    result_maxs_zero = mkbar(score, pot, 0.0)
    assert result_maxs_zero == VOID * WIDTH, "Quand maxs est 0, la barre doit être vide"
    

create_property_based_test(test_mkbar)