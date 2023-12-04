class LinkController:
    def __init__(self, link_data, link_view):
        self.link_data = link_data
        self.link_view = link_view

    def search_link(self, link_id):
        search_attempt = False
        node_data = []
        if link_id:
            search_attempt = True
            node_data = self.link_data.get_link_data(link_id)
        return self.link_view.render(node_data, search_attempt)
