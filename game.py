import gymnasium as gym
from gymnasium.utils.play import play
from gymnasium.wrappers import PixelObservationWrapper

import pygame


class Game():
    def __init__(self, game_name) -> None:
        if not pygame.get_init():
            pygame.init()

        env = gym.make(game_name, obs_type="ramd", render_mode="rgb_array", frameskip=1)
        keys = env.unwrapped.gett_keys_to_action()
        env.metadata["render_fps"] = 30
