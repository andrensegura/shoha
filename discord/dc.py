#!/usr/local/bin/python3.6

import discord
import config
import canned_responses
import triggered_responses
import emoji
from discord.ext import commands

# INTENTS
intents = discord.Intents.default()
intents.members = True

class DiscordConnect(commands.Bot):

    def __init__(self):
        self.exts = config.exts
        commands.Bot.__init__(self,command_prefix=config.command_prefix,
                              owner_id=config.owner_id, intents=intents)

        @self.event
        async def on_ready():
            owner = self.get_user(config.owner_id)
            exts_list = ', '.join(self.exts)
            await owner.send("I am now online!\nExtensions loaded:\n" + exts_list)

        @self.event
        async def on_message(msg):
            if msg.author.bot:
                return
            msg.content = msg.content.lower()

            if "rocket league" in msg.content.lower():
                msg.content = "shoha mlg"
            
            # Check for triggered responses.
            # e.g. "steve jobs"  -> "who the hell is steve jobs"
            if not msg.content.startswith(config.command_prefix):
                response = triggered_responses.process(msg.content)
                if response:
                    await msg.channel.send(response)
            else:
                # Check for hardcoded responses she uses when addressed
                # e.g. "shoha dab" -> shoha dabs
                response = canned_responses.process(msg.content)
                if response:
                    await msg.channel.send(response)
                # Otherwise, process commands normally.
                else:
                    await self.process_commands(msg)

        @self.event
        async def on_reaction_add(reaction, user):
            #ChID = '195461511492141056'
            #if reaction.message.channel.id != ChID:
            #    return
            #print(emoji.demojize(reaction.emoji))
            if emoji.demojize(reaction.emoji) == ':scissors:':
                await reaction.message.channel.send(emoji.emojize(":scissors:"))
                

    def do_start(self):
        print("Loading extensions:")
        for ext in self.exts:
            try:
                self.load_extension("ext." + ext + ".main")
                print("  - {} loaded".format(ext))
            except Exception as e:
                # TO DO: add logging to file.
                print("  - {} ERROR: {}".format(ext,e))
        print("Connecting to Discord.")
        self.run(config.bot_auth_token)

    def do_stop(self):
        print("Disconnecting from Discord.")
        self.close()


if __name__ == "__main__":
    import time
    dbot = DiscordConnect()
    try:
        dbot.do_start()
    except Exception as e:
        print(e)
