import os

import pandas as pd
import streamlit as st

from accueil import accueil_page
from analyse import analyse_page, visualisation, afficher_carte
from contexte import contexte_page
from prediction import prediction_page
from prediction_API import prediction_api_page

# Configuration de la page (doit être la première commande Streamlit)
st.set_page_config(page_title="GreenTech App", page_icon="⚡", layout="wide")

current_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(current_dir, "..", "data")


@st.cache_data
def load_data():
    file_path = os.path.join(DATA_DIR, "dataset_M2_enedis.csv")
    return pd.read_csv(
        file_path, sep=";", dtype={"Code_INSEE_(BAN)": str}, low_memory=False
    )


# Logo dans la barre latérale
st.sidebar.image(os.path.join(DATA_DIR, "logo.png"), width=300)

# Barre latérale de navigation
st.sidebar.header("GreenTech App ⚡")
options = {
    "🏠 Accueil": "accueil",
    "📊 Contexte": "contexte",
    "🔍 Analyse": "analyse",
    "🔮 Prédiction Locale": "prediction",
    "🔮 Prédiction avec API": "prediction_api",
}

selected_page = st.sidebar.selectbox(
    "Sélectionner une page", options=list(options.keys())
)

# Afficher le contenu de la page sélectionnée
page_key = options[selected_page]
if page_key == "accueil":
    accueil_page()
elif page_key == "contexte":
    contexte_page()
elif page_key == "analyse":
    data = load_data()
    analyse_page()
    visualisation(data)
    # Trop de points ralentit la carte : on n'en prend que 2 000
    data_carte = data.sample(2_000, random_state=42)
    afficher_carte(data_carte)
elif page_key == "prediction":
    prediction_page()
elif page_key == "prediction_api":
    prediction_api_page()

# Pied de page
st.sidebar.markdown("---")
st.sidebar.info("© 2024 GreenTech App. Tous droits réservés.")