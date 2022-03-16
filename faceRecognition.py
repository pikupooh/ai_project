import time
import cv2
from simple_facerec import SimpleFacerec
import speech_recognition as s
import threading
from threading import Timer
import SpeakerIdentification
from queue import Queue

speaker_name = "none"
speech_text = ""
video_frames = Queue()
video_delayed = False
video_delay_time = 6


def face_reg():
    # Encode faces from a folder
    global speaker_name
    sfr = SimpleFacerec()
    sfr.load_encoding_images("images/")
    speaker_thread.start()

    # Load Camera
    cap = cv2.VideoCapture(0)
    print("Face Recognition Started")

    while True:
        ret, frame = cap.read()

        # Detect Faces
        face_locations, face_names = sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

        
        if speaker_name != "none":
            cv2.putText(frame, speaker_name + ' speaking ',(50, 50 ), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        
        
        cv2.putText(frame, speech_text ,(10, 400 ), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 200), 2)

        video_frames.put(frame) 
        draw_video_frames()

        key = cv2.waitKey(1)
        if key == 27 :
            cap.release()
            cv2.destroyAllWindows()
            break

def set_video_delay():
    global video_delayed
    video_delayed = True


def draw_video_frames():
    global video_delayed, video_delay_time
    timer_called = False
    if not video_delayed:
        if not timer_called:
            fun = Timer(video_delay_time, set_video_delay)
            fun.start()
            timer_called = True
        return

    frame = video_frames.get()
    cv2.imshow("Frame", frame)
    return


def speaker_reg():

    global speaker_name
    global speech_text
    sr=s.Recognizer()
    while True:
        print("audio record started")
        SpeakerIdentification.record_audio_test()
        speaker_name = SpeakerIdentification.test_model()
        print("audio record stopped")
        # print("Speech to text started")
        # os.system('python speechReg.py')
        # dir_path = os.getcwd()
        # audio_file = s.AudioFile(dir_path + '\\testing_set\\sample.wav')
        # with audio_file as m:
        #     try:
        #         audio=sr.record(m)
        #         query=sr.recognize_google(audio,language='eng-in')
        #         print(query)
        #         speech_text = query
        #     except:
        #         speech_text = ""


face_thread = threading.Thread(target=face_reg)
speaker_thread = threading.Thread(target=speaker_reg)
face_thread.daemon = True
speaker_thread.daemon = True


if __name__ == "__main__":
    face_thread.start()
    
    face_thread.join()
    


