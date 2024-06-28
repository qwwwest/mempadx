class Page:
    def __init__(self, id, title, content, parent=None):
        self.id = id
        self.title = title
        self.content = content
        self.parent = parent
        self.children = []

    def add_child(self, child_page):
        self.children.append(child_page)
        child_page.parent = self

class TreeModel:
    def __init__(self):
        self.pages = []
        self.all_pages = []
        self.current_page = None

    def add_page(self, id, title, content, parent=None):
        page = Page(id, title, content, parent)
        self.all_pages.append(page)
        if parent:
            parent.add_child(page)
        else:
            self.pages.append(page)
        return page

    def get_page(self, title):
        for page in self.pages:
            if page.title == title:
                return page
        return None

    def get_page_by_id(self, id):
        for page in self.pages:
            if page.id == id:
                return page
        return None
    
    def save(self):
        # Save model to disk or database
        pass
