from discord.ext import commands
import discord

class VSay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mlg(self, ctx):
        channel = ctx.author.voice.channel
        vc = await channel.connect()
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("ext/vsay/mlg-airhorn.mp3"))
        vc.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        while vc.is_playing():
            pass
        await ctx.voice_client.disconnect()

def setup(bot):
    bot.add_cog(VSay(bot))