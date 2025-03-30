# ProjetOCR

Développer une interface OCR

## Installation

### creation environnement

```python
python -m venv ENV
```

### activation venv

```bash
ENV\Scripts\activate.bat 
```

### Installation librairies

```python
pip install -r requirements.txt
```

## Services

### Telechargement de toutes les factures

```python
python dlfact.py
```

## Les schémas

### Schéma de la base de données

Voici le schéma de la base de données illustré avec Mermaid :

```mermaid
%%{init: {'theme':'default'}}%%
erDiagram
    clients {
        varchar(50) mail PK
        varchar(50) nom
        date date_de_naissance
        varchar(1) sexe
        varchar(200) adresse
    }

    factures {
        varchar(14) numero_facture PK
        timestamp creation_date
        float8 total
        varchar(50) mail FK
    }

    factures_produits {
        serial id PK
        varchar(14) numero_facture FK
        varchar(60) produit
        int4 quantite
        float8 prix_unitaire
    }

    clients ||--o{ factures : possede
    factures ||--o{ factures_produits : contient

```

### Schéma conceptuel

Voici le schéma conceptuel illustré avec Mermaid :

```mermaid
%%{init: {'theme':'default'}}%%
flowchart TD 

MAIN[**Point d'Entrée** <br> *main.py*]
FUNC1[**Preprocessing** <br> *outils.py*]
FUNC2[**Segmentation de l'image** <br> *segmentation.py*]
FUNC3[**Image to Texte** <br> *ocr.py*]
FUNC4[**Image to Texte** <br> *qr_code.py*]
FUNC5[**Selection des informations à garder** <br> *parseur.py*]
FUNC6[**Injection BDD** <br> *modele.py*]

	MAIN -->FUNC1
	FUNC1-->FUNC2
	FUNC2-->FUNC3
	FUNC2-->FUNC4
	FUNC3-->FUNC5
	FUNC4-->FUNC5
	FUNC5-->FUNC6

```

### Schéma fonctionnel

Voici le schéma fonctionnel illustré avec Mermaid :

```mermaid
%%{init: {'theme':'default'}}%%
flowchart TD 

MAIN[**Chemin d'acces aux images** <br> *string*]
FUNC1[**image** <br> *numpy.array*]
FUNC2[**Image segmentée en 3 blocs** <br> *_numpy.array_*]
FUNC3[**Segment facture** <br> *string*]
FUNC4[**Segment table** <br> *string*]
FUNC5[**Segment QRCode** <br> *string*]
FUNC6[**Texte facture** <br> *string*]
FUNC7[**Texte table** <br> *string*]
FUNC8[**Texte QRCode** <br> *string*]
FUNC9[**Agregation** <br> *string*]
FUNC10[**Table** <br> *clients*]
FUNC11[**Table** <br> *factures*]
FUNC12[**Table** <br> *factures_produits*]

	MAIN --charger_image-->FUNC1
	FUNC1--segmenter_image-->FUNC2
	FUNC2--extraction_texte-->FUNC3
	FUNC2--extraction_texte-->FUNC4
	FUNC2--extraction_qrcode-->FUNC5
	FUNC3--extraction_texte_facture-->FUNC6
	FUNC4--extraction_texte_table-->FUNC7
	FUNC5--extraction_texte_qrcode-->FUNC8
	FUNC6--->FUNC9
	FUNC7--->FUNC9
	FUNC8--->FUNC9
	FUNC9--add_clients-->FUNC10
	FUNC9--add_factures-->FUNC11
	FUNC9--add_factures_produits-->FUNC12

```

## Application web

### lancement de l'application ( dossier App )

```python
uvicorn main:app --reload
```

