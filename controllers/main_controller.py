# controllers/app_controller.py

import tkinter as tk
import tkinter.ttk as ttk
from models.mempad_model import MemPadModel
from views.main_view import MainView

from beep import Beep

class MainController:

    def __init__(self):
        self.model = MemPadModel()
         
        #Beep.listen('model_new_file', self.info )
        self.current_page = None
        self.last_selected_item = None
 
    
    def init_view(self, View):
 
        self.view = View(self)
        # self.view.tk.call("source", "/www/py/mempad/views/themes/Azure-ttk-theme/azure.tcl")
        # self.view.tk.call("set_theme", "light")

        # Import the tcl file
        self.view.tk.call('source', '/www/py/mempad/views/themes/Forest-ttk-theme/forest-light.tcl')

        # Set the theme with the theme_use method
        ttk.Style().theme_use('forest-light')

 
        # Bind treeview selection
        self.view.treeview.tree.bind("<<TreeviewSelect>>", self.on_treeview_select)

        self.view.textarea.text.event_add( '<<REACT>>', *( '<Motion>', '<ButtonRelease>', '<KeyPress>', '<KeyRelease>' ) )
        b = self.view.textarea.text.bind( '<<REACT>>', self.footer_info )
        self.footer_info( ) # get the ball rolling
 
    def footer_info(self, ev = None ):
            
        if ev == None:
            self.view.footer.setText('')
            return
        
        r, c = self.view.textarea.text.index( 'insert' ).split( '.' )
        
        c = int(c) + 1
        count = ''
        if self.view.textarea.text.tag_ranges(tk.SEL):
            count = len(self.view.textarea.text.get(tk.SEL_FIRST, tk.SEL_LAST))
            count = f'({count})'
        
        self.view.footer.setText(f'{r},{c} {count}')
        
            

    def open(self, file):
        self.model.open(file)
        self.populate_tree()
        self.view.title('Mempad - '+file)

    def populate_tree(self):
        parents = [""]
         
        for id, level, title, item in self.model.pages:
            parents = parents[0:level]
            node = self.view.treeview.tree.insert(parents[level-1], "end", values=(id,level), text=title, open=True)
            parents.insert(level, node)
             

    def on_treeview_select(self, event):
 
        tree = self.view.treeview.tree
        new_selected_item = tree.selection()[0]
        id = int(tree.item(new_selected_item, "values")[0])

        if self.last_selected_item:
            view_id = int(tree.item(self.last_selected_item, "values")[0])
            if view_id == id :
                return
            
            view_level = tree.item(self.last_selected_item, "values")[1]
            view_title = tree.item(self.last_selected_item, "text")
            view_content = self.view.textarea.content
            self.model.setPageById(view_id, view_level,view_title, view_content)
            self.footer_info()
            

        [id, level, title, content] = self.model.getPageById(id)
 
        self.view.textarea.content = content
        # after changing content, we reset the undo/redo stack
        self.view.textarea.text.edit_reset() 
        self.last_selected_item = new_selected_item
        

    def get_content_by_title(self, title):
        pages = self.model.get_pages()
        for page in pages:
            if page.title == title:
                return page.content
        return ""

    def info(self, *args):
        print('info: ', *args)    

 

    def save(self):
        self.model.save()

    def select_page(self, page):
        self.model.current_page = page
        return page.content
    
    def add_child_item(self, parent_id):
        new_page = self.model.add_page(parent_id, level_increment=1)
        self.view.treeview.populate_tree()

    def add_item_after(self, after_id):
        new_page = self.model.add_page(after_id, level_increment=0)
        self.view.treeview.populate_tree()

    def delete_item(self, page_id):
        self.model.delete_page(page_id)
        self.view.treeview.populate_tree()

    def rename_item(self, page_id, new_title):
        self.model.rename_page(page_id, new_title)
