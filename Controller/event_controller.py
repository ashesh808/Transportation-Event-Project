class EventController:
    def __init__(self, event_data, event_view):
        self.event_data = event_data
        self.event_view = event_view

    def all_events(self, start_time_str, end_time_str, link_id):
        search_attempt = False
        events = []
        error_message = None
        if start_time_str and end_time_str and link_id:
            search_attempt = True
            try:
                events = self.event_data.get_event_data(start_time_str, end_time_str, link_id)
            except (ValueError, IndexError) as e:
                error_message = "Invalid input for start or end time, or Link ID. Please enter time in HH:MM:SS format and a valid Link ID."
        return self.event_view.render(events, search_attempt, error_message)

