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



# cards
# animals
# food
# flags
# nature

#Constants

  
DIFFICULTIES = {
"Easy": (3,4), #
"Medium": (4,4),
"Hard": (5,6)
}

CARD_SIZE = (100,100)
PADDING = 6 #Padding / space between cards


#Helper functions

#Loads and resizes an image file into a Tkinter PhotoImage
def load_photo(path, size=CARD_SIZE):
    img = Image.open(path).convert("RGB")
    img = img.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)


#Returns a list of full paths
def list_image_files(folder: str):
    endings = (".png", ".jpg", ".jpeg") #valid file endings
    files = []
    for name in os.listdir(folder):
        if name.lower().endswith(endings):
            files.append(os.path.join(folder, name))
    files.sort()
    return files
  

#Controls Match Madness Game 
class MatchMadness:
    def __init__(self, root):
        self.root = root
        self.root.title("Match Madness")
        self.root.geometry("800x600")
        self.root.config(bg="LightPink1")
    
    #Screens
        self.menu_frame = tk.Frame(root)
        self.game_frame = tk.Frame(root)

        self.menu = MenuFrame(root, self)
# instructions


    def start_game(self, theme):
        # Use correct folder path (Cards with capital C)
        folder = f"Cards/{theme}"
        image_paths = list_image_files(folder)
        
        # Load the images
        self.card_images = [load_photo(path) for path in image_paths]
        
        # Hide menu, show game
        self.menu.menu_frame.pack_forget()
        self.game_frame.pack(expand=True)
        
        # TODO: Create the card grid and game logic
        print(f"Loaded {len(self.card_images)} images from {folder}")


# main menu
class MenuFrame:
    def __init__(self, root, game):
        self.root = root
        self.game = game  # Store reference to the game
        self.menu_frame = tk.Frame(root, bg="LightPink1")
        self.menu_frame.pack(fill="both", expand=True)
        
        # Title at top
        title_label = tk.Label(self.menu_frame, text="Match Madness", font=("Arial", 32, "bold"), bg="LightPink1", fg="deeppink4")
        title_label.pack(pady=10, anchor="n")
        
        # Container for the three columns
        columns_frame = tk.Frame(self.menu_frame, bg="LightPink1")
        columns_frame.pack(expand=True, fill="both")
        
        # Configure columns to have equal weight
        columns_frame.columnconfigure(0, weight=1)  # Left column
        columns_frame.columnconfigure(1, weight=1)  # Middle column
        columns_frame.columnconfigure(2, weight=1)  # Right column
        columns_frame.rowconfigure(0, weight=1)
        
        # === LEFT COLUMN (Quit + future Instructions) ===
        left_frame = tk.Frame(columns_frame, bg="LightPink1")
        left_frame.grid(row=0, column=0, sticky="n", pady=50)
        
        controls_label = tk.Label(left_frame, text="Controls:", font=("Arial", 14), bg="LightPink1", fg="deeppink4")
        controls_label.pack(pady=10)
        
        quit_btn = tk.Button(left_frame, text="Quit", width=15, bg="PaleVioletRed", fg="white", command=root.destroy)
        quit_btn.pack(pady=5)

        rules_btn = tk.Button(left_frame, text="Rules", width=15, bg="PaleVioletRed", fg="white", command=self.show_rules)
        rules_btn.pack(pady=5)
        
        # Instructions button will go here later
        
        # === MIDDLE COLUMN (Themes) ===
        middle_frame = tk.Frame(columns_frame, bg="LightPink1")
        middle_frame.grid(row=0, column=1, sticky="n", pady=50)
        
        theme_label = tk.Label(middle_frame, text="Select Theme:", font=("Arial", 14), bg="LightPink1", fg="deeppink4")
        theme_label.pack(pady=10)
        
        food_btn = tk.Button(middle_frame, text="Food", width=15, bg="PaleVioletRed", fg="white",
                            command=lambda: self.game.start_game("Food"))
        food_btn.pack(pady=5)
        
        nature_btn = tk.Button(middle_frame, text="Nature", width=15, bg="PaleVioletRed", fg="white",
                              command=lambda: self.game.start_game("Nature"))
        nature_btn.pack(pady=5)

        flags_btn = tk.Button(middle_frame, text="Flags", width=15, bg="PaleVioletRed", fg="white",
                            command=lambda: self.game.start_game("Flags"))
        flags_btn.pack(pady=5)

        animals_btn = tk.Button(middle_frame, text="Animals", width=15, bg="PaleVioletRed", fg="white",
                            command=lambda: self.game.start_game("Animals"))
        animals_btn.pack(pady=5)
        
        # === RIGHT COLUMN (Difficulty) ===
        right_frame = tk.Frame(columns_frame, bg="LightPink1")
        right_frame.grid(row=0, column=2, sticky="n", pady=50)
        
        diff_label = tk.Label(right_frame, text="Select Difficulty:", font=("Arial", 14), bg="LightPink1", fg="deeppink4")
        diff_label.pack(pady=10)
        
        # Difficulty buttons placeholder (not implemented yet)
        easy_btn = tk.Button(right_frame, text="Easy", width=15, bg="PaleVioletRed", fg="white")
        easy_btn.pack(pady=5)
        
        medium_btn = tk.Button(right_frame, text="Medium", width=15, bg="PaleVioletRed", fg="white")
        medium_btn.pack(pady=5)
        
        hard_btn = tk.Button(right_frame, text="Hard", width=15, bg="PaleVioletRed", fg="white")
        hard_btn.pack(pady=5)


        #Rules 
    def show_rules(self):
        messagebox.showinfo("Rules",  "How to Play Match Madness:\n\n"
    "1. Player 1 clicks on a card to flip it\n"
    "2. Player 1 clicks on another card to find a match\n"
    "3. If the cards match, they stay flipped\n"
    "4. If not, they flip back over\n"
    "5. If Player 1 got a match, they may go again until they miss. If not, it's Player 2's turn\n"
    "6. Find the most pairs to win!")
        
    # transition to the game screen
    

# game screen
    # displaying the images
    
    # alternating player turns
    
    # score system
    
    
# end screen
    # end + winner screen

if __name__ == "__main__":
    root = tk.Tk()
    game = MatchMadness(root)
    root.mainloop()