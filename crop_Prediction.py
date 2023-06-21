import datetime
import time
import serial
device = serial.Serial ("COM17", 9600)
if device.isOpen () == False:
    device.open ()

import numpy as np
from sklearn import svm

train_Data_devA = [[28.69,10,85],[31.00,1,0],[29.00,1,1],[30.00,1,1],[30.00,0,1],[29.00,0,1]]
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

while infiniteloop == True:
    recVal = device.readline ().decode ('ascii')
    recVal = recVal [: len (recVal) - 2]
    recValSplit = recVal.split (',')
    print (recValSplit)
    predict = linear_svm_devA.predict ([[float (recValSplit [0]), float (recValSplit [1]), float (recValSplit [2])]])
    if predict[0] == 0:
        print ("Rice")
    elif predict[0] == 1:
        print ("rice")
    elif predict[0] == 2:
        print ("Corn")
    break
    
device.close ()
