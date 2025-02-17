from game import GameScreen, StartScreen
import numpy as np

def main():
    StartScreen().run()
    GameScreen(participant_id=0, game_name="ALE/WordZapper-v5")
    # pygame.init()
    # controller = pygame.joystick.Joystick(0)
    # while True:
    #     #     events = pygame.event.get()
    #     #     for event in events:
    #     #         if event.type == pygame.JOYBUTTONDOWN:
    #     #             print("Button Pressed")
    #     #             print(event.button)
    #     for event in pygame.event.get():

    #         if event.type == pygame.JOYHATMOTION:

    #             print(event)



if __name__ == "__main__":
    main()
