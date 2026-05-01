import random

# Function implementing Gibson & Bruck's Next Reaction method.
def next_reaction(model : dict, start : dict, timespan : float, rng : random.Random = None):
    if rng is None: # No predefined random number generator was supplied
        rng = random.Random # Create generator with random seed


