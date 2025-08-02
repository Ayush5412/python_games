import tkinter as tk
import random

# --- Constants ---
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_Y_OFFSET = 50 # Distance from the bottom

BALL_RADIUS = 10
INITIAL_BALL_SPEED_X = 3
INITIAL_BALL_SPEED_Y = -3 # Start moving upwards

BRICK_ROWS = 5
BRICK_COLUMNS = 10
BRICK_WIDTH = WINDOW_WIDTH // BRICK_COLUMNS
BRICK_HEIGHT = 20
BRICK_COLORS = ["#c0392b", "#e67e22", "#f1c40f", "#2ecc71", "#3498db"] # Red, Orange, Yellow, Green, Blue

# --- Game Class ---
class BreakoutGame:
    """
    Main class for the Breakout game.
    """
    def __init__(self, master):
        """
        Initializes the game.
        :param master: The root tkinter window.
        """
        self.master = master
        self.master.title("Breakout")
        self.master.resizable(False, False)

        # --- Game State Variables ---
        self.ball_speed_x = INITIAL_BALL_SPEED_X
        self.ball_speed_y = INITIAL_BALL_SPEED_Y
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.game_started = False

        # --- Create Canvas ---
        self.canvas = tk.Canvas(master, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="#2c3e50") # Dark blue background
        self.canvas.pack()

        # --- Create Game Elements ---
        self.create_paddle()
        self.create_ball()
        self.create_bricks()

        # --- Display Score and Lives ---
        self.score_text = self.canvas.create_text(10, 10, text=f"Score: {self.score}", anchor="nw", fill="white", font=("Helvetica", 16))
        self.lives_text = self.canvas.create_text(WINDOW_WIDTH - 10, 10, text=f"Lives: {self.lives}", anchor="ne", fill="white", font=("Helvetica", 16))
        
        # --- Welcome/Instruction Message ---
        self.start_message = self.canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, text="Press Left or Right Arrow to Start", fill="white", font=("Helvetica", 24))


        # --- Bind Controls ---
        self.master.bind("<Left>", self.move_paddle)
        self.master.bind("<Right>", self.move_paddle)
        self.master.bind("<KeyPress>", self.start_game)


    def create_paddle(self):
        """Creates the paddle rectangle."""
        x = (WINDOW_WIDTH - PADDLE_WIDTH) / 2
        y = WINDOW_HEIGHT - PADDLE_HEIGHT - PADDLE_Y_OFFSET
        self.paddle = self.canvas.create_rectangle(x, y, x + PADDLE_WIDTH, y + PADDLE_HEIGHT, fill="#bdc3c7", outline="") # Silver color

    def create_ball(self):
        """Creates the ball oval."""
        x = WINDOW_WIDTH / 2
        y = WINDOW_HEIGHT - PADDLE_HEIGHT - PADDLE_Y_OFFSET - BALL_RADIUS
        self.ball = self.canvas.create_oval(x - BALL_RADIUS, y - BALL_RADIUS, x + BALL_RADIUS, y + BALL_RADIUS, fill="#ecf0f1", outline="") # White color

    def create_bricks(self):
        """Creates the grid of bricks."""
        self.bricks = []
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLUMNS):
                x1 = col * BRICK_WIDTH
                y1 = row * BRICK_HEIGHT + 50 # Offset from the top
                x2 = x1 + BRICK_WIDTH
                y2 = y1 + BRICK_HEIGHT
                color = BRICK_COLORS[row % len(BRICK_COLORS)]
                brick = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="white", width=2)
                self.bricks.append(brick)

    def start_game(self, event=None):
        """Starts the game loop when a key is pressed."""
        if not self.game_started and not self.game_over:
            self.game_started = True
            # Check if the start_message attribute exists and is not None before deleting
            if hasattr(self, 'start_message') and self.start_message:
                self.canvas.delete(self.start_message) # Remove the start message
                self.start_message = None # Set to None to prevent trying to delete it again
            self.game_loop()

    def move_paddle(self, event):
        """Moves the paddle left or right."""
        if self.game_over:
            return
            
        paddle_coords = self.canvas.coords(self.paddle)
        if event.keysym == "Left":
            if paddle_coords[0] > 0:
                self.canvas.move(self.paddle, -20, 0)
        elif event.keysym == "Right":
            if paddle_coords[2] < WINDOW_WIDTH:
                self.canvas.move(self.paddle, 20, 0)

    def game_loop(self):
        """The main loop of the game, responsible for animation and logic."""
        if self.game_over:
            return

        self.move_ball()
        self.check_collisions()

        if self.lives > 0:
            self.master.after(10, self.game_loop) # ~100 FPS
        else:
            self.end_game("Game Over!")

    def move_ball(self):
        """Moves the ball according to its speed."""
        self.canvas.move(self.ball, self.ball_speed_x, self.ball_speed_y)

    def check_collisions(self):
        """Checks for and handles all collisions."""
        ball_coords = self.canvas.coords(self.ball)
        x1, y1, x2, y2 = ball_coords

        # --- Wall Collisions ---
        if x1 <= 0 or x2 >= WINDOW_WIDTH:
            self.ball_speed_x *= -1 # Bounce off side walls
        if y1 <= 0:
            self.ball_speed_y *= -1 # Bounce off top wall

        # --- Bottom Wall (Lose a life) ---
        if y2 >= WINDOW_HEIGHT:
            self.lives -= 1
            self.update_hud()
            if self.lives > 0:
                self.reset_ball_and_paddle()
            else:
                self.end_game("Game Over!")
            return # Skip rest of collision checks for this frame

        # --- Paddle Collision ---
        paddle_coords = self.canvas.coords(self.paddle)
        if x2 >= paddle_coords[0] and x1 <= paddle_coords[2] and y2 >= paddle_coords[1] and y1 <= paddle_coords[3]:
            self.ball_speed_y *= -1
            # Add a little horizontal english based on where it hits the paddle
            paddle_center = paddle_coords[0] + PADDLE_WIDTH / 2
            ball_center = x1 + BALL_RADIUS
            self.ball_speed_x += (ball_center - paddle_center) / PADDLE_WIDTH * 5


        # --- Brick Collisions ---
        overlapping_items = self.canvas.find_overlapping(x1, y1, x2, y2)
        for item in overlapping_items:
            if item in self.bricks:
                self.bricks.remove(item)
                self.canvas.delete(item)
                self.ball_speed_y *= -1
                self.score += 10
                self.update_hud()

                # Check for win condition
                if not self.bricks:
                    self.end_game("You Win!")
                break # Only handle one brick collision per frame

    def reset_ball_and_paddle(self):
        """Resets the ball and paddle to their starting positions."""
        self.game_started = False
        
        # Reset paddle
        px = (WINDOW_WIDTH - PADDLE_WIDTH) / 2
        py = WINDOW_HEIGHT - PADDLE_HEIGHT - PADDLE_Y_OFFSET
        self.canvas.coords(self.paddle, px, py, px + PADDLE_WIDTH, py + PADDLE_HEIGHT)
        
        # Reset ball
        bx = WINDOW_WIDTH / 2
        by = WINDOW_HEIGHT - PADDLE_HEIGHT - PADDLE_Y_OFFSET - BALL_RADIUS
        self.canvas.coords(self.ball, bx - BALL_RADIUS, by - BALL_RADIUS, bx + BALL_RADIUS, by + BALL_RADIUS)
        
        # Reset ball speed
        self.ball_speed_x = random.choice([-1, 1]) * INITIAL_BALL_SPEED_X
        self.ball_speed_y = INITIAL_BALL_SPEED_Y
        
        # The "Press ... to Continue" message is no longer created here.


    def update_hud(self):
        """Updates the score and lives display."""
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")

    def end_game(self, message):
        """Ends the game and displays a message."""
        self.game_over = True
        self.canvas.delete(self.ball)
        self.canvas.delete(self.paddle)
        self.canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, text=message, fill="white", font=("Helvetica", 40))
        self.canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50, text=f"Final Score: {self.score}", fill="white", font=("Helvetica", 20))


# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    game = BreakoutGame(root)
    root.mainloop()
