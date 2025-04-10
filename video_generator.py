import numpy as np
from events_manager import *
from pathlib import Path




def generate_videos(logs_folder, participant_id, trial, output_folder="videos"):

    logs_path = Path(logs_folder)
    game_files=list(logs_path.glob(f"*{participant_id}*{trial}.npz"))



    functions_dict = {
        "Turmoil": [detect_turmoil_score_stagnation, detect_turmoil_tank_destruction, detect_turmoil_death, detect_turmoil_prize],
        "Boxing": [detect_box_score_difference, detect_box_score_stagnation, detect_box_first_hit],
        "WordZapper": [detect_word_letter_stagnation, detect_word_freebie_use]
    }

    for file in game_files:

        file_name = file.parts[-1]
        user, game_name, trial = tuple(file_name.split("_"))
        game_name = game_name.removesuffix("-v5")
        trial = trial.removesuffix(".npz")
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
                video_path = Path(output_folder)
                video_path = video_path / user / game_name / f"trial_{trial}"
                #print(video_path)
                video_path.mkdir(parents=True, exist_ok=True)
                create_video(event_frames, video_path / f"{funct.__name__}_{i}.avi")
