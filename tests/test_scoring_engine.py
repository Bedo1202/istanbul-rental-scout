
import pytest

from analysis.scoring_engine import (
    calculate_price_score,
    calculate_transport_score,
    calculate_building_score,
    score_listing
)


# Test profile
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
        },
        "scoring": {
            "price": 35,
            "location": 30,
            "transport": 20,
            "building": 10,
            "listing_quality": 5
        }
    }


# 1. Price score tests

def test_minimum_budget_gets_100_points(profile):

    result = calculate_price_score(20000, profile)

    assert result == 100


def test_middle_budget_gets_50_points(profile):

    result = calculate_price_score(25000, profile)

    assert result == 50


def test_maximum_budget_gets_zero_points(profile):

    result = calculate_price_score(30000, profile)

    assert result == 0


# 2. Transport score tests

def test_maximum_metro_distance_gets_zero_points(profile):

    result = calculate_transport_score(15, profile)

    assert result == 0


def test_zero_metro_distance_gets_100_points(profile):

    result = calculate_transport_score(0, profile)

    assert result == 100


# 3. Building score tests

def test_new_building_gets_100_points():

    result = calculate_building_score(0)

    assert result == 100


def test_30_year_old_building_gets_zero_points():

    result = calculate_building_score(30)

    assert result == 0


def test_negative_building_age_raises_error():

    with pytest.raises(ValueError):

        calculate_building_score(-1)


# 4. Missing information test

def test_missing_building_age_does_not_get_zero_score(profile):

    listing = {
        "title": "Kadikoy 2+1 Furnished Apartment",
        "price": 25000,
        "district": "Kadikoy",
        "room_type": "2+1",
        "furnished": 1,
        "neighborhood": "Moda",
        "listing_url": "https://example.com/listing/1",
        "metro_walking_minutes": 5,
        "building_age": None
    }

    result = score_listing(listing, profile)

    assert result["breakdown"]["building"] is None

    assert result["coverage"] == 90
