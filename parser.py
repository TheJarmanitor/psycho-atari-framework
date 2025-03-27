# %%
import numpy as np
import pandas as pd

# %%
test_load = np.load("logs/test_20250325/576457e7-3a4e-4960-ba12-defe1bee9e68_Boxing-v5_0_1742909198954.npz", allow_pickle=True)
print(test_load)
# %%
game_data = test_load.f.arr_0
print(game_data)
# %%
# print(game_data[0].keys())

actions = np.array([obs["action"] for obs in game_data])
frames = np.array([obs["info"]["frame_number"] for obs in game_data])
ram_list = np.array([obs["obs_tp1"]["state"] for obs in game_data])
print(actions)
# ram_df = pd.DataFrame(ram_list, columns=[f"ram_{i}" for i in range(1,ram_list.shape[1]+1)])
