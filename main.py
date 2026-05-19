import tkinter as tk
from ui.login import LoginScreen
from ui.manager import ManagerScreen


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Vault")
        self.configure(bg="#1a1a1a")
        self.state("zoomed")
        self.minsize(1280,600)

        self.current_screen = None
        self.show_login()

    def show_screen(self, screen):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = screen

    def show_login(self):
        # if self.current_screen:
        #     self.current_screen.destroy()
        self.show_screen(LoginScreen(self, self.show_manager))
    
    def show_manager(self,password):
        if self.current_screen:
            self.current_screen.destroy()
        self.show_screen(ManagerScreen(self,password,self.show_login))

App().mainloop()












