import tkinter as tk
import tkinter.ttk
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from auth import setup_masterpasswd, verify_masterpasswd, derive_key, is_first_run


class LoginScreen(tk.Frame):
    def __init__(self, parent , on_success):
        super().__init__(parent, bg="#1a1a1a")
        self.on_success = on_success
        self.parent = parent
        self.parent.update_idletasks()

        # self.bind("<Configure>", self.on_resize)

        self.BG = "#0f0f0f"
        self.CARD = "#1a1a1a"
        self.ENTRY_BG = "#252525"
        self.ACCENT = "#c8f04f"
        self.ACCENT_HV = "#b0d93e"
        self.FG = "#ffffff"
        self.FG_DIM = "#666666"
        self.FG_LABEL = "#888888"
        self.DIVIDER = "#333333"
        self.ERR  = "#e05c5c"
        self.OK = "#5ce08a"

        #frame size
        self.pack(fill="both", expand=True)
        
        self.inner = tk.Frame(self, bg=self.CARD)
        self.inner.pack(expand=True, padx=32, pady=40)
        self.inner.config(
            width=400,
            height=600
            )
        self.inner.pack_propagate(False)

        tk.Frame(self.inner, bg=self.CARD).pack(fill="both", expand=True)

        # self.on_resize()

        self.build_ui()

    # def on_resize(self, event):
    #     if event.widget != self:
    #         return
        
    #     if not self.winfo_exists():
    #         return

    #     self.screen_w = self.parent.winfo_width()
    #     self.screen_h = self.parent.winfo_height()

    #     self.frame_h = int(self.screen_h * 0.8)
    #     self.frame_w = self.screen_w // 4

    #     #centering the frame
    #     self.x = (self.screen_w - self.frame_w)//2
    #     self.y = (self.screen_h - self.frame_h)//2


        
    #     self.inner.place(x=self.x , y=self.y , width=self.frame_w, height=self.frame_h)
    #     return



    def make_entry(self, text , secret=False):
        tk.Label(
            self.inner,
            text=text,
            font=("Courier",9,"bold"),
            fg=self.FG_LABEL,
            bg=self.CARD,
            anchor="w"
        ).pack(fill="x", pady=(20,4))
        entry = tk.Entry(
            self.inner,
            font=("Courier", 11),
            fg=self.FG,
            bg=self.ENTRY_BG,
            insertbackground=self.FG,
            relief="flat",
            bd=0,
            show="●" if secret else "",


        )
        entry.pack(fill="x", ipady=12)
        tk.Frame(self.inner, bg=self.DIVIDER, height=1).pack(fill="x", pady=(0,2))
        return entry


    def make_button(self, text, command):
        tk.Button(
            self.inner,
            width=15,
            text=text,
            font=("Courier", 10, "bold"),
            fg=self.BG,
            bg=self.ACCENT, 
            activebackground=self.ACCENT_HV,
            activeforeground=self.BG,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=command
        ).pack(ipady=14, pady=(30,0))

    
    def build_ui(self):
        if is_first_run():
            self.signup()
        else:
            self.login()



    
    def submit(self):
        if is_first_run():
            p1 = self.entry0.get()
            p2 = self.entry1.get()
            if not p1 or not p2:
                self.show_error("feild is empty!.")
                return
            if p1 != p2:
                self.show_error("password dont match!.")
                return
            if len(p1) < 8:
                self.show_error("Password is weak!")
                return
            setup_masterpasswd(p1)
            self.show_success("Vault created!")
            self.after(800, lambda: self.on_success(p1))
        else:
            p3 = self.entry3.get()
            if not p3:
                self.show_error("Password cannot be empty.")
                return
            if verify_masterpasswd(p3):
                self.show_success("Unlocking...")
                self.after(400, lambda: self.on_success(p3))
            else:
                self.show_error("Incorrect password!.")
    
    def show_error(self, massage):
        self.msg.config(text=massage)

    def show_success(self, massage):
        self.msg.config(fg=self.OK, text=massage)

    
    def signup(self):
        tk.Label(
            self.inner, 
            text="Create Vault",
            font=("Georgia", 22,"bold"),
            fg=self.FG,
            bg=self.CARD,
            anchor="center"
        ).pack(fill="x", pady=(0,4))

        tk.Label(
            self.inner,
            text="Set your master password to get started",
            font=("Georgia", 9),
            fg=self.FG_DIM,
            bg=self.CARD,
            anchor="center"
        ).pack(fill="x", pady=(0,32))

        self.entry0 = self.make_entry("Password")
        self.entry1 = self.make_entry("Confirm")
        self.make_button("Create", self.submit)
        
        self.msg = tk.Label(
            self.inner,
            text="",
            font=("Courier", 9),
            fg=self.ERR,
            bg=self.CARD,
            anchor="center"
        )
        self.msg.pack(fill="x", pady=(12,0))

        tk.Frame(self.inner, bg=self.CARD).pack(fill="both", expand=True)
    
    def login(self):
        tk.Label(
            self.inner,
            text="Welcome Back",
            font=("Georgia", 22, "bold"),
            fg=self.FG,
            bg=self.CARD,
            anchor="center"
        ).pack(fill="x", pady=(0,4))

        tk.Label(
            self.inner,
            text="Enter your master password to unlock",
            font=("Georgia", 9),
            fg=self.FG_DIM,
            bg=self.CARD,
            anchor="center"
        ).pack(fill="x", pady=(0,32))

        self.entry3 = self.make_entry("Password", secret=True)
        self.make_button("Unlock", self.submit)
        
        self.msg = tk.Label(
            self.inner,
            text="",
            font=("Courier", 9),
            fg=self.ERR,
            bg=self.CARD,
            anchor="center"
        )
        self.msg.pack(fill="x", pady=(12,0))

        tk.Frame(self.inner, bg=self.CARD).pack(fill="both", expand=True)










