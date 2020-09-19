import cv2
import numpy as np
from process import *
import threading as th
import time

#-----------------------------------------------------------------------------------------------

#read haarcascade
#detector = "detector_level26.xml"
plates_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_russian_plate_number.xml")
#plates_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "detector_level26.xml")
#plates_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + detector)

font = cv2.FONT_HERSHEY_TRIPLEX

video = cv2.VideoCapture('./vid/teste.mp4')

funcLer = Ler()

global minhaPalavra
acerto = 1
total = 1
porcentagem = 0

# verificando frame por frame do video
while True:

    
    success, img = video.read()

    imS = cv2.resize(img, (960, 540))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plates = plates_cascade.detectMultiScale(gray, minSize=(50, 50))

    for x, y, w, h in plates:
        plates_rec = cv2.rectangle(img, (x,y), (x+w, y+h), (100, 255, 0), 1)
        roi = plates_rec[y:y + h, x:x + w]
        cv2.imwrite('jacira.jpg', roi)
        #print(plates_rec)
        try:
            #print(type(th.activeCount()))
            #print(th.activeCount())
            if th.activeCount() < 20:
                t = th.Thread(target=funcLer.ler)
                t.start()
                minhaPalavra = funcLer.plavara
                total += 1
                #print ("TOTAL É", total)
                

                if minhaPalavra == "DAD-0051":
                    acerto += 1
                    print("ACERTOU ", acerto, " DE ", total - 3)
                    porcentagem = (100*acerto)/(total - 3)
                    print("Taxa de acerto: ", porcentagem, "%")

                elif minhaPalavra == "FTM-5501":
                    acerto += 1
                    print("ACERTOU ", acerto, " DE ", total)
                    porcentagem = (100*acerto)/total
                    print("Taxa de acerto: ", porcentagem, "%")

                elif minhaPalavra == "EET-1045":
                    acerto += 1
                    print("ACERTOU ", acerto, " DE ", total)
                    porcentagem = (100*acerto)/total
                    print("Taxa de acerto: ", porcentagem, "%")

                elif minhaPalavra == "EEG-2913":
                    acerto += 1
                    print("ACERTOU ", acerto, " DE ", total - 5)
                    porcentagem = (100*acerto)/(total -5)
                    print("Taxa de acerto: ", porcentagem, "%")

                elif minhaPalavra == "EUC-3526":
                    acerto += 1
                    print("ACERTOU ", acerto, " DE ", total)
                    porcentagem = (100*acerto)/total
                    print("Taxa de acerto: ", porcentagem, "%")
                               

                #print("Placa detectada: ", minhaPalavra)
                
                                       
        except:
            print("Thiago bonito")   
        #process.ler()
    
    if total > 5:
        cv2.putText(imS, minhaPalavra, (750, 500), font, 1, (60, 0, 255))
        cv2.line(imS, (750, 505), (950, 505), (255, 255, 255), 2)
        cv2.putText(imS, "Ultima placa vista", (750, 530), font, 0.6, (60, 0, 255))    
    
    cv2.imshow(' NOME DO MEU VIDEO', imS) # exibindo o video
    #cv2.imshow(' test', img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'): # se 'q' for precionado o video sera fechado
        break

print(acerto)   
print("BAITOLA")
cv2.waitKey(0)
cv2.destroyAllWindows()