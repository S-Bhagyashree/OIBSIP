from tkinter import *
from PIL import ImageTk, Image
import requests

API_KEY = "68eed7e5a2895f6cdaa3ea1107fddec5"
#-----------UI CONFIG VARIABLES-----------#
BACKGROUND_COLOR = "#4babbb"
FONT_COLOR1 = "#ffffff"
FONT_COLOR2 = "#eeff25"

#--------Application Setup----------------#
def get_weather():
    city_name = location.get()
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}"
    response = requests.get(url = url)
    weather_data = response.json()
    temp = weather_data['main']['temp']-273.15
    weather = ['Description:',weather_data['weather'][0]['description'], 
                       "Temp:",str(round(temp,2)),
                       "Humidity:",str(weather_data['main']['humidity']),
                       "Wind Speed:", str(weather_data['wind']['speed'])]
    part1 = " ".join(weather[:2])
    part2 = " ".join(weather[2:])
    canvas.itemconfig(word_text, text = f"Weather of {city_name} is {part1}",
                      fill = FONT_COLOR1,
                      font = ("Ariel", 20, "bold"))
    canvas.itemconfig(click_text, text = f"{part2}",
                      fill = FONT_COLOR1,
                      font = ("Ariel", 20, "bold"))
    

#--------------UI SETUP-------------------#
window = Tk()
window.title("Weather App")
window.config(padx=50, pady = 50, bg = BACKGROUND_COLOR)

canvas = Canvas(width = 800 , height = 526, bg = BACKGROUND_COLOR,
                borderwidth = 0, highlightthickness = 0)
back_img = ImageTk.PhotoImage(Image.open('back.png'))
canvas_image = canvas.create_image(405, 263, image = back_img)
word_text = canvas.create_text(400, 50, text = "Weather Application", fill = FONT_COLOR2,
                                 font = ("Ariel", 60, "bold"))
click_text = canvas.create_text(400, 420, text = "Enter Location and Click Proceed",
                                 fill = FONT_COLOR2, font = ("Ariel", 20, "bold"))
canvas.grid(column = 0, row = 0, columnspan = 2)

city_label = Label(text = "City:", height = 2, width = 5)
city_label.grid(column = 0, row  =2)

location = Entry(width = 21)
location.grid(column = 1, row  =2, sticky = 'w')

proceed_button = Button(text = "Proceed", height=2, width=8, command = get_weather)
proceed_button.grid(column = 2, row  =2)

window.mainloop()