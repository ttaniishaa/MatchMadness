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
from PIL import Image, ImageTK
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
def load_photo(path, size=CARD_SIZE)
    img = Image.open(path).convert("RGB")
    img = img.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)


#Returns a list of full paths
def list_image_files(folder: str):
    endings = (".png", ".jpg", ".jpeg") #valid file endings
    files = []
    for name in os.listdir(folder):
        if name.lower().endswith(exts):
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
# instructions

# main menu
class MenuFrame:
    def __init__(self, root):
        self.root = root
        self.menu_frame = tk.Frame(root)
        self.menu_frame.pack()
        theme_label = tk.Label(self.menu_frame, text="Theme")
        theme_label.pack()
        # selecting difficulty
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