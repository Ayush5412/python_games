import tkinter as tk
import random

# --- Game Constants ---
WIDTH = 400
HEIGHT = 600
GRAVITY = 0.4
JUMP_STRENGTH = -8
GAME_SPEED = 15  # Lower is faster

# --- Pipe (Fence) Constants ---
PIPE_WIDTH = 65 # Increased width for texture
PIPE_GAP = 200
PIPE_SPEED = -3
PIPE_SPAWN_RATE = 120 # In game ticks

# --- Scenery Constants ---
CLOUD_SPEED = -1

# --- Improved Color Palette ---
PALETTE = {
    "sky_top": "#87CEEB",
    "sky_bottom": "#ADD8E6",
    "ground_top": "#3CB371", # MediumSeaGreen
    "ground_bottom": "#8B4513", # SaddleBrown
    "fence_main": "#A0522D", # Sienna
    "fence_shadow": "#8B4513", # SaddleBrown
    "fence_texture": "#D2691E", # Chocolate
    "cloud": "#FFFFFF",
    "text": "#FFFFFF",
    "text_shadow": "#333333",
    "sign_main": "#DEB887", # BurlyWood
    "sign_shadow": "#8B4513",
}
HORSE_EMOJI = "🐴"

class FlappyHorse:
    """The main class for the Flappy Horse game application."""

    def __init__(self, root):
        """Initialize the game."""
        self.root = root
        self.root.title("Flappy Horse")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0)
        self.canvas.pack()

        self.high_score = 0
        self.start_screen()

    def start_screen(self):
        """Display the initial start screen."""
        self.canvas.delete("all")
        self.create_sky_gradient()
        self.create_ground()
        self.create_clouds()
        
        # Title with shadow
        self.canvas.create_text(WIDTH / 2 + 2, HEIGHT / 3 + 2, text="Flappy Horse", font=("Arial", 40, "bold"), fill=PALETTE["text_shadow"], tags="start_text")
        self.canvas.create_text(WIDTH / 2, HEIGHT / 3, text="Flappy Horse", font=("Arial", 40, "bold"), fill=PALETTE["text"], tags="start_text")
        
        self.canvas.create_text(WIDTH / 2, HEIGHT / 2, text=HORSE_EMOJI, font=("Arial", 80), tags="start_text")
        
        # Subtext with shadow
        self.canvas.create_text(WIDTH / 2 + 1, HEIGHT * 2 / 3 + 1, text="Press Space or Click to Start", font=("Arial", 16), fill=PALETTE["text_shadow"], tags="start_text")
        self.canvas.create_text(WIDTH / 2, HEIGHT * 2 / 3, text="Press Space or Click to Start", font=("Arial", 16), fill=PALETTE["text"], tags="start_text")
        
        self.root.bind("<space>", self.start_game)
        self.canvas.bind("<Button-1>", self.start_game)

    def start_game(self, event=None):
        """Set up and start a new game session."""
        self.root.unbind("<space>")
        self.canvas.unbind("<Button-1>")

        self.canvas.delete("all")
        self.is_game_over = False
        self.score = 0

        # --- Create Scenery ---
        self.create_sky_gradient()
        self.create_ground()
        self.create_clouds()

        # --- Create Game Objects ---
        # Horse with shadow for depth
        self.horse_y = HEIGHT / 2
        self.horse_velocity = 0
        self.horse_shadow = self.canvas.create_text(WIDTH / 4 + 2, self.horse_y + 2, text=HORSE_EMOJI, font=("Arial", 30), fill="gray50")
        self.horse_sprite = self.canvas.create_text(WIDTH / 4, self.horse_y, text=HORSE_EMOJI, font=("Arial", 30))
        
        self.pipes = []
        self.pipe_spawn_counter = PIPE_SPAWN_RATE
        
        # Score display with shadow
        self.score_shadow = self.canvas.create_text(WIDTH / 2 + 2, 52, text=f"Score: {self.score}", font=("Arial", 24, "bold"), fill=PALETTE["text_shadow"])
        self.score_text = self.canvas.create_text(WIDTH / 2, 50, text=f"Score: {self.score}", font=("Arial", 24, "bold"), fill=PALETTE["text"])

        # Re-bind jump events
        self.root.bind("<space>", self.jump)
        self.canvas.bind("<Button-1>", self.jump)

        self.game_loop()

    def create_sky_gradient(self):
        """Creates a vertical gradient for the sky background."""
        top_r, top_g, top_b = self.root.winfo_rgb(PALETTE["sky_top"])
        bot_r, bot_g, bot_b = self.root.winfo_rgb(PALETTE["sky_bottom"])

        for i in range(HEIGHT):
            # Interpolate color components
            new_r = int(top_r + (bot_r - top_r) * (i / HEIGHT))
            new_g = int(top_g + (bot_g - top_g) * (i / HEIGHT))
            new_b = int(top_b + (bot_b - top_b) * (i / HEIGHT))
            color = f'#{new_r:04x}{new_g:04x}{new_b:04x}'
            self.canvas.create_line(0, i, WIDTH, i, fill=color)

    def create_ground(self):
        """Creates a multi-layered ground."""
        self.canvas.create_rectangle(0, HEIGHT - 40, WIDTH, HEIGHT, fill=PALETTE["ground_bottom"], outline="")
        self.canvas.create_rectangle(0, HEIGHT - 40, WIDTH, HEIGHT - 30, fill=PALETTE["ground_top"], outline="")

    def create_clouds(self):
        """Create a set of clouds for the background."""
        self.clouds = []
        for _ in range(5):
            x = random.randint(0, WIDTH)
            y = random.randint(50, HEIGHT // 2)
            size = random.randint(20, 50)
            cloud_part1 = self.canvas.create_oval(x, y, x + size * 2, y + size, fill=PALETTE["cloud"], outline="")
            cloud_part2 = self.canvas.create_oval(x + size, y - size / 2, x + size * 3, y + size / 2, fill=PALETTE["cloud"], outline="")
            self.clouds.append([cloud_part1, cloud_part2])

    def jump(self, event=None):
        if not self.is_game_over:
            self.horse_velocity = JUMP_STRENGTH

    def game_loop(self):
        if self.is_game_over:
            return

        # Update Horse (and its shadow)
        self.horse_velocity += GRAVITY
        self.horse_y += self.horse_velocity
        self.canvas.coords(self.horse_sprite, WIDTH / 4, self.horse_y)
        self.canvas.coords(self.horse_shadow, WIDTH / 4 + 2, self.horse_y + 2)

        # Update Scenery
        self.update_scenery()

        # Update and Spawn Pipes
        self.update_pipes()
        self.pipe_spawn_counter += 1
        if self.pipe_spawn_counter >= PIPE_SPAWN_RATE:
            self.spawn_textured_pipe()
            self.pipe_spawn_counter = 0

        self.check_collisions()
        self.root.after(GAME_SPEED, self.game_loop)
        
    def update_scenery(self):
        """Moves clouds for a parallax effect."""
        for cloud_pair in self.clouds:
            for part in cloud_pair:
                self.canvas.move(part, CLOUD_SPEED, 0)
                coords = self.canvas.coords(part)
                if coords and coords[2] < 0:
                    self.canvas.move(part, WIDTH + 150, random.randint(-10, 10))

    def update_pipes(self):
        """Moves and manages all parts of the textured pipes."""
        pipes_to_remove = []
        scored_this_frame = False
        for pipe_group in self.pipes:
            for part in pipe_group["parts"]:
                self.canvas.move(part, PIPE_SPEED, 0)
            
            pipe_coords = self.canvas.coords(pipe_group["top_main"])
            if pipe_coords:
                pipe_x = pipe_coords[0]
                if not pipe_group["scored"] and pipe_x < WIDTH / 4:
                    self.score += 1
                    pipe_group["scored"] = True
                    self.update_score()
                    scored_this_frame = True
                if pipe_x < -PIPE_WIDTH:
                    pipes_to_remove.append(pipe_group)
        
        for pipe_group in pipes_to_remove:
            self.pipes.remove(pipe_group)
            for part in pipe_group["parts"]:
                self.canvas.delete(part)
        
        if scored_this_frame:
            self.canvas.itemconfig(self.score_text, font=("Arial", 28, "bold"))
            self.root.after(100, lambda: self.canvas.itemconfig(self.score_text, font=("Arial", 24, "bold")))


    def spawn_textured_pipe(self):
        """Creates a new pair of fence obstacles with texture and shading."""
        gap_y = random.randint(150, HEIGHT - 250)
        top_height = gap_y - PIPE_GAP / 2
        bottom_y = gap_y + PIPE_GAP / 2
        
        all_parts = []
        
        # --- Top Fence ---
        # Main body and shadow for 3D effect
        top_shadow = self.canvas.create_rectangle(WIDTH, 0, WIDTH + PIPE_WIDTH, top_height, fill=PALETTE["fence_shadow"], outline="")
        top_main = self.canvas.create_rectangle(WIDTH, 0, WIDTH + PIPE_WIDTH - 5, top_height, fill=PALETTE["fence_main"], outline="")
        all_parts.extend([top_shadow, top_main])
        # Wood grain texture
        for _ in range(5):
            line_x = WIDTH + random.randint(5, PIPE_WIDTH - 10)
            line = self.canvas.create_line(line_x, 0, line_x, top_height, fill=PALETTE["fence_texture"], width=random.randint(1,2))
            all_parts.append(line)

        # --- Bottom Fence ---
        # Main body and shadow
        bottom_shadow = self.canvas.create_rectangle(WIDTH, bottom_y, WIDTH + PIPE_WIDTH, HEIGHT - 40, fill=PALETTE["fence_shadow"], outline="")
        bottom_main = self.canvas.create_rectangle(WIDTH, bottom_y, WIDTH + PIPE_WIDTH - 5, HEIGHT - 40, fill=PALETTE["fence_main"], outline="")
        all_parts.extend([bottom_shadow, bottom_main])
        # Wood grain texture
        for _ in range(7):
            line_x = WIDTH + random.randint(5, PIPE_WIDTH - 10)
            line = self.canvas.create_line(line_x, bottom_y, line_x, HEIGHT - 40, fill=PALETTE["fence_texture"], width=random.randint(1,2))
            all_parts.append(line)

        self.pipes.append({"top_main": top_main, "bottom_main": bottom_main, "parts": all_parts, "scored": False})

    def check_collisions(self):
        """Check for collisions with ground, sky, or fences."""
        horse_coords = self.canvas.bbox(self.horse_sprite)
        
        if horse_coords[3] >= HEIGHT - 40 or horse_coords[1] < 0:
            self.end_game()
            return

        for pipe_group in self.pipes:
            top_coords = self.canvas.bbox(pipe_group["top_main"])
            bottom_coords = self.canvas.bbox(pipe_group["bottom_main"])
            
            if (self.is_overlapping(horse_coords, top_coords) or 
                self.is_overlapping(horse_coords, bottom_coords)):
                self.end_game()
                return

    def is_overlapping(self, box1, box2):
        if not box1 or not box2: return False
        return box1[0] < box2[2] and box1[2] > box2[0] and box1[1] < box2[3] and box1[3] > box2[1]

    def update_score(self):
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        self.canvas.itemconfig(self.score_shadow, text=f"Score: {self.score}")
        if self.score >= 100:
            self.win_game()

    def win_game(self):
        if self.is_game_over: return
        self.is_game_over = True
        self.end_game(won=True)

    def end_game(self, won=False):
        if self.is_game_over and not won: return
        self.is_game_over = True
        
        self.root.unbind("<space>")
        self.canvas.unbind("<Button-1>")

        self.canvas.itemconfig(self.horse_sprite, fill="red")
        self.show_end_game_modal(won)

    def show_end_game_modal(self, won=False):
        """Display a stylized wooden sign for the restart screen."""
        if self.score > self.high_score:
            self.high_score = self.score

        # Determine horse rank
        if self.score >= 100: rank_name, rank_emoji, rank_color = "Diamond Horse", "💎", "cyan"
        elif self.score > 70: rank_name, rank_emoji, rank_color = "Diamond Horse", "💎", "cyan"
        elif self.score > 40: rank_name, rank_emoji, rank_color = "Golden Horse", "🥇", "gold"
        elif self.score > 20: rank_name, rank_emoji, rank_color = "Silver Horse", "🥈", "silver"
        elif self.score >= 5: rank_name, rank_emoji, rank_color = "Bronze Horse", "🥉", "#CD7F32"
        else: rank_name, rank_emoji, rank_color = "Brown Horse", "🐴", "#A52A2A"

        # Create a wooden sign look
        self.canvas.create_rectangle(50, HEIGHT/2 - 120, WIDTH-50, HEIGHT/2 + 120, fill=PALETTE["sign_shadow"], outline="")
        self.canvas.create_rectangle(60, HEIGHT/2 - 110, WIDTH-60, HEIGHT/2 + 110, fill=PALETTE["sign_main"], outline="")
        
        # Modal Text with shadows
        title_text = "Victory!" if won else "Game Over"
        self.canvas.create_text(WIDTH / 2 + 2, HEIGHT / 2 - 88, text=title_text, font=("Arial", 28, "bold"), fill=PALETTE["text_shadow"])
        self.canvas.create_text(WIDTH / 2, HEIGHT / 2 - 90, text=title_text, font=("Arial", 28, "bold"), fill=PALETTE["text"])
        
        self.canvas.create_text(WIDTH / 2 + 1, HEIGHT / 2 - 49, text=f"Score: {self.score}", font=("Arial", 18), fill=PALETTE["text_shadow"])
        self.canvas.create_text(WIDTH / 2, HEIGHT / 2 - 50, text=f"Score: {self.score}", font=("Arial", 18), fill=PALETTE["text"])

        self.canvas.create_text(WIDTH / 2 + 1, HEIGHT / 2 - 19, text=f"High Score: {self.high_score}", font=("Arial", 18), fill=PALETTE["text_shadow"])
        self.canvas.create_text(WIDTH / 2, HEIGHT / 2 - 20, text=f"High Score: {self.high_score}", font=("Arial", 18), fill=PALETTE["text"])
        
        self.canvas.create_text(WIDTH / 2, HEIGHT / 2 + 30, text=f"{rank_emoji} {rank_name} {rank_emoji}", font=("Arial", 20, "bold"), fill=rank_color)
        
        self.canvas.create_text(WIDTH / 2 + 1, HEIGHT / 2 + 81, text="Press Space to Restart", font=("Arial", 14), fill=PALETTE["text_shadow"])
        self.canvas.create_text(WIDTH / 2, HEIGHT / 2 + 80, text="Press Space to Restart", font=("Arial", 14), fill=PALETTE["text"])
        
        self.root.after(500, lambda: self.root.bind("<space>", self.start_game))


if __name__ == "__main__":
    main_window = tk.Tk()
    game = FlappyHorse(main_window)
    main_window.mainloop()
