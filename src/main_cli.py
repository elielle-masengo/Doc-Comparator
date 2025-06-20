from cli_interface.doc_comparison_menu import doc_comparison_menu

def show_main_menu() -> None:
    print("="*80)
    print(' '*30 + "DOCUMENT COMPARATOR" + ' '*30)
    print("="*80)
    print(
        "Bienvenue! Cet outil vous permet de comparer le contenu de deux fichiers texte\n" +
        "(.txt ou .pdf) et met en évidence les similitudes et les différences."
    )
    print("MENU PRINCIPAL:")
    print(" "*4 + "[1] Comparaison des Documents")
    print(" "*4 + "[2] Quitter")

def ask_choice(possible_choices: set[int]) -> int:
    choice = None
    while choice not in possible_choices:
        try:
            choice = int(input("Entrez votre choix : "))
        except ValueError:
            choice = None
        if choice not in possible_choices:
            print("Saisie incorrecte !\n")
    return choice

def main() -> None:
    while True:
        show_main_menu()
        print()
        choice = ask_choice({1, 2})

        match choice:
            case 1:
                doc_comparison_menu()
            case 2:
                print("\nMerci d’avoir utilisé le comparateur de documents. À bientôt !\n")
                break


if __name__ == "__main__":
    main()