import tkinter
from tkinter import  messagebox
from tkinter import filedialog
import time


def messageBox(message,title=""):
    root = tkinter.Tk()
    root.withdraw()
    root.update()
    res = messagebox.showinfo(title,message)
    root.update()
    root.destroy()
    return res

def showMessageforXseconds(message,timer):
    root = tkinter.Tk()
    root.withdraw()
    root.update()
    top = tkinter.Toplevel(root)
    #top.title("Copy RTPCs from source to targets")
    tkinter.Message(top,text=message,padx=100,pady=100,font=("Ariel", 20)).pack()
    top.after(timer*1000, top.destroy)
    root.update()
    time.sleep(timer)
    return True


def askUserForDirectory():
    root = tkinter.Tk()
    root.withdraw()
    root.update()
    dir = filedialog.askdirectory(title="Choose source directory")
    root.update()
    root.destroy()
    return dir