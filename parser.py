import numpy as np
import pandas as pd

test_load = np.load("logs/00000_3900841174_0_1733222095057.npz", allow_pickle=True)
game_data = test_load.f.arr_0

print(game_data[0].keys())

ram_list = np.array([obs["obs_tp1"]["state"] for obs in game_data])

ram_df = pd.DataFrame(ram_list, columns=[f"ram_{i}" for i in range(1,ram_list.shape[1]+1)])
# print(ram_df)
