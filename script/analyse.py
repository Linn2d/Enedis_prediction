import streamlit as st
import pandas as pd
import folium
import os

from streamlit_folium import st_folium
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from utils import (
    create_plotly_pie_chart,
    create_seaborn_bar_chart,
    create_plotly_histogram,
    create_plotly_line_chart,
    calculate_kpis,
    afficher_kpis,
)


def analyse_page():
    st.title("Analyse des Données")

    st.write(
        """
        Cette page offre une analyse approfondie des données de performance énergétique des logements de la région Rhône-Alpes.
        Elle permet de visualiser les données sous forme de graphiques interactifs et intuitifs, afin de mieux comprendre les tendances
        générales et d'explorer les relations entre différentes variables, telles que l’étiquette DPE, la consommation énergétique,
        la taille des logements, l’année de construction, et bien d'autres paramètres.
        
        En utilisant divers outils de filtrage et de tri, vous pouvez examiner les indicateurs clés de performance et isoler les
        caractéristiques qui influencent le plus les performances énergétiques. Cette analyse facilite ainsi l’identification des
        principaux leviers pour améliorer l'efficacité énergétique des logements dans la région.
        """
    )


def visualisation(data):
    kpis = calculate_kpis(data)
    afficher_kpis(kpis)

    st.sidebar.header("Sélection des mesures et filtres")

    # Définition des variables à utiliser
    consommation_vars = [
        "Type_bâtiment",
        "Qualité_isolation_enveloppe",
        "Etiquette_GES",
        "Surface_habitable_logement",
        "Etiquette_DPE",
        "Type_installation_chauffage",
        "Ubat_W/m²_K",
        "Qualité_isolation_murs",
        "Type_énergie_n°1",
        "Qualité_isolation_plancher_bas",
        "Méthode_application_DPE",
        "Qualité_isolation_menuiseries",
        "Conso_5_usages_é_finale",
    ]

    etiquette_vars = [
        "Conso_chauffage_é_primaire",
        "Conso_5_usages_é_finale",
        "Emission_GES_5_usages_par_m²",
        "Etiquette_GES",
        "Coût_éclairage",
        "Etiquette_DPE",
    ]

    all_vars = list(set(consommation_vars + etiquette_vars))

    # Sélection de la mesure à visualiser
    selected_measure = st.sidebar.selectbox(
        "Choisissez une mesure à visualiser",
        all_vars,
        index=all_vars.index("Etiquette_DPE") if "Etiquette_DPE" in all_vars else 0,
    )

    # Filtrage des modalités si la variable sélectionnée est catégorielle
    filtered_data = data[all_vars].copy()
    if filtered_data[selected_measure].dtype == "object":
        unique_values = filtered_data[selected_measure].unique().tolist()
        selected_modalities = st.sidebar.multiselect(
            f"Filtrer les modalités de {selected_measure}",
            unique_values,
            default=unique_values,
        )
        filtered_data = filtered_data[
            filtered_data[selected_measure].isin(selected_modalities)
        ]

    st.sidebar.header("Sélection des graphiques")

    # Sélection des types de graphiques avec "Barres" par défaut
    graph_options = ["Barres", "Camembert", "Histogramme", "Ligne"]
    selected_graphs = st.sidebar.multiselect(
        "Choisissez les graphiques à afficher", graph_options, default=["Barres"]
    )

    # Préparation des données
    values = filtered_data[selected_measure].dropna()

    def create_plotly_pie_chart(labels, sizes):
        fig = px.pie(
            names=labels,
            values=sizes,
            title="Répartition des valeurs",
            color_discrete_sequence=px.colors.sequential.Viridis,
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(title_font_size=20)
        return fig

    def create_seaborn_bar_chart(labels, values):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=labels, y=values, palette="viridis", ax=ax)
        ax.set_title(
            "Répartition des données par catégorie", fontsize=14, weight="bold"
        )
        ax.set_xlabel("Catégories", fontsize=12)
        ax.set_ylabel("Valeurs", fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig

    def create_plotly_histogram(values):
        fig = px.histogram(
            values,
            nbins=20,
            title="Distribution des valeurs",
            color_discrete_sequence=["skyblue"],
        )
        fig.update_layout(
            xaxis_title="Valeurs", yaxis_title="Fréquence", title_font_size=20
        )
        return fig

    def create_plotly_line_chart(x, y):
        fig = px.line(
            x=x, y=y, title="Évolution des valeurs", markers=True, line_shape="spline"
        )
        fig.update_layout(
            xaxis_title="Catégories", yaxis_title="Valeurs", title_font_size=20
        )
        return fig

    for graph in selected_graphs:
        if pd.api.types.is_numeric_dtype(filtered_data[selected_measure]):
            chart_data = filtered_data[selected_measure].value_counts().sort_index()
            labels = chart_data.index
            sizes = chart_data.values
        else:
            chart_data = filtered_data[selected_measure].value_counts()
            labels = chart_data.index
            sizes = chart_data.values

        if graph == "Barres":
            fig = create_seaborn_bar_chart(labels, sizes)
            st.pyplot(fig)
        elif graph == "Camembert":
            fig = create_plotly_pie_chart(labels, sizes)
            st.plotly_chart(fig)
        elif graph == "Histogramme":
            if pd.api.types.is_numeric_dtype(filtered_data[selected_measure]):
                fig = create_plotly_histogram(values)
                st.plotly_chart(fig)
            else:
                st.warning(
                    "L'histogramme n'est disponible que pour les variables numériques."
                )
        elif graph == "Ligne":
            fig = create_plotly_line_chart(labels, sizes)
            st.plotly_chart(fig)


DPE_COLORS = {
    "A": "#2e7d32",
    "B": "#66bb6a",
    "C": "#c0ca33",
    "D": "#fdd835",
    "E": "#fb8c00",
    "F": "#e53935",
    "G": "#8e0000",
}
def ajouter_legende(m):
    lignes = "".join(
        f'<div style="margin:2px 0;">'
        f'<span style="display:inline-block;width:12px;height:12px;border-radius:50%;'
        f'background:{couleur};margin-right:6px;"></span>{etiquette}</div>'
        for etiquette, couleur in DPE_COLORS.items()
    )
    legende = f"""
    <div style="position:fixed; bottom:30px; left:30px; z-index:9999;
                background:white; padding:8px 12px; border:1px solid #999;
                border-radius:6px; font-size:13px; color:#222;
                box-shadow:0 1px 4px rgba(0,0,0,0.3);">
        <b>Étiquette DPE</b>
        {lignes}
    </div>
    """
    m.get_root().html.add_child(folium.Element(legende))

@st.cache_resource(show_spinner="Construction de la carte...")
def build_map(points):
    m = folium.Map(
        location=[points["lat"].mean(), points["lon"].mean()],
        zoom_start=10,
        prefer_canvas=True,  # dessine sur un canvas au lieu de milliers d'éléments HTML
    )
    for lat, lon, etiq in zip(points["lat"], points["lon"], points["Etiquette_DPE"]):
        folium.CircleMarker(
            location=[lat, lon],
            radius=4,
            color=DPE_COLORS.get(etiq, "#757575"),
            fill=True,
            fill_opacity=0.8,
            weight=0,
            tooltip=f"Étiquette DPE : {etiq}",
        ).add_to(m)
    ajouter_legende(m)
    return m


def afficher_carte(data):
    st.title("Carte des étiquettes DPE")

    # Seules les 3 colonnes utiles sont gardées (cache plus léger)
    points = data[["lat", "lon", "Etiquette_DPE"]].dropna(subset=["lat", "lon"])

    if st.toggle("Afficher la carte (peut prendre quelques secondes)", value=False):
        m = build_map(points)
        st_folium(m, height=600, use_container_width=True, returned_objects=[])