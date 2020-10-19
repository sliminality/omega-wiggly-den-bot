import discord
import os
from discord.ext import commands

TOKEN = os.environ["omega-wiggly-bot-token"]
bot = commands.Bot(command_prefix="%")

emoteChannelID1 = 706432315349401670
emoteChannelID2 = 714532044083953737


@bot.event
async def on_ready():
    print("Bot is online and ready!")


@bot.command()
async def getEmotes(ctx):
    emoteChannel1 = bot.get_channel(emoteChannelID1)
    # emoteChannel2 = bot.get_channel(emoteChannelID2)

    with open("Emoji-Retrieval\\raw_emoji_names.txt", "a") as f:
        async for message in emoteChannel1.history():
            f.write(message.content)


bot.run(TOKEN)