import time
import os
import cv2
from simple_facerec import SimpleFacerec
import speech_recognition as s
import threading
import SpeakerIdentification
from queue import Queue
from speaker import Speaker
from speech_text import SpeechText

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

    prev_timestamp = time.time()
    first_frame = True

    speaker = speakers.get()
    text = ""
    
    while True:
        new_frame = video_frames.get()
        frame = new_frame.getFrame()
        
        delta_time = (new_frame.getTimestamp() - prev_timestamp ) / 3
        prev_timestamp = new_frame.getTimestamp()

        if speaker.getEndTimestamp() < prev_timestamp:
            speaker = speakers.get()

        if not first_frame:
            time.sleep(delta_time)

        if text == "":
            try:
                text = speech_texts.get_nowait()
            except:
                text = ""
        
        if text != "":
            cv2.putText(frame, text.getText() ,(50, 200 ), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)

            if text.getEndTimestamp() < prev_timestamp:
                try:
                    text = speech_texts.get_nowait()
                except:
                    text = ""

        cv2.putText(frame, speaker.getSpeaker() + ' speaking ',(50, 50 ), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)

        # t1 = str(new_frame.getTimestamp())
        # t2 = str(speaker.getTimestamp())
        # cv2.putText(frame, "frame - " + t1 , (50, 100 ), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        # cv2.putText(frame, "speaker - " + t2 , (50, 150 ), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        

        cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Frame", 1000, 800)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == 27 :
            cv2.destroyAllWindows()
            return

        first_frame = False


def speaker_reg():

    global speaker_name
    global speech_text
    sr = s.Recognizer()

    while True:  
        startTimestamp = time.time()      
        SpeakerIdentification.record_audio_test()
        endTimestamp = time.time()
        speaker_name = SpeakerIdentification.test_model()
        
        speaker = Speaker(startTimestamp, endTimestamp, speaker_name)
        speakers.put(speaker)

        global video_display_started
        video_display_started = True

        dir_path = os.getcwd()
        audio_file = s.AudioFile(dir_path + '\\testing_set\\sample.wav')
        with audio_file as m:
            try:
                audio=sr.record(m)
                query=sr.recognize_google(audio,language='eng-in')
                speechText = SpeechText(startTimestamp, endTimestamp, query)
                speech_texts.put(speechText)
            except:
                speechText = SpeechText(startTimestamp, endTimestamp, "")
                speech_texts.put(speechText)

        

face_thread = threading.Thread(target=face_reg)
speaker_thread = threading.Thread(target=speaker_reg)
video_display_thread = threading.Thread(target = draw_video_frames)

face_thread.daemon = True
speaker_thread.daemon = True
video_display_thread.daemon = True



if __name__ == "__main__":
    face_thread.start()
    face_thread.join()
    


