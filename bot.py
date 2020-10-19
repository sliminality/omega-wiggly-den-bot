import discord
import os
import Dens
from discord.ext import commands

TOKEN = os.environ["omega-wiggly-bot-token"]
bot = commands.Bot(command_prefix="%")


@bot.event
async def on_ready():
    print("Bot is online and ready!")


@bot.command()
async def den(ctx, denNum, version, denType="reg"):
    if version == "sw" and denType == "reg":
        await ctx.send(Dens.swordReg[int(denNum)])
    elif version == "sw" and denType == "baby":
        await ctx.send(Dens.swordBaby[int(denNum)])
    elif version == "sh" and denType == "reg":
        await ctx.send(Dens.shieldReg[int(denNum)])
    elif version == "sh" and denType == "baby":
        await ctx.send(Dens.shieldBaby[int(denNum)])
    else:
        await ctx.send("Wow, don't even know how to use your own bot? smhmhmhmh")


bot.run(TOKEN)