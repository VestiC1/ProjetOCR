from PIL import Image
import numpy as np

def charger_image(nom_du_fichier: str):
    '''Chargement d'une image'''
    return Image.open(nom_du_fichier)

def afficher_image(image):
    '''Affichage d'une image'''
    image.show()

def pil_to_cv2(image):
    return np.array(image)