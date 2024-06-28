# MemPadPy

- It is a work in Progress
- do NOt try to use it yet
- it is here on my Github only for my own source code management :)

MemPadPy is a port in Python of Mempad (for Windows).
Mempad is a plain text outliner and note taking program with a structured index. 
All pages are stored in a single file.

The program offers standard editing functions including cut, copy, paste, undo/redo, drag&drop... 

The index structure can be modified.


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

