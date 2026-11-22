
from processing.normalizer import normalize_listing


def main():

    # Simulated raw data from a listing source
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

    listing = normalize_listing(
        raw_data,
        source="test_source"
    )

    print("NORMALIZATION TEST")
    print("--------------------")

    print(f"Title: {listing.title}")
    print(f"Price: {listing.price} TL")
    print(f"District: {listing.district}")
    print(f"Rooms: {listing.room_type}")
    print(f"Furnished: {listing.furnished}")
    print(f"Neighborhood: {listing.neighborhood}")
    print(f"Building age: {listing.building_age}")
    print(f"Metro walking: {listing.metro_walking_minutes} min")
    print(f"Unique ID: {listing.get_unique_key()}")


if __name__ == "__main__":
    main()
