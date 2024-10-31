

import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime
import shutil
from tkinterdnd2 import DND_FILES
from tkinter.messagebox import askyesno
from models.mempad_model import MemPadModel
from  views.export_dialog import ExportDialog
from tkinter.messagebox import showinfo
import os.path
from beep import Beep
import threading
import time
from settings import MemPadSettings
from controllers.search_controller import SearchController

class MainController:

    def __init__(self, conf):
        self.model = MemPadModel()
        self.conf = conf
        
         
        #Beep.listen('model_new_file', self.info )
        self.last_selected_item = None

        self.model_to_view_id = []

        self.search_results = []
        self.search_index = -1
        self.last_search_term = None

        Beep.listen('tree-has-changed', self.tree_has_changed)
        Beep.listen('page-title-has-changed', self.page_title_has_changed)
        Beep.listen('add_page_child', self.add_page)
        Beep.listen('save_page_to_model', self.save_page_to_model)
        Beep.listen('alert', self.alert)
        Beep.listen('info', self.info)
 
        # run command in menus bar (File, Settings...)
        Beep.listen('command', self.run_command)
 
    
    def init_view(self, View):
 
        self.view = View(self, self.conf)

        self.search_controller = SearchController(self.model, self.view, self)

        # Import the tcl file
       
        self.view.tk.call('source', MemPadSettings.theme)

        # Set the theme with the theme_use method
        ttk.Style().theme_use('forest-dark')

        # Bind treeview selection
        self.view.treeview.tree.bind("<<TreeviewSelect>>", self.on_treeview_select)
        self.view.treeview.tree.bind("<Double-Button-1>", self.on_treeview_select_click)
        # self.view.treeview.tree.bind("<Button-3>", self.on_treeview_select)

        self.view.textarea.text.event_add( '<<REACT>>', *( '<Motion>', '<ButtonRelease>', '<KeyPress>', '<KeyRelease>' ) )
        b = self.view.textarea.text.bind( '<<REACT>>', self.footer_info )
        self.footer_info( ) # first time

        self.view.bind("<Escape>", self.on_escape)
        self.view.bind("<Control-s>", lambda e: self.save())
        # save when app lose focus
        # self.view.bind("<FocusOut>", lambda e: self.save())
         
        self.view.bind("<Control-o>", lambda e:self.view.menu.open_file_dialog())
        self.view.bind("<Control-n>", lambda e:self.view.menu.save_new_file_dialog())


        self.view.protocol("WM_DELETE_WINDOW", self.window_exit)

        self.view.drop_target_register(DND_FILES)
        self.view.dnd_bind('<<Drop>>', self.on_drop_file)

       
        
        self.set_autosave(self.conf.getValue('AutoSave'))
        self.run_command('command','settings-update','renderMarkdown') 



    def on_drop_file(self, event):
        file_path = event.data.strip('{}')
        
        if file_path:
            self.open(file_path)

    def on_escape(self, *args):
        if self.conf.getValue('ExitEsc'):
            self.window_exit()
         
    def window_exit(self, *args):
        # YYYY-MM-DD_HourMinuteSecond for Backup:
        # stamp = datetime.today().strftime('%Y-%m-%d_%H%M%S') 
        # file_bak = self.model.filename[0:-4] + '_' + stamp + '.lst'
        # self.save(file_bak)
        #self.timer_runs.clear()

        # strop autosave Thread if running
        if hasattr(self,'timer_runs') :
            self.timer_runs.set()
 
        self.conf.setValue('MRU', self.model.filename)
        self.save()
        self.view.destroy()
 
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
      
        if self.conf.getValue('NoBackup', 'bool') == False:
            shutil.copyfile(file, file + '.bak')
        self.populate_tree(self.model.current_page)

        self.view.title('MemPadX - ' + self.model.filename )
        self.view.menu.add_open_mempad_file_item(self.model.filename)

    def populate_tree(self, idsel = 0):

        parents = [""]
        tree = self.view.treeview.tree

        self.model_to_view_id = []
  
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
 
            self.model_to_view_id.insert(p['id'], node)

        if snode:
            self.view.treeview.tree.selection_add(snode)
        self.last_selected_item = None
 

    def select_tree_item_with_model_id(self, model_id):

        self.view.treeview.tree.selection_set(self.model_to_view_id[model_id])
        self.on_treeview_select('blep')
        


    def on_treeview_select_click(self, event):

        tree = self.view.treeview.tree
        
        if len(tree.selection()) == 0: 
           return
        new_selected_item = tree.selection()[0]
        # click on already selected item to rename it
        if self.last_selected_item == new_selected_item :
             
            # tree.selection_set(self.last_selected_item)
            self.view.treeview.rename_item()
            return

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
        self.model.current_page = id
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
 
    
    def add_page(self, type, parent_id, title):
        if type == "add_page_child":
            new_page = self.model.add_page_child(parent_id,title)

        # if type == "add_page_after":
        #     new_page = self.model.add_page_after(parent_id,title)

        if new_page:    
            self.populate_tree(self.model.current_page)

    def save_page_to_model(self, _, m_id):
        
        self.model.set_content_by_id(m_id, self.view.textarea.content)
           

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
                if self.model.filename == args[0]: 
                    return
                self.open(args[0])
                return
            case 'close_mempad_file':
                self.close()
                return
            case 'save_mempad_file':
                self.save()
                return            
            case 'open_export_dialog':
                self.open_export_dialog()

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
            case 'settings-update':
                self.conf.hasChanged(args[0])
                if args[0] == 'OnTop':
                    self.view.always_on_top(self.conf.getValue(args[0]))
                    return
                if args[0] == 'AutoSave':
                    self.set_autosave(self.conf.getValue(args[0]))
                    return 
                if args[0] == 'renderMarkdown':
                    value = self.conf.getValue(args[0])
                    self.view.textarea.renderMarkdown(value)
                    return
            case _:
                print ("command not found", action, *args)



    def set_autosave(self, state):
        
        if state :
            self.timer_runs = threading.Event()
            self.autosave_thread = threading.Thread(target=self.timer, args=(self.timer_runs,))
            self.autosave_thread.start()
        else: 
            if hasattr(self, 'timer_runs') :
                self.timer_runs.set()


    def timer(self, timer_runs):
        print('START THREAD TIMER...')
        while True:
            finished = timer_runs.wait(300)   # 5 minutes
            print('wait...', finished)
            if finished:
                break
          
            if  self.conf.getValue('AutoSave', 'bool'):
                print('autosave...')
                self.save()
                 
        print('THREAD ENDED...')
    
    
    def open_export_dialog(self):

        dialog = ExportDialog(self.view, self.model.filename)
        if dialog.result:
            print("Export Settings:")
            print(f"Format: {dialog.result['format']}")
            print(f"File choice: {dialog.result['file_choice']}")
            print(f"Autotitle: {dialog.result['autotitle']}")
            print(f"Add Page Title: {dialog.result['add_page_title']}")
            print(f"Document Title: {dialog.result['doc_title']}")
            print(f"Export Folder: {dialog.result['export_folder']}")
 
            self.model.export_to(dialog.result)
