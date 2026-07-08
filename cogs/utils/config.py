import json
import os

def load_project_data():
    with open("data/project_files.json", "r") as json_file:
        return json.load(json_file)

def load_script_data():
    with open("data/scripts.json", "r") as json_file:
        return json.load(json_file)

def load_extension_data():
    with open("data/extensions.json", "r") as json_file:
        return json.load(json_file)

def load_presets_data():
    with open("data/presets.json", "r") as presets_file:
        return json.load(presets_file)

def load_messages_config():
    with open("data/messages.json", "r") as f:
        return json.load(f)

def save_messages_config(config):
    os.makedirs("data", exist_ok=True)
    with open("data/messages.json", "w") as f:
        json.dump(config, f, indent=4)

def load_trending():
    try:
        with open("data/trending.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"Animes": [], "Songs": []}

def save_trending(data):
    os.makedirs("data", exist_ok=True)
    with open("data/trending.json", "w") as f:
        json.dump(data, f, indent=4)

def count_presets_in_categories():
    presets_data = load_presets_data()
    presetscategories = presets_data.get("presetscategories", {})
    category_counts = {}
    for category_name, folder_name in presetscategories.items():
        folder_path = os.path.join("resources/presets", folder_name)
        assets = [f for f in os.listdir(folder_path) if f.endswith(".ffx")]
        category_counts[category_name] = len(assets)
    return category_counts
