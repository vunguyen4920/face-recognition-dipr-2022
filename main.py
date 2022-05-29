from detector import main_app
from classifier import train_classifer
from dataset import capture
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox,PhotoImage
names = set()


class Main(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        with open("nameslist.txt", "r") as f:
            x = f.read()
            z = x.rstrip().split(" ")
            for i in z:
                names.add(i)
        self.title_font = tkfont.Font(family='Arial', size=16, weight="bold")
        self.title("Personal Identifier")
        self.geometry("500x270")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(False, False)
        self.active_name = None
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (WelcomeScreen, AddUserScreen,  ExecutionScreen, WaitingScreen):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("WelcomeScreen")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure about that?"):
            self.destroy()


class WelcomeScreen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        addBtn = tk.Button(self, text="Add a User", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("AddUserScreen"))
        checkBtn = tk.Button(self, text="Check Users", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("WaitingScreen"))
        quitBtn = tk.Button(self, text="Quit", fg="#263942", bg="#ffffff", command=self.on_closing)
        render = PhotoImage(file='homepagepic.png')
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=0, column=3, rowspan=4, sticky="nsew")
        addBtn.grid(row=1, column=0, ipady=10, ipadx=20)
        checkBtn.grid(row=2, column=0, ipady=10, ipadx=20)
        quitBtn.grid(row=3, column=0, ipady=10, ipadx=20)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            self.controller.destroy()

class AddUserScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Enter the name", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, pady=10, padx=5)
        self.user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_name.grid(row=0, column=1, pady=10, padx=10)
        self.button_cancel = tk.Button(self, text="Cancel", bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("WelcomeScreen"))
        self.button_go_next = tk.Button(self, text="Next", fg="#ffffff", bg="#263942", command=self.train)
        self.button_cancel.grid(row=1, column=0, pady=10, ipadx=5, ipady=4)
        self.button_go_next.grid(row=1, column=1, pady=10, ipadx=5, ipady=4)
    def train(self):
        global names
        if self.user_name.get() == "None":
            messagebox.showerror("Error", "Name cannot be 'None'")
            return
        elif self.user_name.get() in names:
            messagebox.showerror("Error", "User already exists!")
            return
        elif len(self.user_name.get()) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        name = self.user_name.get()
        names.add(name)
        self.controller.active_name = name
        self.controller.show_frame("ExecutionScreen")


class ExecutionScreen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.numimglabel = tk.Label(self, text="Number of images captured = 0", font='Helvetica 12 bold', fg="#263942")
        self.numimglabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        self.capturebutton = tk.Button(self, text="Capture Data Set", fg="#ffffff", bg="#263942", command=self.capture)
        self.trainbutton = tk.Button(self, text="Train The Model", fg="#ffffff", bg="#263942",command=self.train)
        self.capturebutton.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.trainbutton.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)

    def capture(self):
        self.numimglabel.config(text=str("Captured Images = 0 "))
        messagebox.showinfo("INSTRUCTIONS", "We will Capture 300 pic of your Face.")
        x = capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Number of images captured = "+str(x)))

    def train(self):
        if self.controller.num_of_images < 300:
            messagebox.showerror("ERROR", "No enough Data, Capture at least 300 images!")
            return
        train_classifer(self.controller.active_name)
        messagebox.showinfo("SUCCESS", "The model has been successfully trained!")

        with open("nameslist.txt", "w") as f:
            global names

            f.seek(0)
            f.truncate()

            for i in names:
                f.write(i + " ")

        self.controller.show_frame("WaitingScreen")


class WaitingScreen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Face Recognition", font='Helvetica 16 bold')
        label.grid(row=0,column=0, sticky="ew")
        openWebcamBtn = tk.Button(self, text="Face Recognition", command=self.open_webcam, fg="#ffffff", bg="#263942")
        homeBtn = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("WelcomeScreen"), bg="#ffffff", fg="#263942")
        openWebcamBtn.grid(row=1,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        homeBtn.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

    def open_webcam(self):
        main_app()



app = Main()
app.mainloop()

