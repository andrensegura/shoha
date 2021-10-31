from pybooru import Danbooru
from discord import Embed
from discord.ext import commands
import sys

client = Danbooru('danbooru')

class Booru(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = Danbooru('danbooru')

    def get_post(self, search_tag):
        results = client.post_list(limit=1, tags=search_tag, random=True)
        result = results[0]
        page_link = "https://danbooru.donmai.us/posts/" + str(result['id'])
        image_link = result['file_url']
        return (page_link, image_link)

    @commands.command()
    async def booru(self, ctx, *arg):
        if not arg:
            return
        
        tag = arg
        post = self.get_post(tag)
        embed=Embed(title="random " + tag, color=0xfdf6e6)
        embed.add_field(name="Post URL:", inline=False)
        embed.add_field(value=post[0], inline=False)
        embed.set_image(url=post[1])
        return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Booru(bot))



