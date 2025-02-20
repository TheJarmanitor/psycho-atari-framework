# %%
import numpy as np
import pandas as pd

# %%
test_load = np.load("logs/2fb75368-1d86-4ee2-9197-8da59d7db656_1072924176_tutorial_1739958732754.npz", allow_pickle=True)
print(test_load)
# %%
game_data = test_load.f.arr_0
print(game_data)
# %%
# print(game_data[0].keys())

actions = np.array([obs["action"] for obs in game_data])
frames = np.array([obs["info"]["frame_number"] for obs in game_data])
ram_list = np.array([obs["obs_tp1"]["state"] for obs in game_data])
print(frames)
# ram_df = pd.DataFrame(ram_list, columns=[f"ram_{i}" for i in range(1,ram_list.shape[1]+1)])
