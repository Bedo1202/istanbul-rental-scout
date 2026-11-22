
from processing.normalizer import normalize_listing

from database.db_manager import (
    initialize_database,
    save_listing,
    get_all_listings,
    get_price_history
)


def main():

    raw_data = {
        "ilan_no": "987654",
        "baslik": "Kadikoy 2+1 Esyali Daire",
        "fiyat": "26.000 TL",
        "ilce": "Kadikoy",
        "oda_sayisi": "2+1",
        "esyali": "Eşyalı",
        "url": "https://example.com/listing/987654",
        "mahalle": "Moda",
        "bina_yasi": 5,
        "metro_distance": 8
    }

    initialize_database()

    listing = normalize_listing(
        raw_data,
        source="test_source"
    )

    result = save_listing(listing)

    print("DATABASE OPERATION")
    print("--------------------")

    if result == "inserted":
        print("New listing saved!")

    elif result == "price_updated":
        print("Listing price updated!")

    else:
        print("Listing unchanged!")

    listings = get_all_listings()

    print(f"\nTotal listings: {len(listings)}")

    for item in listings:

        print(f"\nListing: {item['title']}")
        print(f"Current price: {item['price']} TL")

        history = get_price_history(item["id"])

        print("\nPRICE HISTORY")

        for record in history:
            print(
                f"{record['recorded_at']} "
                f"- {record['price']} TL"
            )


if __name__ == "__main__":
    main()
