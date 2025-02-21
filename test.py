from game import GameScreen, StartScreen
from random import shuffle
import numpy as np
import uuid
import itertools

from brainlablsl import create_stream

def main():
    participant_id = str(uuid.uuid4())
    with open("psychoatari.yml", 'r') as f:
        stream = create_stream(f)

    game_details = {
        "Turmoil": {"modes": [x for x in range(4)], "difficulties": [0]},
        "WordZapper": {
            "modes": [x for x in range(4)],
            "difficulties": [x for x in range(4)],
        },
        "Boxing": {"modes": [0], "difficulties": [x for x in range(4)]},
    }

    game_list = {
        k: list(itertools.product(*v.values())) for (k, v) in game_details.items()
    }
    game_names = list(game_details.keys())

    shuffle(game_names)

    StartScreen(countdown=5).run()

    GameScreen(
        participant_id="participant_id",
        game_name=f"{game_names[0]}-v5",
        time_limit=120,
        tutorial=True,
        trial_number=0,
        logs_path="test_logs",
        stream=stream
    )


if __name__ == "__main__":
    main()
