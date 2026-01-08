'''
Card Memory Game 
Authors: Tanisha Naser and Angela Xi
Date: December 16th, 2025

Description: 
This program implements a card memory game using Tkinter. 
The player must match pairs of cards by remembering their positions.
'''
import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import os 
import platform
import playsound3 as playsound

# grid size depending on difficulty of game
DIFFICULTIES = {
"Easy": (3,4), #
"Medium": (4,4),
"Hard": (5,6)
}

CARD_SIZE = (90,90)
PADDING = 6 #Space between cards

#Helper functions
# Sound effects
# Get the folder where your script is located
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define paths for your specific sounds
happy_sound = "sound_effects/happy.wav"
sad_sound = "sound_effects/sad.wav"
applause_sound = "sound_effects/applause.wav"

# Playing audio file based on platform
def play_audio(file_path):
    # Mac
    if platform.system() == "Darwin": 
        os.system(f"afplay '{file_path}' &")
    # Windows
    elif platform.system() == "Windows": 
        playsound.playsound(file_path, block=False)

#Loads and resizes an image file into a Tkinter PhotoImage
def load_photo(path, size=CARD_SIZE):
    img = Image.open(path).convert("RGB")
    img = img.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

#Returns a list of full paths for images in cards folder
def list_image_files(folder: str):
    endings = (".png", ".jpg") #valid file endings
    files = []
    for name in os.listdir(folder):
        if name.lower().endswith(endings):
            files.append(os.path.join(folder, name))
    files.sort()
    return files

