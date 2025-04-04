import pandas as pd
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Activity

def import_activities_from_excel(path: str):
    df = pd.read_excel(path, sheet_name="Activities")

    session = SessionLocal()

    for _, row in df.iterrows():
        activity = Activity(
            category_id=int(row["category_id"]),
            name=row["name"],
            instructions=row["instructions"],
            min_time=int(row["min_time"]),
            max_time=int(row["max_time"]),
            prep_time=int(row["prep_time"]) if not pd.isna(row["prep_time"]) else None,
            constraints=row["constraints"]
        )
        session.add(activity)

    session.commit()
    session.close()
    print(f"Imported {len(df)} activities.")

if __name__ == "__main__":
    import_activities_from_excel("data\Activities.xlsx")
