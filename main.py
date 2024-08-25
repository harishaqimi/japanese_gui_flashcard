from tkinter import *
import os,sys
import pandas
import random
from gtts import gTTS
import playsound

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

try:
    data = pandas.read_csv(resource_path("data/words_to_learn.csv"))
except FileNotFoundError:
    original_data = pandas.read_csv(resource_path("data/Japanese FlashCard for Python.csv"))
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    try:
        current_card = random.choice(to_learn)
    except IndexError:
        canvas.itemconfig(card_title, text="")
        canvas.itemconfig(card_word, text="You've memorized every card in this set", fill="black")
        canvas.itemconfig(card_hiragana, text="")
    else:
        canvas.itemconfig(card_title, text="Japanese", fill="black")
        canvas.itemconfig(card_word, text=current_card["Japanese"], fill="black")
        canvas.itemconfig(card_hiragana, text=current_card["Hiragana"], fill="red")
        canvas.itemconfig(card_background, image=card_front_img)
        # window.after(5000)
        flip_timer = window.after(3000, func=flip_card)
        speak_gtts(language='ja')

def speak_gtts(language):
    if language == "ja":
        audio_output = gTTS(text=current_card["Japanese"], lang=language)
    elif language == 'en':
        audio_output = gTTS(text=current_card["English"], lang=language)
    audio_output.save("sound_word.mp3")
    playsound.playsound("sound_word.mp3", True)
    os.remove("sound_word.mp3")

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_hiragana, text="")
    canvas.itemconfig(card_background, image=card_back_img)
    speak_gtts(language='en')
    # window.after(3000)
    # audio_output = gTTS(text=current_card["English"], lang=language)
    # audio_output.save("english_word.mp3")
    # playsound.playsound("english_word.mp3", True)
    # os.remove("english_word.mp3")

def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()



window = Tk()
window.title("Flash Card")
window.config(padx= 50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=526, width=800)
card_front_img = PhotoImage(file=resource_path("images/card_front.png"))
card_back_img = PhotoImage(file=resource_path("images/card_back.png"))
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400,100, text="Title", font=("Ariel", 30, "italic"), fill="black")
card_word = canvas.create_text(400,263, text="word", font=("Ariel", 60, "bold"), fill="black")
card_hiragana = canvas.create_text(400,350, text="Hiragana", font=("Ariel", 20, "normal"), fill="red")
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file=resource_path("images/wrong.png"))
unknown_button = Button(image=cross_image, bg=BACKGROUND_COLOR, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file=resource_path("images/right.png"))
known_button = Button(image=check_image, bg=BACKGROUND_COLOR, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()

window.mainloop()

