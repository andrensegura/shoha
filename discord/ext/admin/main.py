import ext.admin.redditmod as redditmod
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, extension_name : str):
        """Loads an extension."""
        try:
            self.bot.load_extension("ext." + extension_name)
        except (AttributeError, ImportError) as e:
            await ctx.send("```py\n{}: {}\n```".format(
                               type(e).__name__, str(e)))
            return
        await ctx.send("{} loaded.".format(extension_name))

    @commands.command(hidden=True)
    async def unload(self, ctx, extension_name : str):
        """Unloads an extension."""
        self.bot.unload_extension("ext." + extension_name)
        await ctx.send("{} unloaded.".format(extension_name))

    @commands.command(hidden=True)
    async def reload(self, ctx, extension_name : str):
        """Reloads an extension."""
        try:
            self.bot.unload_extension("ext." + extension_name)
            self.bot.load_extension("ext." + extension_name)
        except (AttributeError, ImportError) as e:
            await ctx.send("```py\n{}: {}\n```".format(
                               type(e).__name__, str(e)))
            return
        await ctx.send("{} reloaded.".format(extension_name))

    @commands.command(hidden=True)
    @commands.has_role("sub mod")
    async def remove(self, ctx):
        """removes a reddit post"""
        # only works in the #subfeed channel.
        if str(ctx.channel.id) == '585364148892991489':
            try:
                url = ctx.message.content.split()[2]
                rule = ctx.message.content.split()[3]
                await redditmod.remove_post(url, rule)
                await ctx.send("Post removed for rule " + rule + ".")
            except Exception as e:
                url = ctx.message.content.split()[2]
                await redditmod.remove_post(url)
                await ctx.send("Post removed for no reason. Hehe.")


def setup(bot):
    bot.add_cog(Admin(bot))
