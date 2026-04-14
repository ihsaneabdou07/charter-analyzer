import streamlit as st
import spacy
import re
from textblob import TextBlob
import pandas as pd

# ==========================================
# 1. CONFIGURATION INITIALE (Une seule fois !)
# ==========================================
@st.cache_resource
def load_nlp_model(language):
    if language == "Français":
        return spacy.load("fr_core_news_sm")
    else:
        return spacy.load("en_core_web_sm")

st.set_page_config(page_title="PMO IA - ECC", page_icon="⚙️", layout="wide")

# ==========================================
# 2. BARRE LATÉRALE (SIDEBAR)
# ==========================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Ecole_Centrale_Casablanca_Logo.png/800px-Ecole_Centrale_Casablanca_Logo.png", width=150)
st.sidebar.header("⚙️ Configuration")
lang_choice = st.sidebar.selectbox("Langue de la charte", ["Français", "English"])

mode_analyse = st.sidebar.radio(
    "Type d'analyse :",
    ("Standard (Regex & Mots-clés)", "Pro (IA Complète)")
)

# ==========================================
# 3. INTERFACE PRINCIPALE
# ==========================================
st.title("⚙️ Assistant PMO Intelligent - ECC")
st.markdown("*Outil d'analyse de charte basé sur le référentiel de Gestion de Projet.*")

uploaded_file = st.file_uploader("Chargez le document du projet (.txt)", type=["txt"])

