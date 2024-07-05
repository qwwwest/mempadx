import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import askstring
from tkinter.messagebox import askyesno
from beep import Beep
class TreeView(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.drag_data = {"item": None, "x": 0, "y": 0}
        self.ghost_node = None
        self.create_widgets()
        

    def create_widgets(self):
        self.pack(expand=True, fill=tk.BOTH)

        self.tree = ttk.Treeview(self, show='tree' ) #padding=[-5,0,0,0]
   
        # Create a vertical scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack the tree and the scrollbar
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
       
        # self.tree.pack(expand=True, fill=tk.BOTH)
        self.tree.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        
        # Create right-click menu
        self.menu = tk.Menu(self, tearoff=0)

        self.menu.add_command(label="Insert before", command=self.add_item_before)
        self.menu.add_command(label="Add as child", command=self.add_child_item)
        self.menu.add_command(label="Add as next", command=self.add_item_after)
        self.menu.add_separator()

        self.menu.add_command(label="Rename Item", command=self.rename_item)
        self.menu.add_command(label="Delete Item", command=self.delete_item)
        # self.menu.add_command(label="Copy", command=self.delete_item)
        # self.menu.add_command(label="Move", command=self.delete_item)
        # self.menu.add_command(label="Paste", command=self.delete_item)

        # Drag and Drop logic for reordering pages
        self.tree.bind('<ButtonPress-1>', self.on_start_drag)
        self.tree.bind('<B1-Motion>', self.on_drag)
        self.tree.bind('<ButtonRelease-1>', self.on_drop)


        # Event bindings to display page content on click
        
        self.tree.bind("<Button-3>", self.on_right_click)
 
 
    def getSelectedItem(self):
        selected_item = self.tree.selection()[0]
        id = self.get_item_mid(selected_item)
        level = self.get_item_mlevel(selected_item)
        title = self.tree.item(selected_item, "text")
        return (id, level, title)

    def on_right_click(self, event):
        # Select the item under the right-click
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.menu.post(event.x_root, event.y_root)


    def get_item_mid(self, item):
        return int(self.tree.item(item, "values")[0])

    def get_item_mlevel(self, item):
        return int(self.tree.item(item, "values")[1])

    def add_child_item(self):
        selected_item = self.tree.selection()[0]
        page_id = self.get_item_mid(selected_item)

        new_title = askstring("New Page", "Enter title:\t\t\t\t\t")
        if new_title:
            # self.tree.item(selected_item, text=new_title)
            Beep.dispatch('add_page_child', page_id, new_title)
            


    def add_item_before(self):
        selected_item = self.tree.selection()[0]
        
        index = self.tree.index(selected_item)
        parent = self.tree.parent(selected_item)
        level = self.get_item_mlevel(selected_item)

        title = askstring("New Page", "Enter title:\t\t\t\t\t")
        
        if title:
            item = self.tree.insert(parent,index,text=title, values=(-1,level))
            self.tree.selection_set(item)
            Beep.dispatch('tree-has-changed')


    def add_item_after(self):
        selected_item = self.tree.selection()[0]
        
        index = self.tree.index(selected_item)
        parent = self.tree.parent(selected_item)
        level = self.get_item_mlevel(selected_item)

        title = askstring("New Page", "Enter title:\t\t\t\t\t")
        
        
        if title:
            item = self.tree.insert(parent,index+1,text=title, values=(-1,level))
            # self.tree.item(selected_item, text=new_title)
            self.tree.selection_set(item)
            Beep.dispatch('tree-has-changed')

    def delete_item(self):
        selected_item = self.tree.selection()[0]
        page_id = self.get_item_mid(selected_item)
        num = len(self.tree.get_children(selected_item))
        if num == 0:
            message = 'DELETE this page?'
        else:
            message = f"DELETE this page and its {num} children?" 
   
         
        if askyesno("Delete Page", message):
            new_select =  self.tree.next(selected_item) 

            if not new_select:
                new_select =  self.tree.prev(selected_item)

            if not new_select:
                new_select =  self.tree.parent(selected_item)

          
            self.tree.delete(selected_item)
            self.tree.selection_set(new_select)
            Beep.dispatch('tree-has-changed', page_id)
        
        
        
 

    def get_selected_item(self):
        select = self.tree.selection()
        if select:
            return select[0]
        return None
    
    def rename_item(self):
        selected_item = self.tree.selection()[0]
        page_id = self.get_item_mid(selected_item)
        current_title = self.tree.item(selected_item, "text")
        new_title = askstring("Rename Page", "Enter new title:\t\t\t\t\t", initialvalue=current_title)
        if new_title and new_title != current_title:
            self.tree.item(selected_item, text=new_title)
            Beep.dispatch('page-title-has-changed',page_id, new_title)


    def on_start_drag(self, event):
       
        item = self.tree.identify_row(event.y)
        self.tree.tag_configure('highlight', background='#eeeeee', foreground='#888888')
        self.tree.tag_configure('cut', foreground='#cccccc')
        self.tree.tk.call(self.tree, "tag", "add", "cut", item)
        self.ghost_node = None
        if item: 

            self.drag_data["item"] = item
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
            


    def on_drag(self, event):
      
        if self.drag_data["item"] == None:
            return
        
        item = self.drag_data["item"]
        self.tree.item(item, open=True)
        target = self.tree.identify_row(event.y)
        index = self.tree.index(target)
        level = self.get_item_mid(item)
        
        self.tree.selection_remove(item)
        self.tree.selection_add(target)
        if item == target:
            return
        if self.ghost_node == None:
            self.ghost_node = self.tree.insert(target, index, text= self.tree.item(item, "text"),values=(-1,level), open=False)
            self.tree.tk.call(self.tree, "tag", "add", "highlight", self.ghost_node)
   
        
        #self.tree.selection_set(target)
        
        res = self.tree.bbox(target)
        if not type(res) is tuple :
            return        
       
        x,y,w,h = res
        
        delta_x = event.x - self.drag_data["x"]
      
        #    delta_y = event.y - self.drag_data["y"]
        
        #if event.x < w / 2:
        if delta_x <-10 :
            if event.y < h/2:
                index = self.tree.index(target) - 1
            else: 
                index = self.tree.index(target) + 1
            
            parent = self.tree.parent(target)
            self.tree.move(self.ghost_node, parent, index) 
            
        else:
            if event.y < h/2:
                print('blep')
                self.tree.move(self.ghost_node, '', 0)
            else: 
                self.tree.item(target,open=True)
                if target != self.ghost_node:
                    self.tree.move(self.ghost_node, target, 0) 
                
         
        self.tree.selection_clear()
       
         

    def on_drop(self, event):
        
        self.tree.tk.call(self.tree, "tag", "remove", "highlight")
        self.tree.tk.call(self.tree, "tag", "remove", "cut")
        
        item = self.drag_data["item"]
        self.drag_data["item"] = None
 
        if self.ghost_node == None:
            return
        index = self.tree.index(self.ghost_node)
        parent = self.tree.parent(self.ghost_node)
        self.tree.delete(self.ghost_node)
        self.ghost_node = None

        
        if item:
            target_item = self.tree.identify_row(event.y)
            if(item == target_item):
                return
            if target_item:
                
                self.tree.detach(item)
                self.tree.move(item, parent, index)
                source_id = self.get_item_mid(item)
                target_id = self.get_item_mid(target_item)
                # self.parent.move_page(source_id, target_id)
 

            self.tree.selection_set(item)
            Beep.dispatch('tree-has-changed', self.tree)
 
    def __________update(self):
       # if event in ["page_added", "page_deleted", "page_renamed", "page_moved"]:
             
            Beep.dispatch('tree-has-changed', self.tree)      