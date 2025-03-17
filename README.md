# ProjetOCR
Développer une interface OCR

## Installation

### creation environnement
```python
python -m venv ENV
```

### activation desactivation venv
```bash
venv\Scripts\activate.bat 
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

TEST :

erDiagram
    CLIENTS {
        string mail PK
        string nom
        date datedenaissance
        string sexe
        string adresse
    }
    
    FACTURES {
        string numerofact PK
        timestamp creationdate
        float total
        string mail FK
    }

    PRODUITS {
        int id PK
        string produit
        int quantité
        float "prix unitaire"
        string numerofact FK
    }

    CLIENTS ||--o{ FACTURES : "possède"
    FACTURES ||--o{ PRODUITS : "contient"
