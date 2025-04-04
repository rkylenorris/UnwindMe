from datetime import time
from sqlalchemy.orm import Session
from db import SessionLocal
from models import DimSchedule, TimePeriod

# === Slot Definitions ===

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
WEEKENDS = ["Saturday", "Sunday"]

# Format: (start, end)
weekday_slots = [
    (time(18, 0), time(19, 0)),
    (time(19, 0), time(20, 0)),
    (time(20, 0), time(21, 0)),
    (time(21, 0), time(22, 30)),
]

weekend_slots = [
    (time(10, 0), time(11, 0)), (time(11, 0), time(12, 0)),
    (time(12, 0), time(13, 0)), (time(13, 0), time(14, 0)),
    (time(14, 0), time(15, 0)), (time(15, 0), time(16, 0)),
    (time(16, 0), time(17, 0)), (time(17, 0), time(18, 0)),
    (time(18, 0), time(19, 0)), (time(19, 0), time(20, 0)),
    (time(20, 0), time(21, 0)), (time(21, 0), time(22, 0)),
    (time(22, 0), time(23, 0)),
]

# === Main Logic ===

def get_time_period_id(start, periods):
    for p in periods:
        if p.range_begin <= start < (p.range_end if p.range_end > p.range_begin else time(23, 59)):
            return p.id
        # Handle night wrapping past midnight
        if p.range_begin > p.range_end and (start >= p.range_begin or start < p.range_end):
            return p.id
    return None

def populate_dim_schedule():
    session = SessionLocal()
    time_periods = session.query(TimePeriod).all()

    inserts = []

    for day in WEEKDAYS:
        for start, end in weekday_slots:
            tp_id = get_time_period_id(start, time_periods)
            inserts.append(DimSchedule(day=day, slot_start=start, slot_end=end, time_period_id=tp_id))

    for day in WEEKENDS:
        for start, end in weekend_slots:
            tp_id = get_time_period_id(start, time_periods)
            inserts.append(DimSchedule(day=day, slot_start=start, slot_end=end, time_period_id=tp_id))

    session.bulk_save_objects(inserts)
    session.commit()
    session.close()
    print(f"Inserted {len(inserts)} schedule slots into dim_schedule.")

if __name__ == "__main__":
    populate_dim_schedule()
