import cv2
import numpy as np
from process import *
import threading as th
from DB_Manager import *
import time
import paho.mqtt.client as mqtt
from mqtt import *

# ----------------------------------------------------------------------------------------------- #

# read haarcascade
# detector = "detector_level26.xml"
plates_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_russian_plate_number.xml")
# plates_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "detector_level26.xml")
# plates_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + detector)


font = cv2.FONT_HERSHEY_TRIPLEX

my_mqtt = plate_mqtt()
funcLer = Ler()
db = SQLITEDB()

global minhaPalavra
acerto = 1
total = 1
porcentagem = 0

client = mqtt.Client(client_id="plate_unverified")

client.on_connect = plate_mqtt.connect_msg(plate_mqtt)
client.on_publish = plate_mqtt.publish_msg(plate_mqtt)
client.connect("mqtt.eclipse.org", 1883)

video = cv2.VideoCapture('./vid/teste.mp4')


def change_res(width, height):
    video.set(3, width)
    video.set(4, height)


change_res(1920, 1080)


# verificando frame por frame do video
while True:

    minhaPalavra = funcLer.palavra
    success, img = video.read()

    imS = cv2.resize(img, (960, 540))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plates = plates_cascade.detectMultiScale(gray, minSize=(50,50))
    #fakeP = plates_cascade.detectMultiScale(imS, minSize=(50, 50))

    #for x, y, w, h in fakeP:
    #    fake_rec = cv2.rectangle(imS, (x,y), (x+w, y+h), (100, 255, 0), 1)

    for x, y, w, h in plates:
        plates_rec = cv2.rectangle(img, (x, y), (x+w, y+h), (100, 255, 0), 1)
        roi = plates_rec[y:y + h, x:x + w]
        cv2.imwrite('jacira.jpg', roi)
        # print(plates_rec)

        if minhaPalavra != "":
            db.put_info(minhaPalavra)
            # db.get_data(minhaPalavra)
            cv2.putText(img, minhaPalavra, (x + w + 20, y + 45), font, 1, (100, 255, 0))

        try:
            # print(type(th.activeCount()))
            # print(th.activeCount())
            if th.activeCount() < 20:
                t = th.Thread(target=funcLer.ler)
                t.start()
                client.publish("plate_read", minhaPalavra)

        except:
            print("Thiago bonito")


    #cv2.line(img, (750, 505), (950, 505), (255, 255, 255), 2)
    #cv2.putText(img, "Ultima placa vista", (750, 530), font, 0.6, (60, 0, 255))
    
    #cv2.imshow('Video Adaptado', imS)  # exibindo o video
    cv2.imshow('Video Original', img)
    
    client.loop

    if cv2.waitKey(1) & 0xFF == ord('q'):  # se 'q' for precionado o video sera fechado
        break

print(acerto)   
print("BAITOLA")
cv2.waitKey(0)
cv2.destroyAllWindows()
# "FTM-5501"
# "EET-1045"
# "EEG-2913"
# "EUC-3526"
