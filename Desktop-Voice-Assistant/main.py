from tkinter import *
from helper import *
import speech_recognition as sr
from threading import Thread

EXIT_FLAG = False
#------------------- UI config variables------------------------#
BACKGROUND_COLOR = "#2c2d44"
FONT_COLOR = "#ebf7f7"
BUTTON_BACKBROUND = "#ff876f"
BUTTON_FONT = "#adebea"

#------------------ Assistant Functions--------------------------#
def get_voice_commands(keyword="something", n=0):
    canvas.itemconfig(exit_text, text="")
    if n<2:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            #canvas.itemconfig(instruction, text=f"Please say {keyword}....",
            #                  fill = FONT_COLOR,
            #                         font = ("Ariel", 20, "italic"))
            engine_response(f"Please say {keyword}")
            recognizer.pause_threshold = 0.8
            recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for 1 second of ambient noise
            audio = recognizer.listen(source)

        try:
            #canvas.itemconfig(instruction, text="Recognizing....",
            #                    fill = FONT_COLOR,
            #                    font = ("Ariel", 20, "italic"))
            engine_response("Recognizing")
            query = recognizer.recognize_google(audio, language='en-in')
            print(f"You said: {query}")
        except Exception as e:
            print(e)
            engine_response("Say that again please...")
            get_voice_commands(keyword, n+1)
            return "None"
        return query
    
def do_task():
    global EXIT_FLAG
    while not EXIT_FLAG:
        query = get_voice_commands().lower()
        if "open" in query:
            query = query.replace("open", "")
            open_link(query)
        elif "search" in query:
            query = query.replace("search", "")
            open_link(query)
        elif ("send" in query) and ("mail" in query):
            receiver_addr = input("The Receiver Address is: ")
            subject = get_voice_commands("the subject of the mail")
            body = get_voice_commands("the body of the mail")
            send_mail(receiver_addr, subject, body)
        elif "joke" in query:
            say_joke()
        elif "time" in query:
            get_time()
        elif "find" in query:
            query = query.replace("find", "")
            find_places(query)
        elif "go to sleep" in query:
            exit_assistant()
        else:
            engine_response("Couldn't get your command.")
            
def wake_and_greet():
    global EXIT_FLAG
    EXIT_FLAG = False
    engine_response("Hello! How can I help you at the moment?")
    do_task()
    
def exit_assistant():
    global EXIT_FLAG
    engine_response("Stopping the assistant.....")
    EXIT_FLAG = True

#-------------------- UI SETUP ---------------------------------#
window = Tk()
window.title("Desktop Voice Assistant")
window.geometry("1500x800")
window.config(padx= 50, pady= 100, bg = BACKGROUND_COLOR)

def button_command():
    global EXIT_FLAG
    if not EXIT_FLAG:
        Thread(target = wake_and_greet()).start()
    else:
        exit_assistant() 

canvas = Canvas(width = 1200 , height = 600, bg = BACKGROUND_COLOR ,
                borderwidth = 0, highlightthickness = 0)
back_img = PhotoImage(file = "back.png")
canvas_image = canvas.create_image(600, 300, image = back_img)
title_words = canvas.create_text(600, 30, text = "Your Personal Assistant",
                                 fill = FONT_COLOR,
                                 font = ("Ariel", 60, "bold"))
instruction = canvas.create_text(600, 320, text = "Click the button at the bottom if you need assistance.",
                                 fill = FONT_COLOR,
                                 font = ("Ariel", 20, "italic"))
exit_text = canvas.create_text(600, 400, text = "Say \"GO TO SLEEP\" when you don't need me anymore",
                                 fill = FONT_COLOR,
                                 font = ("Ariel", 20, "italic"))  

canvas.grid(column = 0, row = 0, columnspan = 3, rowspan = 2)
wakeup_button = Button(text = "WAKE UP", fg = BUTTON_FONT, bg = BUTTON_BACKBROUND,
                       font = ("Ariel", 10, "bold"),
                       height = 2, width = 10, command= button_command)
wakeup_button.grid(column = 1, row = 1, padx = 3)

window.mainloop()