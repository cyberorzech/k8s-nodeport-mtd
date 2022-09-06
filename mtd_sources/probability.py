from random import randint

def draw(probability=0.5) -> bool:
    """
    Function that returns True with probability of 0.5 by default
    """
    RANGE = [0, 10]
    random_number = randint(*RANGE) / 10
    if random_number < probability: return True
    return False
    

if __name__ == "__main__":
    raise NotImplementedError("Use as package")
    #draw()