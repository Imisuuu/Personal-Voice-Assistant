#region imports
from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import webbrowser as wb
from pynput.keyboard import Key, Controller
from time import sleep
from googletrans import Translator
import pyperclip
import subprocess
#import keyboard
from time import sleep
#import random
import requests
import math
from datetime import datetime
import winsound 
#endregion

#region initialisation
recognizer = speech_recognition.Recognizer();

speaker = tts.init() 
speaker.setProperty('rate', 160)
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[1].id) #0 polish, 1 american, 2 spanish, 3 british

todo_list = []
#endregion

#region functions
def create_note(): #zepsute nadal
    speaker.say("What do you want to write onto your note?")
    speaker.runAndWait()
    
    done = False
    
    while not done:
        global recognizer
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                
                note = recognizer.recognize_google(audio, language="en-US")
                note = note.lower()
                
                speaker.say("Choose a filename!")
                speaker.runAndWait()
                
                recognizer.adjust_for_ambient_noise(mic,duration=0.2)
                audio = recognizer.listen(mic) 
                
                filename = recognizer.recognize_google(audio, language="en-US")
                filename = filename.lower()
                
            with open(f"{filename}.txt", "a") as f:
                f.write(note)
                done = True
                speaker.say("I successfully create the note")
                speaker.runAndWait()
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand you! Please try again!")
            speaker.runAndWait()

def add_todo(): 
    speaker.say("What to do do you want to add?")
    speaker.runAndWait()
    
    done = False
    
    while not done:
        global recognizer
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                
                item = recognizer.recognize_google(audio, language="en-US")
                item = item.lower()
                
                todo_list.append(item)
                done = True
                
                speaker.say(f'I added {item} to the to do list!')
                speaker.runAndWait()
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand! Please try again.")
            speaker.runAndWait()
            
def show_todos():
    speaker.say("The items on your to do list are the following")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()

def hello():
    speaker.say('Hello. What can I do for you?')
    speaker.runAndWait()
    
def quit_now():
    speaker.say("Bye")
    speaker.runAndWait()
    exit()
    
def search():
   
    speaker.say('What are you looking for?')
    speaker.runAndWait()
    
    done = False
    
    while not done:
        global recognizer
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                
                query = recognizer.recognize_google(audio, language="en-US")
                query = query.lower()
                
                site = 'https://www.google.com/search?q=' + query
                
                wb.get().open_new(site)
                done = True
                speaker.say(f"Here is what I found for {query}")
                speaker.runAndWait()
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand! Please try again.")
            speaker.runAndWait()

def youtube():
    speaker.say('What are you looking for?')
    speaker.runAndWait()
    
    done = False

    while not done:
        global recognizer
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                
                query = recognizer.recognize_google(audio, language="en-US")
                query = query.lower()
                
                site = 'https://www.youtube.com/results?search_query=' + query
                
                wb.get().open_new(site)
                done = True
                speaker.say(f"Here is what I found for {query}")
                speaker.runAndWait()
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand! Please try again.")
            speaker.runAndWait()

def skip():
    kb = Controller()
    kb.press(Key.media_next)

    speaker.say("I skipped this song.")
    speaker.runAndWait()
    
def previous():
    kb = Controller()
    kb.press(Key.media_previous)
    sleep(0.1)
    kb.press(Key.media_previous)

    speaker.say("Now playing previous song.")
    speaker.runAndWait()
    
def stop():
    kb = Controller()
    kb.press(Key.media_play_pause)
    
    speaker.say("I stopped or resumed this song.")
    speaker.runAndWait()
     
def translate(): 
    speaker.say('What would you like to translate?')
    speaker.runAndWait()
    
    done = False

    while not done:
        global recognizer
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                
                
                text = recognizer.recognize_google(audio, language="en-US")
                text = text.lower()
                    
                translator = Translator()
                
                
                translation = translator.translate(text, dest='es')
                speaker.setProperty('voice', voices[2].id)
                speaker.setProperty('rate', 130)
                speaker.say(translation.text)
                pyperclip.copy(translation.text)
                
                done = True
                speaker.setProperty('voice', voices[1].id)
                speaker.setProperty('rate', 160)
                speaker.runAndWait()
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand.")
            speaker.runAndWait()

def you_are_welcome():
    speaker.say("You're welcome.")
    speaker.runAndWait()

def open():
    speaker.say('What program would you like to open?')
    speaker.runAndWait()
    
    done = False
    while not done:
        global recognizer
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                
                program = recognizer.recognize_google(audio, language="en-US")
                program = program.lower()
                
                if program == 'spotify' or program == 'music' or program == '1':
                    subprocess.Popen([r"C:\Users\mikol\AppData\Roaming\Spotify\\Spotify.exe"])
                    speaker.say('I successfully opened spotify')
                    done = True
                    speaker.runAndWait()
                elif program == 'visual studio code' or program == 'vs code' or program == '2':
                    subprocess.Popen([r"C:\Users\mikol\AppData\Local\Programs\Microsoft VS Code\\Code.exe"])
                    speaker.say('I successfully opened vs code')
                    done = True
                    speaker.runAndWait()
                elif 'rocket league' in program or 'soccer' in program or 'football' in program or program == '3':
                    subprocess.Popen([r"C:\Program Files\BakkesMod\\BakkesMod.exe"])
                    sleep(0.5)
                    subprocess.Popen([r"D:\Program Files (x86)\Epic Games\Games\Rocket League\rocketleague\Binaries\Win64\\RocketLeague.exe"])
                    speaker.say('I successfully opened rocket league.')
                    done = True
                    speaker.runAndWait()
                        
                    speaker.say('I successfully opened faceit.')
                    done = True
                    speaker.runAndWait()
                else:
                    speaker.say("I don't know how to open this program.")
                    done = True

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("Please try again.")
            speaker.runAndWait()
   
