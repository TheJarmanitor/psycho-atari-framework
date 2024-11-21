import pygame
import sys
import pandas as pd

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
        for i, option in enumerate(self.options):
            color = BLUE if self.selected_option == i else BLACK
            option_text = f"{option}"
            text_surface = font.render(option_text, True, color)
            screen.blit(text_surface, (70, 100 + i * 40))

    def handle_event(self, event):
        """Handle key press for selecting an option."""
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7]:
                self.selected_option = event.key - pygame.K_1
                self.response = self.options[self.selected_option]
            if event.key == pygame.K_d:
                return "next"  # Move to the next question
            if event.key == pygame.K_a:
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
    def __init__(self, questions):
        self.questions = questions
        self.current_question_index = 0
        self.running = True

    def display_current_question(self):
        """Display the current question or thank-you message if survey is complete."""
        self.screen.fill(WHITE)
        if self.current_question_index < len(self.questions):
            self.questions[self.current_question_index].display(self.screen, self.font)
        else:
            # Display a thank-you message when the survey is complete
            thank_you_text = "Thank you for completing the survey!"
            text_surface = self.font.render(thank_you_text, True, GREEN)
            self.screen.blit(text_surface, (200, 250))
        pygame.display.flip()

    def handle_event(self, event):
        """Handle events for the current question."""
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            if question.handle_event(event) == "next":
                self.current_question_index += 1  # Move to the next question
            elif question.handle_event(event) == "back":
                self.current_question_index -= 1 if self.current_question_index > 0 else 0


    def is_complete(self):
        """Check if the survey is complete."""
        return self.current_question_index >= len(self.questions)

    def collect_responses(self):
        """Collects questions and responses into a DataFrame."""
        data = {
            "Question": [q.question_text for q in self.questions],
            "Response": [q.response for q in self.questions],
        }
        df = pd.DataFrame(data)
        return df

    def run(self, screen_width=800, screen_height=600):
        """Run the main loop for the survey."""
        if not pygame.get_init():
            pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Survey")
        self.font = pygame.font.Font(None, FONT_SIZE)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.handle_event(event)

            self.display_current_question()

            # Exit the survey after completion and short delay
            if self.is_complete():
                pygame.time.delay(2000)
                self.running = False

        # Quit Pygame and exit when the survey is done
        pygame.quit()
