# CITATION 1: https://www.youtube.com/watch?v=AGatX_8gaeM
# CITATION 2: https://www.youtube.com/watch?v=4k9CphTdnWE

# DEPENDENCIES 
import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import random
import wikipedia

# Ignore any warning messages
warnings.filterwarnings('ignore')

# Record audio and return as a string
def record_audio(): 
    # Record the audio
    r = sr.Recognizer() # Creating a recognizer object

    # Turn on the microphone and start recording
    with sr.Microphone() as source: 
        # Print statement for testing purposes
        print('Hello this is SPUN!')
        # Listen with the microphone and record
        audio = r.listen(source)

    # Use Google's speech recognition
    user_audio = ''
    try: 
        user_audio = r.recognize_google(audio)
        print('You said: ' + user_audio)
    except sr.UnknownValueError: # Check for unknown value error
        print('Sorry, Google Speech Recognition could not recognize the audio. Unknown error.')
    except sr.RequestError as e: 
        print('Request results from Google Speech Recognition service error: ' + e)

    return user_audio
