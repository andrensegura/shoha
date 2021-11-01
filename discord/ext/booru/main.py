from pybooru import Danbooru
from discord import Embed
from discord.ext import commands
import sys

class Booru(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = Danbooru('danbooru')

    def get_post(self, search_tag, search_rating='s'):
        # search_rating = s, e, q
        client = Danbooru('danbooru')
        results = client.post_list(limit=1, tags=search_tag, random=True)
        result = results[0]
        while result['rating'] != search_rating:
            results = client.post_list(limit=1, tags=search_tag, random=True)
            result = results[0]
        print(result)
        page_link = "https://danbooru.donmai.us/posts/" + str(result['id'])
        image_link = result['file_url']
        return (page_link, image_link)

    @commands.command()
    async def booru(self, ctx, tag: str, nsfw: str):
        if not tag:
            await ctx.send("Need a tag.\n`shoha booru \"tag_here\"`")
            return

        if nsfw == 'nsfw':
            nsfw = 'e'
            r_color = 0xff0000
        elif nsfw == 'questionable':
            nsfw = 'q'
            r_color = 0x0000ff
        else:
            nsfw = 's'
            r_color = 0x00ff00

        async with ctx.channel.typing():
            post = self.get_post(tag, nsfw)
            embed=Embed(title="random " + tag, color=r_color)
            embed.add_field(name="Post URL:", value=post[0], inline=False)
            embed.set_image(url=post[1])
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Booru(bot))



