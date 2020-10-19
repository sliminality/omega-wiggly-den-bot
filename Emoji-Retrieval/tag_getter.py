import re


def getDiscordTags():
    with open("Emoji-Retrieval\\emoji_names.txt", "r") as f:
        lines = f.readlines()

    tagRegex = re.compile(r"<:s_([a-zA-Z\d]*)(_\w*)*:\d*>")

    with open("taggedNames.txt", "a") as f:
        for line in lines:
            match = re.search(tagRegex, line)
            if match is not None:
                pokemonName = match.group(1)
                if (tags := match.group(2)) is not None:
                    f.write(f"{pokemonName} has tag(s): {tags}\n")


def getDataminedTags():
    for version in ("sword", "shield"):
        with open(f"{version}DensDatamined.txt", "r") as f:
            denFile = f.read()

        denList = denFile.split("\n\t\n\n")
        pokemonInfoRe = re.compile(r"(\d)-Star (\w*\s?\w*['-]*\w*['-]*\d*)\n")

        denNum = 0
        for den in denList:
            denNum += 1
            for pokemonMatch in re.finditer(pokemonInfoRe, den):
                starLevel = pokemonMatch.group(1)
                pokeName = pokemonMatch.group(2)

                tagRegex = re.compile(r"(Gigantamax|-\d)")

                with open("dataminedTags.txt", "a") as f:
                    if (match := re.search(tagRegex, pokeName)) is not None:
                        tag = match.group(1)
                        if starLevel in ("1", "2"):
                            f.write(
                                f"{pokeName} in Baby Den {denNum} v. {version} has tag: {tag}\n"
                            )
                        else:
                            f.write(
                                f"{pokeName} in Regular Den {denNum} v. {version} has tag: {tag}\n"
                            )
