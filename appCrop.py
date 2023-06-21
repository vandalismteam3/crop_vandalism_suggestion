import streamlit as st

import datetime
import time
import serial
import numpy as np
from sklearn import svm

st.title("Crop Prediction")

train_Data_devA = [[30.00,1,0],[31.00,1,0],[29.00,1,1],[30.00,1,1],[30.00,0,1],[29.00,0,1]]
train_label_devA = [0, 0, 1, 1, 2, 2]

infiniteloop = True
predictCount = 0

if len (train_Data_devA) == len (train_label_devA):
    linear_svm_devA = svm.SVC(kernel = 'linear', C = 1)
    linear_svm_devA.fit (train_Data_devA, train_label_devA)
else:
    infiniteloop = False
    print ("Data Mismatch for Device A")

print ("Data Trained")
print ("")


if st.button('Start'):
    device = serial.Serial ("COM15", 9600)
    if device.isOpen () == False:
        device.open ()

    recVal = device.readline ().decode ('ascii')
    recVal = recVal [: len (recVal) - 2]
    recValSplit = recVal.split (',')
    print (recValSplit)
    predict = linear_svm_devA.predict ([[float (recValSplit [0]), float (recValSplit [1]), float (recValSplit [2])]])
    predictedCrop = ""
    if predict[0] == 0:
        predictedCrop = "Rice"
    elif predict[0] == 1:
        predictedCrop = "Wheat"
    elif predict[0] == 2:
        predictedCrop = "Corn"

    print (predictedCrop)
    st.write (recValSplit)
    st.write (predictedCrop)

    device.close ()

st.success("Crop Protection")
