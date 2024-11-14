from game import GameScreen
from survey import MultipleChoiceQuestion, Survey
from random import choice, shuffle


def main(): #add with "tutorial version", later with random difficulties
    questions = [
        MultipleChoiceQuestion(
            "Did you liked the game", ["Yes", "No", "How did you get in my house?"]
        ),
        MultipleChoiceQuestion("Was it hard?", ["Yes", "No", "I'm calling the police"]),
    ]

    game_list = {
        "Turmoil": {"modes": [x for x in range(9)], "difficulties": [0]},
        "WordZapper": {
            "modes": [x for x in range(24)],
            "difficulties": [x for x in range(4)],
        },
        "Centipede": {"modes": [22, 86], "difficulties": [0]},
    }
    game_names = list(game_list.keys()) #change to list of possiblities
    for _ in range(1):
        shuffle(game_names)
        for game_name in game_names:

            game_mode = choice(game_list[game_name]["modes"])
            game_difficulty = choice(game_list[game_name]["difficulties"])

            GameScreen(
                f"ALE/{game_name}-v5",
                time_limit=5,
                game_mode=game_mode,
                game_difficulty=game_difficulty,
            )
            survey = Survey(questions)
            survey.run()


if __name__ == "__main__":
    main()
