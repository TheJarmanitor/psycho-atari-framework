from game import GameScreen, StartScreen, MessageScreen
from survey import MultipleChoiceQuestion, Survey
from video_generator import generate_videos
from random import shuffle
from copy import deepcopy
import uuid
import json
import itertools
from brainlablsl import create_stream
from brainlabgp3 import BrAInLabGP3
import subprocess
import sys
import os
import glob




def main():  
    answers = [
        "Slightly agree",
        "Agree",
        "Strongly Agree",
        "Neutral",
        "slightly disagree",
        "Disagree",
        "Strongly disagree",
    ]
    logs_path = r"D:\Documents\atari_challenge\game_logs"
    video_path = r"D:\Documents\atari_challenge\videos"
    id = 1
    while glob.glob(f"{logs_path}/P%03d*.npz" % (id,)):
        id += 1
    participant_id = "P%03d" % id
    with open("miniPXI.json") as f:
        survey_questions = json.load(f)
    questions = [
        MultipleChoiceQuestion(survey_questions[label], answers, label)
        for label in survey_questions.keys()
    ]
    labels = list(survey_questions.keys())
    with open("psychoatari.yml", "r") as f:
        stream = create_stream(f)
        #stream = None
    with open("pxi.yml", "r") as f:
        pxi_stream = create_stream(f)
        #pxi_stream = None

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
    game_names = list(game_details.keys())  # change to list of possiblities

    ## Tutorial version
    #subprocess.Popen([sys.executable, "record.py"])
    StartScreen(countdown=5).run()
    for game in game_names:
        GameScreen(
            participant_id=f"{participant_id}",
            game_name=f"{game}-v5",
            time_limit=120,
            tutorial=True,
            trial_number=0,
            logs_path=logs_path,
            stream=stream,
        )
    generate_videos(logs_path, participant_id, 0, output_folder=video_path)

    for i in range(3):
        MessageScreen(message="Hold on. Calibration will begin soon", countdown=5).run()
      #  BrAInLabGP3().calibrate(
      #     show_calibration_result_time=5, calibration_result_log="calib.log"
      #  )
        StartScreen(countdown=5).run()
        shuffle(game_names)
        for game_name in game_names:
            shuffle(game_list[game_name])
            game_mode, game_difficulty = game_list[game_name].pop()
            GameScreen(
                participant_id=participant_id,
                game_name=f"{game_name}-v5",
                time_limit=120,
                game_mode=game_mode,
                game_difficulty=game_difficulty,
                trial_number=i + 1,
                logs_path="test_logs",
                stream=stream,
            )

            survey = Survey(
                deepcopy(questions),
                labels,
                screen_width=1000,
                screen_height=600,
                stream=pxi_stream,
            )
            survey.run()
            extra_info = {
                "USERID": participant_id,
                "GYMID": game_name,
                "TRIAL": i + 1,
                "MODE": game_mode,
                "DIFF": game_difficulty,
            }
            survey.send_responses(extra_info)
        generate_videos(logs_path, participant_id, i+1, output_folder="videos")
    MessageScreen(
        message="Experiment has finished. Wait for somebody to come to you", countdown=5
    ).run()


if __name__ == "__main__":
    main()
