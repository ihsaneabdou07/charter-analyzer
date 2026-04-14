import streamlit as st
import spacy
import re
from textblob import TextBlob
import pandas as pd

# ==========================================
# 1. CONFIGURATION INITIALE
# ==========================================
@st.cache_resource
def load_nlp_model(language):
    if language == "Français":
        return spacy.load("fr_core_news_sm")
    else:
        return spacy.load("en_core_web_sm")

st.set_page_config(page_title="PMO IA - Ihsane Abdou", page_icon="⚙️", layout="wide")

# ==========================================
# 2. BARRE LATÉRALE (SIDEBAR)
# ==========================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Ecole_Centrale_Casablanca_Logo.png/800px-Ecole_Centrale_Casablanca_Logo.png", width=150)

linkedin_url = "https://www.linkedin.com/in/ihsane-abdou-a4bab1323"
st.sidebar.markdown("---")
st.sidebar.markdown("### 👤 Développé par")
st.sidebar.write("**Ihsane Abdou**")
st.sidebar.caption("Élève-ingénieure | École Centrale Casablanca")
st.sidebar.markdown(f"[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profil-blue?style=flat&logo=linkedin)]({linkedin_url})")
st.sidebar.markdown("---")

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
st.markdown(f"*Outil d'analyse de charte conçu par [Ihsane Abdou]({linkedin_url}).*")

uploaded_file = st.file_uploader("Chargez le document du projet (.txt)", type=["txt"])

