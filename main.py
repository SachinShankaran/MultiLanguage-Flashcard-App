import pandas
import random
from tkinter import *
from tkinter import simpledialog

# ------------------- Constants ------------------- #
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
flip_timer = None
source_language = ""
data_file = ""

# ------------------- Ask User ------------------- #
window = Tk()
window.withdraw()  # Hide the main window for now

# Ask which language
choice = simpledialog.askstring("Choose Language", "Which language do you want to learn? (French/Tamil)")

if choice is None:
    exit()  # User cancelled

choice = choice.lower()
if choice == "french":
    source_language = "French"
    data_file = "french_words.csv"
elif choice == "tamil":
    source_language = "Tamil"
    data_file = "tamil_words.csv"
else:
    print("Invalid choice! Please choose French or Tamil.")
    exit()

window.deiconify()  # Show the main window

# ------------------- Load Data ------------------- #
try:
    data = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv(data_file)

to_learn = data.to_dict(orient="records")

# ------------------- Functions ------------------- #
def next_card():
    global current_card, flip_timer
    if flip_timer:
        window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_background, image=card_front_img)
    canvas.itemconfig(canvas_title, text=source_language, fill="black")
    canvas.itemconfig(canvas_word, text=current_card[source_language], fill="black")
    flip_timer = window.after(3000, flip_card)

def flip_card():
    canvas.itemconfig(card_background, image=card_back_img)
    canvas.itemconfig(canvas_title, text='English', fill="white")
    canvas.itemconfig(canvas_word, text=current_card['English'], fill="white")

def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("words_to_learn.csv", index=False)
    next_card()

# ------------------- UI Setup ------------------- #
window.title(f"{source_language}-English Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="card_front.png")
card_back_img = PhotoImage(file="card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
canvas_title = canvas.create_text(400, 150, text=source_language, font=("Arial", 40, "italic"))
canvas_word = canvas.create_text(400, 263, text="Word", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file="wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()
window.mainloop()
