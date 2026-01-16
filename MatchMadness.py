'''
Card Memory Game 
Authors: Tanisha Naser and Angela Xi
Date: January 13th, 2026

Description: 
This program implements a card memory game using Tkinter. 
The player(s) can choose to play multiplayer(2 people), or solo.
In a multiplayer game, players take turn flipping cards to find matches. Each match found is a point. The player with the most points wins.
In a solo game, the player will try to flip as many cards as possible within the time limit (3 minutes). The game ends either when the timer finishes or when all cards are matched. 
'''

import tkinter as tk
from tkinter import messagebox
import random
import os 


#Constant variables

#Grid size depending on difficulty of game
DIFFICULTIES = {
"Easy": (3,4), 
"Medium": (4,4),
"Hard": (5,6)
}

#Space between cards
PADDING = 6 

#Turn label colours for multiplayer
PLAYER_TURN_COLOURS = {
    1: "pale violet red",   #Player 1 = pink
    2: "steelblue3", #Player 2 = blue
}


#Timer for solo mode
time_left = 180 


#Helper functions
              
#Loads an image file into a Tkinter PhotoImage
def load_photo(path):
    return tk.PhotoImage(file=path)

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
    #Constructor
    def __init__(self, root):
        self.root = root
        self.root.title("Match Madness")
        self.root.geometry("800x600")
        self.root.config(bg="peach puff")
        self.selected_difficulty = None 
        self.selected_theme = None  
        self.selected_player = None
        self.timer_label = None
        self.timer_running = False  #Tracks if timer is running
        self.game_completed = False  #Tracks if game was completed (vs time out)
        
        #Screens
        self.game_frame = tk.Frame(root)
        self.menu = MenuFrame(root, self, players=self.selected_player)
    
    #Updates the timer display every second and ends the game when time runs out
    def countdown(self):
        global time_left
        if self.timer_running and time_left > 0:
            time_left -= 1 #decrease time by 1 second if time is left
            mins, secs = divmod(time_left, 60)
            timeFormat = '{:02d}:{:02d}'.format(mins, secs) #format the time according to the seconds
            
            if self.timer_label:
                self.timer_label.config(text=f"Timer: {timeFormat}")
                
            #Call countdown again
            self.root.after(1000, self.countdown)
        elif time_left <= 0: #when time runs out
            self.timer_running = False
            self.game_completed = False  #Time ran out
            self.end_game()
            return
                
    #Timer function
    def timer(self):
        global time_left 
        time_left = 180
        self.timer_running = True
        self.countdown() 

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
        
        #Resizes window based on difficulty to avoid cards being cut off 
        if self.selected_difficulty == "Easy":
            self.root.geometry("800x550")
        elif self.selected_difficulty == "Medium":
            self.root.geometry("900x650")
        else: 
            self.root.geometry("1100x750")
        
        #Hide menu & show game
        self.menu.menu_frame.pack_forget()
        self.game_frame.config(bg="peach puff")
        self.game_frame.pack(expand=True, fill="both")

        #Build game screen first
        self.build_game_screen()
        
        #Starts timer only for solo mode
        if self.selected_player == "Solo":
            self.timer()

    
    
    #Sets up the game board
    def build_game_screen(self):
        #Clears existing buttons, text, etc from the game frame
        for widget in self.game_frame.winfo_children():
            widget.destroy() 
        
        #Left sidebar
        sidebar = tk.Frame(self.game_frame, bg="peach puff", width=200)
        sidebar.pack(side="left", fill="y", padx=10, pady=10)
        sidebar.pack_propagate(False)
        
        title = tk.Label(sidebar, text="Match Madness", font=("Times New Roman", 16, "bold"), bg="peach puff", fg="lightsalmon3")
        title.pack(pady=10)

        info_label = tk.Label(sidebar, text=f"Theme: {self.selected_theme} \nDifficulty: {self.selected_difficulty}", font = ("Arial", 10), bg="peach puff", fg="lightsalmon3")
        info_label.pack(pady=5)

        #Scores
        scores_title = tk.Label(sidebar, text="Scores:", font=("Arial", 12, "bold"), bg="peach puff", fg="lightsalmon3")
        scores_title.pack(pady=(10, 5))
            
        #Set up game screen according to player count
        if self.selected_player == "Multiplayer":    
            #Multiplayer scores
            self.p1_score_label = tk.Label(sidebar, text="Player 1: 0", font=("Arial", 12), bg="peach puff", fg="lightsalmon3")
            self.p1_score_label.pack(pady=2)
                
            self.p2_score_label = tk.Label(sidebar, text="Player 2: 0", font=("Arial", 12), bg="peach puff", fg="lightsalmon3")
            self.p2_score_label.pack(pady=2)
        
        #Solo timer
        elif self.selected_player == "Solo":
            # Store reference for timer updates
            self.timer_label = tk.Label(sidebar, text="Timer: 03:00", font=("Arial", 12), bg="peach puff", fg="lightsalmon3")
            self.timer_label.pack(pady=5)
            
            #solo score/match count 
            self.p1_score_label = tk.Label(sidebar, text="Pairs Matched: 0", font=("Arial", 12), bg="peach puff", fg="lightsalmon3")
            self.p1_score_label.pack(pady=2)

        #Turn indicator for multiplayer
        if self.selected_player == "Multiplayer":
            self.turn_label = tk.Label(
                sidebar,
                text=f"Player {self.current_player}'s turn",
                font=("Arial", 14, "bold"),
                bg="peach puff",
                fg=PLAYER_TURN_COLOURS.get(self.current_player, "black"),
            )
            self.turn_label.pack(pady=15)
        else:
            self.turn_label = None
        
        #Rules and quit buttons
        rules_btn = tk.Button(sidebar, text="Rules", width=12,bg="lightsalmon2", fg="white", command=self.menu.show_rules)
        rules_btn.pack(pady=10)

        quit_btn = tk.Button(sidebar, text="Quit", width=12,bg="indian red", fg="white", command=self.root.destroy)
        quit_btn.pack(pady=5)

        #Card grid 
        grid_frame = tk.Frame(self.game_frame, bg="peach puff")
        grid_frame.pack(side="right", expand=True, fill="both", padx=5, pady=5)

        self.card_buttons = []

        for i in range(self.rows): #Setting up rows from user input
            row_buttons = []
            for j in range(self.cols): #Setting up columns from user input
                card_index = i * self.cols + j
                btn = tk.Button(grid_frame, text="?", width=8, height=4,
                    bg="lightsalmon2", fg="white", font=("Arial", 12, "bold"),
                    activebackground="lightsalmon2", activeforeground="white",
                    command=lambda idx=card_index, r=i, c=j: self.flip_card(idx, r, c))
                btn.grid(row=i, column=j, padx=PADDING, pady=PADDING)
                row_buttons.append(btn)
            self.card_buttons.append(row_buttons)

    #Sets up ending/winner screen
    def build_end_screen(self):
        #Clears existing buttons, text, etc
        for widget in self.game_frame.winfo_children():
            widget.destroy() 

        self.game_frame.config(bg="peach puff")

        #Stop timer if running
        self.timer_running = False

        #Determine winner/end message based on mode
        if self.selected_player == "Solo":
            if self.game_completed:
                winner_text = "Congratulations!"
                #Calculate time taken (180 - time_left)
                global time_left
                time_taken = 180 - time_left
                mins, secs = divmod(time_taken, 60)
                time_format = '{:02d}:{:02d}'.format(mins, secs)
                result_text = f"Completed in: {time_format}\nPairs Matched: {self.scores[1]}"
            else:
                winner_text = "Time's Up!"
                result_text = f"Pairs Matched: {self.scores[1]}"
        else:
            #Multiplayer mode
            if self.scores[1] > self.scores[2]:
                winner_text = "Player 1 Wins!"
            elif self.scores[2] > self.scores[1]:
                winner_text = "Player 2 Wins!"
            else:
                winner_text = "It's a Tie!"
            result_text = f"Final Scores:\nPlayer 1: {self.scores[1]}\nPlayer 2: {self.scores[2]}"

        title = tk.Label(self.game_frame, text="Game Over!", font=("Arial", 28, "bold"), bg="peach puff", fg="lightsalmon3")
        title.pack(pady=30)

        # Winner/End message
        winner_label = tk.Label(self.game_frame, text=winner_text, font=("Arial", 20), bg="peach puff", fg="lightsalmon3")
        winner_label.pack(pady=10)
        
        #Final scores/time
        scores_label = tk.Label(self.game_frame, text=result_text, 
                               font=("Arial", 14), bg="peach puff", fg="lightsalmon3")
        scores_label.pack(pady=20)
        
        #Buttons frame
        btn_frame = tk.Frame(self.game_frame, bg="peach puff")
        btn_frame.pack(pady=20)
        
        #Play again button
        play_again_btn = tk.Button(btn_frame, text="Play Again", width=12, bg="PaleGreen3", fg="white",
                                   command=self.play_again)
        play_again_btn.pack(side="left", padx=10)
        
        #Main menu button
        menu_btn = tk.Button(btn_frame, text="Main Menu", width=12, bg="lightsalmon2", fg="white",
                            command=self.go_to_menu)
        menu_btn.pack(side="left", padx=10)
        
        #Quit button
        quit_btn = tk.Button(btn_frame, text="Quit", width=12, bg="indian red", fg="white",
                            command=self.root.destroy)
        quit_btn.pack(side="left", padx=10)
    
    #Starts a new game with same settings
    def play_again(self):
        global time_left
        time_left = 180  #Reset timer
        self.timer_running = False
        self.game_completed = False
        self.start_game()
    

    #Returns to main menu
    def go_to_menu(self):
        """Return to main menu"""
        global time_left
        self.timer_running = False  #Stop timer
        time_left = 180  #Reset timer
        self.game_completed = False
        self.game_frame.pack_forget()
        self.root.geometry("800x600")  #Reset window size
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
            btn.config(image=self.card_images[index], text="", width=90, height=90,activebackground="peach puff")

            #Add to flipped cards
            self.flipped_cards.append(index)

            #If 2 cards are flipped, check for match
            if len(self.flipped_cards) == 2:
                self.root.after(600, self.check_match) #Waits 0.6 seconds before checking for match


    #Checks if 2 flipped cards are a match
    def check_match(self):
        #Exit if timer already ended the game in solo mode due to 0.6 second delay in check match
        if self.selected_player == "Solo" and not self.timer_running:
            return

        idx1, idx2 = self.flipped_cards

        #Get image paths to compare 
        path1 = self.card_paths[idx1]
        path2 = self.card_paths[idx2]

        #Keep cards face up (match)
        if path1 == path2:
            self.matched_cards.append(idx1)
            self.matched_cards.append(idx2)
            
            #Add point to current player 
            self.scores[self.current_player] += 1
            self.update_scores()

            #Check if game is over
            if len(self.matched_cards) == self.rows * self.cols:
                self.game_completed = True  # Game was completed successfully
                self.end_game()
                return
        
        else:
            #No match, flip cards back, find buttons and reset them
            for idx in self.flipped_cards:
                row = idx // self.cols
                col = idx % self.cols 
                btn = self.card_buttons[row][col]
                btn.config(image="", text="?", width=8, height=4, 
                          bg="lightsalmon2", fg="white",
                          activebackground="lightsalmon2", activeforeground="white")

            #Switch player only on no match
            if self.selected_player == "Multiplayer":
                if self.current_player == 1:
                    self.current_player = 2
                else:
                    self.current_player = 1
                if self.turn_label:
                    self.turn_label.config(
                        text=f"Player {self.current_player}'s turn",
                        fg=PLAYER_TURN_COLOURS.get(self.current_player, "black"),
                    )
            elif self.selected_player == "Solo":
                self.current_player = 1  #Always player 1 in solo mode
                #No turn label to update in solo mode

        #Clear flipped cards for next turn
        self.flipped_cards = []

    #Refreshes score display
    def update_scores(self):
        if self.selected_player == "Multiplayer":
            self.p1_score_label.config(text=f"Player 1: {self.scores[1]}")
            self.p2_score_label.config(text=f"Player 2: {self.scores[2]}")
        elif self.selected_player == "Solo":
            self.p1_score_label.config(text=f"Pairs Matched: {self.scores[1]}")

    #Shows end game screen
    def end_game(self):
        self.build_end_screen()

