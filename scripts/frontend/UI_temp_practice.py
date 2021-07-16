import tkinter
import tkinter.ttk
import flask.testing
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog

# client = flask.testing.FlaskClient()
# client = flask.testing.Client()


root = tkinter.Tk()
root.title("My Program - Michael")
root.iconbitmap(default="images\\virtualhand_icons\\virtualhand_icon_YuG_1.ico")
# root.iconify("images\\VirtualHand-icon.ico")
root.geometry('800x600')

my_image = ImageTk.PhotoImage(Image.open("images\\virtualhand_icons\\VirtualHand-icon.png"))

e = tkinter.Entry(root, width=30, borderwidth=5)
e.grid(row=1, column=0)
e.insert(0, "Enter your name")  # Default text inside the textbox
e.delete(0, tkinter.END)
e.insert(0, "My name is something")

def myClick(myParameter):
    print("This button was clicked " + myParameter)
    myLabel3 = tkinter.Label(root, text=e.get())
    myLabel3.grid(row=4, column=1)

# Label widget
myLabel1 = tkinter.Label(root, text="Hello World!", image=my_image)
myLabel2 = tkinter.Label(root, text="My name is Michael Lapshin")

myLabel1.grid(row=0, column=0)
myLabel2.grid(row=1, column=2)

myButton = tkinter.Button(root, text="Click me", command=lambda: myClick(e.winfo_name()), padx=30, pady=15)
myButton.grid(row=3, column=1, padx=50, pady=30, columnspan=3)

# Additional Frame
frame = tkinter.LabelFrame(root, text="This is my frame", padx=50, pady=50)  # the padding inside the frame
frame.grid(row=5, column=6, padx=50, pady=50)  # This is padding outside the frame

flabel1 = tkinter.Label(frame, text="This another label!")
flabel1.grid(row=1, column=1)

def printVar(val):
    print(val.get())  # .get() gets the value of the IntVar() object
    print("slider = " + str(vertical.get()))
    print("checkbox = " + str(checkvar.get()))
    print("List box selected = " + str(LB.curselection()))

myRadVariable=tkinter.IntVar()

flabel1 = tkinter.Button(frame, text="This is my new frame!", command=lambda: printVar(myRadVariable))
flabel1.grid(row=0, column=0)


radbutton1 = tkinter.Radiobutton(frame, text="Rad Button 1", variable=myRadVariable, value=1)
radbutton2 = tkinter.Radiobutton(frame, text="Rad Button 1", variable=myRadVariable, value=2)
radbutton1.grid(row=0, column=1)
radbutton2.grid(row=1, column=0)

# messagebox.showinfo(title="Hello! World!", message="Yeah, think about this....")
# result = messagebox.askretrycancel(title="My queston", message="How are you")
# print(result)
# messagebox.showerror(title="Error", message="this is an error message")

# tkinter.Toplevel() # to create other windows

# Slider
vertical = tkinter.Scale(root, from_=0, to=200, orient=tkinter.HORIZONTAL)
vertical.grid(row=5, column=3)

# Check box
checkvar = tkinter.IntVar(0)
checkbox = tkinter.Checkbutton(root, text="Check this box, do it!", variable=checkvar, onvalue=123, offvalue=321)
checkbox.grid(row=4, column=3)

# For opening files from local drive
# root.filename = filedialog.askopenfilename(initialdir="/images", title="Select a file :)", filetypes=(("png files","*.png"), ("all files", "*.*")))

# Drop-down box
dropVariable = tkinter.StringVar()
dropVariable.set("Default value")

options = ["option A", "option B", "option C"]
drop = tkinter.OptionMenu(root, dropVariable, *options)
drop.grid(row=3, column=1)


SB = tkinter.Scrollbar(root)
SB.grid(row=2, column=1)

LB = tkinter.Listbox(root, yscrollcommand=SB.set, selectmode=tkinter.MULTIPLE)
for l in range(0, 100):
    LB.insert(l, tkinter.Button(root, text="hello " + str(l)))

LB.grid(row=2, column=2)
SB.config(command=LB.yview)

options = ("abc", "def", "hij")
varr = tkinter.StringVar()
op = tkinter.ttk.OptionMenu(root, varr, *options)
# tkinter.tix.
li = tkinter.Listbox(root)
li.insert(0, "a")
li.insert(1, "b")
li.insert(2, "c")
li.insert(3, "d")

op.grid(column=1, row=0)
li.grid(column=2, row=0)


root.mainloop()
