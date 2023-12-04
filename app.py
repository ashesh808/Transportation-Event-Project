from flask import Flask, render_template, request

# Import Person related classes
from Model.person_data import PersonData
from View.person_view import PersonView
from Controller.person_controller import PersonController

# Import Link related classes
from Model.link_data import LinkData
from View.link_view import LinkView
from Controller.link_controller import LinkController

# Import Event related classes
from Model.event_data import EventData
from View.event_view import EventView
from Controller.event_controller import EventController

app = Flask(__name__)
personController = PersonController(PersonData(),PersonView())
link_controller = LinkController(LinkData(), LinkView())
event_controller = EventController(EventData(), EventView())

# Route for the homepage
@app.route('/')
def index():
    # Render the index page with no initial data
    return render_template('index.html', events=None)

#Route for search person feature
#Inputs -> person_ID
#outputs -> person info in table from Project.db
@app.route('/search/person', methods=['GET', 'POST'])
def search_person():
    person_id = request.form.get('personSearch') if request.method == 'POST' else None
    return personController.search_person(person_id)

#Inputs -> link_ID
#outputs -> link_id info in table from Project.db
@app.route('/search/link', methods=['GET', 'POST'])
def search_link():
    link_id = request.form.get('linkSearch') if request.method == 'POST' else None
    return link_controller.search_link(link_id)

#Inputs -> link_id, start_time, end_time. REQUIRED FOR SEARCH
#outputs -> link_id info in table from Project.db between start-end time range.
@app.route('/all/events', methods=['GET', 'POST'])
def all_events():
    start_time_str = request.form.get('start_time') if request.method == 'POST' else None
    end_time_str = request.form.get('end_time') if request.method == 'POST' else None
    link_id = request.form.get('link_id') if request.method == 'POST' else None
    return event_controller.all_events(start_time_str, end_time_str, link_id)

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
