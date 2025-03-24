import re


def extraction_texte_qrcode(qr_texte):

    return {
        "nomfacture" : qr_texte[8:21],
        "datefacture" : qr_texte[27:46],
        "sexeclient" : qr_texte[52:53],
        "datedenaissanceclient" : qr_texte[61:71],
    }

def extraction_texte_facture(ocr_texte):
    nomclient = re.findall(r'Bill to \w+ \w+', ocr_texte)
    nomclient = nomclient[0][8:]
    mailclient = re.findall(r'Email [\w@.]+', ocr_texte)
    mailclient = remove_space(mailclient[0][6:])
    adresseclient = re.findall(r'Address .*\n\n.*', ocr_texte)
    adresseclient = adresseclient[0][8:].replace("\n\n", ", ")
    return {
        "nomclient" : nomclient,
        "mailclient" : mailclient,
        "adresseclient" : adresseclient,
    }

def extract_product_info(line):
    m = re.search(r"([\w\s]+)[,.][^\d]*(\d+)[^\d]*([\d,.]+)",line)
    if m:
        p_name=m.group(1).strip()
        p_quant=int(m.group(2))
        p_price=float(m.group(3).replace(",","."))
        return p_name, p_quant,p_price

def remove_space(text):
    return text.replace(' ', '')

def extract_table_total(line):
    m = re.search(r'\w+\s+([\d,.]+)\s+\w+$', line)
    if m:
        return float (remove_space(m.group(1).replace("," ,".")))

    
def extraction_texte_table(ocr_texte):

    lignes = re.split('\n+', ocr_texte)[:-1]
    table ={
        "item":{
            "product_name":[],
            "quantity":[],
            "price":[]
        }
    }
    for ligne in lignes[:-1]:
        p_name,p_quant,p_price=extract_product_info(ligne)
        table["item"]["product_name"].append(p_name)
        table["item"]["quantity"].append(p_quant)
        table["item"]["price"].append(p_price)
    
    table["totalfacture"]=extract_table_total(lignes[-1])
    return table

if __name__=="__main__":
   
    produits =  'Edge so crime share. 4x 12.18 Euro\nThank do article especially. 1 x 67.86 Euro\nInclude dinner main friend. 3 x 287.99 Euro\nCapital hear moming people. 3.x 55.43 Euro\nTOTAL 1146.84 Euro\n'
    resultat = extraction_texte_table(produits)
    print(resultat)