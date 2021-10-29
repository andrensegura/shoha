from discord.ext import commands

class Swear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def swear(self, ctx):
        """Swears"""
        await ctx.send("Fuck!")

def setup(bot):
    bot.add_cog(Swear(bot))
