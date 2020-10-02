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

# TESTING: Calling the record audio function
# record_audio()

# A function to get the virtual assistant response
def assistant_response(text): 
    print(text)

    # Convert text to speech
    my_obj = gTTS(text=text, lang='en', slow=False)

    # Save the converted audio to a file 
    my_obj.save('assistant_response.mp3')

    os.system('start assistant_response.mp3')

# TESTING: Calling the assistant response function
# text = 'Hello, my name is SPUN. How can I assist you today?'
# assistant_response(text)

