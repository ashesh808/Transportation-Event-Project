class PersonController:
    def __init__(self, person_data, person_view):
        self.person_data = person_data
        self.person_view = person_view

    def search_person(self, person_id):
        search_attempt = False
        person_data = []
        if person_id:
            search_attempt = True
            person_data = self.person_data.get_person_data(person_id)
        return self.person_view.render(person_data, search_attempt)
