import tkinter as tk
from tkinter import ttk
from views.main_view import MainView
from controllers.main_controller import MainController

def main(file):

    controller = MainController()
    controller.init_view(MainView)
    controller.open(file)


    controller.view.mainloop()

if __name__ == "__main__":
    main("mempad.lst")





 


