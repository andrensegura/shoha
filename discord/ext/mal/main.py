# This extension is using a deprecated API.
# MAL deprecated it the fucking day AFTER I wrote this shit.

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
            if "cory in the house" in ctx.message.content.lower():
                syn="Cory in the House is an American anime which aired on the Dizunī Channeru from January 12, 2007, to September 12, 2008, and was a spin-off from the Dizunī show Sore wa Raven. The show focuses on Cory Takanashi, who moves from Hokkaido, Japan to Washington, D.C. with his father, after Victor Takanashi gets a new job in the White House as the official head chef. The series marks a Dizunī Channeru first, as it is the channel's first spin-off. This is also the only Dizunī Channeru spin-off series to be broadcast in 4K definition for the entire length of the show. Reruns of the series..."
                embed = discord.Embed(color=0x00ff00)
                embed.set_image(url="http://i0.kym-cdn.com/photos/images/facebook/000/891/042/9bd.jpg")
                embed.add_field(name='Title', value="Cory in the House", inline=True)
                embed.add_field(name='Rating', value="9.69", inline=True)
                embed.add_field(name='Status', value="Finished", inline=True)
                embed.add_field(name='Episodes', value="34", inline=True)
                embed.add_field(name='Synopsis', value=syn, inline=False)
                await ctx.send("", embed = embed)
                return
            sess = XMLSession()
            query = ctx.message.content.partition(' ')[2]
            query = query.replace(' ', '+')
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

            try:
                img = item['image']['$']
                english = '({})'.format(item['english']['$']) if '$' in item['english'] else ''
                title = "{} {}".format(item['title']['$'], english)
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
            except Exception as e:
                await ctx.send("Sorry, something's fucky with this anime. \n <@99073784803229696>:\n```\n{}\n```".format(e))

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



