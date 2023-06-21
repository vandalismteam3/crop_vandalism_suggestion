import numpy as np
import cv2
from tensorflow.keras.utils import img_to_array

MIN_CONF = 0.01
NMS_THRESH = 0.3

def showChar(d, number_plate_extracted):
    CHARS = []
    for s in d:
        data = d.get(s, "")
        x= s
        y = data[0]
        w = data[1]
        h = data[2]
        crop_char = number_plate_extracted[y:y+h, x:x+w]
        CHARS.append(crop_char)
    return CHARS

def detect_plate (plate_image, plate_net, plate_ln):
    (H, W) = plate_image.shape[:2]

    blob = cv2.dnn.blobFromImage (plate_image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    plate_net.setInput (blob)
    layerOutputs = plate_net.forward (plate_ln)

    boxes = []
    centroids = []
    confidences = []
    idxs = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if confidence > MIN_CONF:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                boxes.append([x, y, int(width), int(height)])
                centroids.append((centerX, centerY))
                confidences.append(float(confidence))

                idxs = cv2.dnn.NMSBoxes(boxes, confidences, MIN_CONF, NMS_THRESH)

    if len(idxs) > 0:
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            crop_img = plate_image[y:y+h, x:x+w]
            return crop_img

##    return (len(idxs), plate_image)
    return plate_image

def detect_charecter(number_plate_extracted, char_net, char_ln):
    (H, W) = number_plate_extracted.shape[:2]

    blob = cv2.dnn.blobFromImage(number_plate_extracted, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    char_net.setInput(blob)
    layerOutputs = char_net.forward(char_ln)

    boxes = []
    confidences = []
    classIDs = []
    count = 0
    sample = dict()
    sample2 = dict()
    idxs = []

    for output in layerOutputs:
        for detection in output:
            count = count+1
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if confidence > MIN_CONF:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                a = int(width)
                b = int(height)
                sample[x] = [y, a, b]
				
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

                idxs = cv2.dnn.NMSBoxes(boxes, confidences, MIN_CONF, NMS_THRESH)

    if len(idxs) > 0:
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            sample2[x] = [y, w, h]

    print(len(sample2))
    n = dict()
    for i in sorted(sample2):
        n[i] = sample2[i]
    chars = showChar(n, number_plate_extracted)
    print(len(chars))

##    return (len(chars), chars)
    return len(chars), chars

def recognise_charecter (detect_charecter, char_classify):
    res = ""

    for image in detect_charecter:
        image = cv2.resize(image, (28, 28))
        image = image.astype("float") / 255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        labelss = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

        l = char_classify.predict(image)[0]
        d = dict(zip(labelss, l))
        Keymax = max(d, key=d.get)
        res = res + Keymax
    print (res)

    return res
