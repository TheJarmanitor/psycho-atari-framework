from game import GameScreen


def main():
    game_names = ["Turmoil", "WordZapper", "Centipede"]
    for game in game_names:
        GameScreen(f"ALE/{game}-v5", time_limit=5)



if __name__ == "__main__":
    main()
