import os

def rename_pdf_files(directory, old_name, new_name):
    try:
        # Vérifier si le dossier existe
        if not os.path.exists(directory):
            print(f"Erreur: Le dossier {directory} n'existe pas.")
            return

        # Chemin complet des fichiers
        old_file_path = os.path.join(directory, old_name)
        new_file_path = os.path.join(directory, new_name)

        # Renommer le fichier s'il existe
        if os.path.exists(old_file_path):
            if os.path.exists(new_file_path):
                os.remove(new_file_path)
                print(f"Supprimé: {new_file_path}")

            os.rename(old_file_path, new_file_path)
            print(f"Renommé: {old_file_path} -> {new_file_path}")
        else:
            print(f"Fichier non trouvé: {old_file_path}")

    except Exception as e:
        print(f"Erreur lors du renommage des fichiers: {e}")

def delete_file(directory, filename):

    try:
        file_path = os.path.join(directory, filename)

        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Fichier {filename} supprimé avec succès dans {directory}")
        else:
            print(f"Le fichier {filename} n'existe pas dans {directory}")

    except Exception as e:
        print(f"Erreur lors de la suppression du fichier {filename}: {e}")


