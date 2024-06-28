import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import askstring

class TreeView(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller

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
        self.menu.add_command(label="Rename Item", command=self.rename_item)
        self.menu.add_command(label="Add Page as child", command=self.add_child_item)
        self.menu.add_command(label="Add Page After me", command=self.add_item_after)
        self.menu.add_command(label="Delete Item", command=self.delete_item)
        # Drag and Drop logic for reordering pages

        # Event bindings to display page content on click
        
        self.tree.bind("<Button-3>", self.on_right_click)


    
 
    def getSelectedItem(self):
        selected_item = self.tree.selection()[0]
        id = self.tree.item(selected_item, "values")[0]
        level = self.tree.item(selected_item, "values")[1]
        title = self.tree.item(selected_item, "text")
        return (id, level, title)

    def on_right_click(self, event):
        # Select the item under the right-click
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.menu.post(event.x_root, event.y_root)


    def add_child_item(self):
        selected_item = self.tree.selection()[0]
        page_id = self.tree.item(selected_item, "values")[0]
        self.controller.add_child_item(page_id)

    def add_item_after(self):
        selected_item = self.tree.selection()[0]
        page_id = self.tree.item(selected_item, "values")[0]
        self.controller.add_item_after(page_id)

    def delete_item(self):
        selected_item = self.tree.selection()[0]
        page_id = self.tree.item(selected_item, "values")[0]
        self.controller.delete_item(page_id)
        self.tree.delete(selected_item)

    def rename_item(self):
        selected_item = self.tree.selection()[0]
        page_id = self.tree.item(selected_item, "values")[0]
        current_title = self.tree.item(selected_item, "text")
        new_title = askstring("Rename Page", "Enter new title:", initialvalue=current_title)
        if new_title:
            # self.controller.rename_item(page_id, new_title)
            self.tree.item(selected_item, text=new_title)