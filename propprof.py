from llama_parse import LlamaParse
import nest_asyncio; nest_asyncio.apply()
import test
import extraire
import os
from dotenv import load_dotenv
import google.generativeai as genai
import requests

# Charger les variables d'environnement
load_dotenv()

# Configuration des APIs
parser = LlamaParse(
    api_key=os.getenv('LLAMA_API_KEY'),
    result_type="markdown",
    verbose=True
)

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Initialisation des modèles
model = genai.GenerativeModel('gemini-pro')
model2 = genai.GenerativeModel('gemini-1.5-pro-latest')

# Headers pour OpenAI
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
}

from IPython.display import display, Markdown
import textwrap
def to_markdown(text):
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


import google.generativeai
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

model = genai.GenerativeModel('gemini-pro')
model2 =genai.GenerativeModel('gemini-1.5-pro-latest')
def gemini2(t):
  response = model2.generate_content(t)
  generated_text = to_markdown(response.text)
  return response.text
def gemini(t):
  response = model.generate_content(t)
  generated_text = to_markdown(response.text)
  return response.text
promp_resume="résume moi le cours suivant avec le plus de détails possible sans oubliant aucune information de base et en ecrivant tous les relations mathematiques importantes si il y en a, , le cours :"
promp_quiz="fait moi un quiz de 10 question du facile au difficile  ,et tu ecrit en bas les reponses bréf de chaque question ,tu peux aporter les exos de votre bases de données , le cours :"
def gemini_resume(texte):
  return gemini(promp_resume+texte)
def gemini_resume2(texte):
  return gemini2(promp_resume+texte)
def gemini_quiz2(texte):
  return gemini2(promp_quiz+texte)

import base64
import requests

def latexgpt(texte):
  payload = {
    "model": "gpt-3.5-turbo",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "transcrit ce texte en code latex complet avec les bibliotheque, tu doit ajouter les bibliotheque tcolorbox et autre dans le code latex pour un coté esthetique et une bonne visualisation chaque theoreme ou chaque idée ou chaque paragraphe doit etre dans une box et tu peut varier les couleurs selon le sens(utilise 2 ou 3 couleurs max) et ne met pas tout le cours dans une seul box et surtout le code latex doit etre correct,tu m ajoute dans tout le debut apres avoir definir les bibliotheque ce code latex : "+rr+", et finalement tu m ajoute dans les bibliotheque la biblio graphicx et [absolute,overlay]{textpos} ,evite l erreur 'Undefined control sequence' et essaye de ne faire aucune faute surtout avec les \end et LaTeX Error: Unicode character car tu fait cette erreur beaucoup pour les signe comme λ et α tu dois faire leur code latex... et evite Is usepackage{amsmath} missing? et Missing $ inserted et 'Undefined control sequence.',... sans rien ajouter ecrit juste le code latex,le texte: "+texte
          },


        ]
      }
    ],
    "max_tokens": 4096
  }

  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

  return response.json()["choices"][0]["message"]["content"]
def latexgpt7(texte):
  payload = {
    "model": "gpt-3.5-turbo",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "transcrit ce texte en code latex complet avec les tout les bibliotheque,  et surtout le code latex doit etre correct,tu m ajoute dans tout le debut apres avoir definir les bibliotheque ce code latex : "+rr+", est tu ne doit pas commetre l erreur du '! Undefined control sequence.' ... sans rien ajouter ecrit juste le code latex,le texte: "+texte
          },


        ]
      }
    ],
    "max_tokens": 4096
  }

  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

  return response.json()["choices"][0]["message"]["content"]
def xens(texte):
  payload = {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "tu prend le cours suivant et tu me crée un probléme tres difficile et trop complexe avec un calcule complexe,et soit le plus créatif possible ,de type X-ens , avec plusieur question qui entamme tout le cours et en bas tu met tous les elements de reponse , le titre c est 'Probleme sur ' nom du cours  ... sans rien ajouter ecrit juste le code latex, le cours : "+texte
          },


        ]
      }
    ],
    "max_tokens": 4096
  }

  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

  return response.json()["choices"][0]["message"]["content"]



rr=r"""\begin{textblock*}{3cm}(0.5cm,1cm)
    \includegraphics[width=3cm]{<<LOGO_PATH>>}
\end{textblock*}"""

def remove_latex_text(input_string):
    # Enlève toutes les occurrences de "```latex"
    cleaned_string = input_string.replace("```latex", "")
    return cleaned_string
def remove_latex_text2(input_string):
    # Enlève toutes les occurrences de "```latex"
    cleaned_string = input_string.replace("```", "")
    return cleaned_string



logo_path="static/img/logo2.png"
def xensfinal2(pdf_path,color):
  doc=parser.load_data(pdf_path)
  text=gemini_resume2(doc[0].text)
  x=xens(text)
  latex=gemini2("tronsfomre le code suivant en un code latex correct avec les bon retour a la ligne et titrage et avec la bibliotheque tcolorbox pour une bonne visualisation tu travail avec plusieur boxe et il ne faut pas que tous soit dans des boxe et en utilisant uniquement la couleur :"+color+"est la couleur gris, mais il faut que la couleur gris qui domine et que l autre couleur soit faible et utilisé seulempent pour la decoration ,tu ajoute les bibliotheque 'graphicx' et '[absolute,overlay]{textpo',le titre du document ne doit pas etre dans la premiere boxe  ,ajoute juste apres avoir definit les bibliotheques le code suivant :: "+rr+"je veux en reponse juste de codelatex , le text est  "+x)
  latex1=remove_latex_text2(remove_latex_text(latex))
  test.compile_latex(latex1)
  return "compitilation latex avec succes"


