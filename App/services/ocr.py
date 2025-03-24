import pytesseract

# Spécifie le chemin de l'exécutable Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extraction_texte(image):
    '''Extraction du texte image'''
    return pytesseract.image_to_string(image, lang="eng", config="--psm 6 --oem 1")