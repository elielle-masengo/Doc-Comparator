from file_selection import file_selection_menu

def show_menu() -> None:
    """
    Affiche le menu de la comparaison des documents.
    Aucun paramètre n'est requis et la fonction ne retourne rien.
    """
    print("-"*30 + " COMPARAISON DES DOCUMENTS " + "-"*30)
    print(" Selectionnez le type de fichier: ")
    print("[1] .txt")
    print("[2] .pdf")
    print("[3] .pdf et .txt")
    print("[0] Retour")

def take_input(possible_choices: set[int]) -> int:
    """
    Demande à l'utilisateur d'entrer un entier présent dans l'ensemble possible_choices.
    
    :param possible_choices: Ensemble (set) d'entiers valides.
    :return: L'entier saisi par l'utilisateur, qui appartient à possible_choices.
    """
    choice = None

    while choice not in possible_choices:
        try:
            choice = int(input("Entrez votre choix (0 à 3): "))
        except ValueError:
            choice = None
        if choice not in possible_choices:
            print(("Saisie invalide, entrez un nombre compris entre 0 et 3"))

    return choice

def doc_comparison_menu() -> None :
    """
    Affiche le menu et informe l'option sélectionnée par l'utilisateur.
    """
    show_menu()
    print("")

    possible_choices = set([0, 1, 2, 3])

    choice = take_input(possible_choices)

    match choice:
        case 1:
            file_selection_menu()
        case 2:
            file_selection_menu()
        case 3:
            file_selection_menu()
        case 0:
            print("Retour au menu principal")
            
if __name__ == "__main__":
    doc_comparison_menu()