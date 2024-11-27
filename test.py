from game import GameScreen
import pygame
import uuid



def main():
    # GameScreen(
    #     participant_id=0,
    #     game_name = "ALE/Centipede-v5",
    #     time_limit=15
    # )
    pygame.init()
    pygame.joystick.init()
    controller = pygame.joystick.Joystick(0)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                print("Button Pressed")
            #     if j.get_button(6):
            #         # Control Left Motor using L2
            #     elif j.get_button(7):
            #         # Control Right Motor using R2
            # elif event.type == pygame.JOYBUTTONUP:
            #     print("Button Released")


if __name__ == "__main__":
    main()
