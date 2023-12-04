import sqlite3
from Helpers.datetime_helper import DateTimeHelper

class LinkData:
    def __init__(self, db_name = 'Project.db'):
        self.db_name = db_name

    def get_link_data(self, link_details):
        conn = sqlite3.connect('Project.db')
        cursor = conn.cursor()
        cursor.execute("""
        SELECT person_ID, Event_type, Link_ID, actType, legMode, Timestamp,
            From_Node, To_Node, Length, Freespeed, Capacity, PermLanes,
            OneWay, Modes, From_X, From_Y, To_X, To_Y
        FROM Connected 
        WHERE Link_ID = ? 
        ORDER BY Timestamp""", (link_details,))
        node_data_raw = cursor.fetchall()
        # Convert 'Timestamp' from seconds to 'HH:MM:SS' format
        node_data = [(data[0], data[1], data[2], data[3], data[4], 
                        DateTimeHelper.seconds_to_hms(data[5]), *data[6:]) for data in node_data_raw]
        conn.close()
        return node_data