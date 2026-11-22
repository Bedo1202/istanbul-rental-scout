
import sqlite3
from pathlib import Path


# Project directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Database location
DB_PATH = PROJECT_ROOT / "data" / "rental_scout.db"


def get_connection():
    """Create a connection to the SQLite database."""

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """Create the listings table if it does not exist."""

    connection = get_connection()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS listings (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                source TEXT NOT NULL,
                source_listing_id TEXT NOT NULL,

                title TEXT NOT NULL,
                price INTEGER NOT NULL,

                district TEXT NOT NULL,
                neighborhood TEXT,

                room_type TEXT NOT NULL,
                furnished INTEGER,

                building_age INTEGER,
                metro_walking_minutes INTEGER,

                listing_url TEXT NOT NULL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                UNIQUE(source, source_listing_id)
            )
        """)

        connection.commit()

    finally:
        connection.close()


def save_listing(listing):
    """Save a listing if it does not already exist."""

    connection = get_connection()

    try:
        cursor = connection.execute("""
            INSERT OR IGNORE INTO listings (
                source,
                source_listing_id,
                title,
                price,
                district,
                neighborhood,
                room_type,
                furnished,
                building_age,
                metro_walking_minutes,
                listing_url
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            listing.source,
            listing.source_listing_id,
            listing.title,
            listing.price,
            listing.district,
            listing.neighborhood,
            listing.room_type,
            None if listing.furnished is None else int(listing.furnished),
            listing.building_age,
            listing.metro_walking_minutes,
            listing.listing_url
        ))

        connection.commit()

        return cursor.rowcount == 1

    finally:
        connection.close()


def get_all_listings():
    """Retrieve all saved listings."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            "SELECT * FROM listings ORDER BY id"
        )

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()
