
import json
from pathlib import Path


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Configuration file path
CONFIG_PATH = PROJECT_ROOT / "config" / "search_profile.json"


def load_search_profile():
    """Load rental search criteria from JSON."""

    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        profile = json.load(file)

    return profile


def main():
    profile = load_search_profile()

    print("ISTANBUL RENTAL SCOUT")
    print("---------------------")

    print(f"Property type: {profile['property_type']}")
    print(f"Rooms: {profile['rooms']}")
    print(f"Budget: {profile['budget']['min']} - {profile['budget']['max']} TL")
    print(f"Furnished: {profile['furnished']}")

    print("\nTarget districts:")

    for district in profile["locations"]:
        print(f"- {district}")


if __name__ == "__main__":
    main()
