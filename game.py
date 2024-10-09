import gymnasium as gym
from gymnasium.utils.play import play

# from gymnasium.wrappers import AddRenderObservation
# from gymnasium.wrappers import AddPixelInformation
import ale_py
import pygame


class Game:
    def __init__(self, game_name, fps=30) -> None:
        if not pygame.get_init():
            pygame.init()

        env = gym.make(game_name, obs_type="ram", render_mode="rgb_array", frameskip=1)

        keys = env.unwrapped.get_keys_to_action()
        print(keys)
        env.metadata["render_fps"] = fps
        # env_wrapper = AddRenderObservation(env, render_only=False)
        # print(keys)

        play(env, fps=fps, keys_to_action=keys, zoom=3)
