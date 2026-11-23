
import json
from pathlib import Path

from analysis.filter_engine import filter_listings
from analysis.scoring_engine import score_listing

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

    profile = load_search_profile()
    listings = get_all_listings()

    print(f"\nTotal listings: {len(listings)}")

    results = filter_listings(
        listings,
        profile
    )

    print("\nFILTERING RESULTS")
    print("=====================")

    for status, items in results.items():
        print(f"{status}: {len(items)}")

    # Score matching listings
    scored_listings = []

    for item in results["MATCH"]:

        listing = item["listing"]

        scoring = score_listing(
            listing,
            profile
        )

        scored_listings.append({
            "listing": listing,
            "scoring": scoring
        })

    # Sort from highest to lowest score
    scored_listings.sort(
        key=lambda item: item["scoring"]["score"],
        reverse=True
    )

    print("\nRANKED LISTINGS")
    print("=====================")

    for rank, item in enumerate(scored_listings, start=1):

        listing = item["listing"]
        scoring = item["scoring"]

        print(f"\n#{rank} - {listing['title']}")
        print(f"Price: {listing['price']} TL")
        print(f"District: {listing['district']}")
        print(f"Score: {scoring['score']}/100")
        print(f"Data coverage: {scoring['coverage']}%")

        print("\nScore Breakdown:")

        for criterion, value in scoring["breakdown"].items():

            if value is None:
                print(f"{criterion}: N/A")
            else:
                print(f"{criterion}: {value:.2f}")

        print("---------------------")


if __name__ == "__main__":
    main()
