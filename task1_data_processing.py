import requests
import time
import json
import os
from datetime import datetime

# -------------------------------
# Configuration
# -------------------------------
BASE_URL = "https://hacker-news.firebaseio.com/v0"
HEADERS = {"User-Agent": "TrendPulse/1.0"}

# Categories and keywords
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

MAX_PER_CATEGORY = 25


# -------------------------------
# Helper: Assign category
# -------------------------------
def get_category(title):
    title_lower = title.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    return None


# -------------------------------
# Step 1: Get top story IDs
# -------------------------------
try:
    response = requests.get(f"{BASE_URL}/topstories.json", headers=HEADERS)
    response.raise_for_status()
    top_ids = response.json()[:500]
except Exception as e:
    print("Failed to fetch top stories:", e)
    top_ids = []

# -------------------------------
# Step 2: Fetch story details
# -------------------------------
collected_data = []
category_count = {cat: 0 for cat in CATEGORIES}

for category in CATEGORIES:
    print(f"\nCollecting category: {category}")

    for story_id in top_ids:
        if category_count[category] >= MAX_PER_CATEGORY:
            break

        try:
            url = f"{BASE_URL}/item/{story_id}.json"
            res = requests.get(url, headers=HEADERS)
            res.raise_for_status()
            story = res.json()

            # Skip if no title
            if not story or "title" not in story:
                continue

            # Check category match
            assigned_category = get_category(story["title"])
            if assigned_category != category:
                continue

            # Extract required fields
            data = {
                "post_id": story.get("id"),
                "title": story.get("title"),
                "category": assigned_category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", "unknown"),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            collected_data.append(data)
            category_count[category] += 1

        except Exception as e:
            print(f"Failed to fetch story {story_id}: {e}")
            continue

    # Sleep after each category
    time.sleep(2)

# -------------------------------
# Step 3: Save JSON
# -------------------------------
# Create data folder if not exists
os.makedirs("data", exist_ok=True)

# File name with date
filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(collected_data, f, indent=4)

# -------------------------------
# Final Output
# -------------------------------
print(f"\nCollected {len(collected_data)} stories.")
print(f"Saved to {filename}")
