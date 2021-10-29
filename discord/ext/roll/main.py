# This extension is using a deprecated API.
# MAL deprecated it the fucking day AFTER I wrote this shit.

import discord
from discord.ext import commands
from random import randrange

class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx):
        """rolls a dX."""
        async with ctx.channel.typing():
            try:
                ran = int(ctx.message.content.partition('roll')[2].strip()[1:])
                roll = randrange(1,ran)
                await ctx.send(str(roll))
            except Exception as e:
                await ctx.send(str(randrange(1,20)))

def setup(bot):
    bot.add_cog(Roll(bot))



