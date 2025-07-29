import tkinter as tk
from tkinter import font as tkfont

class TicTacToe(tk.Tk):
    """
    A stylish and animated Tic-Tac-Toe game using Python's Tkinter library.
    """
    def __init__(self):
        super().__init__()
        self.title("Playful Tic-Tac-Toe")
        self.configure(bg="#2c3e50") # Dark blue background

        # --- Game State ---
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.game_over = False

        # --- Styling ---
        self.player_colors = {"X": "#e74c3c", "O": "#3498db"} # Red for X, Blue for O
        self.base_bg = "#34495e" # Slightly lighter blue for buttons
        self.hover_bg = "#4a6274" # Hover color
        self.win_bg = "#2ecc71" # Green for winning line
        self.font_style = tkfont.Font(family="Poppins", size=36, weight="bold")
        self.info_font = tkfont.Font(family="Poppins", size=14)

        # --- UI Setup ---
        self._create_widgets()
        self.update_info_label()

    def _create_widgets(self):
        """Creates and arranges the widgets for the game board."""
        main_frame = tk.Frame(self, bg="#2c3e50", padx=20, pady=20)
        main_frame.pack(expand=True)

        self.info_label = tk.Label(
            main_frame,
            text="",
            font=self.info_font,
            bg="#2c3e50",
            fg="white",
            pady=10
        )
        self.info_label.pack()

        board_frame = tk.Frame(main_frame, bg="#2c3e50")
        board_frame.pack()

        for r in range(3):
            for c in range(3):
                button = tk.Button(
                    board_frame,
                    text="",
                    font=self.font_style,
                    width=4,
                    height=2,
                    bg=self.base_bg,
                    fg="white",
                    relief="flat",
                    command=lambda r=r, c=c: self.on_button_click(r, c),
                    disabledforeground="white"
                )
                button.grid(row=r, column=c, padx=5, pady=5)
                # --- Animations on Hover ---
                button.bind("<Enter>", lambda e, b=button: self.on_hover(e, b))
                button.bind("<Leave>", lambda e, b=button: self.on_leave(e, b))
                self.buttons[r][c] = button
    
    def on_hover(self, event, button):
        """Change button color on hover if it's active."""
        if button['state'] == 'normal':
            button.config(bg=self.hover_bg)

    def on_leave(self, event, button):
        """Change button color back when mouse leaves."""
        button.config(bg=self.base_bg)


    def on_button_click(self, r, c):
        """Handles the logic when a game board button is clicked."""
        if self.board[r][c] == "" and not self.game_over:
            # Update board state
            self.board[r][c] = self.current_player
            
            # Update button UI
            button = self.buttons[r][c]
            button.config(text=self.current_player, fg=self.player_colors[self.current_player], state="disabled")
            self.on_leave(None, button) # Reset background to base color after click

            # Check for game end
            if self.check_winner(self.current_player):
                self.highlight_winner(self.current_player)
                self.game_over = True
                self.show_end_game_popup(f"Player {self.current_player} wins!")
            elif self.is_draw():
                self.game_over = True
                self.show_end_game_popup("It's a draw!")
            else:
                # Switch player
                self.current_player = "O" if self.current_player == "X" else "X"
                self.update_info_label()

    def update_info_label(self):
        """Updates the label to show whose turn it is."""
        text = f"Player {self.current_player}'s Turn"
        self.info_label.config(text=text, fg=self.player_colors[self.current_player])

    def check_winner(self, player):
        """Checks rows, columns, and diagonals for a win."""
        # Check rows
        for r in range(3):
            if all(self.board[r][c] == player for c in range(3)):
                return True
        # Check columns
        for c in range(3):
            if all(self.board[r][c] == player for r in range(3)):
                return True
        # Check diagonals
        if all(self.board[i][i] == player for i in range(3)):
            return True
        if all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def is_draw(self):
        """Checks if the game is a draw."""
        return all(self.board[r][c] != "" for r in range(3) for c in range(3))

    def highlight_winner(self, player):
        """Highlights the winning combination of buttons."""
        # Rows
        for r in range(3):
            if all(self.board[r][c] == player for c in range(3)):
                for c in range(3):
                    self.buttons[r][c].config(bg=self.win_bg)
                return
        # Columns
        for c in range(3):
            if all(self.board[r][c] == player for r in range(3)):
                for r in range(3):
                    self.buttons[r][c].config(bg=self.win_bg)
                return
        # Diagonals
        if all(self.board[i][i] == player for i in range(3)):
            for i in range(3):
                self.buttons[i][i].config(bg=self.win_bg)
            return
        if all(self.board[i][2 - i] == player for i in range(3)):
            for i in range(3):
                self.buttons[i][2 - i].config(bg=self.win_bg)
            return

    def _handle_play_again(self, popup):
        """Helper function to reset the game and close the popup."""
        popup.destroy()
        self.reset_game()

    def show_end_game_popup(self, message):
        """Displays a custom popup window at the end of the game."""
        popup = tk.Toplevel(self)
        popup.title("Game Over")
        popup.configure(bg="#2c3e50")
        popup.transient(self) # Keep popup on top of the main window
        popup.grab_set() # Modal behavior

        # Center the popup
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - 150
        y = self.winfo_y() + (self.winfo_height() // 2) - 75
        popup.geometry(f"300x150+{x}+{y}")
        popup.resizable(False, False)

        # --- Popup Widgets ---
        popup_frame = tk.Frame(popup, bg="#2c3e50", pady=20)
        popup_frame.pack(expand=True, fill="both")

        message_label = tk.Label(
            popup_frame, text=message, font=self.info_font, bg="#2c3e50", fg="white"
        )
        message_label.pack(pady=10)

        # --- "PLAY AGAIN" BUTTON ---
        # Its command now calls the helper method to reset the game.
        play_again_button = tk.Button(
            popup_frame,
            text="Play Again",
            font=self.info_font,
            bg="#1abc9c", # Turquoise color
            fg="white",
            relief="flat",
            command=lambda: self._handle_play_again(popup)
        )
        play_again_button.pack(pady=10, ipadx=10, ipady=5)
        play_again_button.bind("<Enter>", lambda e: e.widget.config(bg="#16a085"))
        play_again_button.bind("<Leave>", lambda e: e.widget.config(bg="#1abc9c"))

    def reset_game(self):
        """Resets the game to its initial state."""
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.game_over = False
        for r in range(3):
            for c in range(3):
                button = self.buttons[r][c]
                button.config(text="", state="normal", bg=self.base_bg)
        self.update_info_label()

if __name__ == "__main__":
    app = TicTacToe()
    app.mainloop()
