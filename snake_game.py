import tkinter as tk
import random

# --- Constants ---
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100  # Milliseconds, lower is faster
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"  # Green
FOOD_COLOR = "#FF0000"   # Red
BACKGROUND_COLOR = "#000000" # Black


class Snake:
    """Represents the snake in the game."""
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # Initialize snake at the top-left corner
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        # Draw the snake
        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                fill=SNAKE_COLOR, tag="snake"
            )
            self.squares.append(square)


class Food:
    """Represents the food in the game."""
    def __init__(self):
        # Place food in a random spot on the grid
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        # Draw the food
        canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE,
            fill=FOOD_COLOR, tag="food"
        )


def next_turn(snake, food):
    """Handles all logic for a single game turn."""
    x, y = snake.coordinates[0]

    # Update coordinates based on direction
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Add new head to the snake
    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR
    )
    snake.squares.insert(0, square)

    # Check if snake ate the food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        # Remove the tail if no food was eaten
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check for collisions
    if check_collisions(snake):
        game_over()
    else:
        # Schedule the next turn
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    """Updates the snake's direction of movement."""
    global direction

    # Prevent the snake from reversing on itself
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction


def check_collisions(snake):
    """Checks for collisions with walls or self."""
    x, y = snake.coordinates[0]

    # Check for wall collision
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    # Check for self-collision
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    """Displays the Game Over screen and restart button."""
    global restart_button
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2 - 50,
        font=('consolas', 70),
        text="GAME OVER",
        fill="red",
        tag="gameover"
    )
    
    # Create and place the restart button
    restart_button = tk.Button(
        window, text="Restart", command=restart_game, font=('consolas', 20)
    )
    canvas.create_window(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2 + 50,
        window=restart_button
    )


def restart_game():
    """Resets the game state to start a new game."""
    global snake, food, score, direction, restart_button

    # Destroy the restart button widget if it exists
    if restart_button:
        restart_button.destroy()
        restart_button = None

    # Clear the canvas
    canvas.delete("all")

    # Reset game state variables
    score = 0
    direction = 'down'
    label.config(text="Score:{}".format(score))

    # Re-create game objects
    snake = Snake()
    food = Food()

    # Start the game loop again
    next_turn(snake, food)


# --- Main Window Setup ---
window = tk.Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = 'down'
restart_button = None

label = tk.Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

# Center the window on the screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# --- Key Bindings ---
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# --- Start Game ---
snake = Snake()
food = Food()
next_turn(snake, food)

window.mainloop()