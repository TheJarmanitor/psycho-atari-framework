import os

import gymnasium as gym
from gymnasium.utils.play import play
from custom_keys import custom_keys_to_action

# from gymnasium.wrappers import AddRenderObservation
from gymnasium.wrappers import PixelObservationWrapper
from datetime import datetime
import pygame
import ale_py
from pygame.event import Event, post
import hashlib
import numpy as np

import time


class GameScreen:  # labels for tutorials and regular games
    def __init__(
        self,
        participant_id,
        game_name,
        trial_number=0,
        fullscreen=False,
        tutorial=False,
        time_limit=None,
        fps=30,
        game_mode=None,
        game_difficulty=None,
        logs_path="logs",
        stream=None,
    ) -> None:
        self.participant_id = participant_id

        self.time_limit = time_limit
        self.game_name = game_name
        self.trial_number = trial_number
        self.tutorial = tutorial
        # self.game_id = int.from_bytes(
        #     hashlib.sha256(self.game_name.encode()).digest()[:4], "little"
        # )
        self.start_timestamp = int(datetime.timestamp(datetime.now()) * 1000)
        self.fps = fps
        self.logs = []
        self.logs_path = logs_path
        self.game_mode = game_mode
        self.game_difficulty = game_difficulty
        self.stream = stream
        if not pygame.get_init():
            pygame.init()
        if fullscreen:
            pygame.RESIZABLE = pygame.FULLSCREEN
        env = gym.make(
            f"ALE/{self.game_name}",
            obs_type="ram",
            render_mode="rgb_array",
            frameskip=1,
            mode=self.game_mode,
            difficulty=self.game_difficulty,
            full_action_space=True,
        )
        action_set = env.unwrapped._action_set
        env.metadata["render_fps"] = self.fps
        # env_wrapper = AddRenderObservation(env, render_only=False)
        env_wrapper = PixelObservationWrapper(env, pixels_only=False)
        # print(keys)
        keys = custom_keys_to_action(action_set)
        play(
            env_wrapper,
            fps=self.fps,
            keys_to_action=keys,
            callback=self.callback,
            zoom=6,
        )
        # infoObject = pygame.display.Info()
        # print(infoObject)
        if not os.path.exists(self.logs_path):
            os.mkdir(self.logs_path)

        np.savez_compressed(
            os.path.join(
                logs_path,
                f"{self.participant_id}".zfill(5)
                + f"_{self.game_name}_{self.trial_number}_{self.start_timestamp}",
            ),
            self.logs,
        )

    def callback(self, obs_t, obs_tp1, action, rew, terminated, truncated, info):
        timestamp = int(datetime.timestamp(datetime.now()) * 1000)

        if self.stream:
            self.stream.send_data(
                (
                    self.participant_id,
                    self.game_name,
                    self.trial_number,
                    self.game_mode,
                    self.game_difficulty,
                    self.start_timestamp,
                    timestamp,
                    info["frame_number"],
                    terminated,
                    truncated,
                )
            )

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
                "trial_number": self.trial_number,
                "game_name": self.game_name,
                "obs_t": obs_t,
                "obs_tp1": obs_tp1,
                "action": action,
                "rew": rew,
                "info": info,
            }
        )

        if terminated or timeout:
            post(Event(pygame.QUIT))


class StartScreen:
    def __init__(self, screen_width=800, screen_height=600, countdown=3, outlet=None):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.font = pygame.font.Font(None, 48)
        self.running = True
        self.countdown = countdown
        self.started = False

    def display_message(self, message):
        self.screen.fill((0, 0, 0))
        text_surface = self.font.render(message, True, (255, 0, 0))
        text_rect = text_surface.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2)
        )
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def wait_for_start(self):
        self.display_message("Please wait. The experiment should start soon")
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.start_countdown()
                    return

    def start_countdown(self):
        for i in range(self.countdown, 0, -1):
            self.display_message(f"Experiment begins in {i}...")
            time.sleep(1)

            self.running = False

    def run(self):
        self.wait_for_start()
        pygame.quit()


class MessageScreen:
    def __init__(
        self,
        screen_width=800,
        screen_height=600,
        countdown=5,
        message="None",
        outlet=None,
    ):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.font = pygame.font.Font(None, 48)
        self.countdown = countdown
        self.message = message

    def display_message(self):
        self.screen.fill((0, 0, 0))
        text_surface = self.font.render(self.message, True, (255, 0, 0))
        text_rect = text_surface.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2)
        )
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def run(self):
        self.display_message()
        time.sleep(self.countdown)
        pygame.quit()
