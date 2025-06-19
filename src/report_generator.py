def summarize_line_differences(line_comparison: dict) -> str:
    """
    Génère un résumé clair des différences ligne par ligne entre deux documents.

    :param line_comparison: Résultat retourné par compare_lines().
    :return: Résumé texte avec indicateurs (+/-/=) pour chaque type de ligne.
    """
    summary = []

    # Lignes identiques
    if line_comparison.get("common"):
        summary.append("=== Lignes identiques ===")
        for line in line_comparison["common"]:
            summary.append(f"= {line}")
        summary.append("")  # Ligne vide pour aérer

    # Lignes différentes (même position mais contenu différent)
    if line_comparison.get("diff"):
        summary.append("=== Lignes différentes (position équivalente) ===")
        for l1, l2 in line_comparison["diff"]:
            summary.append(f"- {l1}")
            summary.append(f"+ {l2}")
        summary.append("")

    # Lignes présentes uniquement dans le document 1
    if line_comparison.get("unique_to_text1"):
        summary.append("=== Lignes uniquement dans le document 1 ===")
        for line in line_comparison["unique_to_text1"]:
            summary.append(f"- {line}")
        summary.append("")

    # Lignes présentes uniquement dans le document 2
    if line_comparison.get("unique_to_text2"):
        summary.append("=== Lignes uniquement dans le document 2 ===")
        for line in line_comparison["unique_to_text2"]:
            summary.append(f"+ {line}")
        summary.append("")

    if not summary:
        summary.append("Aucune différence détectée. Les documents sont identiques.")

    return "\n".join(summary)

def generate_statistics_report(
        text1: str,
        text2: str,
        comparison_result: dict
    ) -> str:
    """
    Génère un résumé des statistiques globales de la comparaison.

    :param text1: Contenu du premier texte.
    :param text2: Contenu du second texte.
    :param comparison_result: Dictionnaire retourné par compare_documents.
    :return: Texte du résumé des statistiques.
    """
    stats = []

    # Lignes
    nb_lignes_text1 = len(text1.splitlines())
    nb_lignes_text2 = len(text2.splitlines())
    nb_lignes_communes = len(comparison_result["line_comparison"].get("common", []))
    nb_lignes_diff = len(comparison_result["line_comparison"].get("diff", []))
    nb_uniques_1 = len(comparison_result["line_comparison"].get("unique_to_text1", []))
    nb_uniques_2 = len(comparison_result["line_comparison"].get("unique_to_text2", []))

    stats.append("=== Statistiques sur les lignes ===")
    stats.append(f"Nombre total de lignes dans le texte 1 : {nb_lignes_text1}")
    stats.append(f"Nombre total de lignes dans le texte 2 : {nb_lignes_text2}")
    stats.append(f"Lignes identiques : {nb_lignes_communes}")
    stats.append(f"Lignes différentes (à la même position) : {nb_lignes_diff}")
    stats.append(f"Lignes uniquement dans le texte 1 : {nb_uniques_1}")
    stats.append(f"Lignes uniquement dans le texte 2 : {nb_uniques_2}")
    stats.append("")

    # Mots
    nb_mots_text1 = len(text1.split())
    nb_mots_text2 = len(text2.split())

    stats.append("=== Statistiques sur les mots ===")
    stats.append(f"Nombre total de mots dans le texte 1 : {nb_mots_text1}")
    stats.append(f"Nombre total de mots dans le texte 2 : {nb_mots_text2}")
    stats.append(f"Mots uniquement dans le texte 1 : {len(comparison_result['unique_words'].get('only_in_text1', []))}")
    stats.append(f"Mots uniquement dans le texte 2 : {len(comparison_result['unique_words'].get('only_in_text2', []))}")
    stats.append("")

    # Taux de similarité
    stats.append("=== Taux de similarité ===")
    stats.append(f"{comparison_result['similarity_rate']} %")
    stats.append("")

    return "\n".join(stats)

