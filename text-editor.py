from tkinter import *
from tkinter import filedialog

def main():
    root = Tk()
    root.title("xuya Studio v1.0")
    root.geometry("800x600")

    # Configure grid
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Text widget
    text = Text(root)
    text.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

    # Bottom frame
    bottom_frame = Frame(root)
    bottom_frame.grid(row=1, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

    # Save function
    def save():
        content = text.get("1.0", "end-1c")
        file = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file:
            with open(file, 'w') as f:
                f.write(content)

    # Font function
    def change_font(*args):
        text.configure(font=font_var.get())

    # Save button
    Button(bottom_frame, text="Save", command=save).pack(side=LEFT, padx=5)

    # Font selector
    fonts = ["Helvetica", "Courier", "Arial", "Times New Roman",
            "Verdana", "Calibri", "Georgia", "Comic Sans MS"]
    font_var = StringVar(root)
    font_var.set(fonts[0])
    font_var.trace('w', change_font)
    
    OptionMenu(bottom_frame, font_var, *fonts).pack(side=LEFT, padx=5)

    root.mainloop()

if __name__ == "__main__":
    main()