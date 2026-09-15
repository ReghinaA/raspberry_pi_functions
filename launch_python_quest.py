import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings - virtual "design" resolution stays 480x320 so every
# existing coordinate in this file keeps working unchanged.
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320
screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

# Real Raspberry Pi monitor resolution
REAL_WIDTH = 1024
REAL_HEIGHT = 600
SCALE = 1.875  # max scale that fits 320px height into 600px (320 * 1.875 = 600)
GAME_WIDTH = int(SCREEN_WIDTH * SCALE)    # 900
GAME_HEIGHT = int(SCREEN_HEIGHT * SCALE)  # 600
OFFSET_X = (REAL_WIDTH - GAME_WIDTH) // 2  # side margins (pillarboxing)
OFFSET_Y = (REAL_HEIGHT - GAME_HEIGHT) // 2

# Fullscreen switch:
#   True  - fullscreen 1024x600, same as real Raspberry Pi monitor
#   False - normal window 1024x600 for development on laptop
#           (can take screenshots and close window)
FULLSCREEN = False

display_flags = pygame.FULLSCREEN if FULLSCREEN else 0
real_screen = pygame.display.set_mode((REAL_WIDTH, REAL_HEIGHT), display_flags)
LETTERBOX_COLOR = (30, 30, 30)

