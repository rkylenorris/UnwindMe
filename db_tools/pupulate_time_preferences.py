import re
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Activity, TimePeriod, ActivityTimePreference

# === TIME KEYWORDS PER DAY TYPE ===
weekday_keywords = {
    "Morning": ["headspace", "meditate", "routine"],
    "Evening": ["project", "course", "relax", "after work", "game", "write"],
    "Night": ["journal", "reflect", "unwind", "meditate"]
}

weekend_keywords = {
    "Morning": ["journal", "meditate", "read", "start", "fresh", "quiet"],
    "Afternoon": ["course", "project", "reading", "learn", "practice"],
    "Evening": ["game", "friends", "write", "creative", "co-op", "relax"],
    "Night": ["poetry", "story", "solo", "journal", "reflect"]
}

# Extract matches from a set of keywords
def match_time_periods(text, keyword_map, time_map):
    text = text.lower()
    matched_ids = set()
    for name, keywords in keyword_map.items():
        if any(re.search(rf"\b{kw}\b", text) for kw in keywords):
            period_id = time_map.get(name)
            if period_id:
                matched_ids.add(period_id)
    return matched_ids

def tag_activities_with_time_preferences():
    session = SessionLocal()

    # Build time period name → id map
    time_periods = session.query(TimePeriod).all()
    time_map = {tp.name: tp.id for tp in time_periods}

    activities = session.query(Activity).all()
    inserts = []

    for activity in activities:
        text = f"{activity.name} {activity.instructions}"

        # === Weekday Preferences ===
        weekday_ids = match_time_periods(text, weekday_keywords, time_map)
        if not weekday_ids:
            weekday_ids = {time_map["Evening"]}  # Default fallback

        for tp_id in weekday_ids:
            inserts.append(ActivityTimePreference(
                activity_id=activity.id,
                time_period_id=tp_id,
                preference_weight=1,
                day_type="Weekday"
            ))

        # === Weekend Preferences ===
        weekend_ids = match_time_periods(text, weekend_keywords, time_map)
        if not weekend_ids:
            weekend_ids = {time_map["Afternoon"]}  # Default fallback

        for tp_id in weekend_ids:
            inserts.append(ActivityTimePreference(
                activity_id=activity.id,
                time_period_id=tp_id,
                preference_weight=1,
                day_type="Weekend"
            ))

    session.bulk_save_objects(inserts)
    session.commit()
    session.close()
    print(f"Inserted {len(inserts)} time preferences across weekday and weekend.")

if __name__ == "__main__":
    tag_activities_with_time_preferences()
