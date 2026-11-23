
from types import SimpleNamespace

import pytest

from database import db_manager
from notifications import notification_manager


@pytest.fixture
def test_database(tmp_path, monkeypatch):

    test_db_path = tmp_path / "notification_test.db"

    monkeypatch.setattr(
        db_manager,
        "DB_PATH",
        test_db_path
    )

    db_manager.initialize_database()

    notification_manager.initialize_notification_table()

    return test_db_path


@pytest.fixture
def scored_listings(test_database):

    listings = []

    for index in range(2):

        listing = SimpleNamespace(
            source="test_source",
            source_listing_id=f"TEST{index + 1}",
            title=f"Test Apartment {index + 1}",
            price=25000,
            district="Kadikoy",
            neighborhood="Moda",
            room_type="2+1",
            furnished=True,
            building_age=5,
            metro_walking_minutes=8,
            listing_url=f"https://example.com/{index + 1}"
        )

        db_manager.save_listing(listing)

    database_listings = db_manager.get_all_listings()

    for listing in database_listings:

        listings.append({
            "listing": listing,
            "scoring": {
                "score": 80,
                "coverage": 100
            }
        })

    return listings


def test_all_new_listings_are_unnotified(scored_listings):

    result = notification_manager.get_unnotified_listings(
        scored_listings
    )

    assert len(result) == 2


def test_notified_listing_is_not_returned_again(scored_listings):

    notification_manager.mark_listings_notified(
        [scored_listings[0]]
    )

    result = notification_manager.get_unnotified_listings(
        scored_listings
    )

    assert len(result) == 1

    assert result[0]["listing"]["id"] == (
        scored_listings[1]["listing"]["id"]
    )


def test_duplicate_notification_is_prevented(scored_listings):

    first_result = notification_manager.mark_listings_notified(
        [scored_listings[0]]
    )

    second_result = notification_manager.mark_listings_notified(
        [scored_listings[0]]
    )

    assert first_result == 1
    assert second_result == 0


def test_all_listings_can_be_marked_notified(scored_listings):

    notification_manager.mark_listings_notified(
        scored_listings
    )

    result = notification_manager.get_unnotified_listings(
        scored_listings
    )

    assert len(result) == 0