#Main menu
class MenuFrame:

    #Constructor
    def __init__(self, root, game, players):
        self.root = root
        self.game = game  #Lets menu frame access the game
        self.menu_frame = tk.Frame(root, bg="peach puff")
        self.menu_frame.pack(fill="both", expand=True)
        
        #Title at top
        title_label = tk.Label(self.menu_frame, text="Match Madness", font=("Times New Roman", 32, "bold"), bg="peach puff", fg="lightsalmon3")
        title_label.pack(pady=10, anchor="n")
        
        #Container for the three columns
        columns_frame = tk.Frame(self.menu_frame, bg="peach puff")
        columns_frame.pack(expand=True, fill="both")
        
        #Configure columns to have equal width
        columns_frame.columnconfigure(0, weight=1)  # Left column
        columns_frame.columnconfigure(1, weight=1)  # Middle left column
        columns_frame.columnconfigure(2, weight=1)  # Middle right column
        columns_frame.columnconfigure(3, weight=1)  # Right column
        columns_frame.rowconfigure(0, weight=1)
        
        #Left column: quit, rules, play buttons
        left_frame = tk.Frame(columns_frame, bg="peach puff")
        left_frame.grid(row=0, column=0, sticky="n", pady=50)
        
        controls_label = tk.Label(left_frame, text="Controls:", font=("Arial", 14), bg="peach puff", fg="lightsalmon3")
        controls_label.pack(pady=10)
        
        quit_btn = tk.Button(left_frame, text="Quit", width=15, bg="indian red", fg="white", command=root.destroy)
        quit_btn.pack(pady=5)

        rules_btn = tk.Button(left_frame, text="Rules", width=15, bg="lightsalmon2", fg="white", command=self.show_rules)
        rules_btn.pack(pady=5)

        self.play_btn = tk.Button(left_frame, text="Play!", width=15, bg="lightsalmon2", fg="white", command=self.play_game)
        self.play_btn.pack(pady=5)
        
        #Middle column: theme selection
        middle_frame = tk.Frame(columns_frame, bg="peach puff")
        middle_frame.grid(row=0, column=1, sticky="n", pady=50)
        
        theme_label = tk.Label(middle_frame, text="Select Theme:", font=("Arial", 14), bg="peach puff", fg="lightsalmon3")
        theme_label.pack(pady=10)
        
        #Theme buttons 
        self.theme_buttons = {}

        #Food
        food_btn = tk.Button(middle_frame, text="Food", width=15, bg="lightsalmon2", fg="white",
                            command=lambda: self.select_theme("Food"))
        food_btn.pack(pady=5)
        self.theme_buttons["Food"] = food_btn

        #Nature
        nature_btn = tk.Button(middle_frame, text="Nature", width=15, bg="lightsalmon2", fg="white",
                              command=lambda: self.select_theme("Nature"))
        nature_btn.pack(pady=5)
        self.theme_buttons["Nature"] = nature_btn

        #Flags
        flags_btn = tk.Button(middle_frame, text="Flags", width=15, bg="lightsalmon2", fg="white",
                            command=lambda: self.select_theme("Flags"))
        flags_btn.pack(pady=5)
        self.theme_buttons["Flags"] = flags_btn
        #Animals
        animals_btn = tk.Button(middle_frame, text="Animals", width=15, bg="lightsalmon2", fg="white",
                            command=lambda: self.select_theme("Animals"))
        animals_btn.pack(pady=5)
        self.theme_buttons["Animals"] = animals_btn
        
        #Player mode selection
        self.player_button = {}
        
        middle_frame = tk.Frame(columns_frame, bg="peach puff")
        middle_frame.grid(row=0, column=2, sticky="n", pady=50)

        player_label = tk.Label(middle_frame, text="Select Player Count:", font=("Arial", 14), bg="peach puff", fg="lightsalmon3")
        player_label.pack(pady=10)
        
        solo_btn = tk.Button(middle_frame, text="Solo", width=15, bg="lightsalmon2", fg="white", command=lambda: self.selected_player("Solo"))
        solo_btn.pack(pady=5)
        self.player_button["Solo"] = solo_btn

        multi_btn = tk.Button(middle_frame, text="Multiplayer", width=15, bg="lightsalmon2", fg="white", command=lambda: self.selected_player("Multiplayer"))
        multi_btn.pack(pady=5)
        self.player_button["Multiplayer"] = multi_btn
        
        #Right column: difficulty selection
        right_frame = tk.Frame(columns_frame, bg="peach puff")
        right_frame.grid(row=0, column=3, sticky="n", pady=50)
        
        diff_label = tk.Label(right_frame, text="Select Difficulty:", font=("Arial", 14), bg="peach puff", fg="lightsalmon3")
        diff_label.pack(pady=10)
        
        #Difficulty buttons 
        self.difficulty_buttons = {} 

        easy_btn = tk.Button(right_frame, text="Easy", width=15, bg="lightsalmon2", fg="white", command=lambda: self.select_difficulty("Easy"))
        easy_btn.pack(pady=5)
        self.difficulty_buttons["Easy"] = easy_btn

        medium_btn = tk.Button(right_frame, text="Medium", width=15, bg="lightsalmon2", fg="white", command=lambda: self.select_difficulty("Medium"))
        medium_btn.pack(pady=5)
        self.difficulty_buttons["Medium"] = medium_btn

        hard_btn = tk.Button(right_frame, text="Hard", width=15, bg="lightsalmon2", fg="white", command=lambda: self.select_difficulty("Hard"))
        hard_btn.pack(pady=5)
        self.difficulty_buttons["Hard"] = hard_btn 
        
        
        
    #Shows rules in messagebox
    def show_rules(self):
        messagebox.showinfo("Rules",  "How to Play Match Madness:\n\n"
    "SOLO MODE (Timed):\n"
    "1. Click on a card to flip it\n"
    "2. Click on another card to find a match\n"
    "3. If the cards match, they stay flipped and you get a point\n"
    "4. If not, they flip back over\n"
    "5. You have 3 minutes to find as many pairs as possible\n"
    "6. The game ends when time runs out or all pairs are matched\n\n"
    "MULTIPLAYER MODE:\n"
    "1. Player 1 clicks on a card to flip it\n"
    "2. Player 1 clicks on another card to find a match\n"
    "3. If the cards match, they stay flipped and Player 1 gets a point\n"
    "4. If not, they flip back over and it becomes Player 2's turn\n"
    "5. Players take turns until all pairs are matched\n"
    "6. The player with the most pairs wins!")

    #Selects a theme when theme button is clicked
    def select_theme(self, theme):
        self.game.selected_theme = theme
        
        #Updates button colors (highlight selected, unhighlight others)
        for theme_name, btn in self.theme_buttons.items():
            if theme_name == theme:
                btn.config(bg="lightsalmon3")
            else:
                btn.config(bg="lightsalmon2")  
        
        self.update_play_button()  #Checks if play button should turn green (theme, player count, and difficulty are selected)

    #Selects a difficulty when difficulty button is clicked
    def select_difficulty(self, difficulty):
        self.game.selected_difficulty = difficulty

        #Update button colors
        for diff_name, btn in self.difficulty_buttons.items():
            if diff_name == difficulty:
                btn.config(bg="lightsalmon3")
            else:
                btn.config(bg="lightsalmon2")

        self.update_play_button() 

    def selected_player(self, player):
        self.game.selected_player = player

        #Update button colors
        for player_name, btn in self.player_button.items():
            if player_name == player:
                btn.config(bg="lightsalmon3")
            else:
                btn.config(bg="lightsalmon2")
        
        self.update_play_button()
                
    #Turns play button green when theme, player count, and difficulty are selected
    def update_play_button(self):
        if self.game.selected_theme is not None and self.game.selected_difficulty is not None and self.game.selected_player is not None:
            self.play_btn.config(bg="PaleGreen3")
        else:
            self.play_btn.config(bg="lightsalmon2")

    #Starting the game, checks for missing inputs
    def play_game(self):
        if self.game.selected_difficulty is None and self.game.selected_theme is None:
            messagebox.showwarning("Missing selections", "Please select a theme and difficulty level")
        elif self.game.selected_difficulty is None:
            messagebox.showwarning("Missing difficulty", "Please select a difficulty level")
        elif self.game.selected_theme is None:
            messagebox.showwarning("Missing theme", "Please select a theme")
        elif self.game.selected_player is None:
            messagebox.showwarning("Missing player count", "Please select a player count")
        else:
            self.game.start_game()

#Main 
if __name__ == "__main__":
    root = tk.Tk()
    game = MatchMadness(root)
    root.mainloop() 