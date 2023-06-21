
from tensorflow.keras.models import load_model
import cv2
import numpy as np
import pywhatkit
import serial as s
ser = s.Serial('com17', 9600, timeout=0)   # check your com port
print(ser.name,"connected")


np.set_printoptions(suppress=True)
model = load_model("keras_model.h5", compile=False)
class_names = open("labels.txt", "r").readlines()
camera = cv2.VideoCapture(0)

while True:
    ret, image = camera.read()
    cv2.imshow("Webcam Image", image)
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    image = (image / 127.5) - 1

    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

##    print("Class:", class_name[2:], end="")
##    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
    #print("aaaa"+class_name[2:])
    if np.round(confidence_score * 100) > 95:
        res=class_name[2:]
        if str(class_name[2:])=="neutral":
            print("............................................"+res)
        else:
            print("Class:", class_name[2:], end="")
            #print("xdgdfhhfdhhh")
            print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
            pywhatkit.sendwhatmsg_instantly('+918138085189', str(class_name[2:]), 10)
            ser.write(b'B')


    keyboard_input = cv2.waitKey(1)
    if keyboard_input == 27:
        break

camera.release()
cv2.destroyAllWindows()
