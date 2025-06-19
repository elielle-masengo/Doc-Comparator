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


if __name__ == "__main__":
    from comparison_engine import compare_documents

    t1 = "Bonjour monde\nCeci est une ligne\nTest ligne"
    t2 = "Bonjour monde\nCeci est une autre ligne\nNouvelle ligne ajoutée"
    keyword = "ligne"

    result = compare_documents(t1, t2, keyword)

    print(generate_statistics_report(t1, t2, result))
