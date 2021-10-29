import discord
from discord.ext import commands
from requests_xml import XMLSession
import html
import json


class MAL():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def anime(self, ctx):
        """Gets information for an anime."""
        async with ctx.channel.typing():
            sess = XMLSession()
            query = ctx.message.content.partition(' ')[2]
            query = query.replace(' ', '+')
            print(query)
            url = "https://myanimelist.net/api/anime/search.xml?q=" + query
            auth = ('faroeson', '7827scream')

            r = sess.get(url, auth=auth)

            try:
                item = r.xml.xpath('//entry', first=True)
            except Exception as e:
                await ctx.send("No results found :(")
                return
            item = json.loads(item.json())
            item = item['entry']
            print(json.dumps(item))

            img = item['image']['$']
            english = '({})'.format(item['english']['$']) if '$' in item['english'] else '' 
            title = "{} ({})".format(item['title']['$'], english)
            rating = item['score']['$']
            status = item['status']['$']
            eps = item['episodes']['$']
            syn = html.unescape(item['synopsis']['$'].replace('<br />', ''))
            syn = (syn[:800] + '...') if len(syn) > 800 else syn
            embed = discord.Embed(color=0x00ff00) 
            embed.set_image(url=img)
            embed.add_field(name='Title', value=title, inline=True)
            embed.add_field(name='Rating', value=rating, inline=True)
            embed.add_field(name='Status', value=status, inline=True)
            embed.add_field(name='Episodes', value=eps, inline=True)
            embed.add_field(name='Synopsis', value=syn, inline=False)
            await ctx.send("", embed = embed)


    @commands.command()
    async def manga(self, ctx):
        """Gets information for an anime."""
        async with ctx.channel.typing():
            sess = XMLSession()
            query = ctx.message.content.partition(' ')[2]
            query = query.replace(' ', '+')
            url = "https://myanimelist.net/api/manga/search.xml?q=" + query
            auth = ('faroeson', '7827scream')

            r = sess.get(url, auth=auth)

            try:
                item = r.xml.xpath('//entry', first=True)
            except Exception as e:
                await ctx.send("No results found :(")
                return
            item = json.loads(item.json())
            item = item['entry']

            img = item['image']['$']
            title = "{} ({})".format(item['title']['$'], item['english']['$'])
            rating = item['score']['$']
            status = item['status']['$']
            chp = item['chapters']['$']
            syn = html.unescape(item['synopsis']['$'].replace('<br />', ''))
            syn = (syn[:800] + '...') if len(syn) > 800 else syn
            embed = discord.Embed(color=0x00ff00) 
            embed.set_image(url=img)
            embed.add_field(name='Title', value=title, inline=True)
            embed.add_field(name='Rating', value=rating, inline=True)
            embed.add_field(name='Status', value=status, inline=True)
            embed.add_field(name='Chapters', value=chp, inline=True)
            embed.add_field(name='Synopsis', value=syn, inline=False)
            await ctx.send("", embed = embed)

def setup(bot):
    bot.add_cog(MAL(bot))



