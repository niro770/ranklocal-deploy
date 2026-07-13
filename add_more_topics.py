"""
add_more_topics.py — append 3,520 new topics to topic_queue.json

5 new state-level types × 16 trades × 38 states = 3,040
1 city-level type × 16 trades × 30 cities = 480
Total new = 3,520
"""

import json, os, re

QUEUE = os.path.join(os.path.dirname(__file__), "topic_queue.json")

# ── same 16 trades as weekly_seo_batch.py ────────────────────────────────────
TRADES = [
    "Roofing", "Fencing", "Landscaping", "Pest Control", "Garage Door Repair",
    "HVAC", "Plumbing", "Electrical", "Window Replacement", "Siding",
    "Gutter Installation", "Concrete", "Painting", "Insulation",
    "Pressure Washing", "Tree Service",
]

# ── same 38 states as topic_queue.json ───────────────────────────────────────
STATES = [
    ("Alabama",        "alabama"),
    ("Arizona",        "arizona"),
    ("Arkansas",       "arkansas"),
    ("California",     "california"),
    ("Colorado",       "colorado"),
    ("Connecticut",    "connecticut"),
    ("Florida",        "florida"),
    ("Georgia",        "georgia"),
    ("Idaho",          "idaho"),
    ("Illinois",       "illinois"),
    ("Indiana",        "indiana"),
    ("Iowa",           "iowa"),
    ("Kansas",         "kansas"),
    ("Kentucky",       "kentucky"),
    ("Louisiana",      "louisiana"),
    ("Maryland",       "maryland"),
    ("Massachusetts",  "massachusetts"),
    ("Michigan",       "michigan"),
    ("Minnesota",      "minnesota"),
    ("Missouri",       "missouri"),
    ("Nevada",         "nevada"),
    ("New Jersey",     "new-jersey"),
    ("New York",       "new-york"),
    ("North Carolina", "north-carolina"),
    ("Ohio",           "ohio"),
    ("Oklahoma",       "oklahoma"),
    ("Oregon",         "oregon"),
    ("Pennsylvania",   "pennsylvania"),
    ("South Carolina", "south-carolina"),
    ("Tennessee",      "tennessee"),
    ("Texas",          "texas"),
    ("Utah",           "utah"),
    ("Virginia",       "virginia"),
    ("Washington",     "washington"),
    ("Wisconsin",      "wisconsin"),
    ("New Mexico",     "new-mexico"),
    ("Nebraska",       "nebraska"),
    ("Mississippi",    "mississippi"),
]

# ── 30 cities matching CITY_DATA in weekly_seo_batch.py ──────────────────────
CITIES = [
    ("Phoenix",       "phoenix",       "Arizona"),
    ("Atlanta",       "atlanta",       "Georgia"),
    ("Charlotte",     "charlotte",     "North Carolina"),
    ("Raleigh",       "raleigh",       "North Carolina"),
    ("Denver",        "denver",        "Colorado"),
    ("Chicago",       "chicago",       "Illinois"),
    ("Seattle",       "seattle",       "Washington"),
    ("Las Vegas",     "las-vegas",     "Nevada"),
    ("New York City", "new-york-city", "New York"),
    ("Philadelphia",  "philadelphia",  "Pennsylvania"),
    ("Nashville",     "nashville",     "Tennessee"),
    ("Baltimore",     "baltimore",     "Maryland"),
    ("Boston",        "boston",        "Massachusetts"),
    ("Minneapolis",   "minneapolis",   "Minnesota"),
    ("Kansas City",   "kansas-city",   "Missouri"),
    ("Columbus",      "columbus",      "Ohio"),
    ("Detroit",       "detroit",       "Michigan"),
    ("Portland",      "portland",      "Oregon"),
    ("Indianapolis",  "indianapolis",  "Indiana"),
    ("Milwaukee",     "milwaukee",     "Wisconsin"),
    ("New Orleans",   "new-orleans",   "Louisiana"),
    ("Birmingham",    "birmingham",    "Alabama"),
    ("Louisville",    "louisville",    "Kentucky"),
    ("Oklahoma City", "oklahoma-city", "Oklahoma"),
    ("Salt Lake City","salt-lake-city","Utah"),
    ("Hartford",      "hartford",      "Connecticut"),
    ("Newark",        "newark",        "New Jersey"),
    ("Richmond",      "richmond",      "Virginia"),
    ("Wichita",       "wichita",       "Kansas"),
    ("Columbia",      "columbia",      "South Carolina"),
]


def trade_slug(trade):
    return trade.lower().replace(" ", "-")


def make_slug_safe(s):
    return re.sub(r"[^a-z0-9-]", "", s.lower().replace(" ", "-").replace("_", "-"))


def main():
    # Load existing queue and collect existing slugs
    with open(QUEUE, "r", encoding="utf-8") as f:
        queue = json.load(f)

    existing_slugs = {t["slug"] for t in queue}
    print(f"Existing topics: {len(queue)} (slugs known: {len(existing_slugs)})")

    new_topics = []

    # ── 5 new state-level types ───────────────────────────────────────────────
    for trade in TRADES:
        ts = trade_slug(trade)
        for state_name, state_sl in STATES:
            # exclusive-leads
            sl = "exclusive-" + ts + "-leads-" + state_sl
            if sl not in existing_slugs:
                new_topics.append({
                    "slug": sl,
                    "type": "exclusive-leads",
                    "trade": trade,
                    "state": state_name,
                    "status": "pending",
                })
                existing_slugs.add(sl)

            # pay-per-call
            sl = ts + "-pay-per-call-" + state_sl
            if sl not in existing_slugs:
                new_topics.append({
                    "slug": sl,
                    "type": "pay-per-call",
                    "trade": trade,
                    "state": state_name,
                    "status": "pending",
                })
                existing_slugs.add(sl)

            # appointment-setting
            sl = ts + "-appointment-setting-" + state_sl
            if sl not in existing_slugs:
                new_topics.append({
                    "slug": sl,
                    "type": "appointment-setting",
                    "trade": trade,
                    "state": state_name,
                    "status": "pending",
                })
                existing_slugs.add(sl)

            # contractor-leads
            sl = ts + "-contractor-leads-" + state_sl
            if sl not in existing_slugs:
                new_topics.append({
                    "slug": sl,
                    "type": "contractor-leads",
                    "trade": trade,
                    "state": state_name,
                    "status": "pending",
                })
                existing_slugs.add(sl)

            # phone-leads
            sl = ts + "-phone-leads-" + state_sl
            if sl not in existing_slugs:
                new_topics.append({
                    "slug": sl,
                    "type": "phone-leads",
                    "trade": trade,
                    "state": state_name,
                    "status": "pending",
                })
                existing_slugs.add(sl)

    # ── city-leads ────────────────────────────────────────────────────────────
    for trade in TRADES:
        ts = trade_slug(trade)
        for city_name, city_sl, state_name in CITIES:
            sl = ts + "-leads-" + city_sl
            if sl not in existing_slugs:
                new_topics.append({
                    "slug": sl,
                    "type": "city-leads",
                    "trade": trade,
                    "city": city_name,
                    "state": state_name,
                    "status": "pending",
                })
                existing_slugs.add(sl)

    print(f"New topics to add: {len(new_topics)}")

    queue.extend(new_topics)

    with open(QUEUE, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2)

    print(f"Queue saved: {len(queue)} total topics")
    pending = sum(1 for t in queue if t["status"] == "pending")
    print(f"Pending: {pending} | Done: {len(queue) - pending}")


if __name__ == "__main__":
    main()