if uploaded_file:
    text = uploaded_file.getvalue().decode("utf-8")
    text_lower = text.lower()
    
    # Création des 4 onglets
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Audit des 5 Piliers", "💰 Analyse Financière", "🚩 Risques & NLP", "🗂️ Kanban (Jira)"])

    # --- ONGLET 1 : AUDIT DE MATURITÉ ---
    with tab1:
        st.header("📋 Audit de Maturité du Projet")
        st.write("Vérification de la présence des concepts clés du cours de GP.")

        cours_gp = {
            "01 & 02 - Initialisation": ["charte", "objectifs", "smart", "parties prenantes", "sponsor", "périmètre", "scope", "stakeholder"],
            "03 - Planification": ["wbs", "jalon", "milestone", "gantt", "échéancier", "planning", "ressources", "délais"],
            "04 - Exécution & Contrôle": ["livrable", "kpi", "indicateur", "qualité", "avancement", "deliverable"],
            "05 - Risques & Communication": ["risque", "mitigation", "communication", "réunion", "reporting", "matrice"]
        }

        score_total = 0
        max_score = len(cours_gp)
        resultats_audit = []

        for pilier, mots_cles in cours_gp.items():
            mots_trouves = [mot for mot in mots_cles if mot in text_lower]
            if mots_trouves:
                score_total += 1
                resultats_audit.append({"Pilier": pilier, "Statut": "✅ Validé", "Concepts": ", ".join(mots_trouves)})
            else:
                resultats_audit.append({"Pilier": pilier, "Statut": "❌ Manquant", "Concepts": "Aucun"})

        st.metric("Score de Conformité GP", f"{score_total} / {max_score}")
        st.progress(score_total / max_score)
        st.dataframe(pd.DataFrame(resultats_audit), use_container_width=True)

    # --- ONGLET 2 : ANALYSE FINANCIÈRE ---
    with tab2:
        st.header("📈 Extraction Automatique des Budgets")
        regex_pattern = r'\d+(?:[\s.,]\d+)*(?:\s?(?:MAD|USD|EUR|DH|DHs|MDH|درهم|د\.m))'
        money_regex = re.findall(regex_pattern, text)
        
        if mode_analyse == "Pro (IA Complète)":
            nlp = load_nlp_model(lang_choice)
            doc = nlp(text)
            money_nlp = [ent.text for ent in doc.ents if ent.label_ in ["MONEY", "AMOUNT"]]
            all_budgets = list(set(money_regex + money_nlp))
        else:
            all_budgets = money_regex

        if all_budgets:
            st.success(f"Montants globaux détectés : {', '.join(all_budgets)}")
        
        st.info("La simulation des phases s'effectue ici selon votre charte.")

    # --- ONGLET 3 : RISQUES & NLP (VERSION PRO) ---
    with tab3:
        st.header("🚩 Matrice des Risques & Analyse IA")
        
        col_ia, col_matrix = st.columns([1, 2])
        
        with col_ia:
            st.subheader("🧠 Sentiment IA")
            if mode_analyse == "Pro (IA Complète)":
                with st.spinner("Analyse du contexte en cours..."):
                    sentiment = TextBlob(text).sentiment.polarity
                    if sentiment < -0.1:
                        st.error(f"Ton risqué ({sentiment:.2f}).")
                    elif sentiment > 0.1:
                        st.success(f"Ton positif ({sentiment:.2f}).")
                    else:
                        st.info(f"Ton neutre ({sentiment:.2f}).")
            else:
                st.warning("Activez le Mode Pro.")

        with col_matrix:
            st.subheader("🎲 Registre des Risques")
            st.write("Évaluez les risques identifiés par l'IA ou votre équipe.")
            
            with st.expander("➕ Ajouter un risque identifié"):
                with st.form("risk_form"):
                    desc_risque = st.text_input("Description du risque (ex: Retard capteurs IoT)")
                    probabilite = st.slider("Probabilité (1 = Faible, 5 = Très forte)", 1, 5, 3)
                    impact = st.slider("Impact (1 = Mineur, 5 = Critique)", 1, 5, 3)
                    submit_risk = st.form_submit_button("Calculer la criticité")
                    
                    if submit_risk and desc_risque:
                        criticite = probabilite * impact
                        if criticite >= 15:
                            st.error(f"🚨 Risque Majeur (Score: {criticite}/25) - Plan de mitigation urgent requis.")
                        elif criticite >= 8:
                            st.warning(f"⚠️ Risque Modéré (Score: {criticite}/25) - À surveiller.")
                        else:
                            st.success(f"✅ Risque Faible (Score: {criticite}/25) - Acceptable.")

    # --- ONGLET 4 : KANBAN (JIRA) ---
    with tab4:
        st.header("🗂️ Gestion Agile des Tâches")
        st.write("Pilotez l'exécution de votre projet grâce à ce tableau Kanban interactif.")

        if 'taches' not in st.session_state:
            st.session_state.taches = []

        # Bouton d'extraction automatique par IA
        if st.button("🤖 Générer les tickets automatiquement depuis la charte"):
            lignes = text.split('\n')
            taches_ajoutees = 0
            
            for ligne in lignes:
                if re.search(r"(Phase|Étape|Step|Livrable)", ligne, re.IGNORECASE) or ligne.strip().startswith("-"):
                    tache_propre = ligne.strip('- ').strip()
                    if len(tache_propre) > 5:
                        nouvel_id = len(st.session_state.taches) + 1
                        st.session_state.taches.append({"id": nouvel_id, "nom": tache_propre, "resp": "À assigner", "statut": "À faire"})
                        taches_ajoutees += 1
            
            if taches_ajoutees > 0:
                st.success(f"{taches_ajoutees} tâches extraites avec succès !")
                st.rerun()
            else:
                st.warning("Aucune tâche structurée n'a été trouvée dans le texte.")

        # Ajout manuel
        with st.expander("➕ Créer un nouveau ticket manuel"):
            with st.form("ajout_tache_form"):
                nouvelle_tache = st.text_input("Description de la tâche")
                responsable = st.text_input("Responsable (ex: Groupe PLBD 8)")
                soumis = st.form_submit_button("Ajouter au Backlog")
                
                if soumis and nouvelle_tache:
                    nouvel_id = len(st.session_state.taches) + 1
                    st.session_state.taches.append({"id": nouvel_id, "nom": nouvelle_tache, "resp": responsable, "statut": "À faire"})
                    st.rerun()

        # Affichage des colonnes Kanban (Le code qui manquait !)
        col_todo, col_inprog, col_done = st.columns(3)

        with col_todo:
            st.subheader("📝 À faire")
            for i, tache in enumerate(st.session_state.taches):
                if tache['statut'] == "À faire":
                    with st.container(border=True):
                        st.write(f"**{tache['nom']}**")
                        st.caption(f"👤 {tache['resp']}")
                        if st.button("Démarrer ➡️", key=f"btn_start_{tache['id']}"):
                            st.session_state.taches[i]['statut'] = "En cours"
                            st.rerun()

        with col_inprog:
            st.subheader("⏳ En cours")
            for i, tache in enumerate(st.session_state.taches):
                if tache['statut'] == "En cours":
                    with st.container(border=True):
                        st.write(f"**{tache['nom']}**")
                        st.caption(f"👤 {tache['resp']}")
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button("⬅️ Stop", key=f"btn_back_{tache['id']}"):
                                st.session_state.taches[i]['statut'] = "À faire"
                                st.rerun()
                        with col_b:
                            if st.button("Fini ✅", key=f"btn_done_{tache['id']}"):
                                st.session_state.taches[i]['statut'] = "Terminé"
                                st.rerun()

        with col_done:
            st.subheader("✅ Terminé")
            for i, tache in enumerate(st.session_state.taches):
                if tache['statut'] == "Terminé":
                    with st.container(border=True):
                        st.write(f"~~{tache['nom']}~~")
                        st.caption(f"👤 {tache['resp']}")
                        if st.button("Relancer 🔄", key=f"btn_redo_{tache['id']}"):
                            st.session_state.taches[i]['statut'] = "En cours"
                            st.rerun()

        # NOUVEAUTÉ PRO : BOUTON D'EXPORTATION
        st.divider()
        st.subheader("📥 Exporter le plan d'action")
        st.write("Générez un fichier Excel/CSV pour votre rapport de projet.")
        
        if st.session_state.taches:
            df_taches = pd.DataFrame(st.session_state.taches)
            csv = df_taches.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Télécharger le Backlog (CSV)",
                data=csv,
                file_name="backlog_projet.csv",
                mime="text/csv",
            )
        else:
            st.info("Ajoutez des tâches au Kanban pour activer l'exportation.")