from functools import lru_cache
import pygame
import ale_py

# @lru_cache(1)
def get_custom_keys_to_action(action_set, joystick=False):
    """Return keymapping -> actions for human play.

    Up, down, left and right are wasd keys with fire being space.
    No op is 'e'

    Returns:
        Dictionary of key values to actions
    """
    if joystick:
        controller = pygame.joystick.Joystick(0)

        UP = pygame.CONTROLLER_BUTTON_DPAD_UP
        LEFT = pygame.CONTROLLER_BUTTON_DPAD_LEFT
        RIGHT = pygame.CONTROLLER_BUTTON_DPAD_RIGHT
        DOWN = pygame.CONTROLLER_BUTTON_DPAD_DOWN
        FIRE = pygame.CONTROLLERBUTTONDOWN
    else:
        UP = pygame.K_UP
        LEFT = pygame.K_LEFT
        RIGHT = pygame.K_RIGHT
        DOWN = pygame.K_DOWN
        FIRE = pygame.K_SPACE
    NOOP = ord("e")

    mapping = {
        ale_py.Action.NOOP: (NOOP,),
        ale_py.Action.UP: (UP,),
        ale_py.Action.FIRE: (FIRE,),
        ale_py.Action.DOWN: (DOWN,),
        ale_py.Action.LEFT: (LEFT,),
        ale_py.Action.RIGHT: (RIGHT,),
        ale_py.Action.UPFIRE: (UP, FIRE),
        ale_py.Action.DOWNFIRE: (DOWN, FIRE),
        ale_py.Action.LEFTFIRE: (LEFT, FIRE),
        ale_py.Action.RIGHTFIRE: (RIGHT, FIRE),
        ale_py.Action.UPLEFT: (UP, LEFT),
        ale_py.Action.UPRIGHT: (UP, RIGHT),
        ale_py.Action.DOWNLEFT: (DOWN, LEFT),
        ale_py.Action.DOWNRIGHT: (DOWN, RIGHT),
        ale_py.Action.UPLEFTFIRE: (UP, LEFT, FIRE),
        ale_py.Action.UPRIGHTFIRE: (UP, RIGHT, FIRE),
        ale_py.Action.DOWNLEFTFIRE: (DOWN, LEFT, FIRE),
        ale_py.Action.DOWNRIGHTFIRE: (DOWN, RIGHT, FIRE),
    }

    # Map
    #   (key, key, ...) -> action_idx
    # where action_idx is the integer value of the action enum
    #
    return {
        tuple(sorted(mapping[act_idx])): act_idx for act_idx in action_set
    }
