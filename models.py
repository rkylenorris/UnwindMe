from sqlalchemy import Column, Integer, String, Time, Boolean, ForeignKey, Date, Text, DateTime
from sqlalchemy.orm import relationship
from db import Base

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    weight = Column(Integer, nullable=False)
    freq_target = Column(Integer, nullable=False, default=1)

    activities = relationship("Activity", back_populates="category")


class Mood(Base):
    __tablename__ = 'moods'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    weight = Column(Integer, nullable=False)


class TimePeriod(Base):
    __tablename__ = 'time_periods'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    range_begin = Column(Time, nullable=False)
    range_end = Column(Time, nullable=False)


class Activity(Base):
    __tablename__ = 'activities'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    name = Column(String, nullable=False)
    instructions = Column(Text, nullable=False)
    min_time = Column(Integer, nullable=False) # in minutes
    max_time = Column(Integer, nullable=False) # in minutes
    prep_time = Column(Integer) # in minutes
    constraints = Column(Text)

    category = relationship("Category", back_populates="activities")
    moods = relationship("Mood", secondary="activity_moods", backref="activities")
    preferred_times = relationship("TimePeriod", secondary="activity_time_preferences", backref="preferred_activities")


class ActivityMood(Base):
    __tablename__ = 'activity_moods'
    activity_id = Column(Integer, ForeignKey('activities.id'), primary_key=True)
    mood_id = Column(Integer, ForeignKey('moods.id'), primary_key=True)


class ActivityTimePreference(Base):
    __tablename__ = 'activity_time_preferences'
    activity_id = Column(Integer, ForeignKey('activities.id'), primary_key=True)
    time_period_id = Column(Integer, ForeignKey('time_periods.id'), primary_key=True)
    preference_weight = Column(Integer, default=1)


class DimSchedule(Base):
    __tablename__ = 'dim_schedule'
    id = Column(Integer, primary_key=True)
    day = Column(String, nullable=False)
    slot_start = Column(Time, nullable=False)
    slot_end = Column(Time, nullable=False)
    time_period_id = Column(Integer, ForeignKey('time_periods.id'))


class WeeklySchedule(Base):
    __tablename__ = 'weekly_schedule'
    id = Column(Integer, primary_key=True)
    slot_id = Column(Integer, ForeignKey('dim_schedule.id'))
    activity_id = Column(Integer, ForeignKey('activities.id'))
    date = Column(Date, nullable=False)
    time_goal = Column(Integer, nullable=False) # in minutes
    actual_time_spent = Column(Integer) # in minutes
    assigned = Column(DateTime)
    completed = Column(Boolean, default=False)
