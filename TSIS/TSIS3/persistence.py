# persistence.py - save and load scores and settings

import json
import os

# load settings from file, return defaults if file doesn't exist
def load_settings():
    if os.path.exists("settings.json"):
        return json.load(open("settings.json"))
    return {"color": "blue", "difficulty": "normal", "sound": True}

# save settings to file
def save_settings(s):
    json.dump(s, open("settings.json", "w"), indent=2)

# load leaderboard scores
def load_scores():
    if os.path.exists("leaderboard.json"):
        return json.load(open("leaderboard.json"))
    return []

# save new score, keep only top 10
def save_score(name, score, dist, coins):
    data = load_scores()
    data.append({"name": name, "score": score, "dist": dist, "coins": coins})
    data.sort(key=lambda x: x["score"], reverse=True)
    json.dump(data[:10], open("leaderboard.json", "w"), indent=2)