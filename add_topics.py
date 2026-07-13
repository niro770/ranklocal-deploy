#!/usr/bin/env python3
"""One-time script to add Locksmith + buy-calls topics to the queue."""
import json

QUEUE = r"C:\Users\19522\Documents\ranklocal-deploy-push\topic_queue.json"

states = [
    ("Arizona", "arizona"), ("Georgia", "georgia"), ("North Carolina", "north-carolina"),
    ("Colorado", "colorado"), ("Illinois", "illinois"), ("Virginia", "virginia"),
    ("Washington", "washington"), ("Nevada", "nevada"), ("New York", "new-york"),
    ("Pennsylvania", "pennsylvania"), ("Tennessee", "tennessee"), ("South Carolina", "south-carolina"),
    ("Maryland", "maryland"), ("Massachusetts", "massachusetts"), ("Minnesota", "minnesota"),
    ("Missouri", "missouri"), ("Ohio", "ohio"), ("Michigan", "michigan"),
    ("Oregon", "oregon"), ("Indiana", "indiana"), ("Wisconsin", "wisconsin"),
    ("Louisiana", "louisiana"), ("Alabama", "alabama"), ("Kentucky", "kentucky"),
    ("Iowa", "iowa"), ("Kansas", "kansas"), ("Oklahoma", "oklahoma"),
    ("Utah", "utah"), ("Connecticut", "connecticut"), ("New Jersey", "new-jersey"),
    ("Arkansas", "arkansas"), ("Mississippi", "mississippi"), ("New Mexico", "new-mexico"),
    ("Idaho", "idaho"), ("Nebraska", "nebraska"), ("West Virginia", "west-virginia"),
    ("Maine", "maine"), ("Hawaii", "hawaii"),
]

buy_calls_trades = [
    ("Roofing", "roofing"), ("HVAC", "hvac"), ("Plumbing", "plumbing"),
    ("Pest Control", "pest-control"), ("Landscaping", "landscaping"), ("Fencing", "fencing"),
    ("Garage Door", "garage-door"), ("Electrical", "electrical"), ("Painting", "painting"),
    ("Window Replacement", "window-replacement"), ("Siding", "siding"), ("Gutters", "gutter"),
    ("Pressure Washing", "pressure-washing"), ("Tree Service", "tree-service"),
    ("Insulation", "insulation"), ("Locksmith", "locksmith"),
]

with open(QUEUE, "r", encoding="utf-8") as f:
    queue = json.load(f)

existing_slugs = {t["slug"] for t in queue}
new_topics = []

# 1. Locksmith service leads x 38 states
for state_name, state_slug in states:
    slug = "locksmith-leads-" + state_slug
    if slug not in existing_slugs:
        new_topics.append({"slug": slug, "type": "service",
                           "trade": "Locksmith", "state": state_name, "status": "pending"})

# 2. Buy-calls x 16 trades x 38 states
for trade_name, trade_slug in buy_calls_trades:
    for state_name, state_slug in states:
        slug = "buy-" + trade_slug + "-calls-" + state_slug
        if slug not in existing_slugs:
            new_topics.append({"slug": slug, "type": "buy-calls",
                               "trade": trade_name, "state": state_name, "status": "pending"})

queue.extend(new_topics)

with open(QUEUE, "w", encoding="utf-8") as f:
    json.dump(queue, f, indent=2, ensure_ascii=False)

pending = sum(1 for t in queue if t["status"] == "pending")
print("Added:", len(new_topics), "new topics")
print("Total queue:", len(queue))
print("Pending:", pending)
print("Days of content at 50/day:", round(pending / 50, 1))