#Controls Match Madness Game 
class MatchMadness:
    # Window Setup
    def __init__(self, root):
        self.root = root
        self.root.title("Match Madness")
        self.root.geometry("800x600")
        self.root.config(bg="pink1")
        self.selected_difficulty = None 
        self.selected_theme = None  
    
    #Screens
        self.game_frame = tk.Frame(root)
        self.menu = MenuFrame(root, self)


    #Starts the game with selected difficulty and theme
    def start_game(self):

        rows, cols = DIFFICULTIES[self.selected_difficulty]
        num_pairs = (rows*cols) // 2 

        #Get image paths from selected theme
        folder = f"Cards/{self.selected_theme}"
        image_paths = list_image_files(folder)
        selected_paths = image_paths[:num_pairs] #Only uses the necessary number of images

        card_paths = selected_paths * 2 #Each image appears twice
        random.shuffle(card_paths)

        self.card_images = [load_photo(path) for path in card_paths]

        self.rows = rows
        self.cols = cols
        self.card_paths = card_paths
        self.current_player = 1 
        self.scores = {1:0, 2:0} 

        self.flipped_cards = []
        self.matched_cards = [] 
        
        # Resize window based on difficulty to avoid cards being cut off 
        if self.selected_difficulty == "Easy":
            self.root.geometry("800x550")
        elif self.selected_difficulty == "Medium":
            self.root.geometry("900x650")
        else: 
            self.root.geometry("1100x750")
        
        # Hide menu & show game
        self.menu.menu_frame.pack_forget()
        self.game_frame.config(bg="pink1")
        self.game_frame.pack(expand=True, fill="both")

        self.build_game_screen()


    def build_game_screen(self):
        #Clears existing buttons, text, etc
        for widget in self.game_frame.winfo_children():
            widget.destroy() 
        
        #Left sidebar
        sidebar = tk.Frame(self.game_frame, bg="pink1", width=200)
        sidebar.pack(side="left", fill="y", padx=10, pady=10)
        sidebar.pack_propagate(False)
        
        title = tk.Label(sidebar, text="Match Madness", font=("Arial", 16, "bold"), bg="pink1", fg="deeppink4")
        title.pack(pady=10)

        info_label = tk.Label(sidebar, text=f"Theme: {self.selected_theme} \nDifficulty: {self.selected_difficulty}", font = ("Arial", 10), bg="pink1", fg="deeppink4")
        info_label.pack(pady=5)

        #Turn indicator
        self.turn_label = tk.Label(sidebar, text="Player 1's turn", font=("Arial", 14, "bold"), bg="pink1", fg="deeppink4")
        self.turn_label.pack(pady=15)

        #Scores (updated when match is found)
        scores_title = tk.Label(sidebar, text="Scores:", font=("Arial", 12, "bold"), bg="pink1", fg="deeppink4")
        scores_title.pack(pady=(10, 5))
        
        self.p1_score_label = tk.Label(sidebar, text="Player 1: 0", font=("Arial", 12), bg="pink1", fg="deeppink4")
        self.p1_score_label.pack(pady=2)
        
        self.p2_score_label = tk.Label(sidebar, text="Player 2: 0", font=("Arial", 12), bg="pink1", fg="deeppink4")
        self.p2_score_label.pack(pady=2)

        #Rules and quit buttons
        rules_btn = tk.Button(sidebar, text="Rules", width=12,bg="PaleVioletRed", fg="white", command=self.menu.show_rules)
        rules_btn.pack(pady=10)

        quit_btn = tk.Button(sidebar, text="Quit", width=12,bg="indian red", fg="white", command=self.root.destroy)
        quit_btn.pack(pady=5)

        #Card grid 
        grid_frame = tk.Frame(self.game_frame, bg="pink1")
        grid_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        self.card_buttons = []
        for i in range(self.rows): # setting up rows from user input
            row_buttons = []
            for j in range(self.cols): # setting up columns from user input
                card_index = i * self.cols + j
                btn = tk.Button(grid_frame, text="?", width=8, height=4, # unknown card
                    bg="PaleVioletRed", fg="white", font=("Arial", 12, "bold"),
                    activebackground="PaleVioletRed", activeforeground="white",
                    command=lambda idx=card_index, r=i, c=j: self.flip_card(idx, r, c))
                btn.grid(row=i, column=j, padx=PADDING, pady=PADDING)
                row_buttons.append(btn)
            self.card_buttons.append(row_buttons)

    def build_end_screen(self):
        #Clears existing buttons, text, etc
        for widget in self.game_frame.winfo_children():
            widget.destroy() 

        #Determine winner 
        if self.scores[1] > self.scores[2]:
            winner_text = "Player 1 Wins!"
        elif self.scores[2] > self.scores[1]:
            winner_text = "Player 2 Wins!"
        else:
            winner_text = "It's a Tie!"

        # Game over screen
        title = tk.Label(self.game_frame, text="Game Over!", font=("Arial", 28, "bold"), bg="pink1", fg="deeppink4")
        title.pack(pady=30)
        
        # Sound effects
        play_audio(applause_sound)

        # Winner
        winner_label = tk.Label(self.game_frame, text=winner_text, font=("Arial", 20), bg="pink1", fg="deeppink4")
        winner_label.pack(pady=10)
        
        # Final scores
        scores_label = tk.Label(self.game_frame, text=f"Final Scores:\nPlayer 1: {self.scores[1]}\nPlayer 2: {self.scores[2]}", 
                               font=("Arial", 14), bg="pink1", fg="deeppink4")
        scores_label.pack(pady=20)
        
        # Buttons frame
        btn_frame = tk.Frame(self.game_frame, bg="pink1")
        btn_frame.pack(pady=20)
        
        # Play Again button
        play_again_btn = tk.Button(btn_frame, text="Play Again", width=12, bg="PaleGreen3", fg="white",
                                   command=self.play_again)
        play_again_btn.pack(side="left", padx=10)
        
        # Main Menu button
        menu_btn = tk.Button(btn_frame, text="Main Menu", width=12, bg="PaleVioletRed", fg="white",
                            command=self.go_to_menu)
        menu_btn.pack(side="left", padx=10)
        
        # Quit button
        quit_btn = tk.Button(btn_frame, text="Quit", width=12, bg="indian red", fg="white",
                            command=self.root.destroy)
        quit_btn.pack(side="left", padx=10)
    
    #Starts a new game with same settings
    def play_again(self):
        self.start_game()
    

    # Returns to main menu
    def go_to_menu(self):
        """Return to main menu"""
        self.game_frame.pack_forget()
        self.root.geometry("800x600")  # Reset window size
        self.menu.menu_frame.pack(fill="both", expand=True)

    #Flips a card when clicked if requirements are met
    def flip_card(self, index, row, col):
            #Don't flip if already matched
            if index in self.matched_cards:
                return
            
            #Don't flip if already flipped
            if index in self.flipped_cards:
                return

            #Don't flip if 2 cards are already flipped
            if len(self.flipped_cards) >= 2:
                return 

            #Show image
            btn = self.card_buttons[row][col]
            btn.config(image=self.card_images[index], text="", width=90, height=90,
                      activebackground="pink1")

            #Add to flipped cards
            self.flipped_cards.append(index)

            #If 2 cards are flipped, check for match
            if len(self.flipped_cards) == 2:
                self.root.after(1000, self.check_match) #Waits 1 second before checking for match


    #Checks if 2 flipped cards are a match
    def check_match(self):
        idx1, idx2 = self.flipped_cards

        #Get image paths to compare 
        path1 = self.card_paths[idx1]
        path2 = self.card_paths[idx2]

        #Keep cards face up (match)
        if path1 == path2:
            play_audio(happy_sound)
            self.matched_cards.append(idx1)
            self.matched_cards.append(idx2)
            
            #Add point to current player 
            self.scores[self.current_player] += 1
            self.update_scores()

            #Check if game is over
            if len(self.matched_cards) == self.rows * self.cols:
                self.end_game()
                return
        
        else:
            #No match, flip cards back, find buttons and reset them
            play_audio(sad_sound)
            for idx in self.flipped_cards:
                row = idx // self.cols
                col = idx % self.cols 
                btn = self.card_buttons[row][col]
                btn.config(image="", text="?", width=8, height=4, 
                          bg="PaleVioletRed", fg="white",
                          activebackground="PaleVioletRed", activeforeground="white")

            #Switch player only on no match
            self.current_player = 2 if self.current_player == 1 else 1 
            self.turn_label.config(text=f"Player {self.current_player}'s turn")

        #Clear flipped cards for next turn
        self.flipped_cards = []

    def update_scores(self):
        self.p1_score_label.config(text=f"Player 1: {self.scores[1]}")
        self.p2_score_label.config(text=f"Player 2: {self.scores[2]}")

    #Shows end game screen
    def end_game(self):
        self.build_end_screen()

