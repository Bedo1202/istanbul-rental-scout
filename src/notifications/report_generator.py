
from datetime import datetime


def format_value(value, suffix=""):
    """Format values while handling missing information."""

    if value is None or value == "":
        return "Unknown"

    return f"{value}{suffix}"


def generate_report(scored_listings):
    """
    Generate a readable report from scored listings.

    Expected structure:
    [
        {
            "listing": {...},
            "scoring": {...}
        }
    ]
    """

    report_lines = []

    report_lines.append("=" * 55)
    report_lines.append("ISTANBUL RENTAL SCOUT")
    report_lines.append("PROPERTY SEARCH REPORT")
    report_lines.append("=" * 55)

    report_lines.append(
        f"Generated at: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    )

    report_lines.append(
        f"Matching listings: {len(scored_listings)}"
    )

    report_lines.append("-" * 55)

    if not scored_listings:
        report_lines.append(
            "No matching listings found."
        )

        return "\n".join(report_lines)

    # Sort listings by score
    sorted_listings = sorted(
        scored_listings,
        key=lambda item: item["scoring"]["score"],
        reverse=True
    )

    for rank, item in enumerate(sorted_listings, start=1):

        listing = item["listing"]
        scoring = item["scoring"]

        report_lines.append("")
        report_lines.append(
            f"#{rank} - {listing['title']}"
        )

        report_lines.append(
            f"Price: {format_value(listing.get('price'), ' TL')}"
        )

        report_lines.append(
            f"District: {format_value(listing.get('district'))}"
        )

        report_lines.append(
            f"Neighborhood: {format_value(listing.get('neighborhood'))}"
        )

        report_lines.append(
            f"Rooms: {format_value(listing.get('room_type'))}"
        )

        report_lines.append(
            f"Furnished: {format_value(listing.get('furnished'))}"
        )

        report_lines.append(
            f"Building age: {format_value(listing.get('building_age'), ' years')}"
        )

        report_lines.append(
            f"Metro walking: {format_value(listing.get('metro_walking_minutes'), ' min')}"
        )

        report_lines.append(
            f"Score: {scoring['score']}/100"
        )

        report_lines.append(
            f"Data coverage: {scoring['coverage']}%"
        )

        report_lines.append(
            f"URL: {format_value(listing.get('listing_url'))}"
        )

        report_lines.append("-" * 55)

    report_lines.append("")
    report_lines.append("END OF REPORT")
    report_lines.append("=" * 55)

    return "\n".join(report_lines)
