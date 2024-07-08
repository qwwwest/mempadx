# MemPadPy

- It is a work in Progress...

MemPadPy is a port in Python of Mempad (for Windows).
Mempad is a plain text outliner and note taking program with a structured index. 
All pages are stored in a single file. 

I needed to use it in Linux but the windows app failed to work in Wine, so i decided to bring it to Linux by rewriting it in Python.

The program offers standard editing functions including cut, copy, paste, undo/redo, drag&drop nodes to modify the tree structure.

# Features

- drag and drop to open mempad files (.lst)
- drag and drop to reorder nodes in the tree structures 
- autosave when exit
- save configuration

The windows version has many features i did not bring to Python because they were Windows specific.


# other python projects used in MemPadPy

- Markdown
- Forest-ttk-theme


## Project Structure

The MVC Project Structure gives a well-organized application with a clean separation of concerns. The main view combines several subviews, each responsible for a part of the UI. The controller handles interactions and logic, keeping the model and view decoupled.

```
mempad/
├── controllers/
│   ├── __init__.py
│   ├── app_controller.py
├── models/
│   ├── __init__.py
│   ├── page_model.py
├── views/
│   ├── __init__.py
│   ├── main_view.py
│   ├── menu_view.py
│   ├── toolbar_view.py
│   ├── treeview_view.py
│   ├── textarea_view.py
│   ├── footer_view.py
├── resources/
│   ├── ...
├── main.py
└── README.md
```

