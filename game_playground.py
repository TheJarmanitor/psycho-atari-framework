from game import GameScreen


game_name = "Boxing" # Names include Boxing, Turmoil, WordZapper

logs_folder= "logs" # where do you want your logs to be
game_mode = 0 # game mode, specific to each game
'''
turmoil: difficulty : 0 | modes: 0,1,2,3,4
WordZapper: difficulty: 0,1,2,3 | modes: 0,1,2,3
Boxing: difficulty: 0,1,2,3 | modes: 0
'''

game_difficulty = 0 #game difficulty, specific to each game

GameScreen(
    participant_id="erica_test",
    game_name=f"{game_name}-v5",
    time_limit=120,
    game_mode=game_mode,
    game_difficulty=game_difficulty,
    trial_number=0,
    logs_path=logs_folder,
)
