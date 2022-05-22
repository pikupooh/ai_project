# pip install pipwin
# pipwin install pyaudio

from os import error
import time
import speech_recognition as s 
import os

sr=s.Recognizer()
print("Speech Recognition Started")

while True:
    dir_path = os.getcwd()
    audio_file = s.AudioFile(dir_path + "\\testing_set\\sample.wav")
    with audio_file as m:
        try:
            audio=sr.record(m)
            query=sr.recognize_google(audio,language='eng-in')
            print(query)
            speech_text = query
        except:
            speech_text = ""

        
  
    # with s.Microphone() as m:
    #     try:
    #         audio=sr.listen(m)
    #         query=sr.recognize_google(audio,language='eng-in')
    #         print(query)

            
    #     except:
    #         print("Unable to recognize speech :(  Please try again  and talk loudly and clearly")
