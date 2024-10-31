import gymnasium as gym
from gymnasium.utils.play import play

# from gymnasium.wrappers import AddRenderObservation
from gymnasium.wrappers import PixelObservationWrapper
from datetime import datetime
import ale_py
import pygame
from pygame.event import Event, post


class GameScreen:
    def __init__(self, game_name, time_limit=None, fps=30) -> None:
        self.time_limit=time_limit

        self.start_timestamp = int(datetime.timestamp(datetime.now()) * 1000)

        if not pygame.get_init():
            pygame.init()

        env = gym.make(game_name, obs_type="ram", render_mode="rgb_array", frameskip=1)

        keys = env.unwrapped.get_keys_to_action()
        env.metadata["render_fps"] = fps
        # env_wrapper = AddRenderObservation(env, render_only=False)
        env_wrapper = PixelObservationWrapper(env, pixels_only=False)
        # print(keys)

        play(env_wrapper, fps=fps, keys_to_action=keys, callback=self.callback, zoom=3)
        infoObject = pygame.display.Info()
        print(infoObject)

    def callback(self, obs_t, obs_tp1, action, rew, terminated, truncated, info):
        timestamp = int(datetime.timestamp(datetime.now()) * 1000)

        if self.time_limit and timestamp - self.start_timestamp > self.time_limit * 1000:
            terminated = True
            timeout = True
        else:
            timeout = False

        if terminated:
            post(Event(pygame.QUIT))

class TransitionScreen:
    def __init__(self) -> None:
        pass