# Small "X" exit button, drawn in the left letterbox margin (real-screen
# coordinates, not the virtual 480x320 canvas) so it stays out of the way
# of the game content and doesn't look like a game button to a child.
EXIT_BTN_CENTER = (OFFSET_X // 2, 30)
EXIT_BTN_RADIUS = 16


def draw_exit_button():
    cx, cy = EXIT_BTN_CENTER
    pygame.draw.circle(real_screen, (80, 80, 80), EXIT_BTN_CENTER, EXIT_BTN_RADIUS)
    pygame.draw.circle(real_screen, (150, 150, 150), EXIT_BTN_CENTER, EXIT_BTN_RADIUS, 2)
    d = 6
    pygame.draw.line(real_screen, (220, 220, 220), (cx - d, cy - d), (cx + d, cy + d), 3)
    pygame.draw.line(real_screen, (220, 220, 220), (cx - d, cy + d), (cx + d, cy - d), 3)


def is_exit_button_click(pos):
    cx, cy = EXIT_BTN_CENTER
    x, y = pos
    return (x - cx) ** 2 + (y - cy) ** 2 <= EXIT_BTN_RADIUS ** 2


def present():
    """Scale the virtual 480x320 screen up and show it centered on the real monitor."""
    scaled = pygame.transform.smoothscale(screen, (GAME_WIDTH, GAME_HEIGHT))
    real_screen.fill(LETTERBOX_COLOR)
    real_screen.blit(scaled, (OFFSET_X, OFFSET_Y))
    draw_exit_button()
    pygame.display.flip()
pygame.display.set_caption("Python Quest")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (34, 139, 34)
BLUE = (0, 100, 255)
TEAL = (76, 154, 147)
ORANGE = (224, 142, 69)
PURPLE = (132, 100, 160)
SELECTED_HIGHLIGHT = (255, 150, 0)  # quiz "answer selected, waiting" color
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
YELLOW = (255, 200, 0)
RED = (255, 50, 50)

# Clock for FPS
clock = pygame.time.Clock()
FPS = 30

# Font
FONT_TITLE_PATH = "assets/fonts/Fredoka-Bold.ttf"
FONT_BODY_PATH = "assets/fonts/Nunito-Regular.ttf"

font_title = pygame.font.Font(FONT_TITLE_PATH, 16)
font_large = pygame.font.Font(FONT_TITLE_PATH, 18)
font_hi = pygame.font.Font(FONT_TITLE_PATH, 24)
font_code = pygame.font.Font(None, 20)
font_small = pygame.font.Font(FONT_BODY_PATH, 14)
font_comment = pygame.font.Font(FONT_BODY_PATH, 12)
font_tiny = pygame.font.Font(FONT_BODY_PATH, 12)

# Load dinosaur image
try:
    dinosaur_image = pygame.image.load("dinosaur.png")
    dinosaur_image = pygame.transform.smoothscale(dinosaur_image, (90, 100))
    dinosaur_loaded = True
except:
    print("Warning: dinosaur.png not found.")
    dinosaur_loaded = False

# Load "WELCOME" title image
try:
    welcome_image = pygame.image.load("assets/images/welcome.png").convert_alpha()
    welcome_image = pygame.transform.smoothscale(welcome_image, (300, 62))
    welcome_image_loaded = True
except:
    print("Warning: welcome.png not found.")
    welcome_image_loaded = False

# Load quiz feedback cat icons - shown next to the Correct/Wrong text
try:
    smiling_cat_image = pygame.image.load("smiling_cat.png")
    smiling_cat_image = pygame.transform.smoothscale(smiling_cat_image, (60, 60))
    smiling_cat_loaded = True
except:
    print("Warning: smiling_cat.png not found.")
    smiling_cat_image = None
    smiling_cat_loaded = False

try:
    thinking_cat_image = pygame.image.load("thinking_cat.png")
    thinking_cat_image = pygame.transform.smoothscale(thinking_cat_image, (60, 60))
    thinking_cat_loaded = True
except:
    print("Warning: thinking_cat.png not found.")
    thinking_cat_image = None
    thinking_cat_loaded = False


def draw_dinosaur():
    """Draw dinosaur image in the bottom right corner"""
    if dinosaur_loaded:
        dino_x = SCREEN_WIDTH - dinosaur_image.get_width() - 10
        dino_y = SCREEN_HEIGHT - dinosaur_image.get_height() - 10
        screen.blit(dinosaur_image, (dino_x, dino_y))


# ===== WELCOME SCREEN =====

def show_welcome_screen():
    """Show welcome screen"""
    screen.fill(WHITE)

    # Main title - "WELCOME" as an image, with text fallback if it's missing
    if welcome_image_loaded:
        title1_x = SCREEN_WIDTH // 2 - welcome_image.get_width() // 2
        screen.blit(welcome_image, (title1_x, 20))
    else:
        title1 = font_title.render("WELCOME", True, BLACK)
        title1_x = SCREEN_WIDTH // 2 - title1.get_width() // 2
        screen.blit(title1, (title1_x, 30))

    title2_part1 = font_large.render("to ", True, BLACK)
    title2_part2 = font_large.render("Python Quest", True, TEAL)

    # "to Python Quest" on next line
    title2_combined_width = title2_part1.get_width() + title2_part2.get_width()
    title2_x = SCREEN_WIDTH // 2 - title2_combined_width // 2
    screen.blit(title2_part1, (title2_x, 88))
    screen.blit(title2_part2, (title2_x + title2_part1.get_width(), 88))

    # Subtitle - multiline
    subtitle_lines = [
        "an educational app for kids",
        "who want to know more about",
        "Python language"
    ]

    y = 116
    for line in subtitle_lines:
        subtitle = font_small.render(line, True, BLACK)
        subtitle_x = SCREEN_WIDTH // 2 - subtitle.get_width() // 2
        screen.blit(subtitle, (subtitle_x, y))
        y += 20

    # Instruction to continue
    instruction = font_small.render("Click to continue", True, DARK_GREEN)
    instruction_x = SCREEN_WIDTH // 2 - instruction.get_width() // 2
    screen.blit(instruction, (instruction_x, SCREEN_HEIGHT - 70))

    # Credits at bottom
    credit1 = font_tiny.render("Developed by BirchTree", True, BLUE)
    credit1_x = SCREEN_WIDTH // 2 - credit1.get_width() // 2
    screen.blit(credit1, (credit1_x, SCREEN_HEIGHT - 45))

    credit2 = font_tiny.render("Image credits: ArtsyBeeKids (Dinosaur and Welcome images)", True, BLUE)
    credit2_x = SCREEN_WIDTH // 2 - credit2.get_width() // 2
    screen.blit(credit2, (credit2_x, SCREEN_HEIGHT - 25))

    # Draw dinosaur in bottom right corner
    draw_dinosaur()

    present()


# ===== LESSON 1: FUNCTIONS =====

# Function code with explanations for each line
FUNCTION_HELLO = [
    ("def write_hello():", "This is the start of our function"),
    ("    screen.fill(WHITE)", "Fill the whole screen with white color"),
    ("    text = font.render('Hi!', True, GREEN)", "Create the text 'Hi!' in green color"),
    ("    text_rect = text.get_rect(", ""),
    ("        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))", "Get the position to center the text"),
    ("    screen.blit(text, text_rect)", "Draw the text on the screen"),
    ("    pygame.display.flip()", "Show everything we drew!")
]

FUNCTION_SQUARE = [
    ("def draw_square():", "This is the start of our function"),
    ("    screen.fill(WHITE)", "Fill the whole screen with white color"),
    ("    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH // 2 - 50,", ""),
    ("        SCREEN_HEIGHT // 2 - 50, 100, 100))", "Draw a blue square in the middle"),
    ("    pygame.display.flip()", "Show the square on the screen!")
]

FUNCTION_CIRCLE = [
    ("def draw_circle():", "This is the start of our function"),
    ("    screen.fill(WHITE)", "Fill the whole screen with white color"),
    ("    pygame.draw.circle(screen, RED, (SCREEN_WIDTH // 2,", ""),
    ("        SCREEN_HEIGHT // 2), 50)", "Draw a red circle in the middle"),
    ("    pygame.display.flip()", "Show the circle on the screen!")
]

# Horizontal center of the 2x2 answer-button grid (button_x_start=25,
# button_width=150, gap=20 -> block spans 25 to 345). The feedback
# text/icon under the buttons lines up with this, not the full screen.
ANSWERS_CENTER_X = 185


def draw_icon_and_text(icon, icon_loaded, text_surface, y, center_x=SCREEN_WIDTH // 2):
    """Draw an icon (if available) immediately to the left of a text
    surface, with the pair centered horizontally on center_x"""
    icon_w = icon.get_width() + 6 if icon_loaded else 0
    total_w = icon_w + text_surface.get_width()
    start_x = center_x - total_w // 2

    if icon_loaded:
        icon_y = y + (text_surface.get_height() - icon.get_height()) // 2
        screen.blit(icon, (start_x, icon_y))

    screen.blit(text_surface, (start_x + icon_w, y))


# Quiz questions with code and visual answers
# Each question has: code_to_show, correct_answer_index, answer_options
QUIZ_QUESTIONS = [
    {
        "code": "def greet():\n    print('Hi!')",
        "title": "What does def do in Python?",
        "correct_index": 1,  # "Creates function" is at index 1
        "answers": ["Starts program", "Creates function", "Deletes function", "Prints text"],
        "answer_type": "text"
    },
    {
        "code": "def say_hello():\n    print(\"Hello!\")\nsay_hello()",
        "title": "What will this code print?",
        "correct_index": 2,  # "Hello!" is at index 2
        "answers": ["Nothing", "say_hello", "Hello!", "Error"],
        "answer_type": "text"
    },
    {
        "code": "def add(a, b):\n    return a + b\nresult = add(3, 5)\nprint(result)",
        "title": "What will this program print?",
        "correct_index": 2,  # "8" is at index 2
        "answers": ["3", "5", "8", "35"],
        "answer_type": "text"
    },
    {
        "code": "def double(number):\n    return number * 2\nx = double(4)\ny = double(x)\nprint(y)",
        "title": "Boss Level! What will this code print?",
        "note": "(Double means two times as much — or multiply by 2)",
        "correct_index": 3,  # "16" is at index 3
        "answers": ["4", "6", "8", "16"],
        "answer_type": "text"
    }
]


def write_hello():
    """This function writes 'Hi!' on the screen"""
    screen.fill(WHITE)
    text = font_hi.render("Hi!", True, GREEN)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)


def draw_square():
    """This function draws a blue square"""
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50, 100, 100))


