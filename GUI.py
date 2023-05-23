import tkinter as tk
from tkinter import *
import test_update
from test_update import chat

root = tk.Tk()
root.title('Chatbot by Cobra_Codes')

Canvas = tk.Canvas(width = 500, height = 500)
Canvas.grid(columnspan = 2)

#Create chat window

ChatWindow = Text(root, bd = 1, wrap = WORD, bg = 'white', width = 70, height = 8, font =('Arial', 12), fg='white')
ChatWindow.place(x = 6, y = 6, height = 385, width = 370)

MessageWindow = Text(root, bg = 'white', width = 20, height = 3, font =('Arial', 12), fg='black')
MessageWindow.place(x = 128, y= 400, width = 250, height = 88)

#Scroll Bar

Scrollbar = Scrollbar(root, command = ChatWindow.yview())
Scrollbar.place(x=375, y=5, height = 385)


def send():
    message = MessageWindow.get('1.0', END)

    # Check if the user's input is "exit"
    if message.strip().lower() == "exit":
        # Destroy the root window
        root.destroy()
        # End the send function by returning from it
        return

    send = f"You: {message}"
    ChatWindow.insert(END, "\n" + send, "\n")
    test_update.chat(MessageWindow, ChatWindow)  # Call the chat function with the ChatWindow and MessageWindow widgets as arguments
    MessageWindow.delete('1.0', END)

#Message send button

Button = Button(root, text='Send', bg='purple',
                activebackground='red', width=12, height=5, font=('Arial', 18), fg='white', command=send)
Button.place(x=6, y=400, height=88, width=120)

root.mainloop()
