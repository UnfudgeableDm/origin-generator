import streamlit as st
import pandas as pd
import random

# === CUSTOM STREAMLIT STYLING ===
st.set_page_config(page_title="Origin Generator", layout="wide", initial_sidebar_state="auto")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .st-emotion-cache-18ni7ap {display: none;}
    </style>
""", unsafe_allow_html=True)

# Font Color
st.markdown("""
    <style>
    body, div, span, p, td, th {
        color: #FFFCDB !important;
    }
    </style>
""", unsafe_allow_html=True)

# Sample input UI
plate_options = ["Plate 0", "Plate 1", "Plate 2", "Plate 3", "Plate 4", "Plate 5", "Plate 6"]
district_options = ["Azure", "Amethyst", "Ruby", "Citrine", "Rhodonite", "Amber", "Jade", "Obsidian"]
faction_options = ["Paragons", "Optimists", "Gilded Gaze", "Transneuroclasts", "Chronomancers", "New Faith", "Unpinned"]

selected_plate = st.selectbox("Select Plate", plate_options)
selected_district = st.selectbox("Select District", district_options)
selected_faction = st.selectbox("Select Faction", faction_options)

# Deterministic random seed based on user input
seed_input = f"{selected_plate}_{selected_district}_{selected_faction}"
random.seed(seed_input)

faction_options = [
    "Paragons", "Optimists", "Gilded Gaze", "Transneuroclasts",
    "Chronomancers", "New Faith", "Unpinned"
]


# Stat abbreviation to full name mapping
stat_full_names = {
    "STR": "Strength",
    "DEX": "Dexterity",
    "CON": "Constitution",
    "INT": "Intelligence",
    "WIS": "Wisdom",
    "CHA": "Charisma"
}

# Standard D&D stat order
standard_stat_order = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]


# ===============================
# RIBBON ITEM DATA AND EQUIPMENT COSTS
# ===============================

# Ribbon items by background
background_ribbons = {
    "Acolyte": ["Book (prayers)", "Robe", "10x Parchment", "Bedroll", "Tinderbox", "10x Candles", "Amulet", "Holy Water", "Antitoxin"],
    "Artisan": ["Flask of Whiskey", "Chisel", "Air Dry Porcelain Clay (1 lb)", "Fancy Bell", "Ball Bearings", "2x Pouch", "Lamp, Oil", "Charcoal, 2x Parchment", "Whetstone", "Leather Apron"],
    "Attendant": ["Set of 10x Teas", "Polite Bell, Marble Cloche", "Flask, Fancy Hat", "50x Needle, Thread", "Iron Spikes", "Hourglass, Enchanted Mood Ring", "Lace Gloves", "Clipboard, Engraved Pen", "Serving Towel, Bedroll", "Backpack"],
    "Charlatan": ["Costume, Sandals", "Grappling Hook", "Iron Spikes", "Pole", "50x Needle, Thread", "String (100 ft)", "Two-Sided Coin", "Trick Card Deck", "Three Trick Cups, Three Trick Balls", "Bedroll, Nutcracker"],
    "Criminal": ["2x Pouches", "Traveler's Clothes", "Crowbar", "Caltrops", "Rope (25 feet)", "Block and Tackle", "Grappling Hook", "Lock, Ceramic Mask", "10x Rations", "10 Extra Gold"],
    "Enforcer": ["Traveler's Clothes", "String (100 ft)", "Manacles", "Crowbar", "Ball Bearings", "Lamp, Oil", "Block and Tackle", "Healer's Kit", "Book (of Policy)", "Heavy Duty Boots"],
    "Elite": ["30 Extra Gold", "Silk Gloves", "Perfume, Ivory Pipe", "Family Heirloom", "Caltrops", "2x Aged Wine", "Dulcimer", "Letter from a Senator", "Parrot (trained)", "Very Loud Whistle"],
    "Executor": ["Writ of Execution", "Lamp, Oil", "Tinderbox", "Book (of Regulations)", "Net", "Pole, Gloves", "Robe", "Chains (10 feet)", "Credentials (for your Plate and District)", "Snuffbox, Notepad"],
    "Laborer": ["Hand Trowel", "Knee Pads", "Lamp, Oil", "Block and Tackle", "Flask", "Shovel", "Bedroll", "Heavy Duty Gloves", "20x Nails in a Bag", "Flint and Steel"],
    "Merchant": ["Abacus", "2x Pouch", "50x Needle, Thread", "5x Cheese", "Basket, Jug", "Ledger, Bell", "10x Candles", "Sample Swatch Set", "Antitoxin", "2x Dagger"],
    "Rebel": ["Two Silver'd Arrows", "Crowbar", "Signal Whistle", "Blanket", "Tent", "Caltrops", "Backpack", "Hunting Trap", "Healer's Kit", "Ball Bearings"],
    "Professor": ["Reading Glasses", "Book (Academic)", "Ink Pen", "10x Candles", "Paper x10", "Antitoxin", "Fanny Pack and Lecture Pointer (extendable)", "Embroidered Sash", "Book (That you wrote)", "Spork, Steak Knife"],
    "Researcher": ["Tuning Fork", "Jar of Bees", "Iron Spikes", "Lamp, Oil", "Backpack", "Tinderbox", "2x Pouch", "Scroll of Friends", "Rubbing Charcoal + 2x Paper", "Journal"],
    "Engineer": ["Goggles", "Caliper Tool", "2x Pouch", "3x Jugs", "Lamp, Oil", "Ball Bearings", "Block and Tackle", "Copper Wire (25 ft)", "Kite", "Flint and Steel"],
    "Recluse": ["Mortar and Pestle", "Healer's Kit", "Pole", "Basket of Dried Beans", "10x Candles", "Flask", "Bedroll", "Antitoxin", "Fine Tweezers", "Caltrops"],
    "Entertainer": ["Fake Dagger", "Backpack", "Rope (25 feet)", "Common Wine", "2x Poles", "Pan Flute", "Playing Cards, Tablecloth", "2x Costume", "Wig, Cape", "Hand Mirror, Perfume"]
}

# Rare ribbon item alternates (50/50 appearance)
rare_item_pairs = {
    "Flask of Whiskey": "24x Small Magnets",
    "Fancy Bell": "50x Small Business Cards",
    "Nutcracker": "2x Bedroll",
    "Parrot (trained)": "District Gem Earrings",
    "Very Loud Whistle": "District Gem Clothing",
    "5x Cheese": "Manacles",
    "Two Silver’d Arrows": "Scroll of Guidance",
    "Spork, Steak Knife": "Rare Stamp Collection",
    "Jar of Bees": "Jar of Honey",
    "Your Plate Travel Encyclopedia": "Your Plate Slangbook",
    "3x Jugs": "Your Faction Handbook",
    "Kite": "Wrench, Screwdriver",
    "Wig, Cape": "Portable Podium"
}


tool_costs = {
    "Alchemist's Supplies": 35,
    "Brewer's Supplies": 20,
    "Calligrapher's Supplies": 10,
    "Carpenter's Tools": 8,
    "Cartographer's Tools": 15,
    "Cobbler's Tools": 5,
    "Cook's Utensils": 1,
    "Disguise Kit": 25,
    "Forgery Kit": 15,
    "Gaming Set": 1,
    "Glassblower's Tools": 30,
    "Herbalism Kit": 5,
    "Jeweler's Tools": 25,
    "Leatherworker's Tools": 5,
    "Mason's Tools": 10,
    "Musical Instrument": 17,
    "Navigator's Tools": 25,
    "Painter's Supplies": 10,
    "Poisoner's Kit": 35,
    "Smith's Tools": 20,
    "Thieves' Tools": 25,
    "Tinkerer's Tools": 35,
    "Tinker's Tools": 35,
    "Weaver's Tools": 1,
    "Woodcarver's Tools": 1
}

weapon_costs = {
    "Dagger": 3,
    "Dagger x2": 5,
    "Dart x4": 3,
    "Shortbow, 20 Arrows, Quiver": 28,
    "Light Crossbow, 20 Bolts, Quiver": 28,
    "Quarterstaff": 0.4,
    "Mace, Shield": 13,
    "Handaxe": 5,
    "Spear": 2,
    "Greatclub": 0.6,
    "Sling, 20 Bullets, Pouch": 0.5,
    "Club": 0.3,
    "Light Hammer": 3,
    "Sickle": 1
}

ribbon_costs = {
    "2x Aged Wine": 20,
    "2x Costume": 10,
    "2x Dagger": 4,
    "2x Poles": 1,
    "2x Pouch": 1,
    "3x Jugs": 0.6,
    "5x Cheese": 0.5,
    "10 Extra Gold": 5,
    "10x Candles": 0.1,
    "10x Rations": 5,
    "20x Nails in a Bag": 1,
    "30 extra gold": 15,
    "50 x Needle, Thread": 2,
    "Abacus": 2,
    "Air Dry Porcelain Clay (1 lb)": 2,
    "Amulet": 5,
    "Backpack": 2,
    "Ball Bearings": 1,
    "Basket, Jug": 0.6,
    "Basket of Dried Beans": 0.9,
    "Bedroll": 1,
    "Block and Tackle": 1,
    "Book (Academic)": 8,
    "Book (of Policy)": 8,
    "Book (of Regulations)": 8,
    "Book (that you wrote)": 8,
    "Book(prayers)": 8,
    "Caliper Tool": 1,
    "Caltrops": 5,
    "Chains (10 feet)": 5,
    "Charcoal, 2x Parchment": 0.4,
    "Chisel": 0.1,
    "Clipboard, Engraved Pen": 0.5,
    "Common Wine": 0.2,
    "Copper Wire (25 ft)": 0.2,
    "Costume, Sandals": 0.5,
    "Credentials (for your Plate and District)": 10,
    "Crowbar": 2,
    "Dulcimer": 20,
    "Embroidered Sash": 1,
    "Fake Dagger": 1,
    "Family Heirloom": 5,
    "Fancy Bell": 1.5,
    "Fanny Pack and Lecture Pointer (extendable)": 1.8,
    "Fine Tweezers": 0.05,
    "Flask": 0.02,
    "Flask of Whiskey": 0.2,
    "Flint and Steel": 0.1,
    "Goggles": 0.2,
    "Grappling Hook": 2,
    "Hand Mirror, Perfume": 8,
    "Hand Trowel": 0.08,
    "Healer's Kit": 5,
    "Heavy Duty Boots": 1,
    "Heavy Duty Gloves": 1,
    "Holy Water": 5,
    "Hourglass, Enchanted Mood Ring": 5,
    "Hunting Trap": 5,
    "Ink Pen": 0.02,
    "Iron Spikes": 1,
    "Jar of Bees": 0.5,
    "Journal": 18,
    "Kite": 0.5,
    "Knee Pads": 1,
    "Lace Gloves": 2,
    "Lamp, Oil": 0.6,
    "Ledger, Bell": 1.5,
    "Letter from a Senator": 20,
    "Lock, Ceramic Mask": 10,
    "Manacles": 2,
    "Mortar and Pestle": 0.5,
    "Net": 1,
    "Pan Flute": 8,
    "Parrot (trained)": 8,
    "Paper x10": 1,
    "Perfume, Ivory Pipe": 5,
    "Playing Cards, Tablecloth": 0.7,
    "Pole": 0.5,
    "Pole, Gloves": 0.7,
    "Polite Bell, Marble Cloche": 2,
    "Reading Glasses": 1,
    "Robe": 1,
    "Rope (25 feet)": 1,
    "Rubbing Charcoal + 2x Paper": 0.4,
    "Sample Swatch Set": 1,
    "Serving Towel, Bedroll": 1,
    "Set of 10x Teas": 2,
    "Shovel": 2,
    "Signal Whistle": 0.5,
    "Silk Gloves": 1,
    "Snuffbox, Notepad": 0.7,
    "Spork + Steak Knife": 1,
    "String (100 ft)": 1,
    "Tent": 2,
    "Three Tricks Cups,Three Trick Balls": 1,
    "Tinderbox": 0.5,
    "Trick Card Deck": 0.5,
    "Traveler's Clothes": 2,
    "Tuning Fork": 0.5,
    "Two Silver'd Arrows": 20,
    "Two-Sided Coin": 0.5,
    "Very loud whistle": 0.5,
    "Whetstone": 1,
    "Wig, Cape": 1,
    "Writ of Execution": 4
}


# Stat score data
df_plate = pd.DataFrame({
    "STR": [35, -10, 14, 22, 24, 26, 33],
    "DEX": [33, 10, 25, 27, 22, 38, 34],
    "CON": [37, -11, -16, 0, 35, 20, 31],
    "INT": [-11, 47, 38, 26, 22, 10, 0],
    "WIS": [25, -15, -10, 0, 15, 34, 38],
    "CHA": [17, 20, 20, 30, 0, 20, 13]
}, index=plate_options)

df_district = pd.DataFrame({
    "STR": [12, -2, 31, 4, 2, -5, 24, 11],
    "DEX": [2, 0, 10, 10, 14, 14, 4, 14],
    "CON": [0, -1, 30, 0, 20, 18, 10, 16],
    "INT": [15, 30, 0, 20, 10, 15, 9, 14],
    "WIS": [15, 20, 0, 20, 30, 10, 0, -1],
    "CHA": [13, 0, -10, 20, 30, 0, 0, -4]
}, index=district_options)

df_faction = pd.DataFrame({
    "STR": [21, -15, -19, 12, 0, 2, 32],
    "DEX": [22, 13, 13, 15, 0, 9, 31],
    "CON": [21, 8, 0, 21, 0, 12, 37],
    "INT": [10, 31, 27, 37, 33, -12, 0],
    "WIS": [0, 0, 0, 0, 0, 40, 0],
    "CHA": [7, 13, 27, 14, -6, 1, 11]
}, index=faction_options)



background_skills = {
    "Acolyte": {"STR": "Athletics", "DEX": "Sleight of Hand", "INT": "Religion", "WIS": "Insight", "CHA": "Persuasion", "backup": ["WIS", "INT", "CHA", "DEX"]},
    "Artisan": {"STR": "Athletics", "DEX": "Sleight of Hand", "INT": "Investigation", "WIS": "Perception", "CHA": "Persuasion", "backup": ["INT", "DEX", "CHA", "WIS"]},
    "Attendant": {"STR": "Athletics", "DEX": "Sleight of Hand", "INT": "Investigation", "WIS": "Medicine", "CHA": "Deception", "backup": ["DEX", "INT", "CHA", "WIS"]},
    "Charlatan": {"STR": "Athletics", "DEX": "Sleight of Hand", "INT": "Investigation", "WIS": "Perception", "CHA": "Deception", "backup": ["DEX", "CHA", "WIS", "INT"]},
    "Criminal": {"STR": "Athletics", "DEX": "Stealth", "INT": "Investigation", "WIS": "Survivial", "CHA": "Intimidation", "backup": ["DEX", "WIS", "CHA", "INT"]},
    "Enforcer": {"STR": "Athletics", "DEX": "Acrobatics", "INT": "Investigation", "WIS": "Perception", "CHA": "Intimidation", "backup": ["DEX", "CHA", "WIS", "INT"]},
    "Elite": {"STR": "Athletics", "DEX": "Sleight of Hand", "INT": "History", "WIS": "Insight", "CHA": "Performance", "backup": ["INT", "CHA", "DEX", "WIS"]},
    "Executor": {"STR": "Athletics", "DEX": "Sleight of Hand", "INT": "Arcana", "WIS": "Perception", "CHA": "Persuasion", "backup": ["INT", "CHA", "DEX", "WIS"]},
    "Laborer": {"STR": "Athletics", "DEX": "Acrobatics", "INT": "Nature", "WIS": "Medicine", "CHA": "Deception", "backup": ["DEX", "WIS", "CHA", "INT"]},
    "Merchant": {"STR": "Athletics", "DEX": "Sleight of Hand", "INT": "Investigation", "WIS": "Insight", "CHA": "Persuasion", "backup": ["CHA", "WIS", "DEX", "INT"]},
    "Rebel": {"STR": "Athletics", "DEX": "Stealth", "INT": "Arcana", "WIS": "Survival", "CHA": "Deception", "backup": ["CHA", "WIS", "DEX", "INT"]},
    "Professor": {"STR": "Athletics", "DEX": "Stealth", "INT": "Arcana", "WIS": "Medicine", "CHA": "Performance", "backup": ["INT", "WIS", "CHA", "DEX"]},
    "Researcher": {"STR": "Athletics", "DEX": "Stealth", "INT": "Arcana", "WIS": "Perception", "CHA": "Persuasion", "backup": ["INT", "WIS", "DEX", "CHA"]},
    "Engineer": {"STR": "Athletics", "DEX": "Sleight of Hand", "INT": "Arcana", "WIS": "Perception", "CHA": "Persuasion", "backup": ["INT", "WIS", "DEX", "CHA"]},
    "Recluse": {"STR": "Athletics", "DEX": "Acrobatics", "INT": "History", "WIS": "Survival", "CHA": "Deception", "backup": ["INT", "DEX", "WIS", "CHA"]},
    "Entertainer": {"STR": "Athletics", "DEX": "Acrobatics", "INT": "History", "WIS": "Insight", "CHA": "Performance", "backup": ["CHA", "DEX", "WIS", "INT"]}
}

# Background score lookup tables
df_bg_plate = pd.DataFrame({
    "Plate 0": [21, 0, 8, 16, 39, -18, -50, -99, 49, 0, 99, -99, 0, 0, 21, 0],
    "Plate 1": [-50, -50, -50, 0, 0, 0, 99, 30, -50, 19, 0, 0, 37, 0, 24, 0],
    "Plate 2": [-30, 10, 0, -20, 0, 0, 39, 32, -50, 25, 0, 23, 45, 11, 17, 0],
    "Plate 3": [-30, 35, 18, -5, 12, 19, -50, 26, 0, 37, 19, 39, 15, 28, 0, 15],
    "Plate 4": [-10, 33, 10, -2, 24, 10, -50, 19, 19, 7, 0, 18, 29, 20, 34, -15],
    "Plate 5": [16, 17, 21, 17, 20, 0, -50, 9, 30, 29, 29, 17, 0, 24, 17, 26],
    "Plate 6": [18, 0, 16, 21, 28, -9, -50, 0, 39, 22, 99, -99, 0, 17, 6, 19],
}, index=background_skills.keys()).T

df_bg_district = pd.DataFrame({
    "Azure": [0, 12, 0, 25, 19, 29, 6, 25, 9, 39, 0, -19, 0, 17, -15, 11],
    "Amethyst": [0, 7, 0, 4, 0, 0, 9, 9, -14, -9, 0, 39, 48, 14, 24, -20],
    "Ruby": [0, 24, 0, 0, 0, 0, -9, 24, 31, -8, -13, -15, -10, 21, -10, -20],
    "Citrine": [0, 39, 9, 0, 0, 0, -9, 19, 17, 7, 0, -25, -10, 18, 0, -20],
    "Rhodonite": [20, 18, 0, 14, 9, 0, -14, 0, 0, 28, 29, -25, -10, 0, 0, 39],
    "Amber": [2, 13, 0, 13, 7, 0, -17, 13, 21, 15, 0, 10, -15, 27, -5, -5],
    "Jade": [0, 0, 0, -8, 0, 9, 29, 0, 24, 9, -4, 0, -20, 9, 19, 9],
    "Obsidian": [-20, -10, -3, 0, 32, 19, 19, 15, 8, -99, 0, 10, 24, 5, 18, 0]
}, index=background_skills.keys()).T


df_bg_faction = pd.DataFrame({
    "Paragons": [0, 0, 0, 0, -10, 99, 21, 0, -10, -10, -14, 0, 19, 0, -19, -9],
    "Optimists": [-9, 0, -9, 0, 0, -99, 31, 99, -20, 10, -21, 17, 28, 13, 0, -7],
    "Gilded Gaze": [0, -7, 0, 0, 0, -99, 24, 99, -10, 0, 0, 0, 0, 0, 18, 12],
    "Transneuroclasts": [0, 4, 0, 0, 13, 0, 0, 99, 8, 0, 27, 21, 19, 11, 19, 0],
    "Chronomancers": [0, 0, 0, -10, -10, -99, 0, 0, -99, 0, 0, 10, 0, 38, 24, -19],
    "New Faith": [6, 9, 6, 5, 5, 0, -99, -99, 39, 12, 17, -9, 0, 6, 14, 0],
    "Unpinned": [0, 0, 0, 22, 27, 0, -99, -99, 99, 14, 99, 0, 0, 0, 15, 0],
}, index=background_skills.keys()).T


# Weapon scores by District
finesse_district_scores = pd.DataFrame({
    "Azure": [20, 30, 10, 0, 40],
    "Amethyst": [30, 40, 20, 0, 10],
    "Ruby": [10, 0, 40, 20, 30],
    "Citrine": [20, 30, 40, 0, 10],
    "Rhodonite": [20, 40, 30, 10, 0],
    "Amber": [40, 20, 30, 10, 0],
    "Jade": [10, 0, 20, 40, 30],
    "Obsidian": [30, 40, 20, 10, 0]
}, index=["Dagger", "2 Daggers", "4 Darts", "Shortbow, 20 Arrows, Quiver", "Light Crossbow, 20 Bolts, Quiver"])

# Weapon scores by Background
finesse_background_scores = pd.DataFrame({
    "Acolyte": [0, 0, 0, -41, -41],
    "Artisan": [-41, 11, 0, 0, 0],
    "Attendant": [0, 0, 21, 0, 0],
    "Charlatan": [0, 21, 21, 0, 0],
    "Criminal": [21, 21, 0, 0, 0],
    "Enforcer": [0, 0, 0, 31, 31],
    "Elite": [0, -41, 0, 0, 31],
    "Executor": [0, -61, 0, 0, 0],
    "Laborer": [0, -21, 0, 0, -21],
    "Merchant": [-11, 21, 0, 0, 0],
    "Rebel": [-11, 41, 0, 0, 0],
    "Professor": [0, -21, -21, 11, 11],
    "Researcher": [11, -31, -21, 0, 0],
    "Engineer": [-31, -51, -51, 0, 31],
    "Recluse": [-31, -41, 31, 11, -31],
    "Entertainer": [11, 0, 0, 0, 0]
}, index=["Dagger", "2 Daggers", "4 Darts", "Shortbow, 20 Arrows, Quiver", "Light Crossbow, 20 Bolts, Quiver"])

# Weapon scores by Faction
finesse_faction_scores = pd.DataFrame({
    "Paragons": [0, 0, -22, 22, 0],
    "Optimists": [22, 0, 0, -12, 0],
    "Gilded Gaze": [22, 0, 0, -12, 0],
    "Transneuroclasts": [0, 22, -22, 0, 0],
    "Chronomancers": [22, 0, 0, -12, 0],
    "New Faith": [0, 0, 0, -42, -42],
    "Unpinned": [0, 22, 22, 22, 0]
}, index=["Dagger", "2 Daggers", "4 Darts", "Shortbow, 20 Arrows, Quiver", "Light Crossbow, 20 Bolts, Quiver"])




import pandas as pd

# Useful weapon score tables
useful_district_scores = pd.DataFrame({
    "Azure": [20, 30, 10, 40],
    "Amethyst": [40, 30, 10, 20],
    "Ruby": [10, 20, 20, 30],
    "Citrine": [10, 30, 40, 20],
    "Rhodonite": [40, 10, 20, 30],
    "Amber": [10, 20, 30, 40],
    "Jade": [10, 20, 40, 30],
    "Obsidian": [30, 40, 10, 20]
}, index=["Quarterstaff", "Mace, Shield", "Handaxe", "Spear"])

useful_background_scores = pd.DataFrame({
    "Acolyte": [22, 22, 0, 0],
    "Artisan": [-12, -12, 32, 0],
    "Attendant": [22, 0, 0, 0],
    "Charlatan": [22, -22, 22, 0],
    "Criminal": [0, -12, 12, 12],
    "Enforcer": [-99, 32, 0, 12],
    "Elite": [32, -22, 0, 0],
    "Executor": [42, -12, -12, -22],
    "Laborer": [0, 22, 0, 0],
    "Merchant": [-32, 0, 0, 32],
    "Rebel": [0, 42, 42, 0],
    "Professor": [32, -99, -42, -32],
    "Researcher": [0, -99, 0, 0],
    "Engineer": [-22, -12, 0, 0],
    "Recluse": [22, 0, 0, 0],
    "Entertainer": [0, -22, 42, -22]
}, index=["Quarterstaff", "Mace, Shield", "Handaxe", "Spear"])

useful_faction_scores = pd.DataFrame({
    "Paragons": [0, 21, 0, 0],
    "Optimists": [21, 0, 0, 0],
    "Gilded Gaze": [21, 0, 0, 0],
    "Transneuroclasts": [-21, 0, 21, 21],
    "Chronomancers": [21, 0, 0, 0],
    "New Faith": [31, 11, 0, 0],
    "Unpinned": [0, 0, 0, 0]
}, index=["Quarterstaff", "Mace, Shield", "Handaxe", "Spear"])


import pandas as pd

# Sample borderline weapon score data (provided by user)

borderline_background_scores = pd.DataFrame({
    "Greatclub": [22, -22, 0, 0, 0, 0, -42, -22, 22, -32, 22, -22, -99, 0, 0, -12],
    "Sling, 20 Bullets, Pouch": [0, None, 32, 12, 0, -22, -22, -12, 0, -12, 0, 0, 22, 0, 0, 22],
    "Club": [0, -22, 0, 0, 0, 22, 0, 22, 0, 32, 0, 0, -22, 0, 0, 0],
    "Light Hammer": [0, 42, 32, -32, 0, 0, -12, 0, 22, 0, 0, 0, 0, 12, -22, 0],
    "Sickle": [22, 0, 0, -32, -22, -99, -42, 0, -12, -22, -12, 0, 0, -12, 0, 0]
}, index=[
    "Acolyte", "Artisan", "Attendant", "Charlatan", "Criminal", "Enforcer",
    "Elite", "Executor", "Laborer", "Merchant", "Rebel", "Professor",
    "Researcher", "Engineer", "Recluse", "Entertainer"
])

borderline_faction_scores = pd.DataFrame({
    "Greatclub": [0, -11, 0, 11, -21, 0, 0],
    "Sling, 20 Bullets, Pouch": [0, 21, 21, -11, 0, 0, 0],
    "Club": [21, 0, 0, 11, 0, 0, 0],
    "Light Hammer": [-21, 0, 0, 0, 0, 0, 0],
    "Sickle": [-21, 0, 0, 11, 0, 21, -21]
}, index=[
    "Paragons", "Optimists", "Gilded Gaze", "Transneuroclasts",
    "Chronomancers", "New Faith", "Unpinned"
])

borderline_district_scores = pd.DataFrame({
    "Azure": [10, 20, 40, 30, 0],
    "Amethyst": [0, 40, 10, 20, 30],
    "Ruby": [30, 10, 20, 40, 0],
    "Citrine": [10, 40, 20, 30, 0],
    "Rhodonite": [0, 30, 10, 20, 40],
    "Amber": [40, 20, 30, 10, 0],
    "Jade": [10, 30, 0, 20, 40],
    "Obsidian": [20, 10, 30, 40, 0]
}, index=[
    "Greatclub",
    "Sling, 20 Bullets, Pouch",
    "Club",
    "Light Hammer",
    "Sickle"
])

def pick_best_borderline_weapon(district, background, faction):
    total_scores = (
        borderline_district_scores[district] +
        borderline_background_scores.loc[background] +
        borderline_faction_scores.loc[faction]
    )
    return total_scores.idxmax()






# Skill priority by stat (used for diversification)
skill_priority = {
    "INT": ["Arcana", "Investigation", "History", "Religion", "Nature"],
    "DEX": ["Sleight of Hand", "Stealth", "Acrobatics", "Investigation", "Perception"],
    "WIS": ["Perception", "Insight", "Medicine", "Survival", "Animal Handling"],
    "STR": ["Athletics", "Investigation", "Perception", "Intimidation", "Animal Handling"],
    "CON": [],  # No direct skills, fallback to first stat's list
    "CHA": ["Persuasion", "Deception", "Performance", "Intimidation"]
}



def diversify_skills(results, skill_priority):
    from collections import Counter

    # Step 1: Normalize and count skill pairs
    normalized_pairs = [tuple(sorted(entry[2])) for entry in results]
    counts = Counter(normalized_pairs)
    duplicates = {pair for pair, count in counts.items() if count > 1}

    used_skills = set(skill for entry in results for skill in entry[2])
    updated_results = results.copy()

    for i in range(len(updated_results)):
        bg_i, stat_str_i, skills_i, tool_i, weapon_i = updated_results[i]
        pair_i = tuple(sorted(skills_i))

        # Only fix if duplicate and not the first one
        if pair_i in duplicates and normalized_pairs.index(pair_i) != i:
            primary_stat, secondary_stat = stat_str_i.split(", ")[0], stat_str_i.split(", ")[1]
            first, second = skills_i

            # Try to find new second skill from secondary stat
            replacement_found = False
            for candidate in skill_priority.get(secondary_stat, []):
                if candidate not in used_skills and candidate != first:
                    updated_results[i] = (bg_i, stat_str_i, [first, candidate], tool_i, weapon_i)
                    used_skills.add(candidate)
                    replacement_found = True
                    break

            # If no replacement, try to replace first skill instead
            if not replacement_found:
                for candidate in skill_priority.get(primary_stat, []):
                    if candidate not in used_skills and candidate != second:
                        updated_results[i] = (bg_i, stat_str_i, [candidate, second], tool_i, weapon_i)
                        used_skills.add(candidate)
                        break

    return updated_results

from collections import Counter

def reduce_skill_quads(results, skill_priority):
    from collections import defaultdict

    used_skills = []
    new_results = []

    skill_usage = defaultdict(int)  # count how many times each skill has been used so far

    for bg, stat_str, skills, tool, weapon in results:
        s1, s2 = skills
        updated = [s1, s2]

        for i in [0, 1]:  # Check each skill separately
            skill = updated[i]
            if skill_usage[skill] >= 3:
                stat = stat_str.split(", ")[i]
                for candidate in skill_priority.get(stat, []):
                    if candidate not in used_skills:
                        updated[i] = candidate
                        break
            skill_usage[updated[i]] += 1
            used_skills.append(updated[i])

        new_results.append((bg, stat_str, updated, tool, weapon))

    return new_results


# Tool proficiency matrix
tool_matrix = {
    "Azure": {
        "Acolyte": "Painter's Supplies", "Artisan": "Jeweler's Tools", "Attendant": "Navigator's Tools",
        "Charlatan": "Forgery Kit", "Criminal": "Poisoner's Kit", "Enforcer": "Gaming Set",
        "Elite": "Calligrapher's Supplies", "Executor": "Tinker's Tools", "Laborer": "Cook's Utensils",
        "Merchant": "Calligrapher's Supplies", "Rebel": "Painter's Supplies", "Professor": "Calligrapher's Supplies",
        "Researcher": "Cartographer's Tools", "Engineer": "Cartographer's Tools", "Recluse": "Disguise Kit",
        "Entertainer": "Disguise Kit"
    },
    "Amethyst": {
        "Acolyte": "Calligrapher's Supplies", "Artisan": "Alchemist's Supplies", "Attendant": "Calligrapher's Supplies",
        "Charlatan": "Forgery Kit", "Criminal": "Forgery Kit", "Enforcer": "Woodcarver's Tools",
        "Elite": "Calligrapher's Supplies", "Executor": "Calligrapher's Supplies", "Laborer": "Mason's Tools",
        "Merchant": "Calligrapher's Supplies", "Rebel": "Thieves' Tools", "Professor": "Calligrapher's Supplies",
        "Researcher": "Tinker's Tools", "Engineer": "Tinker's Tools", "Recluse": "Calligrapher's Supplies",
        "Entertainer": "Musical Instrument"
    },
    "Ruby": {
        "Acolyte": "Jeweler's Tools", "Artisan": "Smith's Tools", "Attendant": "Smith's Tools",
        "Charlatan": "Disguise Kit", "Criminal": "Thieves' Tools", "Enforcer": "Leatherworker's Tools",
        "Elite": "Calligrapher's Supplies", "Executor": "Calligrapher's Supplies", "Laborer": "Mason's Tools",
        "Merchant": "Smith's Tools", "Rebel": "Forgery Kit", "Professor": "Calligrapher's Supplies",
        "Researcher": "Alchemist's Supplies", "Engineer": "Smith's Tools", "Recluse": "Herbalism Kit",
        "Entertainer": "Gaming Set"
    },
    "Citrine": {
        "Acolyte": "Calligrapher's Supplies", "Artisan": "Weaver's Tools", "Attendant": "Cobbler's Tools",
        "Charlatan": "Disguise Kit", "Criminal": "Thieves' Tools", "Enforcer": "Leatherworker's Tools",
        "Elite": "Calligrapher's Supplies", "Executor": "Tinker's Tools", "Laborer": "Leatherworker's Tools",
        "Merchant": "Calligrapher's Supplies", "Rebel": "Forgery Kit", "Professor": "Calligrapher's Supplies",
        "Researcher": "Alchemist's Supplies", "Engineer": "Tinker's Tools", "Recluse": "Herbalism Kit",
        "Entertainer": "Gaming Set"
    },
    "Rhodonite": {
        "Acolyte": "Calligrapher's Supplies", "Artisan": "Brewer's Supplies", "Attendant": "Disguise Kit",
        "Charlatan": "Disguise Kit", "Criminal": "Poisoner's Kit", "Enforcer": "Gaming Set",
        "Elite": "Gaming Set", "Executor": "Tinker's Tools", "Laborer": "Carpenter's Tools",
        "Merchant": "Brewer's Supplies", "Rebel": "Musical Instrument", "Professor": "Musical Instrument",
        "Researcher": "Tinker's Tools", "Engineer": "Mason's Tools", "Recluse": "Musical Instrument",
        "Entertainer": "Disguise Kit"
    },
    "Amber": {
        "Acolyte": "Herbalism Kit", "Artisan": "Glassblower's Tools", "Attendant": "Tinker's Tools",
        "Charlatan": "Cook's Utensils", "Criminal": "Thieves' Tools", "Enforcer": "Smith's Tools",
        "Elite": "Musical Instrument", "Executor": "Tinker's Tools", "Laborer": "Mason's Tools",
        "Merchant": "Herbalism Kit", "Rebel": "Thieves' Tools", "Professor": "Gaming Set",
        "Researcher": "Calligrapher's Supplies", "Engineer": "Smith's Tools", "Recluse": "Alchemist's Supplies",
        "Entertainer": "Musical Instrument"
    },
    "Jade": {
        "Acolyte": "Herbalism Kit", "Artisan": "Cook's Utensils", "Attendant": "Carpenter's Tools",
        "Charlatan": "Brewer's Supplies", "Criminal": "Thieves' Tools", "Enforcer": "Woodcarver's Tools",
        "Elite": "Musical Instrument", "Executor": "Tinker's Tools", "Laborer": "Carpenter's Tools",
        "Merchant": "Herbalism Kit", "Rebel": "Herbalism Kit", "Professor": "Calligrapher's Supplies",
        "Researcher": "Calligrapher's Supplies", "Engineer": "Tinker's Tools", "Recluse": "Alchemist's Supplies",
        "Entertainer": "Musical Instrument"
    },
    "Obsidian": {
        "Acolyte": "Forgery Kit", "Artisan": "Tinker's Tools", "Attendant": "Calligrapher's Supplies",
        "Charlatan": "Forgery Kit", "Criminal": "Disguise Kit", "Enforcer": "Smith's Tools",
        "Elite": "Poisoner's Kit", "Executor": "Tinker's Tools", "Laborer": "Mason's Tools",
        "Merchant": "Calligrapher's Supplies", "Rebel": "Thieves' Tools", "Professor": "Calligrapher's Supplies",
        "Researcher": "Calligrapher's Supplies", "Engineer": "Smith's Tools", "Recluse": "Disguise Kit",
        "Entertainer": "Musical Instrument"
    }
}


# Define the upgrade matrix as three rows: Upgrade, Current Tool, Downgrade
tool_matrix_data = {
    "ToolUpgrade": [
        None, "Alchemist's Supplies", None, "Mason's Tools", None, "Glassblower's Tools", "Herbalism Kit",
        None, None, None, None, None, None, None, "Smith's Tools", None, None, None,
        "Alchemist's Supplies", None, "Tinker's Tools", None, None, None
    ],
    "ToolHave": [
        "Alchemist's Supplies", "Brewer's Supplies", "Calligrapher's Supplies", "Carpenter's Tools",
        "Cartographer's Tools", "Cobbler's Tools", "Cook's Utensils", "Disguise Kit", "Forgery Kit",
        "Gaming Set", "Glassblower's Tools", "Herbalism Kit", "Jeweler's Tools", "Leatherworker's Tools",
        "Mason's Tools", "Musical Instrument", "Navigator's Tools", "Painter's Supplies", "Poisoner's Kit",
        "Smith's Tools", "Thieves' Tools", "Tinker's Tools", "Weaver's Tools", "Woodcarver's Tools"
    ],
    "ToolDowngrade": [
        "Cook's Utensils", "Thieves' Tools", "Forgery Kit", "Cobbler's Tools", "Painter's Supplies", "Thieves' Tools",
        "Gaming Set", "Thieves' Tools", None, None, "Potter's Tools", None, "Carpenter's Tools", "Forgery Kit",
        None, "Gaming Set", None, None, None, "Forgery Kit", None, "Thieves' Tools", None, "Disguise Kit"
    ]
}

def extract_unique_digits(number, count=3):
    digits = [int(d) for d in str(number)]
    unique_digits = []
    for d in digits:
        while d in unique_digits:
            d = (d + 1) % 10
        unique_digits.append(d)
        if len(unique_digits) == count:
            break
    while len(unique_digits) < count:
        for fallback in range(10):
            if fallback not in unique_digits:
                unique_digits.append(fallback)
            if len(unique_digits) == count:
                break
    return unique_digits


# === Compute Logic ===
total_stats = df_plate.loc[selected_plate] + df_district.loc[selected_district] + df_faction.loc[selected_faction]
top_stats_display = total_stats.sort_values(ascending=False).index.tolist()
top_three_stats_str = ", ".join(top_stats_display[:3])

adjusted_stats = total_stats.drop("CON").sort_values(ascending=False)
top_stats = adjusted_stats.index.tolist()
stat_total = int(total_stats.sum())
ribbon_digits = extract_unique_digits(stat_total)


# === Totals Background


bg_scores = df_bg_plate.loc[selected_plate] + df_bg_district.loc[selected_district] + df_bg_faction.loc[selected_faction]

# === Enforcer custom placement logic for Gilded Gaze Precrim ===
if selected_faction == "Gilded Gaze":
    valid_enforcer_conditions = [
        (selected_plate in ["Plate 1", "Plate 2", "Plate 3", "Plate 4"] and selected_district == "Azure"),
        (selected_plate == "Plate 3" and selected_district == "Amethyst")
    ]
    if any(valid_enforcer_conditions):
        bg_scores["Enforcer"] += 130  # Strong boost to force it in
    else:
        bg_scores["Enforcer"] = -1000  # Effectively removes it from selection




top_backgrounds = bg_scores.sort_values(ascending=False).head(5).index.tolist()





def assign_weapon_bucket(top_stats, total_stats, selected_plate, selected_faction):
    physical_stats = ["STR", "DEX", "CON"]
    top_two = top_stats[:2]

    bucket = "Borderline"  # default fallback

    if not any(stat in physical_stats for stat in top_two):
        bucket = "Borderline"
    elif "DEX" in top_two and top_two[0] != "STR":
        bucket = "Finesse"
    elif "STR" in top_two and top_two[0] != "DEX":
        bucket = "Useful"
    elif "CON" in top_two:
        bucket = "Finesse" if total_stats["DEX"] > total_stats["STR"] else "Borderline"

    # Faction-specific rule: Unpinned downgrades Useful to Borderline
    if selected_faction == "Unpinned" and bucket == "Useful":
        bucket = "Borderline"

    return bucket

weapon_bucket = assign_weapon_bucket(top_stats, total_stats, selected_plate, selected_faction)

def pick_best_finesse_weapon(district, background, faction):
    total_scores = (
        finesse_district_scores[district] +
        finesse_background_scores[background] +
        finesse_faction_scores[faction]
    )
    return total_scores.idxmax()

def pick_best_useful_weapon(district, background, faction):
    total_scores = (
        useful_district_scores[district] +
        useful_background_scores[background] +
        useful_faction_scores[faction]
    )
    return total_scores.idxmax()


results = []


for i, bg in enumerate(top_backgrounds):
    data = background_skills[bg]
    if i == 0 or i == 1 or i == 2:
        s1, s2 = top_stats[0], top_stats[1]
    elif i == 3:
        s1, s2 = top_stats[0], top_stats[2]
    else:
        s1, s2 = top_stats[1], top_stats[2]

    skills = []

    if "STR" in [s1, s2] and top_stats.index("STR") == 0:
        skills.append("Athletics")
        s2 = s2 if s2 != "STR" else top_stats[1]
    elif "STR" in [s1, s2]:
        for stat in data["backup"]:
            if stat != s1 and stat != s2:
                skills.append(data.get(stat, "None"))
                break
    else:
        skills.append(data.get(s1, "None"))

    skills.append(data.get(s2, "None"))
    if weapon_bucket == "Finesse":
        weapon = pick_best_finesse_weapon(selected_district, bg, selected_faction)
    elif weapon_bucket == "Useful":
        weapon = pick_best_useful_weapon(selected_district, bg, selected_faction)
    else:
        weapon = pick_best_borderline_weapon(selected_district, bg, selected_faction)
    tool = tool_matrix[selected_district][bg]
    results.append((bg, top_three_stats_str, skills, tool, weapon))



results = diversify_skills(results, skill_priority)

results = reduce_skill_quads(results, skill_priority)



def get_tool_proficiency(district, background):
    try:
        return tool_matrix[district][background]
    except KeyError:
        return "None"




def nudge_tool_proficiency(results, plate, tool_matrix_data):
    from collections import Counter


    upgrade_map = dict(zip(tool_matrix_data["ToolHave"], tool_matrix_data["ToolUpgrade"]))
    downgrade_map = dict(zip(tool_matrix_data["ToolHave"], tool_matrix_data["ToolDowngrade"]))

    tool_counts = Counter(entry[3] for entry in results if entry[3] is not None)
    updated_results = []

    for entry in results:
        bg, stat_str, skills, tool, weapon = entry
        new_tool = tool

        if tool is not None:
            if plate in [1, 2]:
                upgrade = upgrade_map.get(tool)
                if upgrade and tool_counts[upgrade] <= 1:
                    print(f"Upgrading {tool} -> {upgrade} for {bg}")
                    new_tool = upgrade
            elif plate in [0, 5, 6]:
                downgrade = downgrade_map.get(tool)
                if downgrade and tool_counts[downgrade] <= 1:
                    print(f"Downgrading {tool} -> {downgrade} for {bg}")
                    new_tool = downgrade

        # Update counts only if tool is not None
        if tool is not None:
            tool_counts[tool] -= 1
        if new_tool is not None:
            tool_counts[new_tool] += 1

        updated_results.append((bg, stat_str, skills, new_tool, weapon))

    return updated_results

plate_number = int(selected_plate.split()[-1])  # "Plate 6" -> 6
results = nudge_tool_proficiency(results, plate_number, tool_matrix_data)


# Add tool proficiency item to equipment
TOOL_COL = 3  # Tool Proficiency column
EQUIP_COL = 4  # Equipment column

for idx, row in enumerate(results):
    row_list = list(row)  # Convert tuple to list
    tool_prof = row_list[TOOL_COL]
    current_equip = row_list[EQUIP_COL]

    if tool_prof and tool_prof not in current_equip:
        if current_equip:
            row_list[EQUIP_COL] = f"{current_equip}, {tool_prof}"
        else:
            row_list[EQUIP_COL] = tool_prof

    results[idx] = tuple(row_list)  # Convert list back to tuple


# Get ribbon items for this background
background = results[0][0]  # Grabbing the background name from the first result
ribbon_pool = background_ribbons.get(background, [])

# Use digits to pick items
ribbon_items = []
for digit in ribbon_digits:
    if digit < len(ribbon_pool):
        ribbon_items.append(ribbon_pool[digit])


# Ribbon + Gold Processing Block
plate_gold = {
    "Plate 1": 57,
    "Plate 2": 51,
    "Plate 3": 46,
    "Plate 4": 43,
    "Plate 5": 40,
    "Plate 6": 37,
    "Plate 0": 31
}



# Create a new list to hold updated result rows
updated_results = []

for row in results:
    background = row[0]
    tool = row[3]
    weapon = row[4].split(",")[0]  # First item is always the weapon

    # Start with gold for selected plate
    gold = plate_gold.get(selected_plate, 50)

    # Subtract tool and weapon costs
    gold -= tool_costs.get(tool, 0)
    gold -= weapon_costs.get(weapon.strip(), 0)

    # Get the three ribbon items
    ribbons = []
    ribbon_pool = background_ribbons.get(background, [])
    for digit in ribbon_digits:
        if digit < len(ribbon_pool):
            item = ribbon_pool[digit]
            # If the item has a rare alternate, roll a 50/50 and swap
            if item in rare_item_pairs and random.random() < 0.5:
                item = rare_item_pairs[item]
            ribbons.append(item)

    # Subtract ribbon costs one by one
    ribbon_equipped = []
    for item in ribbons:
        cost = ribbon_costs.get(item, 0)
        if gold - cost >= 3:
            gold -= cost
            ribbon_equipped.append(item)
        else:
            break  # Don't equip if it brings us below 3g

    # Special case: allow first ribbon even if gold went negative
    if gold < 0 and ribbons:
        first_item = ribbons[0]
        ribbon_equipped = [first_item]
        gold = 3  # Set minimum gold to 3

    # Add optional high-cost item if ≥ 31g and not already equipped with a bow/crossbow
    if gold >= 31 and not any("Shortbow" in item or "Crossbow" in item for item in ribbon_equipped):
        high_cost_items = [
            "Preferred Ranged",
            "Preferred Ranged",
            "Climber's Kit",
            f"{selected_district} Inlaid Ring",
            "Sled",
            "Vial of Acid",
            "Fine Clothes",
            "Orb",
            "Wool Tweed Cloak",
            "Magnifying Glass"
        ]
        try:
            fallback_index = int(str(int(gold))[-1])
            selected_item = high_cost_items[fallback_index]

            already_has_ranged = any(
                "Shortbow" in item or "Crossbow" in item for item in [weapon, tool] + ribbon_equipped
            )

            if selected_item == "Preferred Ranged":
                if already_has_ranged:
                    selected_item = "Ceremonial Rapier"
                else:
                    district_scores = finesse_district_scores[selected_district]
                    shortbow_score = district_scores["Shortbow, 20 Arrows, Quiver"]
                    crossbow_score = district_scores["Light Crossbow, 20 Bolts, Quiver"]

                    if shortbow_score >= crossbow_score:
                        selected_item = "Shortbow, 20 Arrows, Quiver"
                    else:
                        selected_item = "Light Crossbow, 20 Bolts, Quiver"

            ribbon_equipped.append(selected_item)
            gold -= 27  # Standardized cost

        except Exception as e:
            print(f"Error choosing high-cost item: {e}")

    # Optional 4th ribbon if enough left (≥ 13g)
    if gold >= 13:
        remaining_items = [item for item in ribbon_pool if item not in ribbon_equipped]
        used_digits = {ribbon_pool.index(item) for item in ribbon_equipped if item in ribbon_pool}
        digit = int(str(int(gold))[-1])  # Last digit of gold

        for _ in range(10):  # Try up to 10 times to avoid infinite loop
            if digit not in used_digits and digit < len(ribbon_pool):
                candidate = ribbon_pool[digit]
                if candidate in rare_item_pairs and random.random() < 0.5:
                    candidate = rare_item_pairs[candidate]
                cost = ribbon_costs.get(candidate, 0)
                if gold - cost >= 0:
                    ribbon_equipped.append(candidate)
                    gold -= cost
                    break
            digit = (digit + 1) % 10  # Roll up

    #  Convert bonus gold ribbons into actual gold
    gold_bonus_map = {
        "10 Extra Gold": 10,
        "30 Extra Gold": 30
    }

    ribbon_equipped_cleaned = []
    for item in ribbon_equipped:
        if item in gold_bonus_map:
            gold += gold_bonus_map[item]
        else:
            ribbon_equipped_cleaned.append(item)

# Convert tuple to list so we can edit it
    row_list = list(row)

# Convert stat abbreviations to full names
    stat_full_names = {
        "STR": "Strength",
        "DEX": "Dexterity",
        "CON": "Constitution",
        "INT": "Intelligence",
        "WIS": "Wisdom",
        "CHA": "Charisma"
        }
    standard_stat_order = [
        "Strength",
        "Dexterity",
        "Constitution",
        "Intelligence",
        "Wisdom",
        "Charisma"
    ]

# Handle stat string safely
    try:
        full_stats = [stat_full_names.get(s.strip(), s.strip()) for s in row[1].split(",")]
        ordered_stats = [s for s in standard_stat_order if s in full_stats]
        row_list[1] = ", ".join(ordered_stats)
    except Exception as e:
        print(f"Stat parsing error: {e}")
        row_list[1] = row[1]  # fallback

# Update equipment field
    row_list[4] = row_list[4] + ", " + ", ".join(ribbon_equipped_cleaned) + f", {int(gold)}g"

# Append final result
    updated_results.append(tuple(row_list))


# Replace the original results
results = updated_results

#-----------------------------------------------------------------------------------------------------



# Output
# Create DataFrame with labels
df_out = pd.DataFrame(results, columns=["Background", "Stats", "Skills", "Tool", "Equipment"])

# CSS style for wider dataframe

st.markdown("""
    <style>
    div[data-testid="stDataFrame"] div[role="grid"] {
        min-width: 1000px;
        max-width: none;
        overflow-x: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Display the properly labeled, wide dataframe
st.markdown("""
<style>
div[data-testid="stDataFrame"] td {
    white-space: normal !important;
    word-wrap: break-word !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("### Origin Results (Two-Column View)")

cols = st.columns(2)  # Two columns side by side

for idx, row in df_out.iterrows():
    col = cols[idx % 2]  # Alternate between columns
    col.markdown(f"""
<div style="font-size: 14px; line-height: 1.4; margin-bottom: 1.5em;">
<b>{idx}. {row['Background']}</b><br>
<b>Stats:</b> {row['Stats']}<br>
<b>Skills:</b> {', '.join(row['Skills'])}<br>
<b>Tool:</b> {row['Tool']}<br>
<b>Equipment:</b> {row['Equipment']}
</div>
""", unsafe_allow_html=True)








finesse_weapons = [
    "Dagger",
    "2 Daggers",
    "4 Darts",
    "Shortbow, 20 Arrows, Quiver",
    "Light Crossbow, 20 Bolts, Quiver"
]




useful_weapons = [
    "Quarterstaff",
    "Mace, Shield",
    "Handaxe",
    "Spear"
]

borderline_weapons = [
    "Greatclub",
    "Sling, 20 Bullets, Pouch",
    "Club",
    "Light Hammer",
    "Sickle"
]




