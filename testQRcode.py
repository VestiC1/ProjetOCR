from qreader import QReader
import cv2
import os
import model
import re
import pytesseract
from PIL import Image


# Create a QReader instance
qreader = QReader()

def readqrcode(fn):
    # Get the image that contains the QR code
    image = cv2.cvtColor(cv2.imread(fn), cv2.COLOR_BGR2RGB)

    # Use the detect_and_decode function to get the decoded QR data
    decoded_text = qreader.detect_and_decode(image=image)

    #print(decoded_text)

    #decoded_split = decoded_text[0].split("\n")

    #print(decoded_split)

    INVOICE = decoded_text[0][8:21]
    nDATE = decoded_text[0][27:46]
    nCUST = decoded_text[0][52:53]
    birth = decoded_text[0][61:71]

    # Spécifie le chemin de l'exécutable Tesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Mets le bon chemin ici

    # Ouvre l'image
    img = Image.open(fn)

    # Définir les coordonnées de la région à extraire
    x1, y1 = 0, 0  # Coin supérieur gauche (x1, y1)
    x2, y2 = 500, 180  # Coin inférieur droit (x2, y2)

    # Découper la région d'intérêt (ROI)
    zone1 = img.crop((x1, y1, x2, y2))

    # Définir les coordonnées de la région à extraire
    x1, y1 = 0, 175  # Coin supérieur gauche (x1, y1)
    x2, y2 = 800, 800  # Coin inférieur droit (x2, y2)

    # Découper la région d'intérêt (ROI)
    zone2 = img.crop((x1, y1, x2, y2))

    # Extraction du texte
    text1 = pytesseract.image_to_string(zone1, lang="eng", config="--psm 6 --oem 1")

    # Extraction du texte
    text2 = pytesseract.image_to_string(zone2, lang="eng", config="--psm 6 --oem 1")

    print(text1, text2)

    total = re.findall(r'TOTAL [0-9.]*', text2)
    nom = re.findall(r'Bill to \w+ \w+', text1)
    mail = re.findall(r'Email [\w@.]+', text1)
    adresse = re.findall(r'Address .*\n\n.*', text1)

    try:
        total = float(total[0][6:])
        nom = nom[0][8:]
        mail = mail[0][6:]
        adresse = adresse[0][8:].replace("\n\n", " ")

        print(INVOICE, nDATE, nCUST, birth, total, nom, mail, adresse)

        model.add_clients(nom, mail, birth, nCUST, adresse)
        model.add_invoice(INVOICE, nDATE, total, mail)

    except:
        pass

listfichiers = os.listdir(r"C:\Users\steve\Documents\Formation IA\ProjetOCR\ProjetOCR\factures\2018")
#print(listfichiers)

for fn in listfichiers:
    readqrcode(r"C:\Users\steve\Documents\Formation IA\ProjetOCR\ProjetOCR\factures\2018\\" + fn)