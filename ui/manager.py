import tkinter as tk
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from vault import get_all_entries, add_entry, delete_entry
from utils import generate_password, copy_to_clipboard


class ManagerScreen(tk.Frame):
    def __init__(self, parent, password, on_lock):
        super().__init__(parent, bg="#1a1a1a")
        self.pack(fill="both", expand=True)

        self.on_lock = on_lock

        self.password = password
        self.parent = parent

        self.parent.update_idletasks()


        self.sideframe = tk.Frame(self, bg="#1a1a1a", padx=20, pady=20)
        self.sideframe.pack(side="left", fill="y")

        rightwing = tk.Frame(self, bg="black")
        rightwing.pack(side="right",fill="both", expand=True)

        self.searchbar = tk.Frame(rightwing, bg="black", pady=20, padx=20)
        self.searchbar.pack(side="top", fill="x")

        self.controls = tk.Frame(self.searchbar, bg="black")
        self.controls.pack(anchor="center")

        scrollarea = tk.Frame(rightwing, bg="black")
        scrollarea.pack(side="top", fill="both", expand=True)

        self.canvas = tk.Canvas(scrollarea, bg="black", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(
            scrollarea,
            orient="vertical",
            command=self.canvas.yview,
            bg="#252525",
            troughcolor="#111111",
            activebackground="#3A3A3A",

            width=10,

            relief="flat",
            bd=0,
            highlightthickness=0
                )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)


        self.entry_field = tk.Frame(self.canvas, bg="black", pady=20, padx=20)

        self.canvas_window = self.canvas.create_window((0, 0), window=self.entry_field, anchor="nw")

        self.entry_field.bind("<Configure>",self.on_frame_configure)
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self._on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))
        


        self.build_ui()




    def build_ui(self):
        self.sidebar()
        self.righside()

    

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")



    def sidebar(self):
        tk.Label(
            self.sideframe,
            text="🔒 VAULT",
            font=("Georgia", 12, "bold"),
            fg="#C8F04F",
            bg="#1a1a1a",
            anchor="w"
        ).pack(fill="x")

        tk.Label(
            self.sideframe,
            text="your passwords, encrypted",
            font=("Georgia", 8),
            fg="#666666",
            bg="#1a1a1a",
            anchor="center"
        ).pack(fill="x", pady=(0,40))

        tk.Frame(self.sideframe,  bg="#2A2A2A", height=1).pack(fill="x", pady=(0,2))

        btn = self.makebtn(self.sideframe,"+ Add entry", command=self.entrywin)
        btn.pack(fill="x", ipady=14, pady=(5,0))
        tk.Frame(self.sideframe, bg="#1a1a1a").pack(fill="both", expand=True)
        btn1 = self.makebtn(self.sideframe,"🔒 Lock vault", command=self.lock_vault)
        btn1.pack(fill="x", ipady=14, pady=(5,0))



    
    def makebtn(self,parent, text, command):
        btn = tk.Button(
            parent,
            text=text,
            font=("Courier", 13, "bold"),
            fg="#ffffff",
            bg="#1a1a1a", 
            activebackground="#30302E",
            activeforeground="#ffffff",
            relief="solid",
            cursor="hand2",
            command=command
        )
        return btn




    def righside(self):
        tk.Label(
            self.controls,
            text="Search",
            bg="black",
            font=("Courier",20,"bold"),
            fg="#ffffff",
            anchor="center"

        ).grid(row=0, column=0, padx=(0,20))
        self.search_entry = tk.Entry(
            self.controls,
            width=60,
            font=("Courier", 11),
            fg="#ffffff",
            bg="#252525",
            insertbackground="#ffffff",
            relief="flat",
            bd=0,
        )
        self.search_entry.grid(row=0, column=1, ipady=12,sticky="w")
        tk.Frame(self.searchbar,  bg="#2A2A2A", height=3).pack(fill="x", pady=15)

        self.search_entry.bind("<KeyRelease>", self.search)

        entries = get_all_entries(self.password)
        for entry in entries:
            self.contents(entry)


        self.entry_field.columnconfigure(0, weight=0)
        self.entry_field.columnconfigure(1, weight=1)
        self.searchbar.columnconfigure(0, weight=0)
        self.searchbar.columnconfigure(1, weight=1)

    
    def contents(self, entry):

        service = entry["service"]
        username = entry["username"]
        password = entry["password"]
        entry_id = entry["id"]

        fields = tk.Frame(
            self.entry_field,
            padx=20,
            pady=20,
            width=360,
            bg="#1A1A1A"
            

        )
        fields.pack(fill="x", pady=10,padx=100,)
        fields.expanded = False

        def toggle(e, f=fields, p=password, eid=entry_id):
            self.toggle_entry(f,p,eid)

        fields.bind("<Button-1>", toggle)

        serv = tk.Label(
            fields,
            text=service,
            font=("Georgia", 16, "bold"),
            fg="#FFFFF8",
            bg="#1A1A1A"
        )
        serv.grid(row=2, column=0, sticky="w",ipady=5)
        serv.bind("<Button-1>", toggle)

        name = tk.Label(
            fields,
            text=username,
            font=("Georgia", 9),
            bg="#1A1A1A",
            fg="#666666"

        )
        name.grid(row=3, column=0, sticky="w", ipady=5)
        name.bind("<Button-1>", toggle)

        copy = self.makebtn(fields, "copy", command=None)
        copy.config(command= lambda text=password: copy_to_clipboard(text=text) )
        copy.grid(row=2, column=1, sticky="e",ipady=9, ipadx=9)

 
        fields.columnconfigure(0, weight=1)
        fields.columnconfigure(1, weight=0)

    
    def toggle_entry(self,fields, password, eid):
        if fields.expanded:
            fields.extra.destroy()
            fields.expanded = False
        else:
            fields.extra = tk.Frame(fields, bg="#1A1A1A")
            fields.extra.grid(row=4, column=0,columnspan=2,sticky="ew")
            password_field = tk.Label(fields.extra, text=password,  font=("Georgia", 16, "bold"),fg="#FFFFF8",bg="#1A1A1A").pack(side="left")
            delete = self.makebtn(fields.extra, "delete", command=None)
            delete.config(fg="#E05C5C",activebackground="#2A1010", activeforeground="#E05C5C", command=lambda id=eid: self.delete_row(id))
            delete.pack(side="right", ipady=9, ipadx=9)

            fields.expanded = True

    def delete_row(self, entry_id):
        delete_entry(self.password, entry_id=entry_id)
        self.refresh()


    def entrywin(self):

        self.popup = tk.Toplevel(
            self,
            bg="#1E2A10",
            padx=2,
            pady=2,
        )


        self.pophighlight = tk.Frame(
            self.popup,
            padx=20,
            pady=20,
            bg="#1A1A1A",
        )
        self.pophighlight.pack(fill="both", expand=True)

        tk.Frame(self.pophighlight, bg="#1A1A1A").pack(fill="both", expand=True)
        

        
        tk.Label(
            self.pophighlight, 
            text="Add new entry",
            font=("Georgia", 22,"bold"),
            fg="#ffffff",
            bg="#1A1A1A",
            anchor="center"
        ).pack(fill="x", pady=(0,4))

        tk.Label(
            self.pophighlight,
            text="Fill in the details for this account",
            font=("Georgia", 9),
            fg="#666666",
            bg="#1A1A1A",
            anchor="center"
        ).pack(fill="x", pady=(0,40))

        self.entry1 =self.make_entry("SERVICE")
        self.entry2 =self.make_entry("USERNAME")
        self.entry3 =self.make_entry("PASSWORD")
        
        

        self.btnframe = tk.Frame(
            self.pophighlight,
            pady=10,
            padx=10,
            bg="#1a1a1a",

        )
        self.btnframe.pack(fill="x", pady=(15,0))

        btn = self.makebtn(self.btnframe, "Generate password", self.paswd_gen)
        btn.grid(row=0, column=0,ipady=15, sticky="ew")

        btn0 = self.makebtn(self.btnframe, "Save", self.saveEntry)
        btn0.grid(row=0, column=1,ipady=15, sticky="ew")


        tk.Frame(self.pophighlight, bg="#1A1A1A").pack(fill="both", expand=True)


        self.btnframe.columnconfigure(0, weight=1)
        self.btnframe.columnconfigure(1, weight=1)


        self.popup.resizable(False,False)
        self.popup.transient(self)
        self.popup.grab_set()
        self.popup.update_idletasks()

        w = 700
        h = 900

        screen_w = self.popup.winfo_screenwidth()
        screen_h = self.popup.winfo_screenheight()

        x = (screen_w - w) // 2
        y = (screen_h - h) // 2
        self.popup.geometry(f"{w}x{h}+{x}+{y}")

    
    def make_entry(self, text , secret=False):
        tk.Label(
            self.pophighlight,
            text=text,
            font=("Courier",9,"bold"),
            fg="#888888",
            bg="#1A1A1A",
            anchor="w"
        ).pack(fill="x", pady=(20,4))
        entry = tk.Entry(
            self.pophighlight,
            font=("Courier", 11),
            fg="#ffffff",
            bg="#252525",
            insertbackground="#ffffff",
            relief="flat",
            bd=0,
            show="●" if secret else "",


        )
        entry.pack(fill="x", ipady=12)
        tk.Frame(self.pophighlight, bg= "#333333", height=1).pack(fill="x", pady=(0,2))
        return entry



    def saveEntry(self):
        add_entry(self.password, self.entry1.get(), self.entry2.get(), self.entry3.get())

        self.entry1.delete(0,tk.END)
        self.entry2.delete(0,tk.END)
        self.entry3.delete(0,tk.END)
        self.refresh()

    def search(self,event=None):
        term = self.search_entry.get().lower()
        entries = get_all_entries(self.password)
        filtred = [entry for entry in entries if term in entry["service"].lower() or term in entry["username"].lower() or term in entry["password"].lower() ]
        for widget in self.entry_field.winfo_children():
            widget.destroy()

        for i, entry in enumerate(filtred):
            self.contents(entry=entry)


    
    def refresh(self):
        self.search()
        # for widget in self.entry_field.winfo_children():
        #     widget.destroy()
        # entries = get_all_entries(self.password)

        # for i,entry in enumerate(entries):
        #     self.contents(entry=entry)

    
    def paswd_gen(self):
        passwd = generate_password(16)

        self.entry3.delete(0,tk.END)
        self.entry3.insert(0,passwd)


    def lock_vault(self):
        self.on_lock()

    





















