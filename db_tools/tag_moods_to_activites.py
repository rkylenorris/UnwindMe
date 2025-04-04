from sqlalchemy.orm import Session
from models import Activity, Mood, ActivityMood
from db import SessionLocal
import re

# Define keywords for each mood
mood_keywords = {
    "Creative": ["write", "poetry", "novel", "music", "draw", "story", "prompt", "project"],
    "Focused": ["learn", "course", "code", "continue", "essay", "practice", "reading"],
    "Relaxing": ["read", "story", "book", "solo game", "journal"],
    "Reflective": ["journal", "essay", "write", "meditate"],
    "Excited": ["brainstorm", "fun", "fast", "challenging", "exciting"],
    "Fun": ["game", "friends", "play", "fun"],
    "Escapist": ["game", "online", "discord", "solo"],
    "Peaceful": ["meditate", "quiet", "journal"]
}

def tag_activities_with_moods():
    session = SessionLocal()
    moods = {m.name: m.id for m in session.query(Mood).all()}
    activities = session.query(Activity).all()

    for activity in activities:
        text = f"{activity.name.lower()} {activity.instructions.lower()}"
        assigned = set()

        for mood, keywords in mood_keywords.items():
            if any(re.search(rf"\b{kw}\b", text) for kw in keywords):
                mood_id = moods.get(mood)
                if mood_id:
                    assigned.add((activity.id, mood_id))

        for act_id, mood_id in assigned:
            session.merge(ActivityMood(activity_id=act_id, mood_id=mood_id))

    session.commit()
    session.close()
    print("Tagged activities with moods.")

if __name__ == "__main__":
    tag_activities_with_moods()
