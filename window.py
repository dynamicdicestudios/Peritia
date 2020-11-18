#Import the library
from tkinter import *
import tkinter.scrolledtext as tkst
import time, threading, random

#import model
#from model import model_response

import detect_sentiments
from detect_sentiments import analyse_sentiments


"""root = Tk()

root.title("Chat Bot")
root.geometry("400x500")
root.resizable(width=FALSE, height=FALSE)

main_menu = Menu(root)

chatWindow = Text(root, bd=1, bg="black",  width="50", height="8", font=("Arial", 23), foreground="#00ffff")
chatWindow.place(x=6,y=6, height=385, width=370)

input_user = StringVar()
input_field = Entry(root, text=input_user, bd=0, bg="black", font=("Arial", 15))
input_field.place(x=128, y=400, height=88, width=260)

#interesting option: add star cursor using cursor="star"
scrollbar = Scrollbar(root, command=chatWindow.yview)
scrollbar.place(x=375,y=5, height=385)

chatWindow.configure(background='light steel blue')
input_field.configure(background='light grey')

def enter_message():
    editArea.config(state="normal")
    editArea.insert(END, 'You: %s\n\n' % input_get)
    editArea.config(state=DISABLED)

Button= Button(root, text="Send",  width="12", height=5,
                    bd=0, bg="#0080ff", activebackground="#00bfff",foreground='#ffffff',font=("Arial", 12))
Button.place(x=6, y=400, height=88)

root.mainloop()"""

def greeting() -> str:
    t = time.localtime()
    current_hour = time.strftime("%H", t)
    if int(current_hour) < 12:
        greeting = "Good morning!"
    elif int(current_hour) >= 12 and int(current_hour) <= 16:
        greeting = "Good afternoon!"
    elif int(current_hour) > 16:
        greeting = "Good evening!"
    else:
        greeting = "Good Night!"

    return greeting

def respond(message) -> str:
    return "This message is " + analyse_sentiments(message).lower()        

window = Tk()

window.title("DIG Bot")
window.geometry("400x500")
window.resizable(False, False)

#respond("hi")

greet = greeting()

editArea = tkst.ScrolledText(
    master = window,
    wrap   = WORD,
    width  = window.winfo_width(),
    height = window.winfo_height()
)

editArea.insert(END, "DIG Bot: " + greet + "\n\n")
editArea.config(state=DISABLED)

input_user = StringVar()
input_field = Entry(window, text=input_user)
#None used to be the value for the fill option
input_field.pack(side=BOTTOM, fill=BOTH, ipadx=15)

editArea.configure(background='light steel blue')
#messages.configure(background='white')
input_field.configure(background='light grey')

# Don't use widget.place(), use pack or grid instead, since
# they behave better on scaling the window -- and you don't
# have to calculate it manually!
editArea.pack(padx=10, pady=10, fill=BOTH, expand=True)

def enter_pressed(event):
    input_get = input_field.get()
    if input_get.isspace() or len(input_get) == 0:
        return "break"
    
    editArea.config(state="normal")
    editArea.insert(END, 'You: %s\n\n' % input_get)
    editArea.config(state=DISABLED)
    input_user.set('')
        
    thread = threading.Thread(target=answer, args = (input_get,))
    thread.start()
    
    return "break"
    
def answer(text:str):
    answer = respond(text)
    editArea.config(state=NORMAL)
    editArea.insert(END, 'DIG Bot: %s\n\n' % answer)
    editArea.config(state=DISABLED)

input_field.bind("<Return>", enter_pressed)

window.mainloop()
