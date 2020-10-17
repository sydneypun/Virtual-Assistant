# DEPENDENCIES 
import speech_recognition as sr
import os
import re
import time
import webbrowser
import random
from selenium import webdriver
from selenium.webdriver.common.keys import keys
import smtplib
import requests 
from pygame import mixer
import urllib.request
import urllib.parse
from gtts import gTTs
import calendar
import bs4

# Function allowing the user to speak to the assistant. 
def talk(audio):
    "speaks audio passed as argument"

    print(audio)
    for line in audio.splitlines():
        text_to_speech = gTTS(text=audio, lang='en-uk')
        text_to_speech.save('audio.mp3')
        mixer.init()
        mixer.music.load("audio.mp3")
        mixer.music.play()

# Function that listens for commands 
def my_command():
    "listens for commands"
    # Initialize the recognizer
    # The primary purpose of a Recognizer instance is, of course, to recognize speech. 
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('TARS is Ready...')
        r.pause_threshold = 1
        # Wait for a second to let the recognizer adjust the  
        # Energy threshold based on the surrounding noise level 
        r.adjust_for_ambient_noise(source, duration=1)
        # Listens for the user's input
        audio = r.listen(source)
        print('analyzing...')

    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
        time.sleep(2)

    # Loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')
        command = my_command()

    return command

# Function that contains the different types of commands i.e. email, google, youtube and wikipedia search, etc. 
def tars(command):
    errors=[
        "I don't know what you mean",
        "Excuse me?",
        "Can you repeat it please?",
    ]
    "if statements for executing commands"

    # Search on Google
    if 'open google and search' in command:
        reg_ex = re.search('open google and search (.*)', command)
        search_for = command.split("search",1)[1] 
        print(search_for)
        url = 'https://www.google.com/'
       
        if reg_ex:
            subgoogle = reg_ex.group(1)
            url = url + 'r/' + subgoogle
        talk('Okay!')
        driver = webdriver.Firefox(executable_path='/home/coderasha/Desktop/geckodriver')
        driver.get('http://www.google.com')
        search = driver.find_element_by_name('q')
        search.send_keys(str(search_for))
        
        # Hit return after you enter search text
        search.send_keys(keys.RETURN) 

    # Sending an email
    elif 'email' in command:
        talk('What is the subject?')
        time.sleep(3)
        subject = my_command()
        talk('What should I say?')
        message = my_command()
        content = 'Subject: {}\n\n{}'.format(subject, message)

        # Initialize Gmail SMTP
        mail = smtplib.SMTP('smtp.gmail.com', 587)

        # Identify the server
        mail.ehlo()

        # Encrypt the session
        mail.starttls()

        # Login
        mail.login('your_mail', 'your_mail_password')

        # Send message
        mail.sendmail('FROM', 'TO', content)

        # End mail connection
        mail.close()

        talk('Email sent.')

    # Search in wikipedia (e.g. Can you search in wikipedia apples)
    elif 'wikipedia' in command:
        reg_ex = re.search('wikipedia (.+)', command)
       
        if reg_ex: 
            query = command.split("wikipedia",1)[1] 
            response = requests.get("https://en.wikipedia.org/wiki/" + query)
            
            if response is not None:
                html = bs4.BeautifulSoup(response.text, 'html.parser')
                title = html.select("#firstHeading")[0].text
                paragraphs = html.select("p")
                for para in paragraphs:
                    print (para.text)
                intro = '\n'.join([ para.text for para in paragraphs[0:3]])
                print (intro)
                mp3name = 'speech.mp3'
                language = 'en'
                myobj = gTTS(text=intro, lang=language, slow=False)   
                myobj.save(mp3name)
                mixer.init()
                mixer.music.load("speech.mp3")

            elif 'stop' in command:
                mixer.music.stop()

    # Search videos on Youtube and play (e.g. Search in youtube believer)
    elif 'youtube' in command:
        talk('Ok!')
        reg_ex = re.search('youtube (.+)', command)
        if reg_ex:
            domain = command.split("youtube",1)[1] 
            query_string = urllib.parse.urlencode({"search_query" : domain})
            html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
            
            # Print("http://www.youtube.com/watch?v=" + search_results[0])
            webbrowser.open("http://www.youtube.com/watch?v={}".format(search_results[0]))
            pass

    elif 'hello' in command:
        talk('Hello! I am TARS. How can I help you?')
        time.sleep(3)

    elif 'who are you' in command:
        talk('I am one of four former U.S. Marine Corps tactical robots')
        time.sleep(3)

    else:
        error = random.choice(errors)
        talk(error)
        time.sleep(3)

talk('TARS activated!')

# Loop to continue executing multiple commands
while True:
    time.sleep(4)
    tars(my_command())