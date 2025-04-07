import numpy as np
from events_manager import *
from glob import glob



# print(game_frames.shape)

"""

Event functions for each game and its parameters:

Boxing:
    detect_box_score_difference:
        Check a time frame when the difference between scores is beyond a certaing threshold.
        Parameters:
            box_data, the ram info for the game boxing
            threshold: the socre difference to represent the event
            pre: how many seconds prior to the event you want captured. set at 10
            post: how many seconds after the event you want captured. set at 5
            fps: frames per second
    detect_box_score_stagnation:
        Check a time frame when the scores don't changes for a certain time
        Parameters:
            box_data: the ram info for the game boxing
            stagnation: the amount of seconds to check for how long.
            fps: frames per second
    detect_box_first_hit:
        Detect the first effecctive hit by the player
        Parameters:
            box_data, the ram info for the game boxing
            pre: how many seconds prior to the event you want captured. set at 10
            post: how many seconds after the event you want captured. set at 5
            fps: frames per second

Turmoil:
    detect_turmoil_score_stagnation:
        Check a time frame when the score doesn't change for a certain time
        Parameters:
            turm_data: the ram info for the game turmoil
            stagnation: the amount of seconds to check for how long.
            fps: frames per second
    detect_turmoil_tank_destruction:
        Check a time frame when the tank appears and dissapears (whether its buy hitting it or just dissapearing)
        Parameters:
            turm_data: the ram info for the game turmoil
            pre: how many seconds prior to the event you want captured. set at 10
            post: how many seconds after the event you want captured. set at 5
            fps: frames per second
    detect_turmoil_death:
        Check the time frames when the player loses a life.
        Parameters:
            turm_data: the ram info for the game turmoil
            pre: how many seconds prior to the event you want captured. set at 10
            post: how many seconds after the event you want captured. set at 5
            fps: frames per second
    detect_turmoil_prize:
        Check the time frames when the prize appear and dissapears (whether by collecting it or turning into canon ball)
        Parameters:
            turm_data: the ram info for the game turmoil
            pre: how many seconds prior to the event you want captured. set at 3
            post: how many seconds after the event you want captured. set at 3
            fps: frames per second
WordZapper:
    detect_word_freebie_use:
        Check the time frames when the freebie is used.
        Parameters:
            word_data: the ram info for the game WordZapper
            pre: how many seconds prior to the event you want captured. set at 3
            post: how many seconds after the event you want captured. set at 3
            fps: frames per second
    detect_word_letter_stagnation:
        Check a time frame when target letters are not being chosen after a certain time
            Parameters:
                word_data: the ram info for the game WordZapper
                stagnation: the amount of seconds to check for how long.
                fps: frames per second
"""

logs_folder = input()
print(logs_folder)


game_files=glob(f"{logs_folder}\\*.npz")

print(game_files)


# game_states = np.array([frame["obs_tp1"]["state"] for frame in game_data], dtype="f")
# game_frames = np.array([frame["obs_tp1"]["pixels"] for frame in game_data])
# game_frames = game_frames[..., ::-1]

functions_dict = {
    "Turmoil": [detect_turmoil_score_stagnation, detect_turmoil_tank_destruction, detect_turmoil_death, detect_turmoil_prize],
    "Boxing": [detect_box_score_difference, detect_box_score_stagnation, detect_box_first_hit],
    "WordZapper": [detect_word_letter_stagnation, detect_word_freebie_use]
}

for file in game_files:
    file_name = file.split("\\")[1]
    user, game_name, trial = tuple(file_name.split("_"))
    game_name = game_name.removesuffix("-v5")
    game_load = np.load(
    file,
    allow_pickle=True,
    )
    game_data = game_load.f.arr_0
    game_states = np.array([frame["obs_tp1"]["state"] for frame in game_data], dtype="f")
    game_frames = np.array([frame["obs_tp1"]["pixels"] for frame in game_data])
    game_frames = game_frames[..., ::-1]
    for funct in functions_dict[game_name]:
        for i, (s_frame, e_frame) in enumerate(funct(game_states)):

            event_frames = game_frames[range(s_frame, e_frame)]
            create_video(event_frames, f"{user}_{trial}_{game_name}_{funct.__name__}_{i}.avi")
