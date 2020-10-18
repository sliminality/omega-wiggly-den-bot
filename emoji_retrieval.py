import discord
import os
from discord.ext import commands

TOKEN = os.environ["omega-wiggly-bot-token"]
bot = commands.Bot(command_prefix="%")

emoteChannelID = 767479616528056380


@bot.event
async def on_ready():
    print("Bot is online and ready!")


@bot.command()
async def getEmotes(ctx):
    emoteChannel = bot.get_channel(emoteChannelID)

    with open("Shines-EX-Emotes.txt", "w") as f:
        async for message in emoteChannel.history():
            f.write(message.content)


bot.run(TOKEN)