def draw_circle():
    """This function draws a red circle"""
    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 50)


def draw_buttons():
    """Draw all three buttons"""
    # Button 1 (Teal)
    button1_rect = pygame.Rect(20, 20, 140, 50)
    pygame.draw.rect(screen, TEAL, button1_rect)
    pygame.draw.rect(screen, DARK_GRAY, button1_rect, 2)
    text1 = font_small.render("Say Hi!", True, BLACK)
    screen.blit(text1, (button1_rect.centerx - text1.get_width() // 2,
                        button1_rect.centery - text1.get_height() // 2))

    # Button 2 (Orange)
    button2_rect = pygame.Rect(170, 20, 140, 50)
    pygame.draw.rect(screen, ORANGE, button2_rect)
    pygame.draw.rect(screen, DARK_GRAY, button2_rect, 2)
    text2 = font_small.render("Draw Box", True, BLACK)
    screen.blit(text2, (button2_rect.centerx - text2.get_width() // 2,
                        button2_rect.centery - text2.get_height() // 2))

    # Button 3 (Purple)
    button3_rect = pygame.Rect(320, 20, 140, 50)
    pygame.draw.rect(screen, PURPLE, button3_rect)
    pygame.draw.rect(screen, DARK_GRAY, button3_rect, 2)
    text3 = font_small.render("Draw Circle", True, WHITE)
    screen.blit(text3, (button3_rect.centerx - text3.get_width() // 2,
                        button3_rect.centery - text3.get_height() // 2))

    return button1_rect, button2_rect, button3_rect


def show_lesson_screen():
    """Show what a function is"""
    screen.fill(WHITE)

    # Title
    title = font_title.render("What is a FUNCTION?", True, BLACK)
    screen.blit(title, (20, 20))

    # Explanation lines
    lines = [
        "A function is a block of code",
        "that does ONE job",
        "Write once, use many times!",
        "",
        "Example:",
        "def greet():",
        "    print('Hello!')"
    ]

    y = 60
    for line in lines:
        if line:
            text = font_small.render(line, True, BLACK)
        else:
            y += 10
            continue
        screen.blit(text, (20, y))
        y += 22

    # Blue instruction at bottom
    instruction = font_small.render("Click to see real functions!", True, BLUE)
    screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2,
                              SCREEN_HEIGHT - 35))

    # Draw dinosaur in bottom right corner
    draw_dinosaur()

    present()


def show_code_screen(function_name, code_lines):
    """Show the code of a function with explanations"""
    screen.fill(LIGHT_GRAY)

    # Title showing which function we clicked
    title = font_title.render(f"Function: {function_name}()", True, BLACK)
    screen.blit(title, (20, 6))

    # Draw code background
    code_box = pygame.Rect(15, 30, SCREEN_WIDTH - 30, 286)
    pygame.draw.rect(screen, WHITE, code_box)
    pygame.draw.rect(screen, BLACK, code_box, 2)

    # Show code lines with explanations
    y = 38
    for code_line, explanation in code_lines:
        # Show the code in dark gray
        code_text = font_code.render(code_line, True, DARK_GRAY)
        screen.blit(code_text, (25, y))

        if explanation:
            # Show the explanation right under its code line (tight gap),
            # then leave more room before the next statement starts
            explanation_text = font_comment.render("- " + explanation, True, BLUE)
            screen.blit(explanation_text, (35, y + 14))
            y += 43
        else:
            # Continuation line (wrapped code, no separate explanation) -
            # stays tight to the line above, it's the same statement
            y += 16

    # Instruction at bottom - shift right only for write_hello, where the
    # last explanation line is long enough to collide with centered text
    instruction = font_small.render("Click to see result!", True, BLUE)
    x_offset = 85 if function_name == "write_hello" else 0
    screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2 + x_offset,
                              SCREEN_HEIGHT - 35))

    # Draw dinosaur in bottom right corner
    draw_dinosaur()

    present()


def show_result_screen(result_type):
    """Show what the function does"""
    if result_type == "hello":
        write_hello()
    elif result_type == "square":
        draw_square()
    elif result_type == "circle":
        draw_circle()

    # Instruction to go back
    instruction = font_small.render("Click to return to buttons", True, BLUE)
    screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2,
                              SCREEN_HEIGHT - 35))

    # Draw dinosaur in bottom right corner
    draw_dinosaur()

    present()


