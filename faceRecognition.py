from asyncio.windows_events import NULL
import math
import time
import os
from xml.etree.ElementTree import tostring
import cv2
from simple_facerec import SimpleFacerec
import speech_recognition as s
import threading
from threading import Timer
import SpeakerIdentification
from queue import Queue
from speaker import Speaker
from speechText import SpeechText

from videoFrame import VideoFrame

video_frames = Queue()
video_display_started = False

speakers = Queue()
speech_texts = Queue()

def face_reg():
    # Encode faces from a folder
    sfr = SimpleFacerec()
    sfr.load_encoding_images("images/")
    speaker_thread.start()
    video_display_thread.start()
    

    # Load Camera
    cap = cv2.VideoCapture(0)
    
    # print("Face Recognition Started")

    while True:
        ret, frame = cap.read()

        # Detect Faces
        face_locations, face_names = sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

        videoframe = VideoFrame(time.time(), frame)
        video_frames.put(videoframe) 

        key = cv2.waitKey(1)
        if key == 27 :
            cap.release()
            cv2.destroyAllWindows()
            break


def draw_video_frames():

    global video_display_started
    while not video_display_started:
        continue

    prev_timestamp = 0
    first_frame = True

    speaker = speakers.get()
    subs = speech_texts.get()
    
    while True:
        new_frame = video_frames.get()
        frame = new_frame.getFrame()
        
        delta_time = new_frame.getTimestamp() - prev_timestamp
        prev_timestamp = new_frame.getTimestamp()

        if speaker.getTimestamp() < prev_timestamp:
            speaker = speakers.get()

        if subs.getTimestamp() < prev_timestamp:
            subs = speech_texts.get()

        if not first_frame:
            time.sleep(delta_time)

        cv2.putText(frame, speaker.getSpeaker() + ' speaking ',(50, 50 ), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        cv2.putText(frame, subs.getSpeechText() ,(200, 600 ), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == 27 :
            cv2.destroyAllWindows()
            return

        first_frame = False

        
        


def speaker_reg():

    global speaker_name
    global speech_text
    sr=s.Recognizer()

    while True:
        # print("audio record started")
        
        SpeakerIdentification.record_audio_test()
        timestamp = time.time()
        speaker_name = SpeakerIdentification.test_model()
        
        speaker = Speaker(timestamp, speaker_name)
        speakers.put(speaker)

        dir_path = os.getcwd()
        audio_file = s.AudioFile(dir_path + '\\testing_set\\sample.wav')
        with audio_file as m:
            try:
                audio=sr.record(m)
                query=sr.recognize_google(audio,language='eng-in')
                # print(query)
                speech_text = query
            except:
                speech_text = "none"
            
            finally:
                speech_texts.put(SpeechText(timestamp, speech_text, speaker))
            
        print(speech_text)

face_thread = threading.Thread(target=face_reg)
speaker_thread = threading.Thread(target=speaker_reg)
video_display_thread = threading.Thread(target = draw_video_frames)

face_thread.daemon = True
speaker_thread.daemon = True
video_display_thread.daemon = True



if __name__ == "__main__":
    face_thread.start()
    
    face_thread.join()
    


