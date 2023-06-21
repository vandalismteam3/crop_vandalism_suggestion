import streamlit as st
from keras.models import load_model
import cv2
import numpy as np

st.title("Rodent detection system")
section_option = st.selectbox('Choose your option', ('Webcam', 'File'))
if section_option == 'Webcam':
    webcam_selected = st.selectbox('Choose your Webcam Index', ('0'))
    
label_file = "C:/Python310/work/labels.txt"
model_file = "C:/Python310/work/keras_model.h5"

np.set_printoptions(suppress=True)
model = load_model(model_file, compile=False)
class_names = open(label_file, "r").readlines()

import serial
import time

prevLbl = "neutral"
prevCount = 0
sentStat = 0

def sendSMS (msg):
    ser.write ("AT\r\n".encode())
    print ("AT")
    time.sleep (2)
    ser.write ("AT+W\r\n".encode())
    print ("AT+W")
    time.sleep (2)
    ser.write ("AT+CMGF=1\r\n".encode())
    print ("AT+CMGF=1")
    time.sleep (2)
    ser.write ("AT+CMGS=\"8138085189\"\r\n".encode())
    print ("AT+CMGS=\"8138085189\"")
    time.sleep (2)
    ser.write (msg.encode())
    print (msg)
    time.sleep (2)

    ser.write (chr(26).encode())
    print (chr(26))
    time.sleep (5)


if st.button('Start'):
    if section_option == 'Webcam':
        vs = cv2.VideoCapture(0)

    writer = None
    image_placeholder = st.empty()

    label = st.empty()    
    while True:
        (grabbed, frame) = vs.read()

        if not grabbed:
            break

        t = st.empty()
        image = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
        cv2.imshow("Webcam Image", image)
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
        image = (image / 127.5) - 1

        prediction = model.predict(image)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        classNametoPrint = ""
        confiPer = 0
        if np.round(confidence_score * 100) > 95:
            classNametoPrint = class_name[2:]
            confiPer = np.round(confidence_score * 100)
##            print("Class:" + classNametoPrint)
##            print("Confidence Score:" + str(confiPer) + "%")
        else:
            classNametoPrint = "neutral"
            confiPer = np.round(confidence_score * 100)
##            print("Class:neutral")
##            print("Confidence Score:" + str(confiPer) + "%")

        print (classNametoPrint)
        if classNametoPrint == "buffalo" or classNametoPrint == "deer" or classNametoPrint == "elephant" or classNametoPrint == "pigeon" or classNametoPrint == "rabbit" or classNametoPrint == "sheep":
            if sentStat == 0:
                if prevLbl != classNametoPrint:
                    sentStat = 1
                    prevLbl = classNametoPrint
                    prevCount += 1
            print (prevCount)
        else:
            if sentStat == 1:
                sentStat = 0
                prevCount = 0
            print (prevCount)

        if prevCount == 5:
            print ("Intrution detected")
            prevCount = 0

            ser = serial.Serial ("COM5", 9600)
            if not ser.isOpen():
                ser.open ()

            ser.write ("AT\r\n".encode())
            print ("AT")
            time.sleep (2)
            ser.write ("AT+W\r\n".encode())
            print ("AT+W")
            time.sleep (2)
            ser.write ("AT+CMGF=1\r\n".encode())
            print ("AT+CMGF=1")
            time.sleep (2)
            ser.write ("AT+CMGS=\"8138085189\"\r\n".encode())
            print ("AT+CMGS=\"8138085189\"")
            time.sleep (2)
            ser.write ("Intrution detected".encode())
            print (msg)
            time.sleep (2)

            ser.close ()

        printlabel = str (classNametoPrint) + "(" + str(confiPer) + "%)"
        cv2.putText (frame, printlabel, (0,100), cv2.FONT_HERSHEY_COMPLEX, 2, (255,255,120), 2)
        
        display = 1
        if display > 0:
            image_placeholder.image(frame, caption='System Running..!', channels="BGR")

        if writer is not None:
            writer.write(frame)

st.success("Crop Protection")