def show_buttons_screen():
    """Draw buttons and return their rectangles"""
    screen.fill(LIGHT_GRAY)

    instruction = font_small.render("Click a button to learn functions!", True, BLACK)
    screen.blit(instruction, (20, SCREEN_HEIGHT - 30))

    button1, button2, button3 = draw_buttons()

    # Draw dinosaur in bottom right corner
    draw_dinosaur()

    present()

    return button1, button2, button3


def show_start_quiz_screen():
    """Shown once all 3 functions have been explored - offers to start the quiz"""
    screen.fill(WHITE)

    title = font_title.render("Great job!", True, TEAL)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

    lines = [
        "You've learned all 3 functions!",
        "Ready to test what you know?"
    ]
    y = 90
    for line in lines:
        text = font_small.render(line, True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y))
        y += 22

    start_text = font_title.render("Start Quiz", True, DARK_GREEN)
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 160))

    instruction = font_small.render("Click to begin", True, BLUE)
    screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2,
                              SCREEN_HEIGHT - 35))

    draw_dinosaur()
    present()


def draw_answer_button(rect, answer_text, is_correct=None, is_selected=False):
    """Draw a single quiz answer button with optional highlight"""
    if is_selected and is_correct is None:
        color = SELECTED_HIGHLIGHT
    elif is_correct is True:
        color = DARK_GREEN
    elif is_correct is False:
        color = PURPLE
    else:
        color = LIGHT_GRAY

    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)

    text_surface = font_small.render(answer_text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

    return rect


def show_quiz_screen(question_index, selected_answer=None, status=None):
    """Show a quiz question with visual answer options.

    status is one of:
      None          - no answer chosen yet
      "correct"     - chosen answer was right
      "try_again"   - first wrong attempt (correct answer stays hidden)
      "final_wrong" - second wrong attempt (correct answer is revealed)
    """
    question = QUIZ_QUESTIONS[question_index]

    screen.fill(WHITE)

    # Title showing question number
    title = font_title.render(f"Question {question_index + 1}/{len(QUIZ_QUESTIONS)}", True, BLACK)
    screen.blit(title, (20, 10))

    # Code box (taller to fit multi-line function definitions)
    code_box = pygame.Rect(15, 30, SCREEN_WIDTH - 150, 104)
    pygame.draw.rect(screen, LIGHT_GRAY, code_box)
    pygame.draw.rect(screen, BLACK, code_box, 2)

    # Show code with line wrapping
    code_lines = question["code"].split("\n")
    y = 36
    for line in code_lines:
        code_text = font_code.render(line, True, DARK_GRAY)
        screen.blit(code_text, (25, y))
        y += 19

    # Question text
    question_text = font_small.render(question["title"], True, BLACK)
    screen.blit(question_text, (20, 138))

    # Optional hint/note under the title (e.g. explaining a tricky word) -
    # its slot is always reserved so the buttons sit at a fixed height
    # whether or not a given question has a note
    has_note = bool(question.get("note"))
    if has_note:
        note_text = font_tiny.render(question["note"], True, BLACK)
        screen.blit(note_text, (20, 156))

    # Answer buttons (2x2 grid) - wider to fit longer answer text.
    # Compact height/gaps so there's still room below for a big feedback icon.
    button_width = 150
    button_height = 32
    button_x_start = 25
    button_y_start = 175
    row_gap = 6

    answer_buttons = []

    for i, answer in enumerate(question["answers"]):
        row = i // 2
        col = i % 2
        x = button_x_start + col * (button_width + 20)
        y = button_y_start + row * (button_height + row_gap)

        rect = pygame.Rect(x, y, button_width, button_height)
        answer_buttons.append(rect)

        button_is_correct = None
        button_is_selected = False

        if status is not None and i == selected_answer:
            button_is_selected = True
            button_is_correct = (status == "correct")

        draw_answer_button(rect, answer, button_is_correct, button_is_selected)

    # Instruction text - fixed y positions leave exactly enough room below
    # the (now more compact) button grid for the 60x60 feedback icon
    if status == "correct":
        instruction = font_small.render("Correct! Click to continue", True, DARK_GREEN)
        draw_icon_and_text(smiling_cat_image, smiling_cat_loaded, instruction, SCREEN_HEIGHT - 48, ANSWERS_CENTER_X)
    elif status == "try_again":
        instruction = font_small.render("Not quite! Try again", True, PURPLE)
        draw_icon_and_text(thinking_cat_image, thinking_cat_loaded, instruction, SCREEN_HEIGHT - 48, ANSWERS_CENTER_X)
    elif status == "final_wrong":
        correct_answer = question["answers"][question["correct_index"]]
        line1 = font_small.render(f"Good try! Correct answer: {correct_answer}", True, PURPLE)
        line2 = font_small.render("Click to continue", True, BLUE)
        draw_icon_and_text(thinking_cat_image, thinking_cat_loaded, line1, SCREEN_HEIGHT - 48, ANSWERS_CENTER_X)
        screen.blit(line2, (ANSWERS_CENTER_X - line2.get_width() // 2, SCREEN_HEIGHT - 26))
    else:
        instruction = font_small.render("Click an answer", True, BLUE)
        screen.blit(instruction, (ANSWERS_CENTER_X - instruction.get_width() // 2,
                                  SCREEN_HEIGHT - 48))

    draw_dinosaur()
    present()

    return answer_buttons


def show_quiz_intro_screen():
    """Show introduction to the quiz"""
    screen.fill(WHITE)

    title = font_title.render("Quiz: Guess the Output!", True, BLACK)
    screen.blit(title, (20, 20))

    lines = [
        "Now you are a code detective!",
        "",
        "Read the code carefully.",
        "Guess what the computer will",
        "display as output.",
        "",
        "Choose the correct answer",
        "from the options."
    ]

    y = 70
    for line in lines:
        if line:
            text = font_small.render(line, True, BLACK)
        else:
            y += 12
            continue
        screen.blit(text, (20, y))
        y += 22

    instruction = font_small.render("Click to start the quiz!", True, BLUE)
    screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2,
                              SCREEN_HEIGHT - 35))

    draw_dinosaur()
    present()


def show_quiz_completion_screen():
    """Show quiz completion message"""
    screen.fill(WHITE)

    title = font_title.render("You Did It!", True, GREEN)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 40))

    lines = [
        "You completed all questions!",
        "",
        "Great job learning about",
        "how code works!",
        "",
        "You're becoming a real",
        "programmer!"
    ]

    y = 100
    for line in lines:
        if line:
            text = font_small.render(line, True, BLACK)
        else:
            y += 12
            continue
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y))
        y += 22

    instruction = font_small.render("Click to play the quiz again", True, BLUE)
    screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2,
                              SCREEN_HEIGHT - 35))

    draw_dinosaur()
    present()


