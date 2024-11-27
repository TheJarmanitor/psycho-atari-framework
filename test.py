from game import GameScreen
import pygame
import uuid



def main():
    GameScreen(
        participant_id=0,
        game_name = "ALE/Centipede-v5",
        time_limit=15
    )
    # pygame.init()
    # pygame.joystick.init()
    # controller = pygame.joystick.Joystick(0)
    # while True:
    #     events = pygame.event.get()
    #     for event in events:
    #         if event.type == pygame.JOYBUTTONDOWN:
    #             print("Button Pressed")
    #             if controller.get_button(0):
    #                 print("This is the 0 button")
    #             if controller.get_button(1):
    #                 print("This is the 1 button")
    #             if controller.get_button(2):
    #                 print("This is the 2 button")
    #             if controller.get_button(3):
    #                 print("This is the 3 button")
            #     elif j.get_button(7):
            #         # Control Right Motor using R2
            # elif event.type == pygame.JOYBUTTONUP:
            #     print("Button Released")


if __name__ == "__main__":
    main()
