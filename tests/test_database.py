
from types import SimpleNamespace

import pytest

from database import db_manager


@pytest.fixture
def test_database(tmp_path, monkeypatch):

    # Create an isolated test database
    test_db_path = tmp_path / "test_rental.db"

    monkeypatch.setattr(
        db_manager,
        "DB_PATH",
        test_db_path
    )

    db_manager.initialize_database()

    return test_db_path


@pytest.fixture
def sample_listing():

    return SimpleNamespace(
        source="test_source",
        source_listing_id="TEST3001",
        title="Kadikoy 2+1 Furnished Apartment",
        price=27500,
        district="Kadikoy",
        neighborhood="Moda",
        room_type="2+1",
        furnished=True,
        building_age=5,
        metro_walking_minutes=8,
        listing_url="https://example.com/3001"
    )


# 1. New listing test

def test_new_listing_is_inserted(
    test_database, sample_listing
):

    result = db_manager.save_listing(sample_listing)

    listings = db_manager.get_all_listings()

    assert result == "inserted"
    assert len(listings) == 1
    assert listings[0]["price"] == 27500


# 2. Duplicate listing test

def test_duplicate_listing_is_not_inserted(
    test_database, sample_listing
):

    db_manager.save_listing(sample_listing)

    result = db_manager.save_listing(sample_listing)

    listings = db_manager.get_all_listings()

    assert result == "unchanged"
    assert len(listings) == 1


# 3. Price update test

def test_price_change_is_detected(
    test_database, sample_listing
):

    db_manager.save_listing(sample_listing)

    sample_listing.price = 26000

    result = db_manager.save_listing(sample_listing)

    listings = db_manager.get_all_listings()

    assert result == "price_updated"
    assert listings[0]["price"] == 26000


# 4. Price history test

def test_price_history_records_changes(
    test_database, sample_listing
):

    db_manager.save_listing(sample_listing)

    listing_id = db_manager.get_all_listings()[0]["id"]

    sample_listing.price = 26000

    db_manager.save_listing(sample_listing)

    history = db_manager.get_price_history(listing_id)

    assert len(history) == 2
    assert history[0]["price"] == 27500
    assert history[1]["price"] == 26000
