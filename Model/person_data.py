import sqlite3

class PersonData:
    def __init__(self, db_name = 'Project.db'):
        self.db_name = db_name

    def get_person_data(self, person_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT person_ID, Event_type, Link_ID, actType, legMode, Timestamp,
                From_Node, To_Node, Length, Freespeed, Capacity, PermLanes,
                OneWay, Modes, From_X, From_Y, To_X, To_Y
            FROM Connected 
            WHERE person_ID = ? 
            ORDER BY Timestamp""", (person_id,))
        data = cursor.fetchall()
        conn.close()
        return data