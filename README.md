# ⚙️ Assistant PMO Intelligent - ECC

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![spaCy](https://img.shields.io/badge/NLP-spaCy-green.svg)

Une application d'ingénierie web conçue pour automatiser l'analyse, l'audit et la gestion de chartes de projets. Développé dans le cadre des méthodologies de Gestion de Projet de l'**École Centrale Casablanca**.

## 🎯 Objectif du Projet
Transformer un document texte brut (Charte de projet) en un véritable tableau de bord interactif d'aide à la décision. L'outil utilise le Traitement du Langage Naturel (NLP) et des expressions régulières pour auditer la maturité du projet, extraire les données financières et générer un plan d'action Agile.

> **Cas d'usage principal :** Projet *Afiya* (Prédiction de fuites d'eau via IoT et Machine Learning).

## 🚀 Fonctionnalités Clés

1. **📊 Audit des 5 Piliers :** Scanne le document pour vérifier la présence des concepts fondamentaux du management de projet (WBS, Charte, SMART, Matrice de risques, KPI).
2. **💰 Analyse Financière Multilingue :** Extraction automatique du budget global et de la répartition par phases grâce à des modèles Regex robustes (Supporte MAD, USD, EUR, DH, MDH, درهم).
3. **🚩 Matrice des Risques & Sentiment IA :** - Analyse du ton émotionnel du document (TextBlob).
   - Registre interactif pour calculer la criticité des risques (Probabilité $\times$ Impact).
4. **🗂️ Tableau Kanban (Jira-like) :**
   - Auto-génération de tickets "À faire" en lisant les livrables du document.
   - Déplacement interactif des tâches (À faire ➡️ En cours ➡️ Terminé).
   - **Export CSV** du Backlog pour intégration dans MS Project ou Excel.

## 🛠️ Stack Technique
- **Interface & Backend :** [Streamlit](https://streamlit.io/)
- **Intelligence Artificielle (NLP) :** `spaCy` (Modèles Français et Anglais)
- **Analyse de Sentiment :** `TextBlob`
- **Manipulation de Données :** `Pandas`
- **Extraction :** `re` (Expressions régulières Python)

## 💻 Installation et Lancement

1. Clonez ce dépôt :
   ```bash
   git clone [https://github.com/votre-nom-utilisateur/charter-analyzer.git](https://github.com/votre-nom-utilisateur/charter-analyzer.git)
   cd charter-analyzer