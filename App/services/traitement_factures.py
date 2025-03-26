import cv2
import os
from outils import charger_image, afficher_image, pil_to_cv2
from qr_code import extraction_qrcode
from segmentation import segmenter_image, dessiner_rectangles
from ocr import extraction_texte
from parseur import extraction_texte_qrcode, extraction_texte_facture, extraction_texte_table
from pprint import pprint

from App.bdd.crud import db_connect, db_close, add_clients, add_factures, add_factures_produits

from glob import glob

error_files = []

def inserer_facture(conn, nom_du_fichier, verbose = True):
    image = charger_image(nom_du_fichier=nom_du_fichier)
    segments, rectangles = segmenter_image(image)

    zone1, zone2, zone3 = segments

    try:
        
        data_z1 = extraction_texte(zone1)
        data_z2 = extraction_texte(zone2)
        data_qr = extraction_qrcode(image=pil_to_cv2(zone3))


        texte_qr = extraction_texte_qrcode(data_qr)
        texte1 = extraction_texte_facture(data_z1)
        texte2 = extraction_texte_table(data_z2)

        if verbose :
            pprint(texte_qr)
            pprint(texte1)
            pprint(texte2)

        add_clients(
            conn = conn,
            nom=texte1["nomclient"], 
            mail=texte1["mailclient"],
            datedenaissance=texte_qr["datedenaissanceclient"],
            sexe=texte_qr["sexeclient"],
            adresse=texte1["adresseclient"]
        )

        add_factures(
            conn = conn,
            numerofacture=texte_qr["nomfacture"],
            creationdate=texte_qr["datefacture"],
            total=texte2["totalfacture"],
            mail=texte1["mailclient"]
        )

        num_produits = len(texte2['item']['product_name'])

        for i in range(num_produits):
            add_factures_produits(
                conn=conn,
                numero_facture=texte_qr["nomfacture"],
                produit=texte2['item']['product_name'][i],
                quantite=texte2['item']['quantity'][i],
                prix_unitaire=texte2['item']['price'][i]
            )

    except Exception as e:
        #print(" ", e)
        error_files.append(nom_du_fichier)
    

def sauvegarde_erreurs():
    with open('error.log', "w") as f :
        for fichier in error_files:
            f.write(fichier + "\n")

def main():

    conn = db_connect()
    # Preciser le chemin a lire
    dossier_facture = "factures/**"

    # [:1] permet de travailler sur la premiere facture uniquement
    listefichiers = sorted(glob(f"{dossier_facture}/*.png"))

    #print(listefichiers)
    num_fichiers = len(listefichiers)
    for i, nomdufichier in enumerate(listefichiers):
        print(f"\r{(i+1)*100/num_fichiers:.2f} % | {nomdufichier}\033[0K", end="", flush=True)
        inserer_facture(conn, nomdufichier, verbose=False)
    print()
    db_close(conn)

    sauvegarde_erreurs()
    
if __name__=="__main__":
    main()