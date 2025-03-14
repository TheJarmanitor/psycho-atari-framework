from game import GameScreen, StartScreen, MessageScreen
from random import shuffle
from survey import MultipleChoiceQuestion, Survey
import numpy as np
import uuid
import itertools
import subprocess
import sys
import json

from brainlablsl import create_stream
from brainlabgp3 import BrAInLabGP3


def main():
    # message_screen = MessageScreen(message="Hold on. Calibration will begin soon", countdown=5)
    # start_screen = StartScreen(countdown=5)

    with open("miniPXI.json") as f:
        survey_questions = json.load(f)

    print(survey_questions.keys())
    # participant_id = str(uuid.uuid4())
    # with open("psychoatari.yml", "r") as f:
    #     stream = create_stream(f)

    #     game_details = {
    #         "Turmoil": {"modes": [x for x in range(4)], "difficulties": [0]},
    #         "WordZapper": {
    #             "modes": [x for x in range(4)],
    #             "difficulties": [x for x in range(4)],
    #         },
    #         "Boxing": {"modes": [0], "difficulties": [x for x in range(4)]},
    #     }

    #     game_list = {
    #         k: list(itertools.product(*v.values())) for (k, v) in game_details.items()
    #     }
    #     game_names = list(game_details.keys())

    #     shuffle(game_names)

    # subprocess.Popen([sys.executable, 'record.py'])

    # StartScreen(countdown=5).run()
    # MessageScreen(message="Hold on. Calibration will begin soon", countdown=5).run()

    # Likert scale options in the required order.
    likert_options = [
        "Strongly disagree",
        "Disagree",
        "Slightly disagree",
        "Neutral",
        "Slightly agree",
        "Agree",
        "Strongly agree",
    ]
    questions = [
        MultipleChoiceQuestion(
            "I find this survey application intuitive to use.", likert_options
        ),
        MultipleChoiceQuestion(
            "I am satisfied with the response options provided.", likert_options
        ),
        MultipleChoiceQuestion(
            "The color scheme is visually appealing.", likert_options
        ),
    ]
    # message_screen.run()
    # start_screen.run()


if __name__ == "__main__":
    main()
