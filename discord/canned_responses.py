# processes extras, like chel's "suck my dick" command

import random

responses = {
    "suck my dick": ["```Shoha's knees hit the floor for the 9th time today.```"],
    "goddammit": [":sob:", ":angry:"],
    "dab": ["https://media1.giphy.com/media/A4R8sdUG7G9TG/giphy.gif", "https://giphy.com/gifs/squidward-dab-dabbing-lae7QSMFxEkkE"],
    "dap me up": ["i gotchu fam! uwu\n:right_facing_fist::left_facing_fist:"],
    "back me up": ["you got this (っಠ‿ಠ)っ", "you go my dude~"]
}

def process(msg):
    for key in responses:
        if key in msg:
            return random.choice(responses[key])
