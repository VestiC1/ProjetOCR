from qreader import QReader
import cv2
import os
import re
import pytesseract
import modele
from PIL import Image


# Créer une instance QReader
qreader = QReader()

def readqrcode(filename):
    # Récupérer l'image qui contient le code QR 
    image = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB)

    # Utilisez la fonction detect_and_decode pour obtenir les données QR décodées 
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
    img = Image.open(filename)

    # Définir les coordonnées de la région 1 à extraire
    x1, y1 = 0, 0  # Coin supérieur gauche (x1, y1)
    x2, y2 = 500, 180  # Coin inférieur droit (x2, y2)

    # Découper la région 1 d'intérêt (ROI)
    zone1 = img.crop((x1, y1, x2, y2))

    # Définir les coordonnées de la région 2 à extraire
    x1, y1 = 0, 175  # Coin supérieur gauche (x1, y1)
    x2, y2 = 800, 800  # Coin inférieur droit (x2, y2)

    # Découper la région 2 d'intérêt (ROI)
    zone2 = img.crop((x1, y1, x2, y2))

    # Extraction du texte 1
    text1 = pytesseract.image_to_string(zone1, lang="eng", config="--psm 6 --oem 1")

    # Extraction du texte 2
    text2 = pytesseract.image_to_string(zone2, lang="eng", config="--psm 6 --oem 1")

    print(text1 ,text2)

    nom = re.findall(r'Bill to \w+ \w+', text1)
    mail = re.findall(r'Email [\w@.]+', text1)
    adresse = re.findall(r'Address .*\n\n.*', text1)
    total = re.findall(r'TOTAL [0-9.]*', text2)

    try:
        nom = nom[0][8:]
        mail = mail[0][6:]
        adresse = adresse[0][8:].replace("\n\n", " ")
        total = float(total[0][6:])

        print(INVOICE, nDATE, nCUST, birth, total, nom, mail, adresse)

        modele.add_clients(nom, mail, birth, nCUST, adresse)
        modele.add_factures(INVOICE, nDATE, total, mail)

    except:
        pass

listfichiers = os.listdir(r"C:\Users\steve\Documents\Formation IA\ProjetOCR\ProjetOCR\factures\2018")
#print(listfichiers)

for filename in listfichiers:
    readqrcode(r"C:\Users\steve\Documents\Formation IA\ProjetOCR\ProjetOCR\factures\2018\\" + filename)