def rocket():
    subprocess.Popen([r"C:\Program Files\BakkesMod\\BakkesMod.exe"])
    sleep(0.5)
    subprocess.Popen([r"D:\Program Files (x86)\Epic Games\Games\Rocket League\rocketleague\Binaries\Win64\\RocketLeague.exe"])
    speaker.say('I successfully opened rocket league.')
    speaker.runAndWait()
    
def messenger():
    site = 'https://www.messenger.com/t/2165983176859263/'
    wb.get().open_new(site)
    speaker.say('I successfully opened messanger')

def close():
    speaker.say('What program would you like to close?')
    speaker.runAndWait()
    
    done = False
    while not done:
        global recognizer
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                
                program = recognizer.recognize_google(audio, language="en-US")
                program = program.lower()
                
                if program == 'spotify' or program == 'music':
                    subprocess.call(["taskkill","/F","/IM","Spotify.exe"])
                    speaker.say('I successfully closed spotify')
                    done = True
                    speaker.runAndWait()
                elif program == 'visual studio code' or program == 'vs code':
                    subprocess.call(["taskkill","/F","/IM","Code.exe"])
                    speaker.say('I successfully closed vs code')
                    done = True
                    speaker.runAndWait()
                else:
                    speaker.say("I don't know how to close this program.")
                    done = True

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("Please try again.")
            speaker.runAndWait()   
            
def lyrics():
    speaker.say('What lyrics are you looking for?')
    speaker.runAndWait()
    
    done = False
    
    while not done:
        global recognizer
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                
                lyrics = recognizer.recognize_google(audio, language="en-US")  
                lyrics = lyrics.lower()  
                
                site = "https://genius.com/search?q=" + lyrics
                
                wb.get().open_new(site)
                done = True
                speaker.say(f"Here is what I found for {lyrics}")
                speaker.runAndWait()
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand! Please try again.")
            speaker.runAndWait()

def joke():
    try:
        url = 'https://v2.jokeapi.dev/joke/Any?type=twopart'
        response = requests.get(url).json()
        setup = response['setup']
        delivery = response['delivery']
        speaker.say(setup)
        sleep(0.8)
        speaker.say(delivery)
        speaker.runAndWait()
    except Exception as e:
        print(e)

def weather():
    try:
        city='XXX'
        api_key='XXX'
        
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        response = requests.get(url).json()
        
        temp = response['main']['temp']
        temp = math.floor(temp - 273.15)
        
        humidity = response['main']['humidity']
        
        feels_like = response['main']['feels_like']
        feels_like = math.floor(feels_like - 273.15)
        
        text = f'The temperature is {temp} Celsius, it feels like {feels_like} Celsius, humidity is {humidity} percent'
        speaker.say(text)
        speaker.runAndWait()
    except Exception as e:
        print(e)
    
def time():
    now = datetime.now() # current date and time

    time = now.strftime("%H PM %M")
    text = f'It is {time}'
    speaker.say(text)    
    speaker.runAndWait()

def location():
    speaker.say('What is the location?')
    speaker.runAndWait()
    
    done = False
    
    while not done:
        global recognizer
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                
                loc = recognizer.recognize_google(audio, language="en-US")
                loc = loc.lower()
                
                site = 'https://google.nl/maps/place/' + loc
                
                wb.get().open_new(site)
                done = True
                speaker.say(f"Here is what I found for {loc}")
                speaker.runAndWait()
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand! Please try again.")
            speaker.runAndWait()
#endregion    

#region intents
mappings = {
    "greeting": hello,
    "create_note": create_note,
    "add_todo": add_todo,
    "show_todos": show_todos,
    "exit": quit_now,
    "search": search,
    "youtube": youtube,
    "next": skip,
    "previous": previous,
    "translate": translate,
    "thankyou": you_are_welcome,
    "stop": stop,
    "close": close,
    "lyrics": lyrics,
    "joke": joke,  
    "weather": weather,
    "time": time,
    "location": location,
    "rocket": rocket,
    "messenger": messenger
}
assistant = GenericAssistant('intents.json', intent_methods=mappings)
#endregion

#region model
assistant.train_model()

assistant.save_model()

assistant.load_model() 

hour = int(datetime.now().hour)
if hour>=0 and hour<=12:
    speaker.say("Good Morning")
elif hour>12 and hour<18:
    speaker.say("Good afternoon")
else:
    speaker.say("Good evening")
speaker.runAndWait()
#endregion

# You need to press key every time you use a command!
#region loop
        
while True:
    try:
        with speech_recognition.Microphone() as mic1:
            recognizer.adjust_for_ambient_noise(mic1, duration=0.2)
            ad = recognizer.listen(mic1)
            
            msg = recognizer.recognize_google(ad, language="en-US")
            msg = msg.lower()
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
       
    if msg == 'hey jarvis' or 'hey jarvis' in msg:    #or keyboard.is_pressed('scroll_lock')
        print('Listening...')
        winsound.PlaySound("beep", winsound.SND_FILENAME)
        try:
            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                message = recognizer.recognize_google(audio, language="en-US")
                message = message.lower()
                print(message)
            assistant.request(message)
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            

#endregion

