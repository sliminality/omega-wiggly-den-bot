import re

emojiRe = re.compile(r"<:\w*:\d*>")

with open("raw-Shinies-1-emotes.txt", "r") as f:
    text = f.read()

emojiTextList = re.findall(emojiRe, text)

with open("Shinies-1-emotes.txt", "w") as g:
    for emojiName in emojiTextList:
        g.write(emojiName + "\n")
