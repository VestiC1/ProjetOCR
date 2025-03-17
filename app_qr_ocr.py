from qreader import QReader
import cv2
import os
import re
import pytesseract
import modele
from PIL import Image


# Créer une instance QReader
qreader = QReader()

def lecturedoc(nomdufichier):
    # Récupérer l'image qui contient le code QR 
    image = cv2.cvtColor(cv2.imread(nomdufichier), cv2.COLOR_BGR2RGB)

    # Utilisez la fonction detect_and_decode pour obtenir les données QR décodées 
    decoded_text = qreader.detect_and_decode(image=image)

    print(decoded_text)

    #decoded_split = decoded_text[0].split("\n")

    #print(decoded_split)

    nomfacture = decoded_text[0][8:21]
    datefacture = decoded_text[0][27:46]
    sexeclient = decoded_text[0][52:53]
    datedenaissanceclient = decoded_text[0][61:71]

    # Spécifie le chemin de l'exécutable Tesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Mets le bon chemin ici

    # Ouvre l'image
    img = Image.open(nomdufichier)

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

    nomclient = re.findall(r'Bill to \w+ \w+', text1)
    mailclient = re.findall(r'Emailclient [\w@.]+', text1)
    adresseclient = re.findall(r'Address .*\n\n.*', text1)
    totalfacture = re.findall(r'TOTAL [0-9.]*', text2)

    try:
        nomclient = nomclient[0][8:]
        mailclient = mailclient[0][6:]
        adresseclient = adresseclient[0][8:].replace("\n\n", " ")
        totalfacture = float(totalfacture[0][6:])

        print(nomfacture, datefacture, sexeclient, datedenaissanceclient, totalfacture, nomclient, mailclient, adresseclient)

        modele.add_clients(nomclient, mailclient, datedenaissanceclient, sexeclient, adresseclient)
        modele.add_factures(nomfacture, datefacture, totalfacture, mailclient)

    except:
        pass

listefichiers = os.listdir(r"C:\Users\steve\Documents\Formation IA\ProjetOCR\ProjetOCR\factures\2018")
#print(listfichiers)

for nomdufichier in listefichiers:
    lecturedoc(r"C:\Users\steve\Documents\Formation IA\ProjetOCR\ProjetOCR\factures\2018\\" + nomdufichier)