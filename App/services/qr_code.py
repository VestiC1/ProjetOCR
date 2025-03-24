from qreader import QReader

# Créer une instance QReader
qreader = QReader()

def extraction_qrcode(image):
    '''Lire un QR code'''
    return qreader.detect_and_decode(image=image)[0]
