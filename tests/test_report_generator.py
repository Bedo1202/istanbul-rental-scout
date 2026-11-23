
from notifications.report_generator import generate_report


def test_report_contains_listing_information():

    scored_listings = [
        {
            "listing": {
                "title": "Kadikoy 2+1 Furnished Apartment",
                "price": 27000,
                "district": "Kadikoy",
                "neighborhood": "Moda",
                "room_type": "2+1",
                "furnished": True,
                "building_age": 5,
                "metro_walking_minutes": 8,
                "listing_url": "https://example.com/1"
            },
            "scoring": {
                "score": 85.5,
                "coverage": 100
            }
        }
    ]

    report = generate_report(scored_listings)

    assert "ISTANBUL RENTAL SCOUT" in report
    assert "27000 TL" in report
    assert "Kadikoy" in report
    assert "85.5/100" in report
    assert "https://example.com/1" in report


def test_report_handles_empty_listings():

    report = generate_report([])

    assert "Matching listings: 0" in report
    assert "No matching listings found." in report


def test_report_handles_missing_information():

    scored_listings = [
        {
            "listing": {
                "title": "Test Apartment",
                "price": 25000,
                "district": "Maltepe",
                "room_type": "2+1",
                "furnished": True,
                "listing_url": "https://example.com/2"
            },
            "scoring": {
                "score": 70,
                "coverage": 90
            }
        }
    ]

    report = generate_report(scored_listings)

    assert "Building age: Unknown" in report
    assert "Metro walking: Unknown" in report
