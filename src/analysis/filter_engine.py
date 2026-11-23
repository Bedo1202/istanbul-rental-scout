
import unicodedata


def normalize_text(value):
    """Normalize text for reliable comparisons."""

    if value is None:
        return ""

    value = str(value).strip().casefold()

    # Handle Turkish characters
    value = value.replace("ı", "i")

    value = unicodedata.normalize("NFKD", value)

    value = "".join(
        char for char in value
        if not unicodedata.combining(char)
    )

    return value


def evaluate_listing(listing, profile):
    """Evaluate a listing against the search profile."""

    reasons = []
    review_reasons = []

    # 1. Budget check
    price = listing.get("price")
    budget = profile["budget"]

    if price is None:
        review_reasons.append("Price information missing")

    elif not budget["min"] <= price <= budget["max"]:
        reasons.append("Price outside budget")

    # 2. District check
    district = listing.get("district")

    allowed_districts = [
        normalize_text(item)
        for item in profile["locations"]
    ]

    if not district:
        review_reasons.append("District information missing")

    elif normalize_text(district) not in allowed_districts:
        reasons.append("District not preferred")

    # 3. Room type check
    room_type = listing.get("room_type")

    if not room_type:
        review_reasons.append("Room information missing")

    elif normalize_text(room_type) != normalize_text(
        profile["rooms"]
    ):
        reasons.append("Room type does not match")

    # 4. Furnished check
    furnished = listing.get("furnished")

    if furnished is None:
        review_reasons.append("Furnished information missing")

    elif bool(furnished) != profile["furnished"]:
        reasons.append("Furnished preference does not match")

    # 5. Metro distance check
    metro_minutes = listing.get("metro_walking_minutes")

    max_metro_minutes = profile["transport"][
        "maximum_walking_minutes"
    ]

    if metro_minutes is None:
        review_reasons.append("Metro distance information missing")

    elif metro_minutes > max_metro_minutes:
        reasons.append("Metro distance exceeds limit")

    # Determine final status
    if reasons:
        status = "REJECTED"

    elif review_reasons:
        status = "REVIEW"

    else:
        status = "MATCH"

    return {
        "status": status,
        "reasons": reasons + review_reasons
    }


def filter_listings(listings, profile):
    """Filter all listings using the search profile."""

    results = {
        "MATCH": [],
        "REVIEW": [],
        "REJECTED": []
    }

    for listing in listings:

        evaluation = evaluate_listing(
            listing,
            profile
        )

        results[evaluation["status"]].append({
            "listing": listing,
            "reasons": evaluation["reasons"]
        })

    return results
