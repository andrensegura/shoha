from discord import Color
from discord.ext import commands

class Sensei(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['colour'])
    @commands.has_role("sensei")
    async def color(self, ctx, color: str):
        """Changes your color"""
        color = Color(int(color, 16))
        role_name = ctx.author.name + "#" + ctx.author.discriminator

        if role_name in [r.name for r in ctx.guild.roles]:
            new_role = [r for r in ctx.guild.roles if r.name == role_name][0]
            await new_role.edit(color=color)
        else:
            new_role = await ctx.guild.create_role(name=role_name, color=color)
            await ctx.author.add_roles(new_role)

        pos = [r.position for r in ctx.guild.roles if r.name == 'shoha'][0]
        await new_role.edit(position = pos - 1)
        await ctx.send("Color updated!")

    @commands.command()
    @commands.has_role("sensei")
    async def say(self, ctx, message: str):
        """Repeats what you say to her."""
        print("Command executed: say")
        await ctx.message.delete()
        await ctx.send(ctx.message.content.partition('say ')[2:][0])

def setup(bot):
    bot.add_cog(Sensei(bot))
