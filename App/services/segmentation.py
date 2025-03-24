from PIL import Image, ImageDraw
import numpy as np

def segmenter_image(image):
    '''Segmenter l'image '''
    x1, y1 = 0, 0  # Coin supérieur gauche (x1, y1)
    x2, y2 = 550, 180  # Coin inférieur droit (x2, y2)

    x1a, y1a = 0, 175
    x2a, y2a = 800, 800

    x1b, y1b = x2, 0
    x2b, y2b = 685, 180

    rectangles = [((x1, y1),(x2, y2)), ((x1a, y1a),(x2a, y2a)), ((x1b, y1b),(x2b, y2b))]
    segments = []
    for rectangle in rectangles:
        x1, y1 = rectangle[0]
        x2, y2 = rectangle[1]
        segments.append(image.crop((x1, y1, x2, y2)))
    return segments, rectangles


def dessiner_rectangles(image, rectangles):
    """Dessiner les rectangles sur une image"""
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
    image_copie = image.copy()
    draw = ImageDraw.Draw(image_copie)
    for rectangle in rectangles:
        draw.rectangle(rectangle, width=3, outline="black")
    return image_copie