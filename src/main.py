
import json
from pathlib import Path

from analysis.filter_engine import filter_listings
from database.db_manager import get_all_listings


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_search_profile():

    profile_path = (
        PROJECT_ROOT / "config" / "search_profile.json"
    )

    with open(
        profile_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def main():

    print("ISTANBUL RENTAL SCOUT")
    print("=====================")

    # Load search criteria
    profile = load_search_profile()

    # Retrieve listings from database
    listings = get_all_listings()

    print(f"\nTotal listings: {len(listings)}")

    # Apply filtering
    results = filter_listings(
        listings,
        profile
    )

    # Display results
    print("\nFILTERING RESULTS")
    print("=====================")

    for status, items in results.items():

        print(f"\n{status}: {len(items)}")

        for item in items:

            listing = item["listing"]

            print(
                f"\n{listing['title']}"
            )

            print(
                f"Price: {listing['price']} TL"
            )

            print(
                f"District: {listing['district']}"
            )

            if item["reasons"]:
                print(
                    f"Reasons: {', '.join(item['reasons'])}"
                )


if __name__ == "__main__":
    main()
