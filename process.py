import pytesseract
import cv2
import imutils
import re

class Ler:
    
    def __init__(self, palavra = ""):

        self.palavra = palavra

    def ler(self):

        try:

            license_plate = re.compile(r"[A-Z]{3}[-][0-9]{4}")

            image = cv2.imread("jacira.jpg")
            #print(image)

            image = imutils.resize(image, width=500)

            cinzento = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            placadoCarro = cv2.bilateralFilter(cinzento, 9, 75, 75)

            #binar = cv2.threshold(placadoCarro, 1, 255, cv2.THRESH_BINARY)
            binar = cv2.adaptiveThreshold(placadoCarro, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY, 29, 5)
            #mecher no primeiro numero, quanto maior mais preto

            blur = cv2.GaussianBlur(binar, (1, 1), 0)

            placaBunito = cv2.bilateralFilter(blur, 15, 60, 50)

            cv2.imwrite("letsee.jpg", placaBunito)

            text = pytesseract.image_to_string(placaBunito, lang='eng', config='--psm 11 --oem 3')
            tratado = re.split(', |\n| ', text)
            #banana = text.split(" ")
            #print(tratado)

            for palavra in tratado:

                if license_plate.search(palavra):
                    self.palavra = palavra
                    self.palavra = re.sub(r'[^\w-]', '', self.palavra)
                    #FAZER O BONITO AQUI
                    print("Placa detectada: |", self.palavra, "|")
                    #return self.palavra
                    
                #print(text)
                #print("------------------------------------------------------------------------")
        except:
            #print("pum")
            pass
            #print (text)
        

    
    
