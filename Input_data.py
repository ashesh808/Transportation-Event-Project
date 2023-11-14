import sqlite3
import xml.etree.ElementTree as ET

# Set up SQLite database and tables
conn = sqlite3.connect('Project.db')
cursor = conn.cursor()

# Define the schema based on the ER diagram
cursor.executescript('''
CREATE TABLE IF NOT EXISTS Nodes (
    ID TEXT PRIMARY KEY,
    X REAL NOT NULL,
    Y REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS Links (
    Link_ID TEXT PRIMARY KEY,
    "From" REAL,
    "To" REAL,
    Length REAL,
    Freespeed REAL,
    Capacity REAL,
    PermLanes INTEGER,
    OneWay INTEGER,
    Modes TEXT,
    FOREIGN KEY("From") REFERENCES Nodes(ID),
    FOREIGN KEY("To") REFERENCES Nodes(ID)
);

CREATE TABLE IF NOT EXISTS Person (
    person_ID TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Transactions (
    transaction_ID TEXT PRIMARY KEY,
    person_ID TEXT,
    transactionPartner TEXT,
    amount REAL,
    purpose TEXT,
    eventTime TEXT,
    transactionDate DATE,
    FOREIGN KEY(person_ID) REFERENCES Person(person_ID)
);

CREATE TABLE IF NOT EXISTS Events (
    Event_ID TEXT PRIMARY KEY,
    Event_type TEXT NOT NULL,
    Person_ID TEXT,
    Link_ID TEXT,
    actType TEXT,
    Leg_Mode TEXT,
    Timestamp DATETIME,
    FOREIGN KEY(Person_ID) REFERENCES Person(person_ID),
    FOREIGN KEY(Link_ID) REFERENCES Links(Link_ID)
);
''')

# Parse network.xml to populate Nodes and Links
tree = ET.parse('network.xml')
root = tree.getroot()

# Inserting nodes data
for node in root.findall('nodes/node'):
    cursor.execute('INSERT INTO Nodes (ID, X, Y) VALUES (?, ?, ?)', 
                   (node.attrib['id'], node.attrib['x'], node.attrib['y']))

# Inserting links data
for link in root.findall('links/link'):
    cursor.execute('INSERT INTO Links (Link_ID, "From", "To", Length, Freespeed, Capacity, PermLanes, OneWay, Modes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                   (link.attrib['id'], link.attrib['from'], link.attrib['to'], link.attrib['length'], link.attrib['freespeed'], link.attrib['capacity'], link.attrib['permlanes'], link.attrib['oneway'], link.attrib['modes']))

# Counter for transaction IDs
i = 1

# Now, let's parse output_events.xml to populate Person, Transactions, and Events
tree_events = ET.parse('output_events.xml')
root_events = tree_events.getroot()

# Inserting person data
for person in root_events.findall('.//event[@type="actstart"]'):
    person_id = person.get('person', '')
    if person_id:
        cursor.execute('INSERT OR IGNORE INTO Person (person_ID) VALUES (?)', 
                       (person_id,))

# Inserting events data
for event in root_events.findall('.//event'):
    event_type = event.get('type', '')
    person_id = event.get('person', None)
    link_id = event.get('link', None)
    act_type = event.get('actType', None)
    leg_mode = event.get('mode', None)
    timestamp = event.get('time', None)
    
    cursor.execute('INSERT INTO Events (Event_type, Person_ID, Link_ID, actType, Leg_Mode, Timestamp) VALUES (?, ?, ?, ?, ?, ?)', 
                   (event_type, person_id, link_id, act_type, leg_mode, timestamp))
    
    # If the event is a transaction event
    if event_type in ['taxi interaction', 'Uber transaction']:
        transaction_id = "txn_" + str(i)
        i += 1
        transaction_partner = event.get('transactionPartner', None)
        amount = event.get('amount', None)
        purpose = event.get('purpose', None)
        event_time = event.get('time', None)
        # Assuming the XML contains the transaction date (adjust accordingly if not)
        transaction_date = event.get('date', None)  
        
        cursor.execute('INSERT INTO Transactions (transaction_ID, person_ID, transactionPartner, amount, purpose, eventTime, transactionDate) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                       (transaction_id, person_id, transaction_partner, amount, purpose, event_time, transaction_date))

# Commit changes and close the connection
conn.commit()
conn.close()
