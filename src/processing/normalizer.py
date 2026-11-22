
import re

from models.listing import Listing


def get_value(data, *keys):
    """Find the first available value from alternative field names."""

    for key in keys:
        value = data.get(key)

        if value is not None and value != "":
            return value

    return None


def parse_price(value):
    """Convert different price formats into an integer."""

    if isinstance(value, (int, float)):
        return int(value)

    if isinstance(value, str):
        digits = re.sub(r"[^\d]", "", value)

        if digits:
            return int(digits)

    raise ValueError(f"Invalid price: {value}")


def parse_furnished(value):
    """Convert furnished information into True, False or None."""

    if isinstance(value, bool):
        return value

    if not isinstance(value, str):
        return None

    value = value.lower().strip()

    if value in ["evet", "eşyalı", "esyali", "furnished", "yes", "true"]:
        return True

    if value in ["hayır", "hayir", "eşyasız", "esyasiz",
                 "unfurnished", "no", "false"]:
        return False

    return None


def normalize_listing(raw_data, source):
    """Convert raw listing data into the standard Listing model."""

    listing_id = get_value(
        raw_data, "source_listing_id", "listing_id", "id", "ilan_no"
    )

    title = get_value(raw_data, "title", "baslik")
    price = get_value(raw_data, "price", "fiyat")
    district = get_value(raw_data, "district", "ilce")
    room_type = get_value(raw_data, "room_type", "rooms", "oda_sayisi")
    listing_url = get_value(raw_data, "listing_url", "url", "link")

    required_fields = {
        "listing_id": listing_id,
        "title": title,
        "price": price,
        "district": district,
        "room_type": room_type,
        "listing_url": listing_url
    }

    missing_fields = [
        field for field, value in required_fields.items()
        if value is None
    ]

    if missing_fields:
        raise ValueError(
            f"Missing required fields: {missing_fields}"
        )

    return Listing(
        source=source,
        source_listing_id=str(listing_id),
        title=str(title),
        price=parse_price(price),
        district=str(district),
        room_type=str(room_type),
        furnished=parse_furnished(
            get_value(raw_data, "furnished", "esyali")
        ),
        listing_url=str(listing_url),
        neighborhood=get_value(raw_data, "neighborhood", "mahalle"),
        building_age=get_value(raw_data, "building_age", "bina_yasi"),
        metro_walking_minutes=get_value(
            raw_data, "metro_walking_minutes", "metro_distance"
        )
    )
