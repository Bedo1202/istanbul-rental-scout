
import pytest

from analysis.filter_engine import (
    evaluate_listing,
    filter_listings,
    normalize_text
)


@pytest.fixture
def profile():

    return {
        "budget": {
            "min": 20000,
            "max": 30000
        },
        "locations": [
            "Kadikoy",
            "Maltepe",
            "Kartal",
            "Uskudar",
            "Pendik"
        ],
        "rooms": "2+1",
        "furnished": True,
        "transport": {
            "maximum_walking_minutes": 15
        }
    }


@pytest.fixture
def valid_listing():

    return {
        "title": "Kadikoy 2+1 Furnished Apartment",
        "price": 25000,
        "district": "Kadikoy",
        "room_type": "2+1",
        "furnished": 1,
        "metro_walking_minutes": 5
    }


def test_valid_listing_returns_match(profile, valid_listing):

    result = evaluate_listing(valid_listing, profile)

    assert result["status"] == "MATCH"
    assert result["reasons"] == []


def test_over_budget_listing_returns_rejected(
    profile, valid_listing
):

    valid_listing["price"] = 35000

    result = evaluate_listing(valid_listing, profile)

    assert result["status"] == "REJECTED"
    assert "Price outside budget" in result["reasons"]


def test_missing_metro_information_returns_review(
    profile, valid_listing
):

    valid_listing["metro_walking_minutes"] = None

    result = evaluate_listing(valid_listing, profile)

    assert result["status"] == "REVIEW"


def test_unpreferred_district_returns_rejected(
    profile, valid_listing
):

    valid_listing["district"] = "Besiktas"

    result = evaluate_listing(valid_listing, profile)

    assert result["status"] == "REJECTED"
    assert "District not preferred" in result["reasons"]


def test_over_budget_and_missing_information_returns_rejected(
    profile, valid_listing
):

    valid_listing["price"] = 35000
    valid_listing["metro_walking_minutes"] = None

    result = evaluate_listing(valid_listing, profile)

    assert result["status"] == "REJECTED"


def test_turkish_text_normalization():

    result = normalize_text("Üsküdar")

    assert result == "uskudar"


def test_filter_listings_separates_results(
    profile, valid_listing
):

    second_listing = valid_listing.copy()
    second_listing["price"] = 35000

    third_listing = valid_listing.copy()
    third_listing["metro_walking_minutes"] = None

    results = filter_listings(
        [valid_listing, second_listing, third_listing],
        profile
    )

    assert len(results["MATCH"]) == 1
    assert len(results["REJECTED"]) == 1
    assert len(results["REVIEW"]) == 1
