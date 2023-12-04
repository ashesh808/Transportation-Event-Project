from flask import render_template

class PersonView:
   def __init__(self, html_file = 'index.html'):
      self.html_file = html_file

   def render(self, person_data, search_attempt):
      return render_template(self.html_file, person_data=person_data, search_attempt=search_attempt)