# ===== MAIN PROGRAM =====

def main():
    """Main game loop"""
    running = True
    current_screen = "welcome"

    # Tracks which of the 3 functions have been opened, e.g. {"hello", "square"}
    visited = set()

    # Quiz state
    current_question = 0
    selected_answer = None
    quiz_status = None  # None / "correct" / "try_again" / "final_wrong"
    attempt_count = 0   # wrong attempts made on the current question

    while running:
        clock.tick(FPS)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Esc to quit - needed since fullscreen has no window controls
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            # Handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_exit_button_click(event.pos):
                    running = False
                    continue

                # Convert from real screen pixels to virtual 480x320 coordinates
                real_x, real_y = event.pos
                mouse_pos = ((real_x - OFFSET_X) / SCALE, (real_y - OFFSET_Y) / SCALE)

                if current_screen == "welcome":
                    current_screen = "lesson"

                elif current_screen == "lesson":
                    current_screen = "buttons"

                elif current_screen == "buttons":
                    button1, button2, button3 = show_buttons_screen()

                    if button1.collidepoint(mouse_pos):
                        current_screen = "code_hello"
                        visited.add("hello")
                    elif button2.collidepoint(mouse_pos):
                        current_screen = "code_square"
                        visited.add("square")
                    elif button3.collidepoint(mouse_pos):
                        current_screen = "code_circle"
                        visited.add("circle")

                elif current_screen == "code_hello":
                    current_screen = "result_hello"
                elif current_screen == "code_square":
                    current_screen = "result_square"
                elif current_screen == "code_circle":
                    current_screen = "result_circle"

                elif current_screen.startswith("result"):
                    # Once all 3 functions have been opened, the next trip
                    # back from a result screen leads to Start Quiz instead
                    # of the regular buttons screen
                    if len(visited) >= 3:
                        current_screen = "start_quiz"
                    else:
                        current_screen = "buttons"

                elif current_screen == "start_quiz":
                    current_screen = "quiz_intro"

                elif current_screen == "quiz_intro":
                    current_screen = "quiz"

                elif current_screen == "quiz":
                    # Get answer buttons for current question
                    answer_buttons = show_quiz_screen(current_question, selected_answer, quiz_status)

                    # Check if user clicked an answer button
                    clicked_answer = None
                    for i, button in enumerate(answer_buttons):
                        if button.collidepoint(mouse_pos):
                            clicked_answer = i
                            break

                    if quiz_status in (None, "try_again"):
                        # Waiting for an answer (1st or 2nd attempt)
                        if clicked_answer is not None:
                            selected_answer = clicked_answer
                            correct_index = QUIZ_QUESTIONS[current_question]["correct_index"]

                            if clicked_answer == correct_index:
                                quiz_status = "correct"
                            elif attempt_count == 0:
                                # First wrong attempt - let them try again,
                                # don't reveal the correct answer
                                quiz_status = "try_again"
                                attempt_count = 1
                            else:
                                # Second wrong attempt - reveal the answer
                                quiz_status = "final_wrong"
                        # Click outside the buttons does nothing yet

                    else:
                        # quiz_status is "correct" or "final_wrong" -
                        # any click moves on to the next question
                        current_question += 1
                        if current_question >= len(QUIZ_QUESTIONS):
                            current_screen = "quiz_completion"
                        else:
                            selected_answer = None
                            quiz_status = None
                            attempt_count = 0

                elif current_screen == "quiz_completion":
                    # Quiz is a self-contained loop for now - back to its
                    # own intro screen, not back to the lesson1 buttons
                    current_screen = "quiz_intro"
                    current_question = 0
                    selected_answer = None
                    quiz_status = None
                    attempt_count = 0

        # Draw current screen
        if current_screen == "welcome":
            show_welcome_screen()

        elif current_screen == "lesson":
            show_lesson_screen()

        elif current_screen == "buttons":
            show_buttons_screen()

        elif current_screen == "code_hello":
            show_code_screen("write_hello", FUNCTION_HELLO)
        elif current_screen == "code_square":
            show_code_screen("draw_square", FUNCTION_SQUARE)
        elif current_screen == "code_circle":
            show_code_screen("draw_circle", FUNCTION_CIRCLE)

        elif current_screen == "result_hello":
            show_result_screen("hello")
        elif current_screen == "result_square":
            show_result_screen("square")
        elif current_screen == "result_circle":
            show_result_screen("circle")

        elif current_screen == "start_quiz":
            show_start_quiz_screen()

        elif current_screen == "quiz_intro":
            show_quiz_intro_screen()

        elif current_screen == "quiz":
            show_quiz_screen(current_question, selected_answer, quiz_status)

        elif current_screen == "quiz_completion":
            show_quiz_completion_screen()

    pygame.quit()
    sys.exit()


# Run the program
if __name__ == "__main__":
    main()
