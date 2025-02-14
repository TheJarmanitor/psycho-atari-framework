import pygame
import os
import pandas as pd
from random import randint

# import pandas as pd  # Importing pandas for DataFrame handling

# Colors and font settings
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
GREEN = (34, 139, 34)
FONT_SIZE = 36


# Question Classes
class Question:
    """Base class for a question in the survey."""

    def __init__(self, question_text):
        self.question_text = question_text
        self.response = None

    def display(self, screen, font):
        """Display the question text."""
        text_surface = font.render(self.question_text, True, BLACK)
        screen.blit(text_surface, (50, 50))

    def handle_event(self, event):
        """Handle user input for the question."""
        pass


class MultipleChoiceQuestion(Question):
    def __init__(self, question_text, options):
        super().__init__(question_text)
        self.options = options
        self.selected_option = None
        # self.keybinds = {
        #     -3: [pygame.],
        #     -2: [""],
        #     -1: [""],
        #     0:
        # }

    def display(self, screen, font):
        """Display the multiple-choice question with options."""
        super().display(screen, font)
        screen_width, screen_height = screen.get_size()

        # Dynamically calculate positions based on screen size
        row_height = screen_height // 6
        col_width = screen_width // 4

        # Define matrix layout
        positions = [
            (col_width, row_height),  # Top Row: Slightly Agree
            (2 * col_width, row_height),  # Top Row: Agree
            (3 * col_width, row_height),  # Top Row: Strongly Agree
            (2 * col_width, 2 * row_height),  # Middle Row: Neutral
            (col_width, 3 * row_height),  # Bottom Row: Slightly Disagree
            (2 * col_width, 3 * row_height),  # Bottom Row: Disagree
            (3 * col_width, 3 * row_height),  # Bottom Row: Strongly Disagreewww
        ]
        for i, option in enumerate(self.options):
            color = BLUE if self.selected_option == i else BLACK
            option_text = f"{option}"
            text_surface = font.render(option_text, True, color)
            x, y = positions[i]
            screen.blit(text_surface, (x, y))

    def handle_event(self, event):
        scale = [
            pygame.K_1,
            pygame.K_2,
            pygame.K_3,
            pygame.K_5,
            pygame.K_7,
            pygame.K_8,
            pygame.K_9,
        ]
        """Handle key press for selecting an option."""
        if event.type == pygame.KEYDOWN:
            if event.key in scale:
                self.selected_option = scale.index(event.key)
                self.response = self.options[self.selected_option]
                #
                # return "next"
            if event.key == pygame.K_6:
                return "next"  # Move to the next question
            if event.key == pygame.K_4:
                return "back"


class ShortAnswerQuestion(Question):
    def __init__(self, question_text):
        super().__init__(question_text)
        self.response = ""

    def display(self, screen, font):
        """Display the short answer question with current response text."""
        super().display(screen, font)
        answer_text = "Answer: " + self.response
        text_surface = font.render(answer_text, True, BLUE)
        screen.blit(text_surface, (70, 150))

    def handle_event(self, event):
        """Handle text input for the short answer."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.response = self.response[:-1]
            elif event.key == pygame.K_RETURN:
                return True  # Move to the next question
            else:
                self.response += event.unicode
        return False


# Survey Class with screen management and DataFrame collection
class Survey:
    def __init__(
        self,
        # participant_id,
        # game_id,
        questions,
        screen_width=800,
        screen_height=600,
        fullscreen=False,
        outlet=None,
    ):
        # self.participant_id = participant_id,
        # self.game_id = game_id,
        self.questions = questions
        self.current_question_index = 0
        self.running = True
        self.fullscreen = fullscreen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.outlet = outlet

        pygame.init()
        self.screen = pygame.display.set_mode(
            (screen_width, screen_height), pygame.FULLSCREEN if fullscreen else 0
        )
        pygame.display.set_caption("Survey")
        self.font = pygame.font.Font(None, FONT_SIZE)

    def display_current_question(self):
        """Display the current question or thank-you message if survey is complete."""
        self.screen.fill(WHITE)
        if self.current_question_index < len(self.questions):
            self.questions[self.current_question_index].display(self.screen, self.font)
        else:
            # Display a thank-you message when the survey is complete
            thank_you_text = "You're done! Now Relax for a bit :)"
            text_surface = self.font.render(thank_you_text, True, GREEN)
            self.screen.blit(
                text_surface, (self.screen_width // 4, self.screen_height // 2)
            )
        pygame.display.flip()

    def handle_event(self, event):
        """Handle events for the current question."""
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            if question.handle_event(event) == "next":
                self.current_question_index += 1  # Move to the next question
            elif question.handle_event(event) == "back":
                self.current_question_index -= (
                    1 if self.current_question_index > 0 else 0
                )

    def is_complete(self):
        """Check if the survey is complete."""
        return self.current_question_index >= len(self.questions)

    def collect_responses(self, data_file, surveyor_info):
        """Collects questions and responses into a DataFrame."""
        data = {
            question.question_text: [question.response] for question in self.questions
        }
        surveyor_info.update(data)
        df = pd.DataFrame(surveyor_info)
        if os.path.exists(data_file):
            df_historic = pd.read_csv(data_file)
            df = pd.concat([df_historic, df], ignore_index=True, axis=0)

        df.to_csv(data_file, index=False)

    def run(self, random_timer=True):
        """Run the main loop for the survey."""
        # if not pygame.get_init():
        #     pygame.init()
        # self.screen = pygame.display.set_mode((screen_width, screen_height))
        # pygame.display.set_caption("Survey")
        # self.font = pygame.font.Font(None, FONT_SIZE)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.handle_event(event)

            self.display_current_question()

            # Exit the survey after completion and short delay
            if self.is_complete():
                if random_timer:
                    timer = randint(2, 10) * 1000
                else:
                    timer = 2000
                pygame.time.delay(timer)
                self.running = False

        # Quit Pygame and exit when the survey is done
        pygame.quit()
