from discord.ext import commands
from discord import Embed as Embed
import sqlite3

class WYR(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_con = sqlite3.connect('ext/wyr/wyrdb')
        self.db_cur = self.db_con.cursor()

    def get_prompts(self,ctx):
        channel_id = str(ctx.channel.id)
        return self.db_cur.execute('''SELECT id,prompt,sfw
                               FROM ?
                               ORDER BY tally, random()
                               LIMIT 2;'''
                               , [channel_id]
                            )
    def get_prompts_sfw(self):
        return self.db_cur.execute('''SELECT id,prompt,sfw
                               FROM prompts
                               WHERE sfw = 1
                               ORDER BY tally, random()
                               LIMIT 2;'''
                            )

    def insert_prompt(self, prompt, sfw):
        self.db_cur.execute('''INSERT INTO prompts
                               (prompt, sfw)
                               VALUES (?, ?);'''
                               , [prompt, sfw]
                            )
        self.db_con.commit()

    def remove_prompt(self, id):
        self.db_cur.execute('''DELETE FROM prompts
                               WHERE id = ?;'''
                               , [id]
                            )
        self.db_con.commit()

    def update_tally(self, id):
        self.db_cur.execute('''UPDATE prompts
                               SET tally = tally + 1
                               WHERE id = ?;'''
                            , [id]
                            )
        self.db_con.commit()
    
    def reset_tally(self):
        self.db_cur.execute('''UPDATE prompts
                               SET tally = 0;'''
                           )
        self.db_con.commit()

    async def send_embed(self, ctx, one, two):
        embed=Embed(title="Would you rather...", color=0xe135f8)
        embed.add_field(name="1️⃣", value=one[1], inline=True)
        embed.add_field(name="\u200b", value="-OR-", inline=True)
        embed.add_field(name="2️⃣", value=two[1], inline=True)
        embed.set_footer(text="[#{} & #{}]".format(one[0],two[0]))
        return await ctx.send(embed=embed)

    @commands.command()
    async def wyr(self, ctx, *arg):
        """'wyr' for all prompts, 'wyr sfw' for sfw only"""
        prompts = []
        if arg == 'sfw':
            prompts = self.get_prompts_sfw().fetchall()
        else:
            prompts = self.get_prompts(ctx).fetchall()
        
        #msg =  "__**Which would you rather do?**__\n"
        #msg += "> - {}\n".format(prompts[0][1])
        #msg += "> - {}".format(prompts[1][1])

        wyrmsg = await self.send_embed(ctx, prompts[0], prompts[1])
        await wyrmsg.add_reaction(emoji='1️⃣')
        await wyrmsg.add_reaction(emoji='2️⃣')

        self.update_tally(prompts[0][0])
        self.update_tally(prompts[1][0])

    @commands.command()
    async def iwr(self, ctx, prompt, is_sfw):
        """iwr "new prompt" <sfw/nsfw>"""
        is_sfw = 1 if is_sfw == 'sfw' else 0
        try:
            self.insert_prompt(prompt, is_sfw)
            await ctx.send("Prompt \"{}\" input successfully.".format(prompt))
        except Exception as e:
            await ctx.send("There was an issue saving your prompt \"{}\".".format(prompt))
            print(e)

    @commands.command(hidden=True)
    @commands.check_any(commands.is_owner())
    async def iwrn(self, ctx, id):
        """iwrn <id> | owner only"""
        try:
            self.remove_prompt(id)
            await ctx.send("Prompt #{} removed successfully.".format(id))
        except Exception as e:
            await ctx.send("ERROR: problem removing prompt #{}.".format(id))
            print(e)

    
    @commands.command(aliases=['wyrrt'], hidden=True)
    @commands.check_any(commands.is_owner())
    async def wyr_reset_tally(self, ctx):
        """resets the tally | owner only"""
        self.reset_tally()
        await ctx.send("Tallies for prompts cleared.")

def setup(bot):
    bot.add_cog(WYR(bot))



