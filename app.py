from flask import Flask, render_template, request
import sqlite3

# Set up the Flask application
app = Flask(__name__)

# Define a route for the root URL which loads the index.html template
@app.route('/')
def index():
    # No event data is passed initially
    return render_template('index.html', events=None)

# Define a route to search for a person
@app.route('/search/person', methods=['GET', 'POST'])
def search_person():
    # Flags to check if a search was attempted
    search_attempt = False
    # Empty lists to store data fetched from the database
    person_data = []
    transaction_data = []

    # Check if the request method is POST, which indicates form submission
    if request.method == 'POST':
        # Set search_attempt to True as form has been submitted
        search_attempt = True
        # Get the person ID from the form input
        person_id = request.form.get('personSearch')

        # Connect to the SQLite database
        conn = sqlite3.connect('Project.db')
        cursor = conn.cursor()

        # If a person_id is provided, perform the database query
        if person_id:
            # Execute a SQL query to retrieve connected events for the given person ID
            cursor.execute("""
                SELECT person_ID, Event_type, Link_ID, actType, legMode, Timestamp,
                       From_Node, To_Node, Length, Freespeed, Capacity, PermLanes,
                       OneWay, Modes, From_X, From_Y, To_X, To_Y
                FROM Connected 
                WHERE person_ID = ? 
                ORDER BY Timestamp""", (person_id,))
            # Fetch all the results
            person_data = cursor.fetchall()

            # Execute another query to get transactions for the person ID
            cursor.execute("""
                SELECT transaction_ID, person_ID, amount, purpose, eventTime
                FROM Transactions
                WHERE person_ID = ?
                ORDER BY eventTime""", (person_id,))
            # Fetch all the transaction data
            transaction_data = cursor.fetchall()

        # Close the database connection
        conn.close()

    # Pass the data to the index.html template to display it
    return render_template('index.html', person_data=person_data, transaction_data=transaction_data, search_attempt=search_attempt)

# Define a route to search for links
@app.route('/search/link', methods=['GET', 'POST'])
def search_link():
    # Empty list to store node data from the database
    node_data = []
    # Flag for search attempt
    search_attempt = False
    # Check if the request method is POST
    if request.method == 'POST':
        # Mark that a search has been attempted
        search_attempt = True
        # Get the link ID from the form
        link_details = request.form.get('linkSearch')
        # Check if the link ID was provided before querying the database
        if link_details:
            # Connect to the database
            conn = sqlite3.connect('Project.db')
            cursor = conn.cursor()
            cursor.execute("""
            SELECT person_ID, Event_type, Link_ID, actType, legMode, Timestamp,
                From_Node, To_Node, Length, Freespeed, Capacity, PermLanes,
                OneWay, Modes, From_X, From_Y, To_X, To_Y
            FROM Connected 
            WHERE Link_ID = ? 
            ORDER BY Timestamp""", (link_details,))
        node_data = cursor.fetchall()
    conn.close()
    # Return the node data to be displayed in the index.html template
    return render_template('index.html', node_data=node_data, search_attempt=search_attempt)

# Route to get all events within a time range
@app.route('/all/events', methods=['GET', 'POST'])
def all_events():
    # Initialize variables to store events and error messages
    events = []
    error_message = None
    search_attempt = False

    # Process form submission
    if request.method == 'POST':
        search_attempt = True
        # Extract and validate start and end times from the form input
        try:
            start_time, end_time = [request.form.get(key) for key in ('start_time', 'end_time')]
            # Convert times to float if valid, else use None
            start_time = float(start_time) if start_time else None
            end_time = float(end_time) if end_time else None

            # Check the validity of the time inputs
            if not all([start_time, end_time]):
                error_message = "Start and end times are required."
            elif start_time >= end_time:
                error_message = "Start time must be less than end time."
            else:
                # Fetch events from the database within the specified time range
                conn = sqlite3.connect('Project.db')
                cursor = conn.cursor()
                cursor.execute("""
                        SELECT person_ID, Event_type, Link_ID, actType, legMode, Timestamp,
                        From_Node, To_Node, Length, Freespeed, Capacity, PermLanes,
                        OneWay, Modes, From_X, From_Y, To_X, To_Y
                        FROM Connected 
                        WHERE Timestamp BETWEEN ? AND ?
                        ORDER BY Timestamp""", (start_time, end_time))
                events = cursor.fetchall()
                
        except (TypeError, ValueError) as e:
            error_message = "Invalid input for start or end time."
            print('Error:', e)
        except sqlite3.Error as e:
            error_message = f"Database error: {e}"
            print('DB Error:', e)

    return render_template('index.html', events=events, search_attempt=search_attempt, start_time=start_time, end_time=end_time, error_message=error_message)
if __name__ == '__main__':
    app.run(debug=True)
