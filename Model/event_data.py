import sqlite3
from Helpers.datetime_helper import DateTimeHelper

class EventData:
    def __init__(self, db_name = 'Project.db'):
        self.db_name = db_name

    def get_event_data(self, start_time_str, end_time_str, link_id):
        # Convert HH:MM:SS to seconds
        start_time = DateTimeHelper.hms_to_seconds(start_time_str) if start_time_str else None
        end_time = DateTimeHelper.hms_to_seconds(end_time_str) if end_time_str else None
        conn = sqlite3.connect('Project.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT person_ID, Event_type, Link_ID, actType, legMode, Timestamp,
            From_Node, To_Node, Length, Freespeed, Capacity, PermLanes,
            OneWay, Modes, From_X, From_Y, To_X, To_Y
            FROM Connected 
            WHERE Timestamp BETWEEN ? AND ? AND Link_ID = ?
            ORDER BY Timestamp""", (start_time, end_time, link_id))
        events = cursor.fetchall()
        # Convert seconds back to HH:MM:SS for display
        events = [(event[0], event[1], event[2], event[3], event[4], 
                    DateTimeHelper.seconds_to_hms(event[5]), *event[6:]) for event in events]
        return events
        
