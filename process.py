import fitz

def extract_text_by_font_size(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = []
    current_paragraph = ""
    previous_size = -1
    previous_font = None

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        page_text = ""  # On prépare une variable pour stocker tout le texte de la page
        page_font_size = None  # On prépare une variable pour la taille de police de la page

        # On parcourt tous les blocs de la page
        for block in blocks:
            if 'lines' in block:  # Chaque ligne est un bloc distinct
                for line in block['lines']:
                    for span in line['spans']:  # Chaque 'span' contient du texte formaté uniformément
                        text = span['text'].strip()
                        size = span['size']
                        font = span['font']  # On prend aussi en compte le nom de la police
                        # On détermine la taille de police dominante de la page
                        if page_font_size is None or size > page_font_size:
                            page_font_size = size

                        # On accumule tout le texte dans page_text
                        page_text += " " + text if page_text else text

                        # On garde la trace de la dernière taille de police et de la dernière police utilisée
                        previous_size = size
                        previous_font = font

        # Après avoir accumulé tout le texte de la page, on décide s'il s'agit d'un nouveau paragraphe
        if page_text:
            # S'il y a une différence significative dans la taille de police, on commence un nouveau paragraphe
            if previous_size != -1 and (previous_size < page_font_size * 0.8 or previous_font != font):
                full_text.append(current_paragraph)
                current_paragraph = page_text
            else:
                current_paragraph += " " + page_text if current_paragraph else page_text
            # Réinitialiser les variables pour la nouvelle page
            page_text = ""
            page_font_size = None

    # On ajoute le dernier paragraphe après la dernière page
    if current_paragraph:
        full_text.append(current_paragraph)

    doc.close()
    return full_text

# Chemin vers votre fichier PDF
pdf_path = "/content/drive/MyDrive/droitt.pdf"
paragraphs = extract_text_by_font_size(pdf_path)
# Affichage des paragraphes
for i, para in enumerate(paragraphs):
    print(f"Paragraphe {i+1}:\n{para}\n")

import fitz

def extract_text_by_font_size(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = []
    current_paragraph = ""
    previous_size = -1
    previous_font = None

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        page_text = ""  # On prépare une variable pour stocker tout le texte de la page
        page_font_size = None  # On prépare une variable pour la taille de police de la page

        # On parcourt tous les blocs de la page
        for block in blocks:
            if 'lines' in block:  # Chaque ligne est un bloc distinct
                for line in block['lines']:
                    for span in line['spans']:  # Chaque 'span' contient du texte formaté uniformément
                        text = span['text'].strip()
                        size = span['size']
                        font = span['font']  # On prend aussi en compte le nom de la police
                        # On détermine la taille de police dominante de la page
                        if page_font_size is None or size > page_font_size:
                            page_font_size = size

                        # On accumule tout le texte dans page_text
                        page_text += " " + text if page_text else text

                        # On garde la trace de la dernière taille de police et de la dernière police utilisée
                        previous_size = size
                        previous_font = font

        # Après avoir accumulé tout le texte de la page, on décide s'il s'agit d'un nouveau paragraphe
        if page_text:
            # S'il y a une différence significative dans la taille de police, on commence un nouveau paragraphe
            if previous_size != -1 and (previous_size < page_font_size * 0.8 or previous_font != font):
                full_text.append(current_paragraph)
                current_paragraph = page_text
            else:
                current_paragraph += " " + page_text if current_paragraph else page_text
            # Réinitialiser les variables pour la nouvelle page
            page_text = ""
            page_font_size = None

    # On ajoute le dernier paragraphe après la dernière page
    if current_paragraph:
        full_text.append(current_paragraph)

    doc.close()
    return full_text

# Chemin vers votre fichier PDF
pdf_path = "/content/drive/MyDrive/AnalyseCh1.pdf"
paragraphs = extract_text_by_font_size(pdf_path)

# Affichage des paragraphes
for i, para in enumerate(paragraphs):
    print(f"Paragraphe {i+1}:\n{para}\n")

import fitz

def extract_text_by_font_size_line_by_line(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = []
    current_paragraph = ""
    previous_size = -1
    previous_font = None

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if 'lines' in block:  # Vérifiez la présence de lignes de texte dans le bloc
                for line in block['lines']:
                    for span in line['spans']:
                        text = span['text'].strip()
                        size = span['size']
                        font = span['font']
                        # Commencez un nouveau paragraphe si la taille de la police change
                        if previous_size != -1 and (size != previous_size or font != previous_font):
                            # Sauvegardez le paragraphe actuel s'il contient du texte
                            if current_paragraph:
                                full_text.append(current_paragraph)
                                current_paragraph = ""
                        current_paragraph += text + " "
                        # Mise à jour de la dernière taille de police et de la police utilisée
                        previous_size = size
                        previous_font = font
                    # Ajouter un saut de ligne entre les lignes pour mieux refléter la structure du document
                    current_paragraph += "\n"
                # Ajouter le dernier paragraphe s'il n'est pas vide
                if current_paragraph.strip():
                    full_text.append(current_paragraph)
                    current_paragraph = ""

    doc.close()
    return full_text

# Chemin vers votre fichier PDF
pdf_path = "/content/drive/MyDrive/droitt.pdf"
paragraphs = extract_text_by_font_size_line_by_line(pdf_path)

# Affichage des paragraphes
for i, para in enumerate(paragraphs):
    print(f"Paragraphe {i+1}:\n{para}\n")

import fitz

def extract_text_by_font_size_line_by_line(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = []
    current_paragraph = ""
    current_font_specs = (None, None)  # (taille, police)

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if 'lines' in block:  # Vérifiez la présence de lignes de texte dans le bloc
                for line in block['lines']:
                    line_text = ""
                    for span in line['spans']:
                        text = span['text'].strip()
                        size = span['size']
                        font = span['font']
                        font_specs = (size, font)
                        if current_font_specs[0] is None:
                            current_font_specs = font_specs
                        # Détecter un changement significatif de mise en forme pour commencer un nouveau paragraphe
                        if font_specs != current_font_specs:
                            # Commencer un nouveau paragraphe si ce n'est pas la première ligne et la mise en forme change
                            if current_paragraph:
                                full_text.append(current_paragraph)
                                current_paragraph = ""
                            current_font_specs = font_specs
                        line_text += text + " "
                    current_paragraph += line_text + "\n"

        # Ajouter le dernier paragraphe de la page si ce n'est pas vide
        if current_paragraph.strip():
            full_text.append(current_paragraph)
            current_paragraph = ""
            current_font_specs = (None, None)  # Réinitialiser pour la nouvelle page

    doc.close()
    return full_text

# Chemin vers votre fichier PDF
pdf_path = "/content/drive/MyDrive/droitt.pdf"
paragraphs = extract_text_by_font_size_line_by_line(pdf_path)

# Affichage des paragraphes
for i, para in enumerate(paragraphs):
    print(f"Paragraphe {i+1}:\n{para}\n")

import re

def supprimer_emails_specifiques(texte):
    # Expression régulière pour trouver les adresses e-mail avec le domaine "centrale-Casablanca.ma"
    regex_specific = r'\b[A-Za-z0-9._%+-]+@centralesupelec\.fr\b'

    # Supprimer les adresses e-mail spécifiques du texte
    texte_sans_emails_specifiques = re.sub(regex_specific, '', texte)

    return texte_sans_emails_specifiques

import fitz

def extract_text_by_font_size_with_tolerance(pdf_path, tolerance=0.05):
    # Ouvrir le document PDF
    doc = fitz.open(pdf_path)
    full_text = []  # Stocker tous les paragraphes
    current_paragraph = ""  # Le paragraphe en cours de construction
    previous_size = None  # La taille de police de la ligne précédente

    for page in doc:  # Parcourir chaque page
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if 'lines' in block:  # Si le bloc contient des lignes
                for line in block['lines']:
                    for span in line['spans']:
                        text = span['text'].strip()
                        size = span['size']

                        # Si c'est le début d'un nouveau paragraphe
                        if previous_size is None:
                            previous_size = size
                            current_paragraph = text
                        else:
                            # Calculer la différence relative de taille de police
                            size_difference = abs(size - previous_size) / previous_size

                            # Si la différence est plus grande que la tolérance, commencer un nouveau paragraphe
                            if size_difference > tolerance:
                                # Ajouter le paragraphe en cours au texte complet et commencer un nouveau
                                full_text.append(current_paragraph)
                                current_paragraph = text
                            else:
                                # Sinon, ajouter la ligne au paragraphe en cours
                                current_paragraph += " " + text

                        # Mise à jour de la taille de police pour la comparaison avec la prochaine ligne
                        previous_size = size

                    # Ajouter un saut de ligne à la fin de chaque span
                    current_paragraph += "\n"

        # À la fin de chaque page, ajouter le paragraphe en cours et réinitialiser pour la prochaine page
        if current_paragraph.strip():
            full_text.append(current_paragraph)
            current_paragraph = ""
            previous_size = None

    doc.close()
    return full_text

# Chemin vers votre fichier PDF
pdf_path = "/content/drive/MyDrive/droitt.pdf"
paragraphs = extract_text_by_font_size_with_tolerance(pdf_path)

# Afficher les paragraphes extraits
for i, para in enumerate(paragraphs):
    print(f"Paragraphe {i+1}:\n{para}\n")

print(len(paragraphs))

paragraphs = extract_text_by_font_size_with_tolerance("/content/drive/MyDrive/testdoc.pdf",0.1)

for i, para in enumerate(paragraphs):
    print(f"Paragraphe {i+1}:\n{para}\n")

paragraphs = extract_text_by_font_size_with_tolerance("/content/drive/MyDrive/Cours LLORED. 2023-2024. 1A. Philosophie des sciences. FECC Séance 1.pdf",0.1)

for i, para in enumerate(paragraphs):
    print(f"Paragraphe {i+1}:\n{para}\n")

paragraphs1 = extract_text_by_font_size_with_tolerance("/content/drive/MyDrive/AnalyseCh1.pdf",0.1)

for i, para in enumerate(paragraphs1):
    print(f"Paragraphe {i+1}:\n{para}\n")

def filter_paragraphs(paragraphs):
    filtered_paragraphs = []
    for paragraph in paragraphs:
        # Supprime les espaces blancs et sépare les mots
        words = paragraph.strip().split()
        # Vérifie si le paragraphe contient plus d'un mot
        if len(words) > 1:
            filtered_paragraphs.append(paragraph)
        # Si le paragraphe contient un seul mot, vérifie si c'est plus qu'une simple lettre ou un chiffre
        elif len(words) == 1 and len(words[0]) > 1 and not words[0].isdigit():
            filtered_paragraphs.append(paragraph)
    return filtered_paragraphs

# Supposons que 'paragraphs' contient tous les paragraphes extraits de votre PDF
filtered_paragraphs = filter_paragraphs(paragraphs)

# Afficher les paragraphes filtrés
for i, para in enumerate(filtered_paragraphs):
    print(f"Paragraphe {i+1}:\n{para}\n")

len (filtered_paragraphs)

from transformers import BertModel, BertTokenizer



def text_to_embedding(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()

import re
def clean_text(text):
    # Supprimer les sauts de ligne et les tabulations
    text = re.sub(r'[\t\n]', ' ', text)
    # Remplacer les espaces multiples par un seul espace
    text = re.sub(r'\s+', ' ', text)
    # Supprimer la ponctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Convertir le texte en minuscules
    text = text.lower()
    return text

cleaned_paragraphs = [clean_text(paragraph) for paragraph in filtered_paragraphs]

# Afficher les paragraphes nettoyés
for i, para in enumerate(cleaned_paragraphs):
    print(f"Paragraphe {i+1}:\n{para}\n")

import re

def clean_text(text):
    # Remplacer les sauts de ligne et les tabulations par des espaces
    text = re.sub(r'[\t\n]', ' ', text)
    # Remplacer la ponctuation par des espaces
    text = re.sub(r'[^\w\s]', ' ', text)
    # Remplacer les espaces multiples par un seul espace
    text = re.sub(r'\s+', ' ', text)
    # Convertir le texte en minuscules
    text = text.lower().strip()
    return text

# Supposons que 'filtered_paragraphs' est votre liste de paragraphes à nettoyer
cleaned_paragraphs = [clean_text(paragraph) for paragraph in filtered_paragraphs]

# Afficher les paragraphes nettoyés
for i, para in enumerate(cleaned_paragraphs):
    print(f"Paragraphe {i+1}:\n{para}\n")



import nltk
from nltk.corpus import stopwords
from transformers import BertTokenizer, BertModel
import torch

# Télécharger la liste des stopwords français
nltk.download('stopwords')
french_stopwords = set(stopwords.words('french'))

french_stopwords

def remove_stopwords(text):
    words = text.split()
    filtered_words = [word for word in words if word not in french_stopwords]
    return ' '.join(filtered_words)
cleaned_paragraphs_without_stopwords = [remove_stopwords(para) for para in cleaned_paragraphs]

for i, para in enumerate(cleaned_paragraphs_without_stopwords):
    print(f"Paragraphe {i+1}:\n{para}\n")

print(len(cleaned_paragraphs_without_stopwords))
print(len(cleaned_paragraphs))

import spacy

# Charger le modèle français
nlp = spacy.load('fr_core_news_sm')

def lemmatize_text(text):
    doc = nlp(text)
    lemmatized_text = ' '.join([token.lemma_ for token in doc])
    return lemmatized_text

# Appliquer la lemmatisation
lemmatized_paragraphs = [lemmatize_text(para) for para in cleaned_paragraphs_without_stopwords]

for i, para in enumerate(lemmatized_paragraphs):
    print(f"Paragraphe {i+1}:\n{para}\n")

tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
model = BertModel.from_pretrained('bert-base-multilingual-cased')

def text_to_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()  # Obtenir l'embedding moyen du dernier état caché

# Calculer les embeddings pour chaque paragraphe nettoyé
embeddings = [text_to_embedding(para) for para in cleaned_paragraphs_without_stopwords]

embeddings

print(type(embeddings))

def traitement_text(t):
  return text_to_embedding(lemmatize_text(remove_stopwords(clean_text(t))))

text_test="on peut comparer nos idées et nos concepts aux lentilles à travers lesquelles nous voyons le monde. En philosophie, le thème d’étude, c’est la lentille elle-même. La réussite ne dépendra pas tant du bagage de connaissances finalement accumulé, que de ce dont on est capable en cas d’avis de tempête : quand les mers de la discussion montent et que la confusion fait irruption. Réussir signifiera prendre au sérieux les implications des idées."

test1=traitement_text(text_test)

type(test1)

len(test1[0])

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
def calculate_cosine_similarity(vector, embeddings):
    # Convertir la liste d'embeddings en une matrice numpy 2D
    # Chaque embedding doit être une ligne dans la matrice
    embeddings_matrix = np.vstack(embeddings)  # Utilisation de vstack pour empiler les embeddings verticalement

    # Assurer que le vecteur est au bon format (1D numpy array)
    vector = np.array(vector).flatten()  # S'assurer qu'il est plat

    # Calculer la similarité cosinus
    similarity_scores = cosine_similarity([vector], embeddings_matrix)
    return similarity_scores[0]  # Retourner les scores de similarité

calculate_cosine_similarity(test1, embeddings)

def find_top_indices(similarity_scores, top_n=5):
    # Trier les indices des scores par ordre décroissant basé sur la similarité cosinus
    top_indices = np.argsort(similarity_scores)[::-1][:top_n]
    top_scores = similarity_scores[top_indices]
    return top_indices, top_scores

ff=find_top_indices(calculate_cosine_similarity(test1, embeddings), top_n=5)

ff

ff[0][0]

import re

def supprimer_emails_specifiques(texte):
    # Expression régulière pour trouver les adresses e-mail avec le domaine "centrale-Casablanca.ma"
    regex_specific = r'\b[A-Za-z0-9._%+-]+@centralesupelec\.fr\b'
    # Supprimer les adresses e-mail spécifiques du texte
    texte_sans_emails_specifiques = re.sub(regex_specific, '', texte)

    return texte_sans_emails_specifiques



def remove_duplicates_simple(lst):
    return list(set(lst))

def pdf_to_clean_data(pdf_path):
  paragraphs = extract_text_by_font_size_with_tolerance(pdf_path)
  para_sans_mail=[supprimer_emails_specifiques(texte) for texte in paragraphs ]
  filtered_paragraphs = filter_paragraphs(para_sans_mail)
  cleaned_paragraphs = [clean_text(paragraph) for paragraph in filtered_paragraphs]

  return cleaned_paragraphs

def cleanpara_to_embeddings(cleaned_paragraphs):
  cleaned_paragraphs_without_stopwords = [remove_stopwords(para) for para in cleaned_paragraphs]
  lemmatized_paragraphs = [lemmatize_text(para) for para in cleaned_paragraphs_without_stopwords]
  embeddings = [text_to_embedding(para) for para in cleaned_paragraphs_without_stopwords]
  return embeddings

def text_to_indice(text,embeddings):

  text_traité= traitement_text(text)
  cossim=calculate_cosine_similarity(text_traité, embeddings)
  topindice=find_top_indices(cossim, top_n=5)
  return topindice

pdf_path2="/content/drive/MyDrive/Cours_POO_CH1 (1).pdf"

cleandata2=pdf_to_clean_data(pdf_path2)

for i, para in enumerate(cleandata2):
    print(f"Paragraphe {i+1}:\n{para}\n")

embeddings2=cleanpara_to_embeddings(cleandata2)

pdf_path3="/content/drive/MyDrive/Text Mining_introMTD (1).pdf"

cleandata3=pdf_to_clean_data(pdf_path3)

embeddings3=cleanpara_to_embeddings(cleandata3)

embeddings3

text3="L'indexation est essentielle pour la recherche et l'évaluation de la similitude entre les documents, avec de nombreuses applications pratiques telles que la détection de plagiat ou la recherche de dossiers médicaux. Des bibliothèques logicielles efficaces comme Lucene et Elasticsearch facilitent ce processus."

print(type(embeddings3))

i=text_to_indice(text3,embeddings3)

text_traité= traitement_text(text3)
text_traité

i

cleandata3[40]

cleandata3[30]

cleandata3

for i, para in enumerate(cleandata3):
    print(f"Paragraphe {i+1}:\n{para}\n")

text4="Un nuage de mots, aussi appelé WordCloud, est un outil efficace pour résumer les idées clés d'un texte, d'une page web ou même d'un livre. Dans ce type de représentation visuelle, les mots les plus fréquents dans le texte sont affichés en plus gros, tandis que les mots moins fréquents sont affichés en plus petit. Cette méthode permet de visualiser rapidement les thèmes principaux et les concepts dominants d'un contenu écrit. De nos jours, il existe de nombreuses plateformes en ligne et applications gratuites qui permettent de créer facilement des nuages de mots à partir de n'importe quel texte."

i2=i=text_to_indice(text4,embeddings3)

i2

cleandata3[98]

cleandata3[139]

fp="/content/drive/MyDrive/Cours LLORED. 2023-2024. 1A. Philosophie des sciences. FECC Séance 1.pdf"

ll=pdf_to_clean_data(fp)

for i, para in enumerate(ll):
    print(f"Paragraphe {i+1}:\n{para}\n")

aa = extract_text_by_font_size_with_tolerance(fp)
for i, para in enumerate(aa):
    print(f"Paragraphe {i+1}:\n{para}\n")

aa[2]

import re

def supprimer_emails_specifiques(texte):
    # Expression régulière pour trouver les adresses e-mail avec le domaine "centrale-Casablanca.ma"
    regex_specific = r'\b[A-Za-z0-9._%+-]+@centralesupelec\.fr\b'

    # Supprimer les adresses e-mail spécifiques du texte
    texte_sans_emails_specifiques = re.sub(regex_specific, '', texte)

    return texte_sans_emails_specifiques

supprimer_emails_specifiques(aa[2])