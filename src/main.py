
from processing.normalizer import normalize_listing

from database.db_manager import (
    initialize_database,
    save_listing,
    get_all_listings
)


def main():

    # Sample raw listing data
    raw_data = {
        "ilan_no": "987654",
        "baslik": "Kadikoy 2+1 Esyali Daire",
        "fiyat": "27.500 TL",
        "ilce": "Kadikoy",
        "oda_sayisi": "2+1",
        "esyali": "Eşyalı",
        "url": "https://example.com/listing/987654",
        "mahalle": "Moda",
        "bina_yasi": 5,
        "metro_distance": 8
    }

    # Step 1: Initialize database
    initialize_database()

    # Step 2: Normalize raw data
    listing = normalize_listing(
        raw_data,
        source="test_source"
    )

    # Step 3: Save listing
    saved = save_listing(listing)

    if saved:
        print("New listing saved successfully!")
    else:
        print("Listing already exists!")

    # Step 4: Retrieve listings
    listings = get_all_listings()

    print("\nDATABASE CONTENT")
    print("--------------------")

    for item in listings:
        print(f"ID: {item['id']}")
        print(f"Title: {item['title']}")
        print(f"Price: {item['price']} TL")
        print(f"District: {item['district']}")
        print("--------------------")

    print(f"Total listings: {len(listings)}")


if __name__ == "__main__":
    main()
