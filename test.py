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

    likert_options = [
        "Slightly agree",
        "Agree",
        "Strongly Agree",
        "Neutral",
        "slightly disagree",
        "Disagree",
        "Strongly disagree",
    ]
    questions = [
        MultipleChoiceQuestion(survey_questions[label], likert_options, label)
        for label in survey_questions.keys()
    ]
    labels = list(survey_questions.keys())
    survey = Survey(questions, labels, screen_width=1000, screen_height=600)
    survey.run()
    extra_info = {
        "USERID": "00000",
        "GYMID": "your mom",
        "TRIAL": 1,
        "MODE": 1,
        "DIFF": 1,
    }
    survey.send_responses(extra_info)


if __name__ == "__main__":
    main()
