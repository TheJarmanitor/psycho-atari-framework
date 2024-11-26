from game import GameScreen
from survey import MultipleChoiceQuestion, Survey
from random import choice, shuffle
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
    questions = [
        MultipleChoiceQuestion("I liked the game", answers),
        MultipleChoiceQuestion("The Game was hard", answers),
    ]

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

    # game_names = list(game_details.keys()) #change to list of possiblities
    # for _ in range(1):
    #     shuffle(game_names)
    #     for game_name in game_names:

    #         game_mode = choice(game_list[game_name]["modes"])
    #         game_difficulty = choice(game_list[game_name]["difficulties"])

    #         GameScreen(
    #             participant_id=participant_id,
    #             game_name=f"ALE/{game_name}-v5",
    #             time_limit=5,
    #             game_mode=game_mode,
    #             game_difficulty=game_difficulty,
    #         )
    #         survey = Survey(deepcopy(questions))
    #         survey.run()


if __name__ == "__main__":
    main()
