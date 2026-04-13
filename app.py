import streamlit as st
import spacy

# Chargement du modèle NLP (le cerveau)
# On utilise try/except au cas où le modèle n'est pas encore téléchargé
try:
    nlp = spacy.load("en_core_web_sm")
except:
    st.error("Modèle NLP non trouvé. Lance 'python -m spacy download en_core_web_sm' dans ton terminal.")

st.set_page_config(page_title="Analyseur IA - ECC", page_icon="🤖")

st.title("🤖 Analyseur Intelligent de Projet")
st.write("Analyse automatique de la Triple Contrainte via NLP.")

uploaded_file = st.file_uploader("Charge ta charte (.txt)", type=["txt"])

if uploaded_file is not None:
    text = uploaded_file.getvalue().decode("utf-8")
    doc = nlp(text) # L'IA analyse le texte ici
    
    st.success("Analyse terminée !")

    # --- SECTION : EXTRACTION DES ENTITÉS ---
    st.subheader("🔍 Détections automatiques")
    
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Dates & Délais (Time)**")
        dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
        if dates:
            for d in dates:
                st.info(f"📅 {d}")
        else:
            st.warning("Aucune date détectée.")

    with col2:
        st.write("**Budget & Coûts (Cost)**")
        money = [ent.text for ent in doc.ents if ent.label_ == "MONEY"]
        if money:
            for m in money:
                st.success(f"💰 {m}")
        else:
            st.warning("Aucun montant détecté.")

    # --- SECTION : ANALYSE DES MOTS CLÉS ---
    st.subheader("🎯 Analyse du Scope")
    keywords = ["deliverable", "objective", "goal", "scope", "phase"]
    found_keywords = [word for word in keywords if word in text.lower()]
    
    if found_keywords:
        st.write(f"Mots-clés de périmètre trouvés : {', '.join(found_keywords)}")
    else:
        st.error("Attention : Le périmètre (Scope) semble mal défini.")
        
        
    # --- SECTION : CALCUL DU SCORE DE SANTÉ ---
    st.divider()
    st.subheader("📊 Bilan de Santé du Projet")

    # Calcul des scores (1 si présent, 0 si absent)
    score_time = 1 if dates else 0
    score_cost = 1 if money else 0
    score_scope = 1 if found_keywords else 0
    
    total_score = score_time + score_cost + score_scope

    # Affichage avec des colonnes et des indicateurs (Metrics)
    m1, m2, m3 = st.columns(3)
    m1.metric("Time", "Prêt" if score_time else "Manquant", delta=score_time)
    m2.metric("Cost", "Prêt" if score_cost else "Manquant", delta=score_cost)
    m3.metric("Scope", "Prêt" if score_scope else "Manquant", delta=score_scope)

    if total_score == 3:
        st.balloons() # Petite animation de célébration
        st.success("La charte est complète ! La Triple Contrainte est respectée.")
    elif total_score >= 1:
        st.warning(f"Charte incomplète. Score : {total_score}/3. Vérifiez les éléments manquants.")
    else:
        st.error("Charte critique : Aucune contrainte majeure détectée.")
        
        
    # ... (ton code précédent sur le score de santé)

    # --- SECTION : ANALYSE DE RISQUE (SENTIMENT) ---
    from textblob import TextBlob
    
    st.divider() # Ajoute une ligne de séparation visuelle
    st.subheader("🚩 Analyse de Risque (Sentiment)")
    
    # TextBlob analyse si le texte est positif ou négatif
    analysis = TextBlob(text).sentiment
    
    if analysis.polarity < 0:
        st.error(f"Le ton du document est risqué ({analysis.polarity:.2f}). Attention aux obstacles mentionnés.")
    elif analysis.polarity > 0.2:
        st.success(f"Le ton du document est très positif et assuré ({analysis.polarity:.2f}).")
    else:
        st.info(f"Le ton du document est neutre ou factuel ({analysis.polarity:.2f}).")