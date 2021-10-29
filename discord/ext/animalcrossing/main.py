from discord.ext import commands
from discord import Member
from discord import abc
import pickle

fossilFile = "animalcrossing/fossil.pickle"
diyFile = "animalcrossing/diy.pickle"
kkFile = "animalcrossing/kk.pickle"
wishFile = "animalcrossing/wish.pickle"

try:
    fossilData = pickle.load(open(fossilFile, "rb"))
except:
    fossilData = {}
    print("Fossil file missing or corrupted.")

try:
    diyData = pickle.load(open(diyFile, "rb"))
except:
    diyData = {}
    print("DIY file missing or corrupted.")

try:
    kkData = pickle.load(open(kkFile, "rb"))
except:
    kkData = {}
    print("KK file missing or corrupted.")

try:
    wishData = pickle.load(open(wishFile, "rb"))
except:
    wishData = {}
    print("Wishlist file missing or corrupted.")

def check_category(cat):
    if cat in ['fossil', 'f']:
        return (True, fossilData, fossilFile, "fossil")
    elif cat in ['diy', 'd']:
        return (True, diyData, diyFile, "DIY")
    elif cat in ['kk', 'music', 'm']:
        return (True, kkData, kkFile, "music")
    elif cat in ['wishlist', 'wish', 'w']:
        return (True, wishData, wishFile, "wish")
    else:
        return (False, '', '')

class AnimalCrossing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # possible commands:
    # fossil: no args, shows all fossils available. w/args, adds fossils
    # diy: same as fossil but with diy
    # turnips: predict turnip prices

    @commands.command()
    async def clear(self, ctx, cat: str):
        user = ctx.author.name + '#' + ctx.author.discriminator
        c = check_category(cat)
        data = c[1]
        datafile = c[2]
        cname = c[3]
        try:
            data[user] = []
            pickle.dump(data, open(datafile, "wb"))
            await ctx.send("`{}` list has been cleared.".format(cname))
        except Exception as e:
            await ctx.send("Error clearing your `{}` category.\n\n```{}```".format(cname, e))

    async def show_list(self, ctx, user, category):
        cat = check_category(category)
        c_data = cat[1]
        c_file = cat[2]
        c_name = cat[3]
        message = ""
        if not user:
            user_list = c_data
        else:
            if str(user) in c_data:
                user_list = [str(user)]
            else:
                await ctx.send("`{}` hasn't added any `{}`.".format(user, c_name))
                return

        if isinstance(ctx.message.channel, abc.PrivateChannel):
            members = [ctx.author.name + '#' + ctx.author.discriminator]
        else:
            members = [m.name + '#' + m.discriminator for m in ctx.message.author.guild.members]

        for u in user_list:
            if u not in members:
                continue
            message += "{}:\n```".format(u)
            for thing in sorted(c_data[u]):
                message += "- {}\n".format(thing)
            message = message[:-1] + "```\n"
        
        try:
            await ctx.send(message)
        except:
            await ctx.send("Looks like the {} list is empty.".format(c_name))
        return

    @commands.command()
    async def fossil(self, ctx, user: Member = None):
        await self.show_list(ctx, user, "fossil")

    @commands.command()
    async def diy(self, ctx, user: Member = None):
        await self.show_list(ctx, user, "diy")

    @commands.command()
    async def music(self, ctx, user: Member = None):
        await self.show_list(ctx, user, "music")

    @commands.command()
    async def wishlist(self, ctx, user: Member = None):
        await self.show_list(ctx, user, "wishlist")

    @commands.command(aliases=['a', '+'])
    async def add(self, ctx, cat: str, *, item: str):
        """add to your ACNH list"""
        c = check_category(cat)
        if not c[0]:
            await ctx.send("`{}` isn't a category you can add things to.".format(cat))
            return
        else:
            data = c[1]
            datafile = c[2]
            cat = c[3]
        user = ctx.author.name + "#" + ctx.author.discriminator
        if user not in data:
            data[user] = []
        
        things = [x.strip() for x in item.split(',')]
        mesg = ""
        for thing in things:
            data[user].append(thing.title())
            mesg += "`{}` was added to your {} list.\n".format(thing.title(), cat)
        await ctx.send(mesg)
        pickle.dump(data, open(datafile, "wb"))

    @commands.command(aliases=['rm', 'r', '-'])
    async def remove(self, ctx, cat: str, *, item: str):
        """remove from your ACNH list"""
        c = check_category(cat)
        if not c[0]:
            await ctx.send("`{}` isn't a category you can add things to.".format(cat))
            return
        else:
            data = c[1]
            datafile = c[2]
            cat = c[3]
        
        user = ctx.author.name + "#" + ctx.author.discriminator
        if user not in data:
            await ctx.send("You haven't added anything to your {} list.".format(cat))
        else:
            things = [x.strip() for x in item.split(',')]
            success = ""
            failure = ""
            for thing in things:
                try:
                    data[user].remove(thing.title())
                    success += "`{}` was removed from your {} list.\n".format(thing.title(), cat)
                except:
                    failure += "You don't have a `{}` in your {} list.\n".format(thing.title(), cat)
            try:
                await ctx.send(success)
            except:
                pass
            try:
                await ctx.send(failure)
            except:
                pass
        pickle.dump(data, open(datafile, "wb"))

    @commands.command(aliases=['s', '?'])
    async def search(self, ctx, *, item: str):
        """search for an item in ACNH lists"""
        has = {}
        for data in [fossilData, diyData]:
            for user in data:
                for i in set(data[user]):
                    if item.lower() in i.lower():
                        if user not in has:
                            has[user] = []
                        has[user].append(i.title())
        if has:
            message = ""
            members = [m.name + '#' + m.discriminator for m in ctx.message.author.guild.members]
            for u in has:
                if u not in members:
                    continue
                message += "{}:\n```".format(u)
                for item in sorted(has[u]):
                    message += "- {}\n".format(item)
                message = message[:-1] + "```\n"
            await ctx.send(message)
        else:
            await ctx.send("Nobody has anything *close* to a `{}`. Are you sure it exists?".format(item.title()))


def setup(bot):
    bot.add_cog(AnimalCrossing(bot))