from game import GameScreen, StartScreen, MessageScreen
from random import shuffle
from survey import MultipleChoiceQuestion, Survey
import numpy as np
import uuid
import itertools
import subprocess
import sys
import json

import os
import glob


def main():
    logs_path = ".logs"
    id = 1
    while glob.glob(".logs/P%03d*.npz" % (id,)):
        id += 1
    participant_id = "sub-P%03d" % id

    print(participant_id)


if __name__ == "__main__":
    main()
