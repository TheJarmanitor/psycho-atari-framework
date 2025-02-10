from game import GameScreen
from survey import MultipleChoiceQuestion, Survey
from random import shuffle
from copy import deepcopy
import uuid
import itertools


def main():  # add with "tutorial version", later with random difficulties
    answers = [
        "Slightly agree",
        "Agree",
        "Strongly Agree",
        "Neutral",
        "slightly disagree",
        "Disagree",
        "Strongly disagree",
    ]
    participant_id = str(uuid.uuid4())
    with open("miniPXI.txt", "r") as f:
        questions = [MultipleChoiceQuestion(line.strip(), answers) for line in f]

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

    for i in range(3):
        shuffle(game_names)
        for game_name in game_names:
            shuffle(game_list[game_name])
            game_mode, game_difficulty = game_list[game_name].pop()
            GameScreen(
                participant_id=participant_id,
                game_name=f"ALE/{game_name}-v5",
                time_limit=100,
                game_mode=game_mode,
                game_difficulty=game_difficulty,
                session_number=i + 1,
            )

            shuffle(questions)
            survey = Survey(deepcopy(questions), screen_width=1000, screen_height=600)
            survey.run()
            extra_info = {
                "participant_id": [participant_id],
                "session_number": [i + 1],
                "game": [game_name],
                "mode": [game_mode],
                "difficulty": [game_difficulty],
            }
            survey.collect_responses("survey_responses.csv", surveyor_info=extra_info)


if __name__ == "__main__":
    main()
