import os

import gymnasium as gym
from gymnasium.utils.play import play
from custom_keys import get_custom_keys_to_action

# from gymnasium.wrappers import AddRenderObservation
from gymnasium.wrappers import PixelObservationWrapper
from datetime import datetime
import pygame
import ale_py
from pygame.event import Event, post
import hashlib
import numpy as np


# from pylsl import StreamInfo, StreamOutle&t


class GameScreen:  # labels for tutorials and regular games
    def __init__(
        self,
        participant_id,
        game_name,
        session_number=0,
        tutorial=False,
        time_limit=None,
        fps=30,
        game_mode=None,
        game_difficulty=None,
        logs_path="logs",
    ) -> None:
        self.participant_id = participant_id

        self.time_limit = time_limit
        self.game_name = game_name
        self.session_number = session_number
        self.tutorial = tutorial
        self.game_id = int.from_bytes(
            hashlib.sha256(self.game_name.encode()).digest()[:4], "little"
        )
        self.start_timestamp = int(datetime.timestamp(datetime.now()) * 1000)
        self.fps = fps
        self.logs = []
        self.logs_path = logs_path
        self.game_mode = game_mode
        self.game_difficulty = game_difficulty
        if not pygame.get_init():
            pygame.init()

        env = gym.make(
            self.game_name,
            obs_type="ram",
            render_mode="rgb_array",
            frameskip=1,
            mode=self.game_mode,
            difficulty=self.game_difficulty,
        )
        action_set = env.unwrapped._action_set
        keys = get_custom_keys_to_action(action_set)
        # keys = env.unwrapped.get_keys_to_action()
        # print(keys)
        env.metadata["render_fps"] = self.fps
        # env_wrapper = AddRenderObservation(env, render_only=False)
        env_wrapper = PixelObservationWrapper(env, pixels_only=False)
        # print(keys)

        play(
            env_wrapper,
            fps=self.fps,
            keys_to_action=keys,
            callback=self.callback,
            zoom=3,
        )
        # infoObject = pygame.display.Info()
        # print(infoObject)
        if not os.path.exists(self.logs_path):
            os.mkdir(self.logs_path)

        np.savez_compressed(
            os.path.join(
                logs_path,
                f"{self.participant_id}".zfill(5)
                + f"_{self.game_id}_{self.session_number}_{self.start_timestamp}",
            ),
            self.logs,
        )

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
                "participant_id": self.participant_id,
                "session_number": self.session_number,
                "tutorial": self.tutorial,
                "game_id": self.game_id,
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
