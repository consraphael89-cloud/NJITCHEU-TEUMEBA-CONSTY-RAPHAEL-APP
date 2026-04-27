import streamlit as st
import pandas as pd
import os
from datetime import datetime
# from docx import Document
from io import BytesIO

# Configuration créative de la page
st.set_page_config(page_title="DataCollect Pro", page_icon="🚀", layout="wide")

# --- STYLE CSS POUR L'ANIMATION ---
st.markdown("""
    <style>
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    .main-title { animation: fadeIn 2s; color: #4A90E2; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🌟 Collecteur de Données Intelligent</h1>", unsafe_allow_html=True)

# Initialisation du stockage en session (pour la robustesse locale)
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["ID", "Date", "Utilisateur", "Secteur", "Note", "Commentaire"])

# --- SECTION COLLECTE (FLEXIBILITÉ) ---
with st.expander("📝 Ouvrir le formulaire de saisie", expanded=True):
    with st.form("form_flexible", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            user = st.text_input("👤 Nom de l'informateur")
            secteur = st.selectbox("📂 Domaine", ["Éducation", "Santé", "Technologie", "Environnement"])
        with col2:
            note = st.select_slider("⭐ Note d'importance", options=range(1, 6))
            tags = st.multiselect("🏷️ Tags", ["Urgent", "Révisé", "Archive", "Public"])
            
        comment = st.text_area("💬 Observations détaillées")
        
        submitted = st.form_submit_button("Enregistrer la donnée")

if submitted:
    if user and comment:
        new_data = {
            "ID": len(st.session_state.db) + 1,
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Utilisateur": user,
            "Secteur": secteur,
            "Note": note,
            "Commentaire": comment
        }
        st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_data])], ignore_index=True)
        st.success("Donnée sécurisée avec succès !")
        st.balloons() # Animation de succès
    else:
        st.warning("Veuillez remplir les champs obligatoires (Nom et Commentaire).")

# --- SECTION EXPORTATION (TÉLÉCHARGEMENT) ---
st.divider()
st.subheader(" ⚡Gestion et Exportation")

if not st.session_state.db.empty:
    st.dataframe(st.session_state.db, use_container_width=True)
    
    c1, c2 = st.columns(2)
    
    # Export CSV
    csv_data = st.session_state.db.to_csv(index=False).encode('utf-8')
    c1.download_button("📥 Télécharger en CSV", csv_data, "export_donnees.csv", "text/csv")
    
    # Export DOCX (Word)
#     def generate_docx(df):
#         doc = Document()
#         doc.add_heading('Rapport de Collecte de Données', 0)
#         for i, row in df.iterrows():
#             p = doc.add_paragraph()
#             p.add_run(f"Entrée n°{row['ID']} - {row['Utilisateur']}").bold = True
#             doc.add_paragraph(f"Secteur : {row['Secteur']} | Note : {row['Note']}")
#             doc.add_paragraph(f"Commentaire : {row['Commentaire']}")
#             doc.add_paragraph("-" * 20)
#         bio = BytesIO()
#         doc.save(bio)
#         return bio.getvalue()

#     word_file = generate_docx(st.session_state.db)
#     c2.download_button("📄 Télécharger en Word (.docx)", word_file, "rapport.docx")
else:
    st.info("La base de données est vide. Commencez par saisir des informations.")