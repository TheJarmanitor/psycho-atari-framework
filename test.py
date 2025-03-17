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
        "Strongly disagree",
        "Disagree",
        "Slightly disagree",
        "Neutral",
        "Slightly agree",
        "Agree",
        "Strongly agree",
    ]
    questions = [MultipleChoiceQuestion(survey_questions[label], likert_options, label) for label in survey_questions.keys()]




if __name__ == "__main__":
    main()
