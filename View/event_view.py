from flask import render_template

class EventView:
   def __init__(self, html_file = 'index.html'):
      self.html_file = html_file

   def render(self, events, search_attempt, error_message):
      return render_template(self.html_file, events=events, search_attempt=search_attempt, error_message=error_message)