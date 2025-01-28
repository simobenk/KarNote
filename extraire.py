import fitz  # PyMuPDF
import shutil
import os
def extract_text_from_pdf(pdf_path):
    # Ouvrir le document PDF
    document = fitz.open(pdf_path)
    text = ""
    
    # Parcourir toutes les pages du document
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()

    return text


def deplacer_pdf(chemin_origine, chemin_destination):
    try:
        # Vérifier si le fichier existe à l'origine
        if os.path.exists(chemin_origine):
            # Déplacer le fichier vers la destination
            shutil.move(chemin_origine, chemin_destination)
            print(f"Le fichier {os.path.basename(chemin_origine)} a été déplacé avec succès.")
        else:
            print(f"Le fichier {os.path.basename(chemin_origine)} n'existe pas à l'emplacement spécifié.")
    except Exception as e:
        print( chemin_origine )