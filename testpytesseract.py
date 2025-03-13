from PIL import Image
import pytesseract
import re

# Spécifie le chemin de l'exécutable Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Mets le bon chemin ici

# Ouvre l'image
img = Image.open('factures/2018/FAC_2018_0031-558.png')

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

# affichage du total
total = re.findall(r'TOTAL [0-9.]*', text2)
print(total)
print("total",float(total[0][6:]))

# affichage du nom
nom = re.findall(r'Bill to \w+ \w+', text1)
print(nom)
print(nom[0][8:])

# affichage du mail
mail = re.findall(r'Email [\w@.]+', text1)
print(mail)
print(mail[0][6:])

# affichage de l'adresse
adresse = re.findall(r'Address .*\n\n.*', text1)
print(adresse)
print(adresse[0][8:].replace("\n\n", " "))