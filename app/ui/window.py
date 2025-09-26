# app/ui_components.py
from customtkinter import *
import os
from PIL import Image, ImageTk
from app.constants import *
from app.backend import BackEnd
from app.game_modes import EasyMode, AIMode
import customtkinter as ctk

attempts = 0

class TicTacToeUI(CTk):
    def __init__(self):
        """
        Initialize the Tic-Tac-Toe UI:
          - sets up the main window
          - creates frames, labels, and canvas
          - loads assets (icons, arrows)
          - initializes the backend and UI state
        """
        super().__init__()

        # Main Window Configuration
        self.title("Tic-Tac-Toe")
        self.geometry("600x600")
        self.resizable(False, False)
        self.config(bg="white")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Creates default instances
        self.buttons = []
        self.placed_items = []
        self.game_over = False
        self.win_icon = None
        self.button_map = {}
        self.format_button = []
        self.format_2 = []

        # Main Frames
        title_frame = CTkFrame(self, fg_color=BG_COL, height=150, width=600)
        title_frame.grid(column=0, row=0, columnspan=2, sticky="nsew")

        self.left_frame = CTkFrame(self, fg_color="white", height=450, width=450, corner_radius=0)
        self.left_frame.grid(column=0, row=1, columnspan=2, sticky="nsew")

        self.right_frame = CTkFrame(self, fg_color="white", height=450, width=150, corner_radius=0)
        self.right_frame.grid(column=1, row=1, columnspan=2, sticky="nsew")

        self.stats_frame = CTkFrame(self, fg_color="white", height=600, width=600)

        # Title
        title_label = CTkLabel(title_frame, text="Tic-Tac-Toe", font=("Helvetica", 80, "bold"), width=12, fg_color=BG_COL, text_color="black", corner_radius=10)
        title_label.place(relx=0.5, rely=0.4, anchor="center")

        # Menu
        stats_button = CTkButton(title_frame,
                    fg_color=MULTI_COL,
                    text_color="black",
                    text="Stats",
                    height=30,
                    width=100,
                    font=("Helvetica", 18, "bold"),
                    hover_color=MULTI_COL_HOV,
                    command=self.stats_page
        )
        stats_button.place(relx=0, rely=1, anchor="sw")

        self.stats_close = CTkButton(self.stats_frame,
                    fg_color=HARD_COL,
                    text_color="black",
                    text="Close",
                    height=30,
                    width=100,
                    font=("Helvetica", 18, "bold"),
                    hover_color=HARD_COL_HOV,
                    command=self.stats_to_home
        )

        self.title_stats = CTkLabel(self.stats_frame, text="Statistics", font=("Helvetica", 80, "bold"), width=12, text_color="black", corner_radius=10)

        # Board Design
        self.canvas_left = CTkCanvas(self.left_frame, width=420, height=420, bg="white", highlightthickness=0)
        self.canvas_left.grid(column=0, row=1, padx=15, pady=15)

        self.canvas_left.create_line(0, 140, 420, 140, width=8, capstyle="round", fill="#FF4A4A")
        self.canvas_left.create_line(0, 280, 420, 280, width=8, capstyle="round", fill="#FF4A4A") 
        self.canvas_left.create_line(140, 0, 140, 420, width=8, capstyle="round", fill="#FF4A4A")
        self.canvas_left.create_line(280, 0, 280, 420, width=8, capstyle="round", fill="#FF4A4A")

        # State Logic Icons
        asset_path_menu_cross = os.path.join(os.path.dirname(__file__), "assets", "blue_cross.png")
        img = Image.open(asset_path_menu_cross).convert("RGBA")
        self.next_mcr = CTkImage(img, size=(30, 30))
        self.menu_cross = CTkLabel(
            self.right_frame,
            image=self.next_mcr,
            fg_color="white",
            text=""
        )
        self.menu_cross.place(relx=0.15, rely=0.1, anchor="center")

        asset_path_menu_circle = os.path.join(os.path.dirname(__file__), "assets", "orange_circle.png")
        img = Image.open(asset_path_menu_circle).convert("RGBA")
        self.next_mcl = CTkImage(img, size=(32, 32))
        self.menu_circle = CTkLabel(
            self.right_frame,
            image=self.next_mcl,
            fg_color="white",
            text=""
        )
        self.menu_circle.place(relx=0.15, rely=0.23, anchor="center")

        # Game Board Icons
        self.asset_path_main_circle = os.path.join(os.path.dirname(__file__), "assets", "orange_circle.png")
        img = Image.open(self.asset_path_main_circle).convert("RGBA")
        self.next_cl = CTkImage(img, size=(110, 110))
        
        self.asset_path_main_cross = os.path.join(os.path.dirname(__file__), "assets", "blue_cross.png")
        img = Image.open(self.asset_path_main_cross).convert("RGBA")
        self.next_cr = CTkImage(img, size=(105, 105))

        # Turn Arrow
        asset_path_left_arrow = os.path.join(os.path.dirname(__file__), "assets", "left-arrow.png")
        img = Image.open(asset_path_left_arrow).convert("RGBA")
        self.next_la = CTkImage(img, size=(30, 30))
        self.la_label = CTkLabel(
            self.right_frame,             
            image=self.next_la,  
            fg_color="white",
            text=""
                )
                
        # Game Result
        self.game_result = CTkLabel(self.right_frame, text="wins!", font=("Helvetica", 25, "bold"), width=12, fg_color=BG_COL, text_color="black", corner_radius=0)
        self.draw_result = CTkLabel(self.right_frame, text="draw...", font=("Helvetica", 25, "bold"), width=12, fg_color=BG_COL, text_color="black", corner_radius=0)
        self.result_box = CTkLabel(self.right_frame,text="",fg_color=BG_COL, corner_radius=5, width=130, height=40)

        # Play Again
        self.play_again = CTkButton(
                    self.right_frame,
                    fg_color=LIGHT_BLUE,
                    text_color="black",
                    text="Play Again?",
                    height=70,
                    width=131,
                    font=("Helvetica", 18, "bold"),
                    hover_color=LIGHT_BLUE_HOVER,
                    command=self.restart
        )

        # Game Mode Select
        select_frame = CTkFrame(self.right_frame, fg_color=BG_COL, height=140, width=131, corner_radius=5)
        select_frame.place(relx=0.45, rely=0.81, anchor="center")

        self.multi_button = CTkButton(
                    select_frame,
                    fg_color=MULTI_COL,
                    text_color="black",
                    text="Multiplayer",
                    width=110,
                    height=22,
                    font=("Helvetica", 14, "bold"),
                    hover_color=MULTI_COL_HOV,
                    command=self.multi_choice
        )
        self.multi_button.place(relx=0.5, rely=0.16, anchor="center")

        black_line = CTkCanvas(select_frame, width=100, height=8, bg=BG_COL, highlightthickness=0)
        black_line.place(relx=0.5, rely=0.31, anchor="center")

        black_line.create_line(0, 2, 100, 2, width=3, capstyle="round", fill="black")

        self.easy_button = CTkButton(
                    select_frame,
                    fg_color=EASY_COL,
                    text_color="black",
                    text="Easy",
                    width=110,
                    height=22,
                    font=("Helvetica", 14, "bold"),
                    hover_color=EASY_COL_HOV,
                    command=self.easy_choice
        )
        self.easy_button.place(relx=0.5, rely=0.44, anchor="center")
        
        self.hard_button = CTkButton(
                    select_frame,
                    fg_color=HARD_COL,
                    text_color="black",
                    text="Hard",
                    width=110,
                    height=22,
                    font=("Helvetica", 14, "bold"),
                    hover_color=HARD_COL_HOV,
                    command=self.hard_choice
        )
        self.hard_button.place(relx=0.5, rely=0.64, anchor="center")

        self.imp_button = CTkButton(
                    select_frame,
                    fg_color=IMP_COL,
                    text_color="black",
                    text="Impossible",
                    width=110,
                    height=22,
                    font=("Helvetica", 14, "bold"),
                    hover_color=IMP_COL_HOV,
                    command=self.imp_choice
        )
        self.imp_button.place(relx=0.5, rely=0.84, anchor="center")

        # Backend (owns game state + logic) and easy_mode game choice as default
        self.easy_choice()

    # Stats page functionality
    def stats_page(self):
        self.stats_frame.place(relx=0, rely=0)
        self.stats_close.place(relx=0, rely=0)
        self.title_stats.place(relx=0.5, rely=0.2, anchor="center")

    def stats_to_home(self):
        self.stats_frame.place_forget()

    # Choice Formatting 
    def choice_format(self, button):
        """
        Helps formatting of which game mode is selected
        """
        list_sel = [self.easy_button, self.hard_button, self.imp_button, self.multi_button]
        list_sel.remove(button)
        for i in list_sel:
            i.configure(border_color=SELECT_COL, border_width=0)

    # Choices
    def multi_choice(self):
        """
        Initiates the multi-player game mode backend
        """
        self.backend = BackEnd()
        self.multi_button.configure(
                            border_color=SELECT_COL,
                            border_width=3
                            )
        self.choice_format(self.multi_button)
        self.restart()
    
    def easy_choice(self):
        """
        Initiates the easy game mode backend
        """
        self.backend = EasyMode()
        self.easy_button.configure(
                            border_color=SELECT_COL,
                            border_width=3
                            )
        self.choice_format(self.easy_button)
        self.restart()

    def hard_choice(self):
        """
        Initiates the hard game mode backend
        """
        self.backend = AIMode("models/hard_agent.pkl")
        self.hard_button.configure(
                            border_color=SELECT_COL,
                            border_width=3
                            )
        self.choice_format(self.hard_button)
        self.restart()
    
    def imp_choice(self):
        """
        Initiates the impossible game mode backend
        """
        self.backend = AIMode("models/imp_agent.pkl")
        self.imp_button.configure(
                            border_color=SELECT_COL,
                            border_width=3
                            )
        self.choice_format(self.imp_button)
        self.restart()

    # Place Turn Selection Buttons
    def button_place(self):
        """
        Create the 3x3 grid of transparent buttons over the board canvas.
        Each button, when clicked, will call `place_item` to place a shape.
        """
        self.button_map = {}
        for i, entry in enumerate(grid_x):
            for j, pos in enumerate(grid_y):
                btn = CTkButton(
                    self.left_frame, 
                    fg_color="transparent", 
                    bg_color="transparent", 
                    hover_color="#F1F1F1", 
                    width=120, 
                    height=120, 
                    text=""
                    )
                btn.place(relx=entry, rely=pos, anchor="center")
                btn.configure(command=lambda e=entry, p=pos, b=btn: self.place_item(e, p, b))
                self.buttons.append(btn)
                self.button_map[(entry, pos)] = btn
    
    # Places actual Buttons to replace selection buttons
    def place_item(self, x, y, btn):
        """
        Handle a player's move:
          - remove the clicked button
          - decide which shape to place (cross or circle) based on backend
          - render the shape
          - update arrow for next player's turn
          - inform backend to update game state
          - if game ends, trigger `game_win`
        """

        # Who plays now (before calling backend)?
        shape_now = self.backend.current_shape()
        if shape_now == "O":
            image = self.next_cl
            self.la_label.place(relx=0.5, rely=0.1, anchor="center")
        else:
            image = self.next_cr
            self.la_label.place(relx=0.5, rely=0.23, anchor="center")

        result = self.backend.register_click(x, y)
        
        placed = result.get("placed_at") or f"{x}, {y}"
        try:
            sx, sy = [float(t.strip()) for t in placed.split(",")]
        except Exception:
            sx, sy = x, y  # safety

        # Remove the correct button
        target_btn = self.button_map.get((sx, sy))
        if target_btn and target_btn.winfo_exists():
            target_btn.destroy()
        elif btn and btn.winfo_exists():
            btn.destroy()

        # Render the piece
        item = CTkLabel(self.left_frame, image=image, fg_color="white", text="")
        item.place(relx=sx, rely=sy, anchor="center")
        self.placed_items.append(item)
        self.format_2.append((item, sx, sy))

        # Arrow hide when attempts hits 10
        if result.get("attempts") == 10:
            try:
                self.la_label.destroy()
            except Exception:
                pass
        
        #End of game?
        if result.get("game_over"):
            self.format_place()
            self.game_win(result.get("winner") or "")
            win_state = result.get("win_state")
            if win_state:
                for btn, v in zip(self.format_button, win_state):
                    if v:
                        btn.configure(fg_color="#FFE96D")
            self.replace_placed_items()
            return

        # Lock mode selection once game begins
        if getattr(self.backend, "selection_off", lambda: False)():
            self.multi_button.configure(state="disabled")
            self.easy_button.configure(state="disabled")

        # If it is now the computer's turn, auto-run it
        if hasattr(self.backend, "comp_move") and self.backend.comp_move():
            self._set_board_enabled(False)
            # small delay for UX; adjust 200ms as you like
            self.after(1000, self.run_computer_turn)

    # Game result display
    def game_win(self, conc):
        """
        Display the result when the game ends:
          - disables remaining buttons
          - shows winner's icon + 'wins!' text OR 'draw...'
          - shows the 'Play Again?' button
        """
        self.game_over = True
        self.disable_remaining_buttons()
        self.la_label.destroy()

        if conc == "X":
            self.game_result.lift()
            img = Image.open(self.asset_path_main_cross).convert("RGBA")
            self.next_cl_2 = CTkImage(img, size=(30, 30))
            self.win_icon = CTkLabel(
                self.right_frame,       
                image=self.next_cl_2,  
                fg_color=BG_COL,
                text=""
                    )
            self.win_icon.place(relx=0.2, rely=0.38, anchor="center")
            self.game_result.place(relx=0.6, rely=0.38, anchor="center")
            self.result_box.place(relx=0.45, rely=0.38, anchor="center")

        elif conc == "O":
            self.game_result.lift()
            self.game_result.place(relx=0.6, rely=0.38, anchor="center")
            img = Image.open(self.asset_path_main_circle).convert("RGBA")
            self.next_cr_2 = CTkImage(img, size=(32, 32))
            self.win_icon = CTkLabel(
                self.right_frame,       
                image=self.next_cr_2,  
                fg_color=BG_COL,
                text=""
                    )
            self.win_icon.place(relx=0.2, rely=0.38, anchor="center")
            self.game_result.place(relx=0.6, rely=0.38, anchor="center")
            self.result_box.place(relx=0.45, rely=0.38, anchor="center")
        elif conc == "":
            self.draw_result.lift()
            self.result_box.place(relx=0.45, rely=0.38, anchor="center")
            self.draw_result.place(relx=0.4, rely=0.38, anchor="center")

        self.play_again.place(relx=0.02, rely=0.46)

        # Make choices available once again because game is over
        self.multi_button.configure(state="normal")
        self.easy_button.configure(state="normal")

    # Disable Remaining Buttons at end of game
    def disable_remaining_buttons(self):
        """
        Disable all remaining active buttons on the board after the game ends.
        """
        for b in self.buttons:
            try:
                if b.winfo_exists():  
                    b.configure(state="disabled")
            except Exception:
                pass   
    
    # Restart game to beginning functionality
    def restart(self):
        """
        Reset the game:
          - clear backend state
          - remove all placed pieces
          - reset result UI and win icon
          - recreate the arrow and 3x3 buttons
          - hide 'Play Again?' until next game over
        """
        # Reset backend state + constants dicts
        self.backend.reset()
        self.game_over = False

        # Clear placed pieces
        for w in self.placed_items:
            try:
                if w.winfo_exists():
                    w.destroy()
            except Exception:
                pass
        self.placed_items = []

        for g in self.format_button:
            try:
                if g.winfo_exists():
                    g.destroy()
            except Exception:
                pass
        self.format_button = []

        # Remove or hide result UI + win icon
        try:
            self.result_box.place_forget()
            self.game_result.place_forget()
            self.draw_result.place_forget()
        except Exception:
            pass

        if self.win_icon and self.win_icon is not None:
            try:
                if self.win_icon.winfo_exists():
                    self.win_icon.destroy()
            except Exception:
                pass
            self.win_icon = None

        # Recreate the turn arrow
        self.la_label.destroy()    
        try:
            self.la_label = CTkLabel(self.right_frame, image=self.next_la, fg_color="white", text="")
            self.la_label.place(relx=0.5, rely=0.1, anchor="center")
        except Exception:
            pass

        # Recreate buttons
        for w in self.buttons:
            try:
                if w.winfo_exists():
                    w.destroy()
            except Exception:
                pass
        self.buttons = []
        self.button_place()

        # Hide Play Again until next win
        try:
            self.play_again.place_forget()
        except Exception:
            pass
    
    # Helper to decide whether board is accessible for play
    def _set_board_enabled(self, enabled: bool):
        """
        Helps decide whether board is accessible for play
        """
        state = "normal" if enabled else "disabled"
        for b in self.buttons:
            try:
                if b.winfo_exists():
                    b.configure(state=state)
            except Exception:
                pass
    
    # Handles computer turn for easy, hard, and impossible modes
    def run_computer_turn(self):
        """
        Let the backend pick and play the AI move, then render it
        and re-enable the board if the game continues.
        """
        # Who is about to play now?
        shape_now = self.backend.current_shape()
        if shape_now == "O":
            image = self.next_cl
            self.la_label.place(relx=0.5, rely=0.1, anchor="center")
        else:
            image = self.next_cr
            self.la_label.place(relx=0.5, rely=0.23, anchor="center")

        # Backend chooses its own cell; user coords not needed
        result = self.backend.register_click(None, None)

        placed = result.get("placed_at")
        if not placed:
            # Shouldn't happen for EasyMode; bail gracefully
            self._set_board_enabled(True)
            return

        try:
            sx, sy = [float(t.strip()) for t in placed.split(",")]
        except Exception:
            self._set_board_enabled(True)
            return

        # Remove the correct button
        target_btn = self.button_map.get((sx, sy))
        if target_btn and target_btn.winfo_exists():
            target_btn.destroy()

        # Render AI piece
        item = CTkLabel(self.left_frame, image=image, fg_color="white", text="")
        item.place(relx=sx, rely=sy, anchor="center")
        self.placed_items.append(item)
        self.format_2.append((item, sx, sy))

        # Hide arrow when attempts hits 10
        if result.get("attempts") == 10:
            try:
                self.la_label.destroy()
            except Exception:
                pass

        # End of game?
        if result.get("game_over"):
            self.format_place()
            self.game_win(result.get("winner") or "")
            win_state = result.get("win_state")
            if win_state:
                for btn, v in zip(self.format_button, win_state):
                    if v:
                        btn.configure(fg_color="#FFE96D")
            self.replace_placed_items()
            return

        # Otherwise, back to the human: re-enable remaining buttons
        self._set_board_enabled(True)

    # Helps track button placement (allows winning pattern to be highlighted)
    def format_place(self):
        """
        Create the 3x3 grid of transparent buttons over the board canvas.
        Each button, when clicked, will call `place_item` to place a shape.
        """
        for i, pos in enumerate(grid_y):
            for j, entry in enumerate(grid_x):
                btn = CTkButton(
                    self.left_frame, 
                    fg_color="transparent", 
                    bg_color="transparent", 
                    hover_color="#F1F1F1", 
                    width=120, 
                    height=120, 
                    text="",
                    state="disabled"
                    )
                btn.place(relx=entry, rely=pos, anchor="center")
                # btn.lift()
                self.format_button.append(btn)
    
    # Another helper for re-placing items (allows winning pattern to be highlighted)
    def replace_placed_items(self):
        """
        Re-place all items from self.placed_items at their original locations.
        """
        for item, sx, sy in self.format_2:
            try:
                item.place(relx=sx, rely=sy, anchor="center")
                item.lift()
            except Exception:
                pass
