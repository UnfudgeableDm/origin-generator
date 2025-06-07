import streamlit as st
import pandas as pd

# Sample input UI
plate_options = ["Plate 0", "Plate 1", "Plate 2", "Plate 3", "Plate 4", "Plate 5", "Plate 6"]
district_options = ["Azure", "Amethyst", "Ruby", "Citrine", "Rhodonite", "Amber", "Jade", "Obsidian"]
faction_options = ["Paragons", "Optimists", "Gilded Gaze", "Transneuroclasts", "Chronomancers", "New Faith", "Unpinned"]

selected_plate = st.selectbox("Select Plate", plate_options)
selected_district = st.selectbox("Select District", district_options)
selected_faction = st.selectbox("Select Faction", faction_options)

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
    "STR": [12, -2, 31, 4, 2, 0, 24, 11],
    "DEX": [2, 0, 10, 10, 14, 16, 4, 14],
    "CON": [0, -1, 30, 0, 20, 15, 10, 16],
    "INT": [15, 30, 0, 20, 10, 3, 9, 14],
    "WIS": [15, 20, 0, 20, 30, 0, 0, -1],
    "CHA": [13, 0, -10, 20, 30, 0, 0, -4]
}, index=district_options)

df_faction = pd.DataFrame({
    "STR": [21, -15, -19, 12, 0, 2, 32],
    "DEX": [22, 12, 12, 15, 0, 9, 31],
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
    "Amber": [0, 0, 0, 27, 24, 0, 17, -7, 0, 9, 19, -15, -15, 7, -6, 9],
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


# === Compute Logic ===
total_stats = df_plate.loc[selected_plate] + df_district.loc[selected_district] + df_faction.loc[selected_faction]
top_stats_display = total_stats.sort_values(ascending=False).index.tolist()
top_three_stats_str = ", ".join(top_stats_display[:3])

adjusted_stats = total_stats.drop("CON").sort_values(ascending=False)
top_stats = adjusted_stats.index.tolist()




bg_scores = df_bg_plate.loc[selected_plate] + df_bg_district.loc[selected_district] + df_bg_faction.loc[selected_faction]
top_backgrounds = bg_scores.sort_values(ascending=False).head(5).index.tolist()

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
    results.append((bg, top_three_stats_str, skills))


# Output
st.subheader("Origin Results")
df_out = pd.DataFrame(results, columns=["Background", "Stats", "Skills"])
st.dataframe(df_out)
