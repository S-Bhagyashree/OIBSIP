import webbrowser
import datetime 
import os
import smtplib
from email.message import EmailMessage
import pyjokes
import pyttsx3
import serpapi
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

MY_EMAIL = os.getenv('mail_id')
MY_PASSWORD = os.getenv("email_pass")

SERP_API_KEY = os.getenv('serp_api_key')

engine = pyttsx3.init('sapi5')#initializing the text to speech engine
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[1].id)#1 for female voice and 0 for male voice



def engine_response(audio):
    '''
    Function accepts audio as input and trasmits the audio.
    '''
    engine.say(audio)
    engine.runAndWait() #runs a loop until the completion of transmission
        
def open_link(link):
    '''
    Function takes the keyword and opens the appropriate app 
    or looks up the keyword and opens the browser with the appropriate web page.
    Args:
        link (str): which app to open or what to search for
    '''
    if "youtube" in link:
        engine_response("Opening youtube..")
        webbrowser.open("https://www.youtube.com/")
    elif ("google" in link) or ("browser" in link):
        engine_response("Opening the search engine..")
        webbrowser.open("https://www.google.com/")
    else:
        engine_response("Looking up and getting the results..")
        client = serpapi.Client(api_key= SERP_API_KEY)
        s = client.search(q=link, engine="google")
        webbrowser.open(s['organic_results'][0]['link'])
    
def get_time():
    '''
    Function responds with the current time.
    '''
    str_time = datetime.datetime.now().strftime("%H:%M:%S")
    engine_response(f"The time is {str_time}")
    
def say_joke():
    '''
    Function used to respond with a joke.
    '''
    engine_response(pyjokes.get_joke())
    

def find_places(place):
    """
    Function returns top search location for the input place from google map results.
    Args:
        place (str): string with information on which place to look up for.
    """
    
    client = serpapi.Client(api_key= SERP_API_KEY)
    s = client.search(q=place, engine="google_maps")
    engine_response(s['local_results'][0]['title']+'Address is'+
          s['local_results'][0]['address']+
          s['local_results'][0]['open_state'])
    
def send_mail(receiver_addr, subject, message_text):
    """Function accepts necessary inputs to send an email and sends a mail
    from you email id to the receiver address.

    Args:
        receiver_addr (str): receiver email address
        subject (str): subject of the mail
        message_text (str): body of the email
    """
    email = EmailMessage()
    email['from'] = MY_EMAIL
    email['to'] = receiver_addr
    email['subject'] = subject
    email.set_content(f"{message_text}")
 
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.send_message(email)
    

    
    