def format_keyword_search(keyword: str, result: dict) -> str:
    """
    Affiche les résultats de la recherche d’un mot-clé dans les deux documents.

    :param keyword: Mot-clé recherché.
    :param result: Dictionnaire retourné par search_keyword ou compare_documents["keyword_search"].
    :return: Texte formaté contenant les résultats de recherche.
    """
    lines = []
    lines.append("=== Résultats de la recherche du mot-clé ===")
    lines.append(f"Mot-clé recherché : '{keyword}'")
    lines.append("")

    for doc, data in result.items():
        presence = "✔️ Présent" if data["found"] else "❌ Absent"
        count = data["count"]
        lines.append(f"- Dans {doc} : {presence}, nombre d’occurrences : {count}")
    
    lines.append("")  # Ligne vide pour séparer proprement
    return "\n".join(lines)

def generate_report(comparison_results: dict) -> str:
    """
    Génère un rapport texte structuré à partir des résultats de comparaison.

    :param comparison_results: Dictionnaire retourné par compare_documents.
    :return: Chaîne de caractères représentant le rapport complet.
    """
    lines = []

    lines.append("==== Rapport de comparaison ====\n")

    similarity = comparison_results["similarity_rate"]
    lines.append(f"Taux de similarité : {similarity:.2f}%\n")

    line_comp = comparison_results["line_comparison"]
    nb_common = len(line_comp["common"])
    nb_diff = len(line_comp["diff"])
    nb_unique1 = len(line_comp["unique_to_text1"])
    nb_unique2 = len(line_comp["unique_to_text2"])
    total = nb_common + nb_diff + nb_unique1 + nb_unique2

    lines.append("=== Statistiques des lignes ===")
    lines.append(f"Total de lignes analysées : {total}")
    lines.append(f"Lignes identiques         : {nb_common}")
    lines.append(f"Lignes différentes        : {nb_diff}")
    lines.append(f"Lignes uniquement dans texte 1 : {nb_unique1}")
    lines.append(f"Lignes uniquement dans texte 2 : {nb_unique2}\n")

    lines.append("=== Lignes différentes (avec détails mot à mot) ===")
    for diff in comparison_results["word_level_differences"]:
        lines.append("- Ligne dans texte 1 : " + diff["line_text1"])
        lines.append("+ Ligne dans texte 2 : " + diff["line_text2"])
        word_diff = diff["word_diff"]
        if word_diff["differences"]:
            lines.append("  > Mots différents :")
            for w1, w2 in word_diff["differences"]:
                lines.append(f"    - {w1}  ≠  {w2}")
        lines.append("")

    uniques = comparison_results["unique_words"]
    lines.append("=== Mots uniques ===")
    lines.append(f"Mots uniques au texte 1 : {', '.join(uniques['only_in_text1']) or 'Aucun'}")
    lines.append(f"Mots uniques au texte 2 : {', '.join(uniques['only_in_text2']) or 'Aucun'}\n")

    keyword_search = comparison_results["keyword_search"]
    lines.append("=== Résultat de la recherche du mot-clé ===")
    lines.append(f"Texte 1 : {'Oui' if keyword_search['text1']['found'] else 'Non'} "
                 f"({keyword_search['text1']['count']} occurrence(s))")
    lines.append(f"Texte 2 : {'Oui' if keyword_search['text2']['found'] else 'Non'} "
                 f"({keyword_search['text2']['count']} occurrence(s))\n")

    lines.append("==== Fin du rapport ====\n")
    return "\n".join(lines)

def export_report_to_file(report_text: str, file_path: str = "rapport_comparaison.txt") -> None:
    """
    Enregistre le rapport de comparaison dans un fichier texte.

    :param report_text: Rapport généré sous forme de texte (via generate_report).
    :param file_path: Chemin du fichier de sortie (par défaut : 'rapport_comparaison.txt').
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(report_text)
        print(f"✅ Rapport exporté avec succès dans '{file_path}'")
    except Exception as e:
        print(f"❌ Erreur lors de l'export du rapport : {e}")


if __name__ == "__main__":
    print("Ce module est destiné à être importé et utilisé dans d'autres scripts.")
