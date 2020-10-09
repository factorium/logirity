import cv2
import pytesseract
from time import sleep
import process
import re

#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#lista =[ x for x in range(80, 180)]
cont = 70

#captura de video
video = cv2.VideoCapture(0)
print("Mostrando vídeo: ")
print("Aperte ESC para sair")

#fonte
font = cv2.FONT_HERSHEY_COMPLEX

while True:

    _, frame = video.read()

    #mudar pra cinza
    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #detectar as bordas OU BICOLOR
    #canny = cv2.Canny(cinza, 170, 200)
    #_, canny = cv2.threshold(cinza, 165, 255, cv2.THRESH_BINARY)
    canny = cv2.adaptiveThreshold(cinza, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 5)

    #achar os contornos
    contornos, hier = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.imshow("Janela Tratada", canny)

    #desenhar os contornos
    for c in contornos:
        perimetro = cv2.arcLength(c, True)
        area = cv2.contourArea(c)
        approx =cv2.approxPolyDP(c, 0.03 * perimetro, True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]

        #PARTE IMPORTANTE, DEFINE O TAMANHO DAS COISAS QUE PODEM SER DETECTADAS
        if 6000 < area < 8000:
            placa = cv2.drawContours(cinza, [approx], 0, (255, 255, 0), 5)

            if len(approx) == 4:
                print(area)
                x,y,w,h = cv2.boundingRect(approx)
                #colocar visuais
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5)
                cv2.putText(frame, "PLACA DETECTADA!", (x, y), font, 0.7, (0, 0, 255))
                roi = placa[y:y + h, x:x + w]
                

                #salvar imagem
                cv2.imwrite('leticia.jpg', roi)
                print("Imagem registrada!")

                #process.ler()
                #cont += 1

    
    #cv2.destroyAllWindows()
    cv2.imshow("Janela Verdade", frame)
    cv2.imshow("janela teste", canny)
    cv2.imshow("janela 3", cinza)
    #sleep(0.2)  
    
    #codigo para encerrar a gravação
    key = cv2.waitKey(1)
    if key == 27:
        print("FECHANDO APLICAÇÃO...")
        break

    if cont == 110:
        cont = 105

video.release()
cv2.destroyAllWindows()