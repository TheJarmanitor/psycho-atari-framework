import pygame
import ale_py


# @lru_cache(1)
def custom_keys_to_action(action_set):
    """Return keymapping -> actions for human play.

    Up, down, left and right are wasd keys with fire being space.
    No op is 'e'

    Returns:
        Dictionary of key values to actions
    """

    UP = pygame.K_w
    LEFT = pygame.K_a
    RIGHT = pygame.K_d
    DOWN = pygame.K_s
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
    return {tuple(sorted(mapping[act_idx])): act_idx for act_idx in action_set}


def joystick_to_keys(action_set):
    """
    Translate joystick input to the corresponding keys for the Arcade Learning Environment.

    Args:
        action_set (list): List of actions available in the environment.

    Returns:
        dict: A mapping of joystick states to action indices.
    """
    # Axis mappings for a standard joystick

    # Initialize pygame joystick if not already initialized
    joystick = pygame.joystick.Joystick(0)

    joystick.init()

    # Directional input states

    # Button states
    fire_button = joystick.get_button(
        0
    )  # Assuming the 'A' button or similar is used for fire

    # Translate joystick input to actions
    actions = set()

    if joystick.get_hat(0)[1]:  # Up
        actions.add(pygame.K_UP)
    elif joystick.get_hat(0)[1] == -1:  # Down
        actions.add(pygame.K_DOWN)

    if joystick.get_hat(0)[0] == -1:  # Left
        actions.add(pygame.K_LEFT)
    elif joystick.get_hat(0)[0] == -1:  # Right
        actions.add(pygame.K_RIGHT)

    if fire_button:  # Fire
        actions.add(pygame.K_SPACE)

    # Map the joystick input to the predefined key-to-action mapping
    key_to_action = custom_keys_to_action(action_set)
    sorted_actions = tuple(sorted(actions))  # Sort for consistent lookup

    return key_to_action.get(sorted_actions, ale_py.Action.NOOP)
