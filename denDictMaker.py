import os
import re

def getEmojiPre(pokemon_name, version):
    alternateFormPokemon = {
        "Shellos-1": "shellos_east",
        "Gastrodon-1": "gastrodon_east",
        "Pumpkaboo": "pumpkaboo_small",
        "Pumpkaboo-1": "pumpkaboo_avg",
        "Pumpkaboo-2": "pumpkaboo_large",
        "Pumpkaboo-3": "pumpkaboo_super",
        "Gourgeist": "gourgeist_small",
        "Gourgeist-1": "gourgeist_avg",
        "Gourgeist-2": "gourgeist_large",
        "Gourgeist-3": "gourgeist",
        "Rotom-1": "rotom_mow",
        "Rotom-2": "rotom_fan",
        "Rotom-3": "rotom_wash",
        "Rotom-4": "rotom_frost",
        "Rotom-5": "rotom_heat",
        "Rockruff-1": "rockruff",
        "Lycanroc": "lycanroc_midday",
        "Lycanroc-1": "lycanroc_midnight",
        "Lycanroc-2": "lycanroc_dusk",
    }
    galarianPokemon = [
        "Meowth-2",
        "Yamask-1",
        "Stunfisk-1",
        "Darumaka-1",
        "Darmanitan-2",
        "Weezing-1",
        "Zigzagoon-1",
        "Linoone-1",
        "Slowpoke-1",
        "Corsola-1",
        "Ponyta-1",
        "Rapidash-1",
        "Slowbro-1",
    ]
    gigantamaxPokemon = [
        "Gigantamax Charizard",
        "Gigantamax Drednaw",
        "Gigantamax Flapple",
        "Gigantamax Appletun",
        "Gigantamax Centiskorch",
        "Gigantamax Machamp",
        "Gigantamax Alcremie",
        "Gigantamax Coalossal",
        "Gigantamax Duraludon",
        "Gigantamax Duraludon",
        "Gigantamax Copperajah",
        "Gigantamax Garbodor",
        "Gigantamax Hatterene",
        "Gigantamax Grimmsnarl",
        "Gigantamax Corviknight",
        "Gigantamax Butterfree",
        "Gigantamax Kingler",
        "Gigantamax Orbeetle",
        "Gigantamax Sandaconda",
        "Gigantamax Venusaur",
        "Gigantamax Blastoise",
        "Gigantamax Eevee",
        "Gigantamax Pikachu",
        "Gigantamax Snorlax",
        "Gigantamax Lapras",
        "Gigantamax Gengar",
        "Gigantamax Meowth",
        "Gigantamax Cinderace",
        "Gigantamax Inteleon",
        "Gigantamax Rillaboom",
    ]
    oddNames = {
        "Mr. Rime": "mrrime",
        "Mr. Mime-1": "mrmime_g",
        "Mr. Mime": "mrmime",
        "Sirfetch'd": "sirfetchd",
        "Jangmo-o": "jangmoo",
        "Hakamo-o": "hakamoo",
        "Kommo-o": "kommoo",
        "Farfetch'd-1": "farfetchd_g",
    }
    exclusivePokemonSW = {
        "Indeedee": "indeedee_m",
        "Meowstic": "meowstic_m",
        "Basculin": "basculin_blue",
    }
    exclusivePokemonSH = {
        "Indeedee-1": "indeedee_f",
        "Meowstic-1": "meowstic_f",
        "Basculin-1": "basculin_red",
    }
    other = {
        "Toxtricity": "toxtricity_amp",
        "Unfezant": "unfezant_m",
        "Hippopotas": "hippopotas_m",
        "Hippowdon": "hippowdon_m",
        "Alcremie": "alcremie_strawberry",
    }

    if pokemon_name in alternateFormPokemon:
        return alternateFormPokemon[pokemon_name]
    elif pokemon_name in galarianPokemon:
        pokemon_name = pokemon_name[:-2].lower()
        return f"{pokemon_name}_g"
    elif pokemon_name in gigantamaxPokemon:
        pokemon_name = pokemon_name.split()[1].lower()
        if pokemon_name == "flapple" or pokemon_name == "appletun":
            pokemon_name = "flappletun"
        return f"{pokemon_name}_gm"
    elif pokemon_name in oddNames:
        return oddNames[pokemon_name]
    elif version == "sword" and pokemon_name in exclusivePokemonSW:
        return exclusivePokemonSW[pokemon_name]
    elif version == "shield" and pokemon_name in exclusivePokemonSH:
        return exclusivePokemonSH[pokemon_name]
    elif pokemon_name in other:
        return other[pokemon_name]
    else:
        return pokemon_name.lower()


def getEmojiString(pokemon_name, version):
    # print(f"Currently working on: {pokemon_name}")
    regexName = getEmojiPre(pokemon_name, version)
    emoteRegex = re.compile(fr"<a?:s_{regexName}:\d*>")

    emojiNames = os.path.join("Emoji-Retrieval", "emoji_names.txt")

    with open(emojiNames, "r") as f:
        emojiNamesText = f.read()

    match = re.search(emoteRegex, emojiNamesText)
    finalString = match.group(0)

    return finalString


def createDenLists():
    for version in ("sword", "shield"):
        with open(f"{version}DensDatamined.txt", "r") as f:
            denFile = f.read()

        denList = denFile.split("\n\t\n\n")
        pokemonInfoRe = re.compile(r"(\d)-Star (\w*.?\s?\w*['-]*\w*['-]*\d*)\n")

        denNum = 0
        babyPokemon = {}
        regPokemon = {}
        for den in denList:
            denNum += 1
            babyMons = []
            regularMons = []
            babyDenEmojiString = ""
            regDenEmojiString = ""

            for pokemonMatch in re.finditer(pokemonInfoRe, den):
                starLevel = pokemonMatch.group(1)
                pokeName = pokemonMatch.group(2)
                emojiString = getEmojiString(pokeName, version)

                if starLevel in ("1", "2"):
                    if pokeName not in babyMons:
                        babyMons.append(pokeName)
                        babyDenEmojiString += f"{emojiString} "
                else:
                    if pokeName not in regularMons:
                        regularMons.append(pokeName)
                        regDenEmojiString += f"{emojiString} "

            babyDenEmojiString = f"{babyDenEmojiString.strip()}"

            if denNum in (94, 95, 96):
                regDenEmojiString = "<:s_skwovet:706229777547132988>"
            else:
                regDenEmojiString = f"{regDenEmojiString.strip()}"

            babyPokemon[denNum] = babyDenEmojiString
            regPokemon[denNum] = regDenEmojiString

        with open(f"Dens.py", "a") as f:
            f.write(f"{version}Reg = {str(regPokemon)}\n\n")
            f.write(f"{version}Baby = {str(babyPokemon)}\n\n")

    print("Finished!")


createDenLists()