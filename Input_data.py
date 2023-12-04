import sqlite3
import xml.etree.ElementTree as ET

# Connect to a SQLite database called 'Project.db'. If it doesn't exist, it will be created.
conn = sqlite3.connect('Project.db')
cursor = conn.cursor()

# Create some tables in the database to store different types of data.
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

# Read data from an XML file named 'network.xml' to put into our Nodes and Links tables.
tree = ET.parse('network.xml')
root = tree.getroot()

# Go through each node in the XML and add its details to the Nodes table.
for node in root.findall('nodes/node'):
    cursor.execute('INSERT INTO Nodes (ID, X, Y) VALUES (?, ?, ?)', 
                   (node.attrib['id'], node.attrib['x'], node.attrib['y']))

# Go through each link in the XML and add its details to the Links table.
for link in root.findall('links/link'):
    cursor.execute('INSERT INTO Links (Link_ID, "From", "To", Length, Freespeed, Capacity, PermLanes, OneWay, Modes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                   (link.attrib['id'], link.attrib['from'], link.attrib['to'], link.attrib['length'], link.attrib['freespeed'], link.attrib['capacity'], link.attrib['permlanes'], link.attrib['oneway'], link.attrib['modes']))

# Set up a counter for creating unique transaction IDs.
i = 1

# Read data from another XML file named 'output_events.xml' to put into Person, Transactions, and Events tables.
tree_events = ET.parse('output_events.xml')
root_events = tree_events.getroot()

# Go through each 'actstart' event and add person details to the Person table.
for person in root_events.findall('.//event[@type="actstart"]'):
    person_id = person.get('person', '')
    if person_id:
        cursor.execute('INSERT OR IGNORE INTO Person (person_ID) VALUES (?)', 
                       (person_id,))

# Go through each event and add its details to the Events table.
for event in root_events.findall('.//event'):
    event_type = event.get('type', '')
    person_id = event.get('person', None)
    link_id = event.get('link', None)
    act_type = event.get('actType', None)
    leg_mode = event.get('mode', None)
    timestamp = event.get('time', None)
    
    cursor.execute('INSERT INTO Events (Event_type, Person_ID, Link_ID, actType, Leg_Mode, Timestamp) VALUES (?, ?, ?, ?, ?, ?)', 
                   (event_type, person_id, link_id, act_type, leg_mode, timestamp))
    
    # Check if the event is a transaction (like a taxi interaction) and then add it to the Transactions table.
    if event_type in ['taxi interaction', 'Uber transaction']:
        transaction_id = "txn_" + str(i)
        i += 1
        transaction_partner = event.get('transactionPartner', None)
        amount = event.get('amount', None)
        purpose = event.get('purpose', None)
        event_time = event.get('time', None)
        transaction_date = event.get('date', None)  # The date might be in the XML.
        
        cursor.execute('INSERT INTO Transactions (transaction_ID, person_ID, transactionPartner, amount, purpose, eventTime, transactionDate) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                       (transaction_id, person_id, transaction_partner, amount, purpose, event_time, transaction_date))

# Save all the changes we made to the database and then close the connection to it.
conn.commit()
conn.close()
