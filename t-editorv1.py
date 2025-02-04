from tkinter import Tk, Text, Button, Menubutton, Menu, IntVar
from tkinter import filedialog as tkFileDialog

root = Tk()
root.title("xuya Studio v1.0")
text = Text(root)
text.grid()
def saveas(text_widget):
    text_content = text_widget.get("1.0", "end-1c")
    savelocation = tkFileDialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if savelocation:
        with open(savelocation, "w") as file1:
            file1.write(text_content)

def save_button_command():
    saveas(text)

button = Button(root, text="Save", command=save_button_command)
button.grid()

root.mainloop()

def FontHelvetica():
    global text
    text.config(font="Helvetica")
def FontCourier():
    global text
    text.config(font="Courier")
font_menu_button=Menubutton(root, text="Font") 
font_menu_button.grid() 
font_menu_button.menu=Menu(font_menu_button, tearoff=0) 
font_menu_button["menu"]=font_menu_button.menu
helvetica_var=IntVar() 
courier_var=IntVar()
font_menu_button.menu.add_checkbutton(label="Courier", variable=courier_var,
command=FontCourier)
font_menu_button.menu.add_checkbutton(label="Helvetica", variable=helvetica_var, 
command=FontHelvetica)