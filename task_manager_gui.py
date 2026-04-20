import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def next_id(tasks):
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CLI Task Manager")
        self.root.geometry("700x500")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(True, True)

        self.tasks = load_tasks()
        self.filter_var = tk.StringVar(value="all")

        self.build_ui()
        self.refresh_list()

    def build_ui(self):
        title_frame = tk.Frame(self.root, bg="#1e1e2e")
        title_frame.pack(fill="x", padx=20, pady=(16, 0))
        tk.Label(title_frame, text="Task Manager", font=("Helvetica", 20, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4").pack(side="left")
        tk.Label(title_frame, text="C + Python project",
                 font=("Helvetica", 11), bg="#1e1e2e", fg="#6c7086").pack(side="left", padx=12, pady=4)

        input_frame = tk.Frame(self.root, bg="#1e1e2e")
        input_frame.pack(fill="x", padx=20, pady=12)

        self.title_entry = tk.Entry(input_frame, font=("Helvetica", 13),
                                    bg="#313244", fg="#cdd6f4", insertbackground="#cdd6f4",
                                    relief="flat", bd=0)
        self.title_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))
        self.title_entry.insert(0, "Enter task title...")
        self.title_entry.bind("<FocusIn>",  lambda e: self.clear_placeholder())
        self.title_entry.bind("<FocusOut>", lambda e: self.restore_placeholder())
        self.title_entry.bind("<Return>", lambda e: self.add_task())

        self.priority_var = tk.StringVar(value="low")
        priority_menu = ttk.Combobox(input_frame, textvariable=self.priority_var,
                                     values=["low", "medium", "high"],
                                     width=8, font=("Helvetica", 12), state="readonly")
        priority_menu.pack(side="left", padx=(0, 8), ipady=4)

        add_btn = tk.Button(input_frame, text="+ Add Task", font=("Helvetica", 12, "bold"),
                            bg="#89b4fa", fg="#1e1e2e", relief="flat", bd=0,
                            padx=14, pady=6, cursor="hand2", command=self.add_task)
        add_btn.pack(side="left")

        filter_frame = tk.Frame(self.root, bg="#1e1e2e")
        filter_frame.pack(fill="x", padx=20, pady=(0, 8))
        tk.Label(filter_frame, text="Show:", font=("Helvetica", 11),
                 bg="#1e1e2e", fg="#6c7086").pack(side="left", padx=(0, 8))
        for label, value in [("All", "all"), ("Pending", "pending"), ("Done", "done")]:
            tk.Radiobutton(filter_frame, text=label, variable=self.filter_var,
                           value=value, font=("Helvetica", 11),
                           bg="#1e1e2e", fg="#cdd6f4", selectcolor="#313244",
                           activebackground="#1e1e2e", activeforeground="#cdd6f4",
                           command=self.refresh_list).pack(side="left", padx=4)

        tree_frame = tk.Frame(self.root, bg="#1e1e2e")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 8))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                         background="#313244", foreground="#cdd6f4",
                         fieldbackground="#313244", rowheight=36,
                         font=("Helvetica", 12))
        style.configure("Treeview.Heading",
                         background="#45475a", foreground="#cdd6f4",
                         font=("Helvetica", 12, "bold"), relief="flat")
        style.map("Treeview", background=[("selected", "#89b4fa")],
                  foreground=[("selected", "#1e1e2e")])

        self.tree = ttk.Treeview(tree_frame,
                                  columns=("id", "title", "priority", "status"),
                                  show="headings", selectmode="browse")
        self.tree.heading("id",       text="ID")
        self.tree.heading("title",    text="Title")
        self.tree.heading("priority", text="Priority")
        self.tree.heading("status",   text="Status")
        self.tree.column("id",       width=40,  anchor="center")
        self.tree.column("title",    width=340, anchor="w")
        self.tree.column("priority", width=100, anchor="center")
        self.tree.column("status",   width=100, anchor="center")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.tag_configure("done",   foreground="#a6e3a1")
        self.tree.tag_configure("high",   foreground="#f38ba8")
        self.tree.tag_configure("medium", foreground="#f9e2af")
        self.tree.tag_configure("low",    foreground="#89dceb")

        btn_frame = tk.Frame(self.root, bg="#1e1e2e")
        btn_frame.pack(fill="x", padx=20, pady=(0, 16))

        tk.Button(btn_frame, text="Mark Done", font=("Helvetica", 12),
                  bg="#a6e3a1", fg="#1e1e2e", relief="flat", bd=0,
                  padx=14, pady=6, cursor="hand2",
                  command=self.mark_done).pack(side="left", padx=(0, 8))

        tk.Button(btn_frame, text="Delete", font=("Helvetica", 12),
                  bg="#f38ba8", fg="#1e1e2e", relief="flat", bd=0,
                  padx=14, pady=6, cursor="hand2",
                  command=self.delete_task).pack(side="left")

        self.status_label = tk.Label(btn_frame, text="", font=("Helvetica", 11),
                                      bg="#1e1e2e", fg="#a6e3a1")
        self.status_label.pack(side="right")

    def clear_placeholder(self):
        if self.title_entry.get() == "Enter task title...":
            self.title_entry.delete(0, tk.END)
            self.title_entry.config(fg="#cdd6f4")

    def restore_placeholder(self):
        if not self.title_entry.get():
            self.title_entry.insert(0, "Enter task title...")
            self.title_entry.config(fg="#6c7086")

    def add_task(self):
        title = self.title_entry.get().strip()
        if not title or title == "Enter task title...":
            self.show_status("Please enter a task title.", error=True)
            return
        task = {
            "id":       next_id(self.tasks),
            "title":    title,
            "done":     False,
            "priority": self.priority_var.get()
        }
        self.tasks.append(task)
        save_tasks(self.tasks)
        self.title_entry.delete(0, tk.END)
        self.restore_placeholder()
        self.refresh_list()
        self.show_status(f"Added: {task['title']}")

    def refresh_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        f = self.filter_var.get()
        for t in self.tasks:
            if f == "pending" and t["done"]:     continue
            if f == "done"    and not t["done"]: continue
            status = "done" if t["done"] else "pending"
            tag    = "done" if t["done"] else t["priority"]
            self.tree.insert("", "end",
                              iid=str(t["id"]),
                              values=(t["id"], t["title"], t["priority"], status),
                              tags=(tag,))

    def get_selected_id(self):
        sel = self.tree.selection()
        if not sel:
            self.show_status("Select a task first.", error=True)
            return None
        return int(sel[0])

    def mark_done(self):
        tid = self.get_selected_id()
        if tid is None: return
        for t in self.tasks:
            if t["id"] == tid:
                if t["done"]:
                    self.show_status("Already marked done.", error=True)
                    return
                t["done"] = True
                save_tasks(self.tasks)
                self.refresh_list()
                self.show_status(f"Done: {t['title']}")
                return

    def delete_task(self):
        tid = self.get_selected_id()
        if tid is None: return
        for t in self.tasks:
            if t["id"] == tid:
                if not messagebox.askyesno("Delete", f"Delete \"{t['title']}\"?"):
                    return
                self.tasks.remove(t)
                save_tasks(self.tasks)
                self.refresh_list()
                self.show_status(f"Deleted task [{tid}]")
                return

    def show_status(self, msg, error=False):
        self.status_label.config(text=msg,
                                  fg="#f38ba8" if error else "#a6e3a1")
        self.root.after(3000, lambda: self.status_label.config(text=""))

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()