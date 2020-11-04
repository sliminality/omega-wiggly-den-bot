import json
import os
import re


def create_den_lists(sword_data, shield_data, emoji_names):
    """Parses dens from JSON and returns emoji mappings."""

    sword = parse_json_dens(sword_data, emoji_names)
    shield = parse_json_dens(shield_data, emoji_names)

    # Write to disk.
    try:
        os.remove("Dens.py")
    except Exception:
        pass

    with open("Dens.py", "a") as f:
        sword_adult_dens = format_den_list(sword["adult"])
        sword_baby_dens = format_den_list(sword["baby"])
        shield_adult_dens = format_den_list(shield["adult"])
        shield_baby_dens = format_den_list(shield["baby"])

        f.write(f"swordReg = {sword_adult_dens}\n\n")
        f.write(f"swordBaby = {sword_baby_dens}\n\n")
        f.write(f"swordReg = {shield_adult_dens}\n\n")
        f.write(f"swordBaby = {shield_baby_dens}\n\n")

        print("Done writing Dens.py")


def format_den_list(dens):
    """Formats a set of dens as a stringified dictionary."""
    entry_dict = {}

    for i, den in enumerate(dens):
        entry_dict[i + 1] = " ".join(den)

    return str(entry_dict)


def parse_json_dens(nest, emoji_names):
    """Parses a den's contents from JSON and returns its species (baby, adult)."""
    with open(nest, "r") as f:
        data = json.load(f)
        baby = [filter_den(den["Entries"], emoji_names, baby=True) for den in data]
        adult = [filter_den(den["Entries"], emoji_names, baby=False) for den in data]

        return { "baby": baby, "adult": adult }


def is_baby(entry):
    """Returns true if a mon appears at the 1- or 2-star level."""
    probabilities = entry["Probabilities"]
    return probabilities[0] > 0 or probabilities[1] > 0


def is_adult(entry):
    """Returns true if a mon appears at the 3-, 4-, or 5-star level."""
    probabilities = entry["Probabilities"]
    return probabilities[2] > 0 \
        or probabilities[3] > 0 \
        or probabilities[4] > 0


def filter_den(den, emoji_names, baby):
    """Filters and formats a den's entries by baby vs. adult."""
    pred = is_baby if baby else is_adult
    formatted = [format_entry(mon, emoji_names) for mon in den if pred(mon)]
    return list(set(formatted)) # Uniquify.


def format_entry(entry, emoji_names):
    """Extracts information about an encounter's species, form, gender."""
    species = entry["Species"]
    gender = None
    if "Gender" in entry:
        gender = "m" if entry["Gender"] == 1 else \
                 "f" if entry["Gender"] == 2 else None
    alt_form = entry["AltForm"] if "AltForm" in entry else None
    gmax = "IsGigantamax" in entry

    prefix = get_emoji_prefix(species, alt_form, gender, gmax)
    return emoji_names[prefix]


def get_emoji_prefix(species_name, alt_form=None, gender=None, gmax=None):
    """Returns the emoji prefix for a given mon."""

    # Handle species names.
    if species_name == "Jangmo-o":
        species = "jangmoo"
    elif species_name == "Kommo-o":
        species = "kommoo"
    elif species_name == "Hakamo-o":
        species = "hakamoo"
    elif species_name == "Farfetch’d":
        species = "farfetchd"
    elif species_name == "Sirfetch’d":
        species = "sirfetchd"
    elif species_name == "Nidoran♀":
        species = "nidoran_f"
    elif species_name == "Nidoran♂":
        species = "nidoran_m"
    elif species_name == "Mr. Mime":
        species = "mrmime"
    elif species_name == "Mr. Rime":
        species = "mrrime"
    elif species_name == "Mime Jr.":
        species = "mimejr"
    else:
        species = species_name.lower()

    # Handle form modifiers.
    forms = {
        "shellos": ("west", "east"),
        "gastrodon": ("west", "east"),
        "pumpkaboo": ("avg", "small", "large", "super"),
        "gourgeist": ("avg", "small", "large", "super"),
        "rotom": (None, "heat", "frost", "wash", "fan", "mow"),
        "rockruff": (None, None), # Own Tempo uses the same sprite.
        "lycanroc": ("midday", "midnight", "dusk"),
        # Regional forms.
        "meowth": (None, "a", "g"),
        "yamask": (None, "g"),
        "stunfisk": (None, "g"),
        "darumaka": (None, "g"),
        "darmanitan": (None, "zen", "g", "g_zen"),
        "weezing": (None, "g"),
        "zigzagoon": (None, "g"),
        "linoone": (None, "g"),
        "slowpoke": (None, "g"),
        "slowbro": (None, "g"),
        "slowking": (None, "g"),
        "corsola": (None, "g"),
        "ponyta": (None, "g"),
        "rapidash": (None, "g"),
        "farfetchd": (None, "g"),
        "mrmime": (None, "g"),
        # Version exclusives.
        "basculin": ("blue", "red"),
        "toxtricity": ("amp", "low"),
        "indeedee": ("m", "f"),
        "meowstic": ("m", "f"),
        # Other.
        "unfezant": ("m",), # There is no ungendered emoji.
        "hippopotas": ("m",),
        "hippowdon": ("m",),
        "alcremie": ("strawberry",),
    }

    result = species

    # Gigantamax sprites ignore other forms.
    if gmax == True:
        # WHY
        if species == "flapple" or species == "appletun":
            result = "flappletun_gm"
        else:
            result = f"{result}_gm"
    elif species in forms:
        # Handle other forms.
        index = 0 if alt_form is None else alt_form
        modifier = forms[species][index]

        if modifier is not None:
            result = f"{result}_{modifier}"

    return result


def build_emoji_names(path):
    """Returns a dictionary mapping emoji prefix to full identifier."""
    entries = {}

    # Load list of names.
    with open(path, "r") as f:
        for emoji in f:
            get_prefix = re.compile("<:s_([a-z_0-9]+):\d+>")
            prefix = get_prefix.match(emoji)

            if prefix is not None and prefix.group(1) is not None:
                entries[prefix.group(1)] = emoji.strip()
            else:
                print("Failed:", emoji)

    return entries


if __name__ == "__main__":
    emojis = build_emoji_names(os.path.join("Emoji-Retrieval", "emoji_names.txt"))

    sword_data = os.path.join("data", "sword-nests.json")
    shield_data = os.path.join("data", "shield-nests.json")

    create_den_lists(sword_data, shield_data, emojis)
