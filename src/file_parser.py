import os
import pdfplumber

def file_exists(filepath: str) -> bool:
    """
    Vérifie si un fichier existe à l'emplacement donné.

    :param filepath: Chemin d'accès au fichier.
    :return: True si le fichier existe, False sinon.
    """
    return os.path.isfile(filepath)

def read_txt_file(filepath: str) -> str:
    """ 
    Lit le contenu d'un fichier texte (.txt) et 
    renvoie le texte sous forme de chaîne de caractères.
    
    :param filepath: Chemin d'accès au fichier texte.
    :return: Contenu du fichier sous forme de chaîne, ou None en cas d'erreur.
    """
    try :
        with open(filepath, 'r', encoding='utf-8') as file:
            contenu = file.read()
            return contenu
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return None

def read_pdf_file(filepath: str) -> str:
    """
    Extrait le texte d'un fichier PDF.
    
    :param filepath: Chemin d'accès au fichier PDF.
    :return: Texte extrait du PDF sous forme de chaîne, ou None en cas d'erreur.
    """
    try:
        texte_complet = ""
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                texte = page.extract_text()
                if texte:
                    texte_complet += texte + "\n"
        return texte_complet
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return None
    

 
# def read_txt_file(filepath: str) -> str:
#     with open(filepath, 'r', encoding='utf-8') as f:
#         return f.read()
    
# def read_pdf_file(filepath: str)  -> str:
#     import pypdf2
#     with open(filepath, 'rb') as f:
#         reader = pypdf2.pdfreader(f)
#         content = ''
#         for page in reader.pages:
#             content += page.extract_text() or ''
#             return content

def parse_file(filepath: str) -> str:
    """
    Détecte l'extension du fichier et appelle la fonction appropriée de lecture
    (texte ou PDF). Gère également la vérification de l'existence du fichier
    et des formats non supportés.
    
    :param filepath: Chemin d'accès au fichier.
    :return: Contenu du fichier sous forme de chaîne, 
    ou None en cas d'erreur ou si le format n'est pas supporté.
    """
    try:
        if not os.path.isfile(filepath):
            return None
        
        _, extension = os.path.splitext(filepath)
        extension = extension.lower()

        if extension == '.txt':
            return read_txt_file(filepath)
        elif extension == '.pdf':
            return read_pdf_file(filepath)
        else:
            return None 
    
    except Exception as e:
        print(f"Erreur dans parse_file : {e}")
        return None 
    
    

    
if __name__ == "__main__":
    chemin = "exemple.txt"
    contenu = parse_file(chemin)

    print(f"contenu extrait de {chemin}:\n")
    print(contenu)

    chemin2 = "exemple.pdf"
    contenu2 = parse_file(chemin2)
    print(f"\ncontenu extrait de {chemin2}:\n")
    print(contenu2)

    