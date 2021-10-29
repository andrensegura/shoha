import random

responses = {
    "steve jobs": ["who the hell is steve jobs"],
    "pogger": ["> pogger\ncringe"],
    "ligma balls": ["https://i.imgur.com/HPduAKn.gif","https://tenor.com/view/ligma-balls-gif-22082587","https://tenor.com/view/dead-i-am-dead-ded-terminator-terminator2-gif-5663820"]
}

def process(msg):
    for key in responses:
        if key in msg:
            return random.choice(responses[key])
