import gymnasium as gym
from gymnasium.utils.play import play

# from gymnasium.wrappers import AddRenderObservation
from gymnasium.wrappers import PixelObservationWrapper
from datetime import datetime
import pygame
import ale_py
from pygame.event import Event, post

# from pylsl import StreamInfo, StreamOutlet


class GameScreen:  # take difficulty into consideration. Randomizing
    def __init__(
        self,
        game_name,
        time_limit=None,
        fps=30,
        game_mode=None,
        game_difficulty=None,
        logs_path="logs",
    ) -> None:
        self.time_limit = time_limit
        self.game_name = game_name
        self.start_timestamp = int(datetime.timestamp(datetime.now()) * 1000)
        self.fps = fps
        self.logs = []
        self.game_mode = game_mode
        self.game_difficulty = game_difficulty
        if not pygame.get_init():
            pygame.init()

        env = gym.make(
            game_name,
            obs_type="ram",
            render_mode="rgb_array",
            frameskip=1,
            mode=self.game_mode,
            difficulty=self.game_difficulty,
        )

        keys = env.unwrapped.get_keys_to_action()
        env.metadata["render_fps"] = fps
        # env_wrapper = AddRenderObservation(env, render_only=False)
        env_wrapper = PixelObservationWrapper(env, pixels_only=False)
        # print(keys)

        play(env_wrapper, fps=fps, keys_to_action=keys, callback=self.callback, zoom=3)
        # infoObject = pygame.display.Info()
        # print(infoObject)

    def callback(self, obs_t, obs_tp1, action, rew, terminated, truncated, info):
        timestamp = int(datetime.timestamp(datetime.now()) * 1000)

        if (
            self.time_limit
            and timestamp - self.start_timestamp > self.time_limit * 1000
        ):
            terminated = True
            timeout = True
        else:
            timeout = False
        self.logs.append(
            {
                "game_name": self.game_name,
                "game_mode": self.game_mode,
                "game_difficulty": self.game_difficulty,
                "start_timestamp": self.start_timestamp,
                "timestamp": timestamp,
                "fps": self.fps,
                "obs_t": obs_t,
                "obs_tp1": obs_tp1,
                "action": action,
                "rew": rew,
                "terminated": terminated,
                "truncated": truncated,
                "info": info,
                "timeout": timeout,
            }
        )

        if terminated or timeout:
            post(Event(pygame.QUIT))


class SurveyScreen:
    pass


class TransitionScreen:  # random restting period, but fixed
    def __init__(self) -> None:
        pass