def quizfinal(pdf_path,color):
  doc=parser.load_data(pdf_path)
  text=gemini_quiz2(doc[0].text)
  latex=gemini2("tronsfomre le code suivant en un code latex correct avec les bon retour a la ligne et titrage et avec la bibliotheque tcolorbox pour une bonne visualisation tu travail avec plusieur boxe et il ne faut pas que tous soit dans des boxe et en utilisant uniquement la couleur "+color+"est la couleur gris,tu ajoute les bibliotheque 'graphicx' et '[absolute,overlay]{textpo',le titre du document ne doit pas etre dans la premiere boxe  , ajoute juste apres avoir definit les bibliotheques le code suivant :: "+rr+" , je veux en reponse juste de codelatex , le text "+text)
  latex1=remove_latex_text2(remove_latex_text(latex))
  test.compile_latex(latex1)
  return "compitilation latex avec succes"


def process(filepath, output):
    texte = extraire.extract_text_from_pdf(output)
    doc = parser.load_data(filepath)
    t = gemini2("tu resume le speech à partir du support du cours , le speech : " + texte + " le support du cours" + doc[0].text)
    
    # Utiliser un chemin relatif pour le dossier de sortie
    output_dir = os.path.join(os.getcwd(), 'static', 'mes_fichiers')
    
    latex = gemini2("tronsfomre le code suivant en un code latex correct avec les bon retour a la ligne et titrage et avec la bibliotheque tcolorbox pour une bonne visualisation tu travail avec plusieur boxe et il ne faut pas que tous soit dans des boxe et en utilisant uniquement la couleur bleu et la couleur gris,tu ajoute les bibliotheque 'graphicx' et '[absolute,overlay]{textpo',le titre du document ne doit pas etre dans la premiere boxe  , ajoute juste apres avoir definit les bibliotheques le code suivant :: "+rr+" , je veux en reponse juste de codelatex , le text "+t)
    latex1 = remove_latex_text2(remove_latex_text(latex))
    test.compile_latex(latex1, output_dir)
    return "success"


def resumee(fillpath):
    texte= extraire.extract_text_from_pdf(fillpath)
    
    t=gemini2("reprend tout les idee essencielles de ce texte (resume en des tirés) ,le text :"+texte )
    latex=gemini2("tronsfomre le code suivant en un code latex correct avec les bon retour a la ligne et titrage et avec la bibliotheque tcolorbox pour une bonne visualisation tu travail avec plusieur boxe et il ne faut pas que tous soit dans des boxe et en utilisant uniquement la couleur bleu et la couleur gris,tu ajoute les bibliotheque 'graphicx' et '[absolute,overlay]{textpo',le titre du document ne doit pas etre dans la premiere boxe  , ajoute juste apres avoir definit les bibliotheques le code suivant :: "+rr+" , je veux en reponse juste de codelatex ,et tu respecte le titrage et mettre en gras si un mot ou un text et entre des **, le text "+t)
    latex1=remove_latex_text2(remove_latex_text(latex))
    test.compile_latex(latex1)
    return "secces"
def resumee1(fillpath):
    texte= parser.load_data(fillpath)
    
    t=gemini2("tu parle de tout les idées qui sont dans ce texte (resume en des tirés)  ,le text :"+texte )
    latex=gemini2("transforme ce texte en un code latex complet et correct,sans rien ajouté reponse juste avec le code latex  , le text :"+t)
    latex1=remove_latex_text2(remove_latex_text(latex))
    test.compile_latex(latex1)
    return "secces"
def enrichir(fillpath):
  texte= extraire.extract_text_from_pdf(fillpath)  
  t=gemini2("reprend tout les idee essencielles de ce texte et tu enrechie le maximaum ces idées ,la reponse dois etre la plus long possible , tu met des /n si tu veuxx faire un retour à la ligne ,le text :"+texte )
  latex=gemini2("tronsfomre le code suivant en un code latex correct avec les bon retour a la ligne et titrage et avec la bibliotheque tcolorbox pour une bonne visualisation tu travail avec plusieur boxe et il ne faut pas que tous soit dans des boxe et en utilisant uniquement la couleur bleu et la couleur gris,tu ajoute les bibliotheque 'graphicx' et '[absolute,overlay]{textpo',le titre du document ne doit pas etre dans la premiere boxe  , ajoute juste apres avoir definit les bibliotheques le code suivant :: "+rr+" , je veux en reponse juste de codelatex, et tu respecte le titrage qui est representer avec des *  et mettre en gras si un mot ou un text et entre des ** , le text "+t)
  latex1=remove_latex_text2(remove_latex_text(latex))
  test.compile_latex(latex1)
  return "secces"


def st(fillpath):
  texte= extraire.extract_text_from_pdf(fillpath)
  t=gemini2("tu prend ce speech et tu reecrit tres bien et d une maniere parfaite les formule mathematique et les equation mathematiques si elles existe  , le speech :"+texte)
  latex=gemini2("tronsfomre le code suivant en un code latex correct avec toutes les bibliotheques ,tu ajoute les bibliotheque 'graphicx' et '[absolute,overlay]{textpo', ajoute juste apres avoir definit les bibliotheques le code suivant :: "+rr+" , je veux en reponse juste de codelatex, voici le texte :  "+t)
  latex1=remove_latex_text2(remove_latex_text(latex))
  test.compile_latex(latex1)
  return "secces"
