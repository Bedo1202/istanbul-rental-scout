
import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "data" / "rental_scout.db"


def get_connection():
    """Create a connection to the SQLite database."""

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database():
    """Create database tables if they do not exist."""

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

        connection.execute("""
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                listing_id INTEGER NOT NULL,
                price INTEGER NOT NULL,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (listing_id)
                REFERENCES listings(id)
            )
        """)

        connection.commit()

    finally:
        connection.close()


def save_listing(listing):
    """
    Insert a new listing or update an existing listing.
    Record price changes in price_history.
    """

    connection = get_connection()

    try:
        existing = connection.execute("""
            SELECT id, price
            FROM listings
            WHERE source = ? AND source_listing_id = ?
        """, (
            listing.source,
            listing.source_listing_id
        )).fetchone()

        # New listing
        if existing is None:

            cursor = connection.execute("""
                INSERT INTO listings (
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

            listing_id = cursor.lastrowid

            connection.execute("""
                INSERT INTO price_history (listing_id, price)
                VALUES (?, ?)
            """, (listing_id, listing.price))

            connection.commit()
            return "inserted"

        # Existing listing
        listing_id = existing["id"]
        old_price = existing["price"]

        # Add baseline history for listings created before this feature
        history_exists = connection.execute("""
            SELECT 1
            FROM price_history
            WHERE listing_id = ?
            LIMIT 1
        """, (listing_id,)).fetchone()

        if history_exists is None:
            connection.execute("""
                INSERT INTO price_history (listing_id, price)
                VALUES (?, ?)
            """, (listing_id, old_price))

        # Check for price change
        if listing.price != old_price:

            connection.execute("""
                UPDATE listings
                SET price = ?
                WHERE id = ?
            """, (listing.price, listing_id))

            connection.execute("""
                INSERT INTO price_history (listing_id, price)
                VALUES (?, ?)
            """, (listing_id, listing.price))

            connection.commit()
            return "price_updated"

        connection.commit()
        return "unchanged"

    finally:
        connection.close()


def get_all_listings():
    """Retrieve all saved listings."""

    connection = get_connection()

    try:
        cursor = connection.execute("""
            SELECT *
            FROM listings
            ORDER BY id
        """)

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


def get_price_history(listing_id):
    """Retrieve the price history of a listing."""

    connection = get_connection()

    try:
        cursor = connection.execute("""
            SELECT price, recorded_at
            FROM price_history
            WHERE listing_id = ?
            ORDER BY id
        """, (listing_id,))

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()
