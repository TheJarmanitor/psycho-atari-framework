import pygame
import os
import pandas as pd
from random import randint
from random import shuffle
from datetime import datetime

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

    def __init__(self, question_text, question_label=None):
        self.question_text = question_text
        self.label = question_label if question_label is not None else question_text
        self.response = None

    def display(self, screen, font):
        """Display the question text."""
        text_surface = font.render(self.question_text, True, BLACK)
        screen.blit(text_surface, (50, 100))

    def handle_event(self, event):
        """Handle user input for the question."""
        pass


class MultipleChoiceQuestion(Question):
    def __init__(self, question_text, options, question_label=None):
        super().__init__(question_text, question_label)
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
        sw, sh = screen.get_size()

        grid_top = 150  # Adjust as needed for your question text
        available_height = sh - grid_top
        cell_width = sw / 3
        cell_height = available_height / 3

        # Compute centers for each cell in a 3x3 grid.
        # We use only the middle cell of row 2 for the middle row.
        centers = [
            (
                cell_width / 2,
                grid_top + cell_height / 2,
            ),  # Top row, left: Option 0 (Strongly disagree)
            (
                cell_width + cell_width / 2,
                grid_top + cell_height / 2,
            ),  # Top row, center: Option 1 (Disagree)
            (
                2 * cell_width + cell_width / 2,
                grid_top + cell_height / 2,
            ),  # Top row, right: Option 2 (Slightly disagree)
            (
                cell_width + cell_width / 2,
                grid_top + cell_height + cell_height / 2,
            ),  # Middle row, center: Option 3 (Neutral)
            (
                cell_width / 2,
                grid_top + 2 * cell_height + cell_height / 2,
            ),  # Bottom row, left: Option 4 (Slightly agree)
            (
                cell_width + cell_width / 2,
                grid_top + 2 * cell_height + cell_height / 2,
            ),  # Bottom row, center: Option 5 (Agree)
            (
                2 * cell_width + cell_width / 2,
                grid_top + 2 * cell_height + cell_height / 2,
            ),  # Bottom row, right: Option 6 (Strongly agree)
        ]

        center_left = (
            cell_width / 2,
            grid_top + cell_height + cell_height / 2,
        )  # Row 1, Col 0
        center_right = (
            2 * cell_width + cell_width / 2,
            grid_top + cell_height + cell_height / 2,
        )  # Row 1, Col 2
        # Define square size as 80% of the cell dimensions
        square_width = cell_width * 0.8
        square_height = cell_height * 0.8

        # Define matrix layout

        for i, option in enumerate(self.options):
            # Compute a gradient from red (option 0) to green (option 6)
            r = int(i * 255 / 6)
            g = 255 - int(i * 255 / 6)
            b = 0
            gradient_color = (r, g, b)

            center = centers[i]
            rect = pygame.Rect(0, 0, cell_width, cell_height)
            rect.center = center

            # Draw filled rectangle with gradient color.
            pygame.draw.rect(screen, gradient_color, rect)

            # If this option is selected, draw a blue border.
            if self.selected_option == i:
                pygame.draw.rect(screen, BLUE, rect, 5)

            # Render the option text (centered in the square)
            text_surface = font.render(option, True, BLACK)
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)
            # Draw arrows in the unused grid cells:
        arrow_size = min(cell_width, cell_height) * 0.5

        # Left arrow (back) at center_left: triangle pointing left
        clx, cly = center_left
        left_arrow = [
            (clx + arrow_size / 2, cly - arrow_size / 2),
            (clx - arrow_size / 2, cly),
            (clx + arrow_size / 2, cly + arrow_size / 2),
        ]
        pygame.draw.polygon(screen, BLACK, left_arrow)

        # Right arrow (next) at center_right: triangle pointing right
        crx, cry = center_right
        right_arrow = [
            (crx - arrow_size / 2, cry - arrow_size / 2),
            (crx + arrow_size / 2, cry),
            (crx - arrow_size / 2, cry + arrow_size / 2),
        ]
        pygame.draw.polygon(screen, BLACK, right_arrow)

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
        labels,
        screen_width=800,
        screen_height=600,
        fullscreen=False,
        shuffle_q=True,
        stream=None,
    ):
        # self.participant_id = participant_id,
        # self.game_id = game_id,
        self.questions = questions
        self.labels = labels
        self.current_question_index = 0
        self.running = True
        self.fullscreen = fullscreen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.stream = stream

        if shuffle_q:
            shuffle(questions)

        pygame.init()
        self.screen = pygame.display.set_mode(
            (screen_width, screen_height), pygame.FULLSCREEN if fullscreen else 0
        )
        pygame.display.set_caption("Survey")
        self.font = pygame.font.Font(None, FONT_SIZE)

    def display_current_question(self):
        """Display the current question or thank-you message if survey is complete."""
        self.screen.fill(WHITE)

        sw, sh = self.screen.get_size()
        progress = self.current_question_index / len(self.questions)
        bar_width = sw * 0.8
        bar_height = 20
        bar_x = sw * 0.1
        bar_y = 10
        # Background of the progress bar (light gray)
        pygame.draw.rect(
            self.screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height)
        )
        # Filled part (blue)
        pygame.draw.rect(
            self.screen, BLUE, (bar_x, bar_y, bar_width * progress, bar_height)
        )
        # Progress percentage text
        progress_percent = int(progress * 100)
        progress_text = self.font.render(f"{progress_percent}% completed", True, BLACK)
        self.screen.blit(progress_text, (bar_x, bar_y + bar_height + 5))

        if self.current_question_index < len(self.questions):
            self.questions[self.current_question_index].display(self.screen, self.font)
        else:
            # Display a thank-you message when the survey is complete
            thank_you_text = "You're done! Now Relax for a bit."
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

    def send_responses(self, surveyor_info):
        timestamp = int(datetime.timestamp(datetime.now()) * 1000)

        data = {question.label: question.response for question in self.questions}

        index_map = {v: i for i, v in enumerate(list(self.labels))}

        surveyor_info.update(
            dict(sorted(data.items(), key=lambda pair: index_map[pair[0]]))
        )

        surveyor_info["TIMES"] = timestamp
        """Collects questions and responses into a DataFrame."""
        if self.stream:
            self.stream.send_data((answer for answer in surveyor_info.values()))
        print(index_map)
        print(surveyor_info)

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