#Main menu
class MenuFrame:
    def __init__(self, root, game):
        self.root = root
        self.game = game  #Lets menu frame access the game
        self.menu_frame = tk.Frame(root, bg="pink1")
        self.menu_frame.pack(fill="both", expand=True)
        
        # Title at top
        title_label = tk.Label(self.menu_frame, text="Match Madness", font=("Arial", 32, "bold"), bg="pink1", fg="deeppink4")
        title_label.pack(pady=10, anchor="n")
        
        # Container for the three columns
        columns_frame = tk.Frame(self.menu_frame, bg="pink1")
        columns_frame.pack(expand=True, fill="both")
        
        #Configure columns to have equal width
        columns_frame.columnconfigure(0, weight=1)  # Left column
        columns_frame.columnconfigure(1, weight=1)  # Middle column
        columns_frame.columnconfigure(2, weight=1)  # Right column
        columns_frame.rowconfigure(0, weight=1)
        
        #Left column: quit, rules, play buttons
        left_frame = tk.Frame(columns_frame, bg="pink1")
        left_frame.grid(row=0, column=0, sticky="n", pady=50)
        
        controls_label = tk.Label(left_frame, text="Controls:", font=("Arial", 14), bg="pink1", fg="deeppink4")
        controls_label.pack(pady=10)
        
        quit_btn = tk.Button(left_frame, text="Quit", width=15, bg="indian red", fg="white", command=root.destroy)
        quit_btn.pack(pady=5)

        rules_btn = tk.Button(left_frame, text="Rules", width=15, bg="PaleVioletRed", fg="white", command=self.show_rules)
        rules_btn.pack(pady=5)

        self.play_btn = tk.Button(left_frame, text="Play!", width=15, bg="PaleVioletRed", fg="white", command=self.play_game)
        self.play_btn.pack(pady=5)
        
        #Middle column: theme selection
        middle_frame = tk.Frame(columns_frame, bg="pink1")
        middle_frame.grid(row=0, column=1, sticky="n", pady=50)
        
        theme_label = tk.Label(middle_frame, text="Select Theme:", font=("Arial", 14), bg="pink1", fg="deeppink4")
        theme_label.pack(pady=10)
        
        #Theme buttons 
        self.theme_buttons = {}

        # Food
        food_btn = tk.Button(middle_frame, text="Food", width=15, bg="PaleVioletRed", fg="white",
                            command=lambda: self.select_theme("Food"))
        food_btn.pack(pady=5)
        self.theme_buttons["Food"] = food_btn

        # Nature
        nature_btn = tk.Button(middle_frame, text="Nature", width=15, bg="PaleVioletRed", fg="white",
                              command=lambda: self.select_theme("Nature"))
        nature_btn.pack(pady=5)
        self.theme_buttons["Nature"] = nature_btn

        # Flags
        flags_btn = tk.Button(middle_frame, text="Flags", width=15, bg="PaleVioletRed", fg="white",
                            command=lambda: self.select_theme("Flags"))
        flags_btn.pack(pady=5)
        self.theme_buttons["Flags"] = flags_btn
        # Animals
        animals_btn = tk.Button(middle_frame, text="Animals", width=15, bg="PaleVioletRed", fg="white",
                            command=lambda: self.select_theme("Animals"))
        animals_btn.pack(pady=5)
        self.theme_buttons["Animals"] = animals_btn
        
        #Right column: difficulty selection
        right_frame = tk.Frame(columns_frame, bg="pink1")
        right_frame.grid(row=0, column=2, sticky="n", pady=50)
        
        diff_label = tk.Label(right_frame, text="Select Difficulty:", font=("Arial", 14), bg="pink1", fg="deeppink4")
        diff_label.pack(pady=10)
        
        # Difficulty buttons 
        self.difficulty_buttons = {} 

        #Difficulty buttons
        easy_btn = tk.Button(right_frame, text="Easy", width=15, bg="PaleVioletRed", fg="white", command=lambda: self.select_difficulty("Easy"))
        easy_btn.pack(pady=5)
        self.difficulty_buttons["Easy"] = easy_btn

        medium_btn = tk.Button(right_frame, text="Medium", width=15, bg="PaleVioletRed", fg="white", command=lambda: self.select_difficulty("Medium"))
        medium_btn.pack(pady=5)
        self.difficulty_buttons["Medium"] = medium_btn

        hard_btn = tk.Button(right_frame, text="Hard", width=15, bg="PaleVioletRed", fg="white", command=lambda: self.select_difficulty("Hard"))
        hard_btn.pack(pady=5)
        self.difficulty_buttons["Hard"] = hard_btn 

    #Shows rules in messagebox
    def show_rules(self):
        messagebox.showinfo("Rules",  "How to Play Match Madness:\n\n"
    "1. Player 1 clicks on a card to flip it\n"
    "2. Player 1 clicks on another card to find a match\n"
    "3. If the cards match, they stay flipped\n"
    "4. If not, they flip back over\n"
    "5. If Player 1 got a match, they may go again until they miss. If not, it's Player 2's turn\n"
    "6. Find the most pairs to win!")

    #Selects a theme when theme button is clicked
    def select_theme(self, theme):
        self.game.selected_theme = theme
        
        # Updates button colors (highlight selected, unhighlight others)
        for theme_name, btn in self.theme_buttons.items():
            if theme_name == theme:
                btn.config(bg="deeppink4")
            else:
                btn.config(bg="PaleVioletRed")  
        
        self.update_play_button()  #Checks if play button should turn green (both theme and difficulty are selected)

    #Selects a difficulty when difficulty button is clicked
    def select_difficulty(self, difficulty):
        self.game.selected_difficulty = difficulty

        # Update button colors
        for diff_name, btn in self.difficulty_buttons.items():
            if diff_name == difficulty:
                btn.config(bg="deeppink4")
            else:
                btn.config(bg="PaleVioletRed")
        # Checks if play button should turn green
        self.update_play_button() 

    # Turns play button green when both theme and difficulty are selected
    def update_play_button(self):
        if self.game.selected_theme is not None and self.game.selected_difficulty is not None:
            self.play_btn.config(bg="PaleGreen3")
        else:
            self.play_btn.config(bg="PaleVioletRed")


    # Starting the game, check for missing inputs
    def play_game(self):
        if self.game.selected_difficulty is None and self.game.selected_theme is None:
            messagebox.showwarning("Missing selections", "Please select a theme and difficulty level")
        elif self.game.selected_difficulty is None:
            messagebox.showwarning("Missing difficulty", "Please select a difficulty level")
        elif self.game.selected_theme is None:
            messagebox.showwarning("Missing theme", "Please select a theme")
        else:
            self.game.start_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = MatchMadness(root)
    root.mainloop()