if uploaded_file:
    text = uploaded_file.getvalue().decode("utf-8")
    text_lower = text.lower()
    
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

    # --- ONGLET 2 : ANALYSE FINANCIÈRE (CORRIGÉ !) ---
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
        
        st.divider()
        st.header("📊 Simulation Prévu vs Réel (Phases)")

        # L'IA cherche "Phase 1", "Étape 2", etc.
        phase_pattern = r"(Phase|Étape|Step)\s?(\d+)"
        phases_trouvees = list(re.finditer(phase_pattern, text, re.IGNORECASE))

        data_auto = []

        # Extraction des montants liés aux phases
        for match in phases_trouvees:
            name = f"{match.group(1)} {match.group(2)}"
            start_pos = match.end()
            remaining_text = text[start_pos:start_pos + 200]
            montant_match = re.search(regex_pattern, remaining_text)
            
            if montant_match:
                montant_str = montant_match.group()
                val_num = float(re.sub(r'[^\d.]', '', montant_str.replace(' ', '').replace(',', '.')))
                data_auto.append({"Phase": name, "Budget Prévu": val_num, "Label": montant_str})

        if data_auto:
            df_auto = pd.DataFrame(data_auto)
            st.success(f"✅ {len(data_auto)} phases détectées avec leurs budgets.")
            
            actual_data = []
            
            for index, row in df_auto.iterrows():
                col1, col2 = st.columns(2)
                col1.info(f"🎯 Prévu ({row['Phase']}) : {row['Label']}")
                reel = col2.number_input(f"💸 Coût Réel ({row['Phase']})", min_value=0.0, value=float(row['Budget Prévu']), key=f"auto_sim_{index}")
                
                actual_data.append({
                    "Phase": row['Phase'],
                    "Théorique": row['Budget Prévu'],
                    "Réel": reel
                })
            
            # Affichage du graphe de simulation
            df_comp = pd.DataFrame(actual_data)
            st.subheader("📉 Visualisation des Écarts")
            st.bar_chart(df_comp.set_index("Phase")[["Théorique", "Réel"]])
            
            # Bilan Mathématique
            total_prevu = df_comp["Théorique"].sum()
            total_reel = df_comp["Réel"].sum()
            
            if total_reel > total_prevu:
                st.error(f"🚨 Dépassement détecté : {total_reel - total_prevu:,.2f} par rapport au plan initial.")
            else:
                st.success(f"✅ Budget maîtrisé. Économie de : {total_prevu - total_reel:,.2f}")
        else:
            st.info("💡 Astuce : Rédigez votre charte sous la forme 'Phase 1 : 5000 MAD' pour activer l'analyse prédictive.")


    # --- ONGLET 3 : RISQUES & NLP ---
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
            with st.expander("➕ Ajouter un risque identifié"):
                with st.form("risk_form"):
                    desc_risque = st.text_input("Description du risque (ex: Retard capteurs IoT)")
                    probabilite = st.slider("Probabilité (1 = Faible, 5 = Très forte)", 1, 5, 3)
                    impact = st.slider("Impact (1 = Mineur, 5 = Critique)", 1, 5, 3)
                    submit_risk = st.form_submit_button("Calculer la criticité")
                    
                    if submit_risk and desc_risque:
                        criticite = probabilite * impact
                        if criticite >= 15:
                            st.error(f"🚨 Risque Majeur (Score: {criticite}/25)")
                        elif criticite >= 8:
                            st.warning(f"⚠️ Risque Modéré (Score: {criticite}/25)")
                        else:
                            st.success(f"✅ Risque Faible (Score: {criticite}/25)")

    # --- ONGLET 4 : KANBAN (JIRA) ---
    with tab4:
        st.header("🗂️ Gestion Agile des Tâches")
        if 'taches' not in st.session_state:
            st.session_state.taches = []

        if st.button("🤖 Générer les tickets automatiquement"):
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
                st.success(f"✅ {taches_ajoutees} tâches extraites avec succès !")
                st.rerun()

        with st.expander("➕ Créer un nouveau ticket manuel"):
            with st.form("ajout_tache_form"):
                nouvelle_tache = st.text_input("Description de la tâche")
                responsable = st.text_input("Responsable (ex: Groupe PLBD 8)")
                if st.form_submit_button("Ajouter au Backlog") and nouvelle_tache:
                    st.session_state.taches.append({"id": len(st.session_state.taches) + 1, "nom": nouvelle_tache, "resp": responsable, "statut": "À faire"})
                    st.rerun()

        st.markdown("---")
        col_todo, col_inprog, col_done = st.columns(3)

        with col_todo:
            st.subheader("📝 À faire")
            for i, tache in enumerate(st.session_state.taches):
                if tache['statut'] == "À faire":
                    with st.container(border=True):
                        st.write(f"**{tache['nom']}**")
                        st.caption(f"👤 {tache['resp']}")
                        if st.button("Démarrer ➡️", key=f"btn_start_{tache['id']}"):
                            st.session_state.taches[i]['statut'] = "En cours"; st.rerun()

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
                                st.session_state.taches[i]['statut'] = "À faire"; st.rerun()
                        with col_b:
                            if st.button("Fini ✅", key=f"btn_done_{tache['id']}"):
                                st.session_state.taches[i]['statut'] = "Terminé"; st.rerun()

        with col_done:
            st.subheader("✅ Terminé")
            for i, tache in enumerate(st.session_state.taches):
                if tache['statut'] == "Terminé":
                    with st.container(border=True):
                        st.write(f"~~{tache['nom']}~~")
                        st.caption(f"👤 {tache['resp']}")
                        if st.button("Relancer 🔄", key=f"btn_redo_{tache['id']}"):
                            st.session_state.taches[i]['statut'] = "En cours"; st.rerun()

        st.divider()
        st.subheader("📥 Exporter le plan d'action")
        if st.session_state.taches:
            csv = pd.DataFrame(st.session_state.taches).to_csv(index=False).encode('utf-8')
            st.download_button("Télécharger le Backlog (CSV)", csv, "backlog_projet.csv", "text/csv")
        else:
            st.info("Ajoutez des tâches au Kanban pour activer l'exportation.")

# ==========================================
# 4. PIED DE PAGE PERSONNALISÉ
# ==========================================
st.divider()
st.markdown(
    f"""
    <div style='text-align: center;'>
        <p>Développé avec ❤️ par <b>Ihsane Abdou</b> pour l'École Centrale Casablanca</p>
        <p><a href='{linkedin_url}' target='_blank'>Retrouvez-moi sur LinkedIn</a></p>
    </div>
    """, 
    unsafe_allow_html=True
)