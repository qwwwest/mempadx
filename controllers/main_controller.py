# controllers/app_controller.py

import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime
import shutil
from tkinterdnd2 import DND_FILES
from tkinter.messagebox import askyesno
from models.mempad_model import MemPadModel
from views.main_view import MainView
from tkinter.messagebox import showinfo
import os.path


from beep import Beep

class MainController:

    def __init__(self, conf):
        self.model = MemPadModel()
        self.conf = conf
         
        #Beep.listen('model_new_file', self.info )
        self.current_page = None
        self.last_selected_item = None

        Beep.listen('tree-has-changed', self.tree_has_changed)
        Beep.listen('page-title-has-changed', self.page_title_has_changed)
        Beep.listen('add_page_child', self.add_page)
        Beep.listen('alert', self.alert)
        Beep.listen('info', self.info)
      

        # run command in menus bar (File, Settings...)
        Beep.listen('command', self.run_command)
 
    
    def init_view(self, View):
 
        self.view = View(self, self.conf)

        # Import the tcl file
        self.view.tk.call('source', '/www/py/mempad/views/themes/Forest-ttk-theme/forest-light.tcl')

        # Set the theme with the theme_use method
        ttk.Style().theme_use('forest-light')

        # Bind treeview selection
        self.view.treeview.tree.bind("<<TreeviewSelect>>", self.on_treeview_select)

        self.view.textarea.text.event_add( '<<REACT>>', *( '<Motion>', '<ButtonRelease>', '<KeyPress>', '<KeyRelease>' ) )
        b = self.view.textarea.text.bind( '<<REACT>>', self.footer_info )
        self.footer_info( ) # first time

        self.view.bind("<Escape>", self.window_exit)
        self.view.bind("<Control-s>", lambda e: self.save())
        self.view.bind("<Control-o>", lambda e:self.view.menu.open_file_dialog())
        self.view.bind("<Control-n>", lambda e:self.view.menu.save_new_file_dialog())
        self.view.protocol("WM_DELETE_WINDOW", self.window_exit)

        self.view.drop_target_register(DND_FILES)
        self.view.dnd_bind('<<Drop>>', self.on_drop_file)

    def on_drop_file(self, event):
        file_path = event.data.strip('{}')
        
        if file_path:
            self.open(file_path)


    def window_exit(self, *args):
        # YYYY-MM-DD_HourMinuteSecond for Backup:
        # stamp = datetime.today().strftime('%Y-%m-%d_%H%M%S') 
        # file_bak = self.model.filename[0:-4] + '_' + stamp + '.lst'
        # self.save(file_bak)

        self.conf.set('Main', 'MRU', self.model.filename)
        self.save()
        self.view.destroy()
        print("bye.")

 
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
             

    def alert(self, _ , icon , message ):
        "open dialog to show Info"
        showinfo ( message = message , icon = icon, title = icon.upper() )
 
    def info(self, _ , message ):
        "open dialog to show Info"
        self.view.footer.setText(message)
 

    def open(self, file):
        "open new file"
        # backup file

        self.save()
        if not self.model.open(file):
           return
      
        shutil.copyfile(file, file + '.bak')
        self.populate_tree(self.model.current_page)
        self.view.title('Mempad - '+file)
        self.view.menu.add_open_mempad_file_item(file, False)

    def populate_tree(self, idsel = 0):

        parents = [""]
        tree = self.view.treeview.tree
  
        # we clean up the old tree
        for item in tree.get_children():
            tree.delete(item)    
        snode = None
        for idx, p in enumerate(self.model.pages) :
            parents = parents[0:p["level"]]
            node = self.view.treeview.tree.insert(parents[p["level"]-1], "end", values=(p["id"],p["level"]), text=p["title"], open=True)
            if idx == idsel:
                snode = node
            parents.insert(p["level"], node)

        if snode:
            self.view.treeview.tree.selection_add(snode)
        self.last_selected_item = None



    def on_treeview_select(self, event):
       
        tree = self.view.treeview.tree
        
        if len(tree.selection()) == 0: 
           return
        new_selected_item = tree.selection()[0]
        if self.view.treeview.ghost_node != None:
            tree.selection_remove(new_selected_item)
            return
       
        id = self.view.treeview.get_item_mid(new_selected_item)

        if self.last_selected_item == new_selected_item :
            # tree.selection_set(self.last_selected_item)
            return
        
        if self.last_selected_item:
            tree.selection_remove(self.last_selected_item)
            view_id = self.view.treeview.get_item_mid(self.last_selected_item)
            if view_id == id :
                return
            
            view_level = self.view.treeview.get_item_mlevel(self.last_selected_item)
            view_title = tree.item(self.last_selected_item, "text")
            view_content = self.view.textarea.content
            self.model.set_page_by_id(view_id, view_level, view_title, view_content)
            self.footer_info()
            

        page = self.model.get_page_by_id(id)
 
        self.view.textarea.content = page["content"]
        # after changing content, we reset the undo/redo stack
        self.view.textarea.text.edit_reset() 
        self.last_selected_item = new_selected_item

    def save(self, filename = None):

        tree = self.view.treeview.tree

        if self.model.num_pages == 0 :
            if self.model.filename != '':
                print(f"Empty model. Cannot save '{self.model.filename}'")
            return

       
        selected_item = tree.selection()[0]
           
        id = self.view.treeview.get_item_mid(selected_item)
   
        view_content = self.view.textarea.content
        self.model.set_content_by_id(id, view_content)
        self.model.current_page = id
        self.model.save(filename)

    def ________________select_page(self, page):
        self.model.current_page = page
        return page.content
    
    def add_page(self, type, parent_id, title):
        if type == "add_page_child":
            new_page = self.model.add_page_child(parent_id,title)

        # if type == "add_page_after":
        #     new_page = self.model.add_page_after(parent_id,title)

        if new_page:    
            self.populate_tree(self.model.current_page)

    def __________________________add_item_after(self, message, after_id):
        new_page = self.model.add_page_child(after_id, level_increment=0)
        self.view.treeview.populate_tree()

    def _________________delete_item(self, page_id):
        self.model.delete_page(page_id)
        self.populate_tree()

    def tree_has_changed(self, *args):
       
        tree = self.view.treeview.tree
        selected = self.view.treeview.get_selected_item()
       
        pages = []
        self.new_selected_item = 0
        self.walk_tree(tree.get_children(), 1, pages) 
        self.model.set_pages(pages)
      
        self.populate_tree(self.new_selected_item)

    def page_title_has_changed(self, event, id, title):
         
        self.model.set_page_title(id, title)
        

    def walk_tree(self, children, level, pages ):
      
        if not children :
           return 

        selected_item = self.view.treeview.get_selected_item()
        for child in children:
            title = self.view.treeview.tree.item(child, "text")
            old_id = self.view.treeview.get_item_mid(child)
            id =  len(pages)
            if old_id == -1:
                content = ''
            else:
                content = self.model.get_content_by_id(old_id)

           
            if old_id == -1 or child == selected_item:
                 
                self.new_selected_item = id

            pages.append({
           "id": id, 
           "level": level, 
           "title": title, 
           "content": content
           })  

            self.walk_tree(self.view.treeview.tree.get_children(child), level + 1, pages) 
        

    def run_command(self, command, action, *args ):  
        
        if command != 'command' :
            print('command ERROR', command)
        match action:           
            case 'exit':
                self.window_exit()
                return
            case 'open_mempad_file':
                print ("action = ", action, *args)
                self.open(args[0])
                return
            case 'close_mempad_file':
                self.close()
                return
            case 'save_mempad_file':
                self.save()
                return
            case 'save_as_mempad_file':
                print ('save_as_mempad_file args[0]=', args[0])
                self.save(args[0])
                self.open(args[0])
                return            
            case 'save_as_new_mempad_file':
                if os.path.isfile(args[0]):
                    self.alert('','info', 'File already exist : \n' + args[0])
                    return
                self.save()
                self.model.new_mempad_file(args[0])
                self.open(args[0])
                return
            case _:
                print ("command not found", action, *args)