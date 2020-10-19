import re

emojiRe = re.compile(r"<:\w*:\d*>")

with open("Emoji-Retrieval\\raw_emoji_names.txt", "r") as f:
    text = f.read()

emojiTextList = re.findall(emojiRe, text)

with open("emoji_names.txt", "w") as g:
    for emojiName in emojiTextList:
        g.write(emojiName + "\n")
