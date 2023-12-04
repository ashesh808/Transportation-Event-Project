from flask import render_template

class LinkView:
   def __init__(self, html_file = 'index.html'):
        self.html_file = html_file

   def render(self, node_data, search_attempt):
         return render_template(self.html_file, node_data=node_data, search_attempt=search_attempt)