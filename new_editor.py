import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import json

class EnhancedEditor:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("xuya Studio v2.0")
        self.window.geometry("1000x700")
        
        # Create main container
        self.main_container = ttk.Frame(self.window)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create text area with line numbers
        self.create_text_area()
        
        # Create status bar
        self.create_status_bar()
        
        # Initialize variables
        self.current_file = None
        self.search_window = None
        self.theme = "light"
        
        # Configure tags
        self.text_area.tag_configure("found", background="yellow")
        
        # Bind shortcuts
        self.bind_shortcuts()

    def create_menu_bar(self):
        menubar = tk.Menu(self.window)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.window.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", command=lambda: self.text_area.edit_undo(), accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=lambda: self.text_area.edit_redo(), accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Find", command=self.show_search_window, accelerator="Ctrl+F")
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # Format menu
        format_menu = tk.Menu(menubar, tearoff=0)
        format_menu.add_command(label="Toggle Theme", command=self.toggle_theme)
        menubar.add_cascade(label="Format", menu=format_menu)

        self.window.config(menu=menubar)

    def create_toolbar(self):
        toolbar = ttk.Frame(self.main_container)
        toolbar.pack(fill=tk.X, padx=5, pady=2)

        # Font selector
        self.fonts = ["Helvetica", "Arial", "Times New Roman", "Courier",
                     "Verdana", "Calibri", "Georgia", "Comic Sans MS"]
        self.font_var = tk.StringVar(value=self.fonts[0])
        ttk.Label(toolbar, text="Font:").pack(side=tk.LEFT, padx=5)
        font_select = ttk.OptionMenu(toolbar, self.font_var, *self.fonts,
                                   command=self.change_font)
        font_select.pack(side=tk.LEFT, padx=5)

        # Font size selector
        self.size_var = tk.StringVar(value="12")
        ttk.Label(toolbar, text="Size:").pack(side=tk.LEFT, padx=5)
        sizes = [str(i) for i in range(8, 73, 2)]
        size_select = ttk.OptionMenu(toolbar, self.size_var, *sizes,
                                   command=self.change_font)
        size_select.pack(side=tk.LEFT, padx=5)

    def create_text_area(self):
        # Create text widget with scrollbar
        text_frame = ttk.Frame(self.main_container)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text_area = ScrolledText(text_frame, wrap=tk.WORD, undo=True)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure default font
        self.text_area.configure(font=("Helvetica", 12))

    def create_status_bar(self):
        self.status_bar = ttk.Label(self.main_container, text="Line: 1 Column: 0")
        self.status_bar.pack(fill=tk.X, padx=5, pady=2)
        self.text_area.bind("<KeyRelease>", self.update_status_bar)
        self.text_area.bind("<Button-1>", self.update_status_bar)

    def bind_shortcuts(self):
        self.window.bind("<Control-n>", lambda e: self.new_file())
        self.window.bind("<Control-o>", lambda e: self.open_file())
        self.window.bind("<Control-s>", lambda e: self.save_file())
        self.window.bind("<Control-f>", lambda e: self.show_search_window())

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.current_file = None

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, file.read())
                self.current_file = file_path
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {str(e)}")

    def save_file(self):
        if not self.current_file:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if not file_path:
                return
            self.current_file = file_path
        
        try:
            with open(self.current_file, 'w') as file:
                file.write(self.text_area.get(1.0, tk.END))
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {str(e)}")

    def show_search_window(self):
        if self.search_window:
            return
        
        self.search_window = tk.Toplevel(self.window)
        self.search_window.title("Find")
        self.search_window.geometry("300x100")
        self.search_window.transient(self.window)
        
        ttk.Label(self.search_window, text="Find:").pack(padx=5, pady=5)
        entry = ttk.Entry(self.search_window)
        entry.pack(padx=5, fill=tk.X)
        
        def find_text():
            self.text_area.tag_remove("found", "1.0", tk.END)
            search_string = entry.get()
            if search_string:
                idx = "1.0"
                while True:
                    idx = self.text_area.search(search_string, idx, nocase=True, stopindex=tk.END)
                    if not idx:
                        break
                    lastidx = f"{idx}+{len(search_string)}c"
                    self.text_area.tag_add("found", idx, lastidx)
                    idx = lastidx

        ttk.Button(self.search_window, text="Find", command=find_text).pack(pady=5)
        
        self.search_window.protocol("WM_DELETE_WINDOW", 
            lambda: [self.text_area.tag_remove("found", "1.0", tk.END), 
                    self.search_window.destroy(), 
                    setattr(self, 'search_window', None)])

    def update_status_bar(self, event=None):
        cursor_position = self.text_area.index(tk.INSERT)
        line, column = cursor_position.split('.')
        self.status_bar['text'] = f"Line: {line} Column: {column}"

    def change_font(self, *args):
        font_name = self.font_var.get()
        font_size = int(self.size_var.get())
        self.text_area.configure(font=(font_name, font_size))

    def toggle_theme(self):
        if self.theme == "light":
            self.text_area.configure(bg="gray20", fg="white", insertbackground="white")
            self.theme = "dark"
        else:
            self.text_area.configure(bg="white", fg="black", insertbackground="black")
            self.theme = "light"

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    editor = EnhancedEditor()
    editor.run()
