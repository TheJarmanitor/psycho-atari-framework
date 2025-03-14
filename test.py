from game import GameScreen, StartScreen, MessageScreen
from random import shuffle
from survey import MultipleChoiceQuestion, Survey
import numpy as np
import uuid
import itertools
import subprocess
import sys

from brainlablsl import create_stream
from brainlabgp3 import BrAInLabGP3


def main():
    MessageScreen(message="Hold on. Calibration will begin soon", countdown=5).run()
    #BrAInLabGP3().calibrate(show_calibration_result_time=5,calibration_result_log="calib.log")
    StartScreen(countdown=5).run()
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
        )
    ]
    survey = Survey(questions, screen_width=800, screen_height=600, fullscreen=False)
    survey.run()


if __name__ == "__main__":
    main()
