from game import GameScreen
import uuid



def main():
    GameScreen(
        participant_id=0,
        game_name = "ALE/Centipede-v5",
        time_limit=15
    )


if __name__ == "__main__":
    main()
