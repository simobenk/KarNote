# Projet de Traitement de Documents PDF

Ce projet permet de traiter des documents PDF pour générer des résumés, des quiz et des problèmes de type X-ENS en utilisant différents modèles d'IA (Gemini, OpenAI, LlamaParse).

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Un compte pour chacun des services suivants :
  - Google Cloud (pour Gemini)
  - OpenAI
  - LlamaParse

## Configuration

1. Clonez le repository :`git clone <adresse_du_repository>`
2. Créez un fichier `.env` et copiez le contenu du fichier `.env.example` dans ce fichier: 
```
cp .env.example .env
```
3. Configurez vos clés API :
   - Ouvrez le fichier `.env`
   - Remplacez les valeurs par vos propres clés API :
     - LLAMA_API_KEY : Créez un compte sur [LlamaParse](https://www.llamaapi.com)
     - GOOGLE_API_KEY : Obtenez une clé sur [Google Cloud Console](https://console.cloud.google.com)
     - OPENAI_API_KEY : Créez une clé sur [OpenAI Platform](https://platform.openai.com/api-keys)

⚠️ **IMPORTANT - SÉCURITÉ** : 
- Ne partagez JAMAIS vos clés API
- N'ajoutez JAMAIS le fichier `.env` à git
- Ne commitez pas vos clés API dans le code
- Si vous avez accidentellement exposé vos clés, régénérez-les immédiatement

## Installation

1. Créez un environnement virtuel (recommandé) :
```bash
python -m venv venv
source venv/bin/activate  # Sur Linux/Mac
# ou
venv\Scripts\activate  # Sur Windows
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Fonctionnalités

Le projet propose plusieurs fonctions pour traiter les documents PDF :

- `process()` : Traite un PDF et son enregistrement audio pour générer un résumé
- `resumee()` : Génère un résumé des points essentiels d'un PDF
- `enrichir()` : Enrichit le contenu d'un PDF avec des informations supplémentaires
- `quizfinal()` : Génère un quiz basé sur le contenu du PDF
- `xensfinal2()` : Crée un problème de type X-ENS à partir du contenu

## Structure du projet

```
.
├── .env                # Fichier de configuration (à créer)
├── .env.example        # Exemple de configuration
├── propprof.py         # Code principal
├── test.py            # Utilitaires de test
├── extraire.py        # Fonctions d'extraction de texte
└── README.md          # Ce fichier
```

## Utilisation

Exemple d'utilisation du code :

```python
from propprof import process, resumee, quizfinal

# Générer un résumé
resumee("chemin/vers/votre/fichier.pdf")

# Générer un quiz
quizfinal("chemin/vers/votre/fichier.pdf", "blue")

# Traiter un PDF avec son audio
process("chemin/vers/fichier.pdf", "chemin/vers/audio.mp3")
```

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## Licence

[Spécifiez votre licence ici]

## Contact

[Vos informations de contact]
