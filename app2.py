import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import json
import os
import time
import random

# ── Configuration de la page ──────────────────────────────────────────────────
st.set_page_config(
    page_title="MedTrack – Système Hospitalier",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS personnalisé ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=DM+Serif+Display&display=swap');

/* Reset & base */
* { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

/* Fond principal */
.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1b2e 50%, #071422 100%);
    min-height: 100vh;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b1829 0%, #091220 100%);
    border-right: 1px solid rgba(0,200,255,0.15);
}

section[data-testid="stSidebar"] .stRadio label {
    color: #a0c4d8 !important;
    font-size: 0.95rem;
    transition: color 0.2s;
}

section[data-testid="stSidebar"] .stRadio label:hover {
    color: #00c8ff !important;
}

/* Titres */
h1 { font-family: 'DM Serif Display', serif !important; color: #e8f4fc !important; }
h2, h3 { color: #c5e3f0 !important; }

/* Animation de bienvenue */
@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-40px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(0,200,255,0.4); }
    50%       { box-shadow: 0 0 0 15px rgba(0,200,255,0); }
}
@keyframes shimmer {
    0%   { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-8px); }
}

.welcome-banner {
    animation: fadeInDown 0.8s ease-out forwards;
    background: linear-gradient(135deg, rgba(0,140,200,0.15) 0%, rgba(0,80,160,0.25) 100%);
    border: 1px solid rgba(0,200,255,0.3);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
}
.welcome-banner::before {
    content: '';
    position: absolute; inset: 0;
    background: linear-gradient(90deg, transparent, rgba(0,200,255,0.05), transparent);
    background-size: 1000px 100%;
    animation: shimmer 3s infinite linear;
}
.welcome-banner h1 {
    font-size: 2.8rem !important;
    margin: 0 !important;
    background: linear-gradient(135deg, #00c8ff, #ffffff, #00e5b4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.welcome-banner p {
    color: #7ec8e3;
    font-size: 1.1rem;
    margin-top: 0.5rem;
}

/* Stats cards */
.stat-card {
    animation: fadeInUp 0.6s ease-out forwards;
    background: linear-gradient(135deg, rgba(0,120,180,0.2), rgba(0,60,120,0.3));
    border: 1px solid rgba(0,200,255,0.2);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    transition: transform 0.3s, border-color 0.3s;
    backdrop-filter: blur(8px);
}
.stat-card:hover {
    transform: translateY(-4px);
    border-color: rgba(0,200,255,0.5);
}
.stat-card .icon { font-size: 2.2rem; margin-bottom: 0.5rem; animation: float 3s ease-in-out infinite; display: block; }
.stat-card .num  { font-size: 2.5rem; font-weight: 800; color: #00c8ff; }
.stat-card .lbl  { font-size: 0.85rem; color: #7ec8e3; text-transform: uppercase; letter-spacing: 1px; }

/* Form cards */
.form-section {
    animation: fadeInUp 0.5s ease-out forwards;
    background: rgba(10,20,40,0.7);
    border: 1px solid rgba(0,200,255,0.15);
    border-radius: 18px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(12px);
}
.section-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #00c8ff;
    border-left: 3px solid #00c8ff;
    padding-left: 0.75rem;
    margin-bottom: 1.2rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Inputs */
.stTextInput input, .stSelectbox select, .stTextArea textarea,
.stNumberInput input, .stDateInput input {
    background: rgba(0,30,60,0.6) !important;
    border: 1px solid rgba(0,200,255,0.2) !important;
    border-radius: 10px !important;
    color: #e0f2fe !important;
    transition: border-color 0.3s, box-shadow 0.3s !important;
}
.stTextInput input:focus, .stSelectbox select:focus, .stTextArea textarea:focus {
    border-color: #00c8ff !important;
    box-shadow: 0 0 0 2px rgba(0,200,255,0.2) !important;
}

/* Labels */
.stTextInput label, .stSelectbox label, .stTextArea label,
.stNumberInput label, .stDateInput label, .stRadio label,
.stMultiSelect label {
    color: #7ec8e3 !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
}

/* Boutons */
.stButton > button {
    background: linear-gradient(135deg, #0077b6, #00b4d8) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 1.8rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    transition: all 0.3s !important;
    animation: pulse 2s infinite;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #0096c7, #48cae4) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(0,180,216,0.4) !important;
}

/* Dataframe */
.stDataFrame { border-radius: 12px !important; overflow: hidden; }

/* Alertes success */
.stSuccess { background: rgba(0,200,130,0.15) !important; border: 1px solid rgba(0,200,130,0.3) !important; border-radius: 12px !important; }
.stWarning { background: rgba(255,160,0,0.15) !important; border: 1px solid rgba(255,160,0,0.3) !important; border-radius: 12px !important; }
.stError   { background: rgba(255,60,60,0.15) !important; border: 1px solid rgba(255,60,60,0.3) !important; border-radius: 12px !important; }

/* Sidebar logo */
.sidebar-logo {
    text-align: center;
    padding: 1.5rem 1rem 1rem;
    border-bottom: 1px solid rgba(0,200,255,0.1);
    margin-bottom: 1rem;
}
.sidebar-logo .logo-icon { font-size: 3rem; display: block; margin-bottom: 0.3rem; }
.sidebar-logo .logo-name { color: #00c8ff; font-weight: 700; font-size: 1.2rem; }
.sidebar-logo .logo-sub  { color: #4a7c9e; font-size: 0.75rem; letter-spacing: 2px; }

/* Badge */
.badge {
    display: inline-block;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
}
.badge-success { background: rgba(0,200,130,0.2); color: #00c882; border: 1px solid rgba(0,200,130,0.3); }
.badge-danger  { background: rgba(255,60,60,0.2);  color: #ff6b6b; border: 1px solid rgba(255,60,60,0.3); }
.badge-warning { background: rgba(255,160,0,0.2);  color: #ffa500; border: 1px solid rgba(255,160,0,0.3); }
.badge-info    { background: rgba(0,180,255,0.2);   color: #00c8ff; border: 1px solid rgba(0,180,255,0.3); }

/* Divider */
hr { border-color: rgba(0,200,255,0.1) !important; }

/* Tab */
.stTabs [data-baseweb="tab"] {
    color: #4a7c9e !important;
    font-weight: 500 !important;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: #00c8ff !important;
    border-bottom-color: #00c8ff !important;
}

/* Metric */
[data-testid="metric-container"] {
    background: rgba(0,40,80,0.4);
    border: 1px solid rgba(0,200,255,0.15);
    border-radius: 14px;
    padding: 0.8rem;
}
[data-testid="metric-container"] label { color: #7ec8e3 !important; }
[data-testid="metric-container"] [data-testid="metric-value"] { color: #00c8ff !important; }

/* Scroll bar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0e1a; }
::-webkit-scrollbar-thumb { background: #0077b6; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Stockage fichier JSON ─────────────────────────────────────────────────────
# ── Navigation via session_state ─────────────────────────────────────────────
PAGES = ["🏠  Accueil", "📋  Inscription Patient", "🩺  Diagnostic", "👥  Patients Enregistrés", "📊  Analyse & Statistiques"]

if "current_page" not in st.session_state or st.session_state.current_page not in PAGES:
    st.session_state.current_page = PAGES[0]

def go_to(page_name):
    # Cherche la page correspondante de façon souple (par emoji)
    for p in PAGES:
        if page_name.strip() in p or p.strip() in page_name:
            st.session_state.current_page = p
            st.rerun()
            return
    # Fallback exact
    st.session_state.current_page = page_name
    st.rerun()

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "medtrack_patients.json")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)

def get_df():
    data = load_data()
    if data:
        return pd.DataFrame(data)
    cols = ["id","nom","prenom","age","sexe","matricule","zone","quartier",
            "telephone","email","groupe_sanguin","allergies","antecedents",
            "maladie","symptomes","causes","gravite","traitement","medicaments",
            "date_admission","statut","notes","date_enregistrement"]
    return pd.DataFrame(columns=cols)

# Lire la page courante AVANT de rendre la sidebar
page = st.session_state.current_page

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <span class="logo-icon">🏥</span>
        <div class="logo-name">MedTrack</div>
        <div class="logo-sub">SYSTÈME HOSPITALIER</div>
    </div>
    """, unsafe_allow_html=True)

    selected = st.radio(
        "Navigation",
        PAGES,
        index=PAGES.index(st.session_state.current_page) if st.session_state.current_page in PAGES else 0,
        label_visibility="collapsed",
        key="nav_radio"
    )
    if selected != st.session_state.current_page:
        st.session_state.current_page = selected
        st.rerun()

    st.markdown("---")
    df_all = get_df()
    total = len(df_all)
    graves = len(df_all[df_all["gravite"] == "Critique"]) if total > 0 and "gravite" in df_all.columns else 0
    st.markdown(f"""
    <div style="padding:1rem;background:rgba(0,40,80,0.3);border-radius:12px;border:1px solid rgba(0,200,255,0.1)">
        <div style="color:#4a7c9e;font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:0.8rem">Résumé</div>
        <div style="display:flex;justify-content:space-between;margin-bottom:0.4rem">
            <span style="color:#7ec8e3">Total patients</span>
            <span style="color:#00c8ff;font-weight:700">{total}</span>
        </div>
        <div style="display:flex;justify-content:space-between">
            <span style="color:#7ec8e3">Cas critiques</span>
            <span style="color:#ff6b6b;font-weight:700">{graves}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"<div style='color:#2a4a6e;font-size:0.72rem;text-align:center;margin-top:1rem'>v2.0 · {datetime.now().strftime('%d/%m/%Y')}</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 : ACCUEIL
# ══════════════════════════════════════════════════════════════════════════════
if "🏠" in page:
    st.markdown("""
    <div class="welcome-banner">
        <h1>🏥 MedTrack</h1>
        <p>Système Intégré de Gestion & Surveillance Médicale</p>
    </div>
    """, unsafe_allow_html=True)

    df = get_df()
    total = len(df)
    zones = df["zone"].nunique() if total > 0 and "zone" in df.columns else 0
    maladies = df["maladie"].nunique() if total > 0 and "maladie" in df.columns else 0
    gueris = len(df[df["statut"] == "Guéri"]) if total > 0 and "statut" in df.columns else 0

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, "🧑‍⚕️", str(total),   "Patients enregistrés", "0.1s"),
        (c2, "🗺️",  str(zones),   "Zones couvertes",       "0.2s"),
        (c3, "🦠",  str(maladies),"Maladies répertoriées", "0.3s"),
        (c4, "✅",  str(gueris),  "Patients guéris",       "0.4s"),
    ]
    for col, icon, num, lbl, delay in cards:
        with col:
            st.markdown(f"""
            <div class="stat-card" style="animation-delay:{delay}">
                <span class="icon">{icon}</span>
                <div class="num">{num}</div>
                <div class="lbl">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([3, 2])

    with c1:
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📈 Activité récente</div>', unsafe_allow_html=True)
        if total > 0 and "date_enregistrement" in df.columns:
            df["date_enregistrement"] = pd.to_datetime(df["date_enregistrement"], errors="coerce")
            df_sorted = df.sort_values("date_enregistrement", ascending=False).head(5)
            for _, row in df_sorted.iterrows():
                gravite = row.get("gravite","")
                badge_class = {"Critique":"badge-danger","Sévère":"badge-warning","Modéré":"badge-info","Léger":"badge-success"}.get(gravite,"badge-info")
                st.markdown(f"""
                <div style="display:flex;align-items:center;justify-content:space-between;
                            padding:0.7rem 1rem;background:rgba(0,40,80,0.3);border-radius:10px;
                            border-left:3px solid rgba(0,200,255,0.4);margin-bottom:0.5rem">
                    <div>
                        <span style="color:#e0f2fe;font-weight:600">{row.get('prenom','')} {row.get('nom','')}</span>
                        <span style="color:#4a7c9e;font-size:0.8rem;margin-left:0.5rem">· {row.get('maladie','')}</span>
                    </div>
                    <span class="badge {badge_class}">{gravite}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Aucun patient enregistré pour l'instant.")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🔗 Accès rapide</div>', unsafe_allow_html=True)
        if st.button("📋 Nouveau patient", use_container_width=True, key="btn_inscription"):
            go_to("📋  Inscription Patient")
        if st.button("🩺 Nouveau diagnostic", use_container_width=True, key="btn_diag"):
            go_to("🩺  Diagnostic")
        if st.button("👥 Voir patients", use_container_width=True, key="btn_patients"):
            go_to("👥  Patients Enregistrés")
        if st.button("📊 Statistiques", use_container_width=True, key="btn_stats"):
            go_to("📊  Analyse & Statistiques")
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 : INSCRIPTION
# ══════════════════════════════════════════════════════════════════════════════
elif "📋" in page:
    st.markdown("""
    <div class="welcome-banner" style="padding:1.5rem">
        <h1 style="font-size:2rem!important">📋 Inscription d'un Patient</h1>
        <p>Renseignez les informations personnelles et médicales</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("inscription_form", clear_on_submit=True):
        # ── Données personnelles ──────────────────────────────────────────────
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">👤 Données Personnelles</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1: nom = st.text_input("Nom *")
        with c2: prenom = st.text_input("Prénom *")
        with c3: matricule = st.text_input("Matricule/ID *")

        c1, c2, c3 = st.columns(3)
        with c1: age = st.number_input("Âge *", 0, 120, 25)
        with c2: sexe = st.selectbox("Sexe *", ["Masculin","Féminin","Autre"])
        with c3: groupe_sanguin = st.selectbox("Groupe sanguin", ["A+","A-","B+","B-","AB+","AB-","O+","O-","Inconnu"])

        c1, c2, c3 = st.columns(3)
        with c1: zone = st.text_input("Zone / Ville *")
        with c2: quartier = st.text_input("Quartier")
        with c3: telephone = st.text_input("Téléphone")

        email = st.text_input("Email (optionnel)")
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Données médicales ─────────────────────────────────────────────────
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🩺 Données Médicales</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            maladie = st.selectbox("Maladie / Pathologie *", [
                "Paludisme","Typhoïde","Choléra","Tuberculose","COVID-19",
                "Diabète","Hypertension","VIH/SIDA","Méningite","Hépatite B",
                "Pneumonie","Dysenterie","Rougeole","Fièvre jaune","Autre"
            ])
        with c2:
            gravite = st.selectbox("Niveau de gravité *", ["Léger","Modéré","Sévère","Critique"])

        symptomes = st.text_area("Symptômes observés *", height=80)
        causes = st.text_area("Causes identifiées / Facteurs de risque", height=70)

        c1, c2 = st.columns(2)
        with c1: allergies = st.text_area("Allergies connues", height=70)
        with c2: antecedents = st.text_area("Antécédents médicaux", height=70)

        traitement = st.text_area("Traitement prescrit", height=70)
        medicaments = st.text_input("Médicaments prescrits")

        c1, c2 = st.columns(2)
        with c1: date_admission = st.date_input("Date d'admission", date.today())
        with c2: statut = st.selectbox("Statut du patient", ["En traitement","Guéri","Hospitalisé","Référé","Décédé"])

        notes = st.text_area("Notes complémentaires", height=70)
        st.markdown('</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("✅ Enregistrer le Patient", use_container_width=True)

    if submitted:
        if not nom or not prenom or not matricule or not zone or not maladie or not symptomes:
            st.error("⚠️ Veuillez remplir tous les champs obligatoires (*)")
        else:
            data = load_data()
            patient = {
                "id": len(data) + 1,
                "nom": nom.strip().upper(),
                "prenom": prenom.strip().capitalize(),
                "age": age,
                "sexe": sexe,
                "matricule": matricule.strip(),
                "zone": zone.strip().capitalize(),
                "quartier": quartier.strip(),
                "telephone": telephone.strip(),
                "email": email.strip(),
                "groupe_sanguin": groupe_sanguin,
                "allergies": allergies.strip(),
                "antecedents": antecedents.strip(),
                "maladie": maladie,
                "symptomes": symptomes.strip(),
                "causes": causes.strip(),
                "gravite": gravite,
                "traitement": traitement.strip(),
                "medicaments": medicaments.strip(),
                "date_admission": str(date_admission),
                "statut": statut,
                "notes": notes.strip(),
                "date_enregistrement": str(datetime.now()),
            }
            data.append(patient)
            save_data(data)
            st.success(f"✅ Patient **{prenom} {nom}** enregistré avec succès ! (ID: #{patient['id']})")
            st.balloons()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 : DIAGNOSTIC
# ══════════════════════════════════════════════════════════════════════════════
elif "🩺" in page:
    st.markdown("""
    <div class="welcome-banner" style="padding:1.5rem">
        <h1 style="font-size:2rem!important">🩺 Module de Diagnostic</h1>
        <p>Analyse des symptômes et aide à la décision médicale</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔍 Diagnostic rapide", "📝 Mise à jour patient"])

    # ── Onglet 1 : Diagnostic rapide ──────────────────────────────────────────
    with tab1:
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🔬 Saisie des Symptômes</div>', unsafe_allow_html=True)

        symptomes_list = st.multiselect("Symptômes observés", [
            "Fièvre","Céphalées","Vomissements","Diarrhée","Frissons","Toux",
            "Fatigue","Douleur abdominale","Éruption cutanée","Perte de poids",
            "Sueurs nocturnes","Jaunisse","Convulsions","Difficultés respiratoires",
            "Douleur thoracique","Œdèmes","Paralysie","Perte de conscience"
        ])

        c1, c2 = st.columns(2)
        with c1:
            temperature = st.slider("Température corporelle (°C)", 35.0, 42.0, 37.0, 0.1)
            tension = st.text_input("Tension artérielle (ex: 120/80)")
        with c2:
            duree = st.selectbox("Durée des symptômes", ["< 24h","1-3 jours","4-7 jours","1-2 semaines","> 2 semaines"])
            zone_diag = st.text_input("Zone géographique du patient")

        if st.button("🔍 Analyser les symptômes", use_container_width=True):
            # Logique de diagnostic basique
            st.markdown("---")
            st.markdown('<div class="section-title">📊 Résultats de l\'Analyse</div>', unsafe_allow_html=True)

            diagnostics = []
            if "Fièvre" in symptomes_list and "Frissons" in symptomes_list:
                diagnostics.append(("Paludisme", 85, "Critique"))
            if "Fièvre" in symptomes_list and "Céphalées" in symptomes_list and "Vomissements" in symptomes_list:
                diagnostics.append(("Typhoïde", 72, "Sévère"))
            if "Toux" in symptomes_list and "Difficultés respiratoires" in symptomes_list:
                diagnostics.append(("Pneumonie / COVID-19", 68, "Modéré"))
            if "Diarrhée" in symptomes_list and "Vomissements" in symptomes_list:
                diagnostics.append(("Choléra / Gastro-entérite", 60, "Modéré"))
            if "Jaunisse" in symptomes_list:
                diagnostics.append(("Hépatite B", 75, "Sévère"))
            if temperature >= 39.5:
                diagnostics.append(("Infection bactérienne sévère", 65, "Sévère"))
            if not diagnostics:
                diagnostics.append(("Syndrome viral non spécifié", 50, "Léger"))

            for diag, proba, grav in sorted(diagnostics, key=lambda x: -x[1]):
                badge_class = {"Critique":"badge-danger","Sévère":"badge-warning","Modéré":"badge-info","Léger":"badge-success"}.get(grav,"badge-info")
                st.markdown(f"""
                <div style="background:rgba(0,40,80,0.4);border-radius:12px;padding:1rem 1.2rem;
                            border-left:4px solid rgba(0,200,255,0.5);margin-bottom:0.8rem">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.4rem">
                        <span style="color:#e0f2fe;font-weight:700;font-size:1.05rem">{diag}</span>
                        <span class="badge {badge_class}">{grav}</span>
                    </div>
                    <div style="color:#4a7c9e;font-size:0.85rem;margin-bottom:0.5rem">Probabilité estimée : {proba}%</div>
                    <div style="background:rgba(0,200,255,0.1);border-radius:6px;height:6px">
                        <div style="background:linear-gradient(90deg,#0077b6,#00c8ff);height:6px;border-radius:6px;width:{proba}%"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            if temperature >= 38.5:
                st.warning(f"⚠️ Fièvre élevée détectée ({temperature}°C). Surveillance rapprochée recommandée.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Onglet 2 : Mise à jour ────────────────────────────────────────────────
    with tab2:
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">✏️ Mettre à Jour un Dossier</div>', unsafe_allow_html=True)

        df = get_df()
        if len(df) == 0:
            st.info("Aucun patient enregistré.")
        else:
            ids = df.apply(lambda r: f"#{r['id']} – {r['prenom']} {r['nom']}", axis=1).tolist()
            choix = st.selectbox("Sélectionner un patient", ids)
            idx = int(choix.split("–")[0].replace("#","").strip()) - 1

            data = load_data()
            patient = data[idx] if idx < len(data) else {}

            c1, c2 = st.columns(2)
            with c1:
                new_statut = st.selectbox("Nouveau statut", ["En traitement","Guéri","Hospitalisé","Référé","Décédé"],
                                          index=["En traitement","Guéri","Hospitalisé","Référé","Décédé"].index(patient.get("statut","En traitement")))
            with c2:
                new_gravite = st.selectbox("Nouveau niveau de gravité", ["Léger","Modéré","Sévère","Critique"],
                                           index=["Léger","Modéré","Sévère","Critique"].index(patient.get("gravite","Modéré")))

            new_traitement = st.text_area("Mise à jour traitement", value=patient.get("traitement",""), height=80)
            new_notes = st.text_area("Notes supplémentaires", value=patient.get("notes",""), height=70)

            if st.button("💾 Sauvegarder les modifications", use_container_width=True):
                data[idx].update({"statut": new_statut, "gravite": new_gravite,
                                  "traitement": new_traitement, "notes": new_notes})
                save_data(data)
                st.success("✅ Dossier mis à jour avec succès !")
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 : PATIENTS ENREGISTRÉS
# ══════════════════════════════════════════════════════════════════════════════
elif "👥" in page:
    st.markdown("""
    <div class="welcome-banner" style="padding:1.5rem">
        <h1 style="font-size:2rem!important">👥 Patients Enregistrés</h1>
        <p>Consulter, rechercher et gérer tous les dossiers patients</p>
    </div>
    """, unsafe_allow_html=True)

    df = get_df()

    if len(df) == 0:
        st.info("📭 Aucun patient enregistré. Commencez par inscrire un patient.")
    else:
        # Filtres
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🔎 Filtres de Recherche</div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1: search = st.text_input("Rechercher (nom/prénom)", "")
        with c2:
            zones_list = ["Toutes"] + sorted(df["zone"].dropna().unique().tolist())
            zone_f = st.selectbox("Zone", zones_list)
        with c3:
            grav_list = ["Toutes"] + sorted(df["gravite"].dropna().unique().tolist())
            grav_f = st.selectbox("Gravité", grav_list)
        with c4:
            stat_list = ["Tous"] + sorted(df["statut"].dropna().unique().tolist())
            stat_f = st.selectbox("Statut", stat_list)
        st.markdown('</div>', unsafe_allow_html=True)

        # Application des filtres
        df_f = df.copy()
        if search:
            df_f = df_f[df_f["nom"].str.contains(search, case=False, na=False) |
                        df_f["prenom"].str.contains(search, case=False, na=False)]
        if zone_f != "Toutes":  df_f = df_f[df_f["zone"] == zone_f]
        if grav_f != "Toutes":  df_f = df_f[df_f["gravite"] == grav_f]
        if stat_f != "Tous":    df_f = df_f[df_f["statut"] == stat_f]

        st.markdown(f"<div style='color:#4a7c9e;font-size:0.85rem;margin-bottom:1rem'>{len(df_f)} patient(s) trouvé(s)</div>", unsafe_allow_html=True)

        # Tableau
        cols_show = ["id","nom","prenom","age","sexe","zone","maladie","gravite","statut","date_admission"]
        st.dataframe(
            df_f[cols_show].rename(columns={
                "id":"ID","nom":"Nom","prenom":"Prénom","age":"Âge","sexe":"Sexe",
                "zone":"Zone","maladie":"Maladie","gravite":"Gravité","statut":"Statut","date_admission":"Admission"
            }),
            use_container_width=True,
            hide_index=True,
        )

        # Détail d'un patient
        st.markdown("---")
        st.markdown('<div class="section-title">📄 Détail d\'un Dossier</div>', unsafe_allow_html=True)
        if len(df_f) > 0:
            ids = df_f.apply(lambda r: f"#{r['id']} – {r['prenom']} {r['nom']}", axis=1).tolist()
            sel = st.selectbox("Choisir un patient", ids)
            pid = int(sel.split("–")[0].replace("#","").strip())
            row = df_f[df_f["id"] == pid].iloc[0]

            badge_class = {"Critique":"badge-danger","Sévère":"badge-warning","Modéré":"badge-info","Léger":"badge-success"}.get(row["gravite"],"badge-info")
            stat_class = {"Guéri":"badge-success","Décédé":"badge-danger","Hospitalisé":"badge-warning","En traitement":"badge-info","Référé":"badge-info"}.get(row["statut"],"badge-info")

            st.markdown(f"""
            <div class="form-section">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:1.5rem">
                    <div>
                        <div style="font-size:1.5rem;font-weight:700;color:#e0f2fe">{row['prenom']} {row['nom']}</div>
                        <div style="color:#4a7c9e">{row['sexe']} · {row['age']} ans · {row['groupe_sanguin']} · {row['zone']}</div>
                    </div>
                    <div style="display:flex;gap:0.5rem">
                        <span class="badge {badge_class}">{row['gravite']}</span>
                        <span class="badge {stat_class}">{row['statut']}</span>
                    </div>
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem">
                    <div style="background:rgba(0,40,80,0.3);border-radius:10px;padding:1rem">
                        <div style="color:#4a7c9e;font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:0.5rem">Maladie</div>
                        <div style="color:#e0f2fe;font-weight:600">{row['maladie']}</div>
                    </div>
                    <div style="background:rgba(0,40,80,0.3);border-radius:10px;padding:1rem">
                        <div style="color:#4a7c9e;font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:0.5rem">Admission</div>
                        <div style="color:#e0f2fe;font-weight:600">{row['date_admission']}</div>
                    </div>
                </div>
                <div style="margin-top:1rem;background:rgba(0,40,80,0.3);border-radius:10px;padding:1rem">
                    <div style="color:#4a7c9e;font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:0.5rem">Symptômes</div>
                    <div style="color:#c5e3f0">{row['symptomes']}</div>
                </div>
                <div style="margin-top:0.8rem;background:rgba(0,40,80,0.3);border-radius:10px;padding:1rem">
                    <div style="color:#4a7c9e;font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:0.5rem">Traitement</div>
                    <div style="color:#c5e3f0">{row['traitement'] or 'Non renseigné'}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 : ANALYSE & STATISTIQUES
# ══════════════════════════════════════════════════════════════════════════════
elif "📊" in page:
    st.markdown("""
    <div class="welcome-banner" style="padding:1.5rem">
        <h1 style="font-size:2rem!important">📊 Analyse & Statistiques</h1>
        <p>Visualisation des données épidémiologiques par zone</p>
    </div>
    """, unsafe_allow_html=True)

    df = get_df()

    if len(df) < 2:
        st.info("📉 Pas assez de données pour les statistiques. Enregistrez au moins 2 patients.")
    else:
        COLORS = ["#00c8ff","#0096c7","#00b4d8","#48cae4","#90e0ef","#00e5b4","#00b4a0"]
        TEMPLATE = "plotly_dark"
        PAPER_BG = "rgba(0,0,0,0)"
        PLOT_BG  = "rgba(0,20,40,0.5)"

        c1, c2 = st.columns(2)

        # Maladies
        with c1:
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            mal_count = df["maladie"].value_counts().reset_index()
            mal_count.columns = ["Maladie","Nombre"]
            fig = px.bar(mal_count, x="Nombre", y="Maladie", orientation="h",
                         color="Nombre", color_continuous_scale=["#023e8a","#00c8ff"],
                         template=TEMPLATE, title="🦠 Répartition des Maladies")
            fig.update_layout(paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
                              title_font_color="#00c8ff", showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Gravité
        with c2:
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            grav_count = df["gravite"].value_counts().reset_index()
            grav_count.columns = ["Gravité","Nombre"]
            fig2 = px.pie(grav_count, names="Gravité", values="Nombre",
                          color_discrete_sequence=["#00e5b4","#00c8ff","#ffa500","#ff6b6b"],
                          template=TEMPLATE, title="⚠️ Niveaux de Gravité")
            fig2.update_layout(paper_bgcolor=PAPER_BG, title_font_color="#00c8ff")
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        # Par zone
        with c1:
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            zone_count = df["zone"].value_counts().reset_index()
            zone_count.columns = ["Zone","Patients"]
            fig3 = px.bar(zone_count, x="Zone", y="Patients",
                          color="Patients", color_continuous_scale=["#023e8a","#00e5b4"],
                          template=TEMPLATE, title="🗺️ Patients par Zone")
            fig3.update_layout(paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
                               title_font_color="#00c8ff", coloraxis_showscale=False)
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Répartition par sexe
        with c2:
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            sexe_count = df["sexe"].value_counts().reset_index()
            sexe_count.columns = ["Sexe","Nombre"]
            fig4 = px.pie(sexe_count, names="Sexe", values="Nombre",
                          color_discrete_sequence=["#00c8ff","#ff6b9d","#7ec8e3"],
                          template=TEMPLATE, title="👥 Répartition par Sexe", hole=0.4)
            fig4.update_layout(paper_bgcolor=PAPER_BG, title_font_color="#00c8ff")
            st.plotly_chart(fig4, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Statuts
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📋 Récapitulatif Global</div>', unsafe_allow_html=True)

        m1, m2, m3, m4, m5 = st.columns(5)
        stats = [
            (m1, "Total", len(df)),
            (m2, "Guéris", len(df[df["statut"]=="Guéri"])),
            (m3, "Hospitalisés", len(df[df["statut"]=="Hospitalisé"])),
            (m4, "Critiques", len(df[df["gravite"]=="Critique"])),
            (m5, "Âge moyen", f"{df['age'].mean():.1f}"),
        ]
        for col, label, val in stats:
            with col: st.metric(label, val)

        # Tableau récap par zone et maladie
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">🗺️ Analyse par Zone</div>', unsafe_allow_html=True)
        pivot = df.groupby(["zone","maladie"]).size().reset_index(name="cas")
        st.dataframe(pivot.rename(columns={"zone":"Zone","maladie":"Maladie","cas":"Nombre de cas"}),
                     use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)