from game import GameScreen
from survey import MultipleChoiceQuestion, Survey
from random import shuffle
from copy import deepcopy
import uuid
import itertools


def main():  # add with "tutorial version", later with random difficulties
    answers = [
        "Strongly disagree",
        "Disagree",
        "slightly disagree",
        "Neutral",
        "Slightly agree",
        "Agree",
        "Strongly Agree",
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
        "Centipede": {"modes": [22, 86], "difficulties": [0]},
    }

    game_list = {
        k: list(itertools.product(*v.values())) for (k, v) in game_details.items()
    }
    print(game_list)

    ## Tutorial version

    game_names = list(game_details.keys())  # change to list of possiblities
    print(game_names)
    for game in game_names:
        GameScreen(
            participant_id=participant_id,
            game_name=f"ALE/{game}-v5",
            time_limit=30,
            game_mode=game_details[game]["modes"][0],
            game_difficulty=game_details[game]["difficulties"][0],
            tutorial=True,
        )

    for i in range(2):
        shuffle(game_names)
        print(game_names)
        for game_name in game_names:
            shuffle(game_list[game_name])
            game_mode, game_difficulty = game_list[game_name].pop()
            GameScreen(
                participant_id=participant_id,
                game_name=f"ALE/{game_name}-v5",
                time_limit=30,
                game_mode=game_mode,
                game_difficulty=game_difficulty,
                session_number=i + 1,
            )
            shuffle(questions)
            survey = Survey(deepcopy(questions))
            survey.run()


if __name__ == "__main__":
    main()
