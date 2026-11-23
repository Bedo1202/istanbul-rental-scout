
from database import db_manager


def initialize_notification_table():
    """Create notification log table if it does not exist."""

    connection = db_manager.get_connection()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS notification_log (
                listing_id INTEGER PRIMARY KEY,
                notified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (listing_id)
                    REFERENCES listings(id)
            )
        """)

        connection.commit()

    finally:
        connection.close()


def get_unnotified_listings(scored_listings):
    """Return matching listings that have not been notified."""

    initialize_notification_table()

    connection = db_manager.get_connection()

    try:
        cursor = connection.execute("""
            SELECT listing_id
            FROM notification_log
        """)

        notified_ids = {
            row["listing_id"]
            for row in cursor.fetchall()
        }

    finally:
        connection.close()

    unnotified = []
    seen_ids = set()

    for item in scored_listings:

        listing = item["listing"]
        listing_id = listing.get("id")

        if listing_id is None:
            raise ValueError("Listing ID is required.")

        if listing_id not in notified_ids and listing_id not in seen_ids:

            unnotified.append(item)
            seen_ids.add(listing_id)

    return unnotified


def mark_listings_notified(scored_listings):
    """Record listings after successful notification delivery."""

    initialize_notification_table()

    connection = db_manager.get_connection()

    inserted_count = 0

    try:
        for item in scored_listings:

            listing_id = item["listing"].get("id")

            if listing_id is None:
                raise ValueError("Listing ID is required.")

            cursor = connection.execute("""
                INSERT OR IGNORE INTO notification_log (listing_id)
                VALUES (?)
            """, (listing_id,))

            inserted_count += cursor.rowcount

        connection.commit()

        return inserted_count

    finally:
        connection.close()
