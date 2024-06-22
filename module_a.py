import json
import os


def save_settings(name, tz, temp, favorites):
    current_dir = os.getcwd()
    filename = os.path.join(current_dir, "favorites.json")
    settings = [name, tz, temp]

    # Append new settings to favorites
    if settings not in favorites:
        favorites.append(settings)

    # Write updated favorites
    with open(filename, 'w') as json_file:
        json.dump(favorites, json_file)


def load_favorites():
    current_dir = os.getcwd()
    filename = os.path.join(current_dir, "favorites.json")

    # Read favorites if exists in the directory
    if os.path.exists(filename):
      with open(filename, "r") as json_file:
        favorites = json.load(json_file)
        return favorites
    else:
      return None


def set_settings_as_default(name, tz, temp):
    settings = [name, tz, temp]
    favorites = load_favorites()

    # Replace current settings with the first item in favorites (default item)
    if settings in favorites:
        settings_index = favorites.index(settings)
        favorites[settings_index] = favorites[0]
        favorites[0] = settings

        # Write updated favorites
        current_dir = os.getcwd()
        filename = os.path.join(current_dir, "favorites.json")
        with open(filename, 'w') as json_file:
            json.dump(favorites, json_file)


def reset_favorites(initial_settings):
    favorites = load_favorites()
    favorites = initial_settings

    current_dir = os.getcwd()
    filename = os.path.join(current_dir, "favorites.json")
    with open(filename, 'w') as json_file:
        json.dump(favorites, json_file)