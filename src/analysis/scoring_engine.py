
def clamp(value, minimum=0, maximum=100):
    """Keep a score within a specified range."""
    return max(minimum, min(value, maximum))


def calculate_price_score(price, profile):
    """Calculate price score based on the rental budget."""

    minimum = profile["budget"]["min"]
    maximum = profile["budget"]["max"]

    if maximum <= minimum:
        raise ValueError("Maximum budget must exceed minimum budget.")

    score = (
        (maximum - price) /
        (maximum - minimum)
    ) * 100

    return clamp(score)


def calculate_location_score(district, profile):
    """Score preferred districts equally."""

    allowed_locations = [
        location.casefold()
        for location in profile["locations"]
    ]

    if district.casefold() in allowed_locations:
        return 100

    return 0


def calculate_transport_score(minutes, profile):
    """Calculate score based on metro walking time."""

    maximum = profile["transport"]["maximum_walking_minutes"]

    if maximum <= 0:
        raise ValueError("Maximum metro walking time must be positive.")

    score = ((maximum - minutes) / maximum) * 100

    return clamp(score)


def calculate_building_score(building_age):
    """Score building age using a provisional 30-year scale."""

    if building_age < 0:
        raise ValueError("Building age cannot be negative.")

    score = ((30 - building_age) / 30) * 100

    return clamp(score)


def calculate_listing_quality(listing):
    """Calculate completeness of listing information."""

    quality_fields = [
        "title",
        "listing_url",
        "neighborhood",
        "building_age",
        "metro_walking_minutes"
    ]

    available_fields = sum(
        1 for field in quality_fields
        if listing.get(field) is not None
        and listing.get(field) != ""
    )

    return (available_fields / len(quality_fields)) * 100


def score_listing(listing, profile):
    """Calculate weighted score for a listing."""

    scores = {
        "price": calculate_price_score(
            listing["price"], profile
        ),
        "location": calculate_location_score(
            listing["district"], profile
        ),
        "transport": calculate_transport_score(
            listing["metro_walking_minutes"], profile
        ),
        "building": None,
        "listing_quality": calculate_listing_quality(listing)
    }

    # Missing building age should not receive zero points.
    if listing.get("building_age") is not None:
        scores["building"] = calculate_building_score(
            listing["building_age"]
        )

    weights = profile["scoring"]

    available_weight = sum(
        weights[key]
        for key, value in scores.items()
        if value is not None
    )

    if available_weight == 0:
        raise ValueError("No scoring criteria available.")

    weighted_total = sum(
        scores[key] * weights[key]
        for key in scores
        if scores[key] is not None
    )

    final_score = weighted_total / available_weight

    coverage = available_weight

    return {
        "score": round(final_score, 2),
        "coverage": round(coverage, 2),
        "breakdown": scores
    }
