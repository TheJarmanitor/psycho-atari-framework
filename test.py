from game import GameScreen, StartScreen
import numpy as np

from brainlablsl import create_stream

def main():
    with open("psychoatari.yml", 'r') as f:
        stream = create_stream(f)



if __name__ == "__main__":
    main()
