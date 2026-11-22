
from pathlib import Path

from collectors.json_collector import JSONCollector
from collectors.csv_collector import CSVCollector

from processing.normalizer import normalize_listing

from database.db_manager import (
    initialize_database,
    save_listing,
    get_all_listings
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def process_listings(raw_listings, source):

    for raw_data in raw_listings:

        listing = normalize_listing(
            raw_data,
            source=source
        )

        result = save_listing(listing)

        print(
            f"{listing.source_listing_id}: {result}"
        )


def main():

    print("ISTANBUL RENTAL SCOUT")
    print("=====================")

    initialize_database()

    # JSON Collection
    json_path = PROJECT_ROOT / "data" / "sample_listings.json"

    json_collector = JSONCollector(json_path)
    json_data = json_collector.collect()

    print(f"\nJSON records: {len(json_data)}")

    process_listings(json_data, "json_import")

    # CSV Collection
    csv_path = PROJECT_ROOT / "data" / "sample_listings.csv"

    csv_collector = CSVCollector(csv_path)
    csv_data = csv_collector.collect()

    print(f"\nCSV records: {len(csv_data)}")

    process_listings(csv_data, "csv_import")

    # Database Summary
    listings = get_all_listings()

    print("\nDATABASE SUMMARY")
    print("=====================")

    print(f"Total listings: {len(listings)}")

    for item in listings:

        print(f"\nTitle: {item['title']}")
        print(f"Price: {item['price']} TL")
        print(f"District: {item['district']}")


if __name__ == "__main__":
    main()
