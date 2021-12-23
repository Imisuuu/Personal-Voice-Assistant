#region imports
from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys
import webbrowser as wb
from pynput.keyboard import Key, Controller, Listener, KeyCode
from pynput import keyboard 
from time import sleep
from googletrans import Translator
import pyperclip
import subprocess #aby otwierać aplikacje
import keyboard
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
def create_note():
    
    
    speaker.say("What do you want to write onto your note?")
    speaker.runAndWait()
    
    done = False
    
    while not done:
        global recognizer
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                
                note = recognizer.recognize_google(audio)
                note = note.lower()
                
                speaker.say("Choose a filename!")
                speaker.runAndWait()
                
                recognizer.adjust_for_ambient_noise(mic,duration=0.2)
                audio = recognizer.listen(mic) 
                
                filename = recognizer.recognize_google(audio)
                filename = filename.lower()
                
            with open(f"{filename}.txt", 'w') as f:
                f.write(note)
                done = True
                speaker.say(f"I successfully create the note {filename}")
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
                
                item = recognizer.recognize_google(audio)
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
                
                query = recognizer.recognize_google(audio)
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
                
                query = recognizer.recognize_google(audio)
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
                
                
                text = recognizer.recognize_google(audio)
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
    try:
        subprocess.call([r"C:\Users\mikol\AppData\Local\Programs\Microsoft VS Code\\Code.exe"])
        subprocess.call([r"C:\Users\mikol\AppData\Roaming\Spotify\\Spotify.exe"])
        speaker.runAndWait()
    except subprocess.UnknownValueError:
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
    "open": open
}
assistant = GenericAssistant('intents.json', intent_methods=mappings)
#endregion

#region model
assistant.train_model()

assistant.save_model()

assistant.load_model() 
#endregion

#You need to press key every time you use a command!
#region loop
while True: 
    if keyboard.is_pressed('scroll_lock'):
        try:
            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                message = recognizer.recognize_google(audio)
                message = message.lower()
                print(message)
            assistant.request(message)
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
#endregion

