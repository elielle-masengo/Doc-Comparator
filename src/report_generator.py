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


if __name__ == "__main__":
    comparaison_exemple = {
        'common': ['Ligne A'],
        'diff': [('Ligne B1', 'Ligne B2')],
        'unique_to_text1': ['Ligne C1', 'Ligne D1'],
        'unique_to_text2': ['Ligne C2']
    }

    print(summarize_line_differences(comparaison_exemple))
