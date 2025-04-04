from db import SessionLocal
from models import Category, Mood, TimePeriod
from datetime import time

def seed_data():
    session = SessionLocal()

    # === Categories ===
    categories = [
        ("Creative Writing", 6, 3),
        ("Reading", 6, 5),
        ("Learning Music", 3, 3),
        ("Coding", 5, 4),
        ("SelfCare", 5, 7),
        ("Gaming", 3, 4),
    ]
    for name, weight, freq in categories:
        session.add(Category(name=name, weight=weight, freq_target=freq))

    # === Moods ===
    moods = [
        ("Creative", 5),
        ("Focused", 5),
        ("Relaxing", 4),
        ("Reflective", 4),
        ("Excited", 3),
        ("Fun", 3),
        ("Escapist", 2),
        ("Peaceful", 3),
    ]
    for name, weight in moods:
        session.add(Mood(name=name, weight=weight))

    # === Time Periods ===
    time_periods = [
        ("Morning", time(6, 0), time(12, 0)),
        ("Afternoon", time(12, 0), time(17, 0)),
        ("Evening", time(17, 0), time(21, 0)),
        ("Night", time(21, 0), time(0, 0)),
    ]
    for name, begin, end in time_periods:
        session.add(TimePeriod(name=name, range_begin=begin, range_end=end))

    session.commit()
    session.close()
    print("Seeded categories, moods, and time periods.")

if __name__ == "__main__":
    seed_data()
