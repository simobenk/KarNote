import os
import subprocess

def compile_latex(tex_content, output_dir=None):
    if output_dir is None:
        output_dir = os.path.join(os.getcwd(), 'static', 'mes_fichiers')
    
    # Utiliser un chemin relatif pour le logo
    logo_path = os.path.join(os.getcwd(), 'static', 'img', 'logo2.png')
    tex_content = tex_content.replace('<<LOGO_PATH>>', logo_path)

    try:
        # Créer le dossier de sortie s'il n'existe pas
        os.makedirs(output_dir, exist_ok=True)
        
        # Créer un nom de fichier temporaire pour le fichier LaTeX
        tex_file = os.path.join(output_dir, 'temp.tex')
        
        # Écrire le contenu LaTeX dans le fichier temporaire
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(tex_content)

        # Changer le répertoire de travail pour celui où se trouve le fichier temporaire
        os.chdir(output_dir)

        # Compiler le fichier LaTeX en PDF avec nonstopmode
        subprocess.run(['pdflatex', '-interaction=nonstopmode', 'temp.tex'])

    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la compilation LaTeX: {e}")
    except Exception as e:
        print(f"Erreur: {e}")
    else:
        print("Compilation LaTeX terminée avec succès.")

