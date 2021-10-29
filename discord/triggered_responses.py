import random

responses = {
    "steve jobs": ["who the hell is steve jobs"],
    "pogger": ["> pogger\ncringe",
               "> pogger\new",
               "> pogger\n:nauseated_face:"
              ],
    "ligma balls": ["https://i.imgur.com/HPduAKn.gif",
                    "https://tenor.com/view/ligma-balls-gif-22082587",
                    "https://tenor.com/view/dead-i-am-dead-ded-terminator-terminator2-gif-5663820",
                    "https://i.imgur.com/1PG4GEC.gif",
                    "https://c.tenor.com/gMACtWvF0v0AAAAC/pissed-angry.gif",
                    "https://thinkinganimation.com/wp-content/uploads/2013/06/tumblr_mowgalVS3O1snfsquo1_400.gif",
                    "https://media1.giphy.com/media/djTw5269awMtW/200.gif",
                    "https://i.gifer.com/ZIEl.gif",
                    "http://pa1.narvii.com/7122/2ff09872e9d4ee1dc65f123ddc9534afa965a9edr1-250-180_00.gif",
                    "https://c.tenor.com/VcU44mUEVj4AAAAC/explosion-anime.gif"
                ]
}

def process(msg):
    for key in responses:
        if key in msg:
            return random.choice(responses[key])
