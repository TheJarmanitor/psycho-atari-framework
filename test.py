from game import GameScreen, StartScreen
import numpy as np

from brainlablsl import create_stream

def main():
    with open("psychoatari.yml", 'r') as f:
        stream = create_stream(f)

    GameScreen(
        participant_id="0000",
        game_name=f"Turmoil-v5",
        time_limit=20,
        tutorial=True,
        trial_number=0,
        stream=stream
    )


if __name__ == "__main__":
    main()
