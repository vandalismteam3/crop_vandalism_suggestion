from streamlit_webrtc import webrtc_streamer, RTCConfiguration
import av
import cv2

from keras.models import load_model
import numpy as np

np.set_printoptions(suppress=True)
model = load_model("keras_model.h5", compile=False)
class_names = open("labels.txt", "r").readlines()
##camera = cv2.VideoCapture(0)

##cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

class VideoProcessor:
    def recv(self, frame):
        frm = frame.to_ndarray(format="bgr24")
        image = cv2.resize(frm, (224, 224), interpolation=cv2.INTER_AREA)
##        cv2.imshow("Webcam Image", image)
        frm = np.asarray(frm, dtype=np.float32).reshape(1, 224, 224, 3)
        frm = (frm / 127.5) - 1

        prediction = model.predict(frm)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

##        print("Class:", class_name[2:], end="")
##        print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
        if np.round(confidence_score * 100) > 95:
            print("Class:", class_name[2:], end="")
            print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
        else:
            print("Class:neutral")
            print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
        
##        frm = frame.to_ndarray(format="bgr24")
##        faces = cascade.detectMultiScale(cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY), 1.1, 3)
##        for x,y,w,h in faces:
##            cv2.rectangle(frm, (x,y), (x+w, y+h), (0,255,0), 3)

        return av.VideoFrame.from_ndarray(frm, format='bgr24')

webrtc_streamer(key="key", video_processor_factory=VideoProcessor,rtc_configuration=RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}))
