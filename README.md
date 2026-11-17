# M2 Enedis

Cette application permet d’analyser et de prédire le Diagnostic de Performance Énergétique (DPE) et la consommation énergétique des logements situés dans le Rhône (69).
Elle utilise des modèles d’apprentissage automatique pour estimer l’étiquette DPE et la consommation énergétique en fonction des caractéristiques du logement.

## 🌐 Démo en ligne

L'application est déployée en ligne, vous pouvez l'essayer [ici](https://enedisprediction-egqsypsddapyezqfkoa3m5.streamlit.app/).

> ⏳ L'API est hébergée sur l'offre gratuite de Render et se met en veille après environ 15 minutes d'inactivité. La première prédiction avec l'API peut donc prendre 30 à 60 secondes.

## Fonctionnalités

- **Accueil** : Présentation de l'application et de ses fonctionnalités.
- **Contexte** : Permet d'explorer les données du projet et d'obtenir de nouvelles données en faisant appel à l'API.
- **Analyse** : Permet de suivre les différents KPI et de visualiser les données à l'aide de divers graphiques ainsi qu'une carte de géolocalisation.
- **Prédiction Locale** : Permet de réaliser des prédictions spécifiques à un logement en fonction de ses caractéristiques locales, en fournissant une estimation personnalisée du Diagnostic de Performance Énergétique (DPE) et de la consommation énergétique.
- **Prédiction avec API** : Permet de réaliser des prédictions en utilisant l'API pour obtenir des estimations automatisées du Diagnostic de Performance Énergétique (DPE) et de la consommation énergétique à partir des caractéristiques des logements.

## ☁️ Déploiement

L'application est déployée en deux services distincts :

| Composant | Plateforme | Détails |
|-----------|------------|---------|
| **API** (FastAPI, `script/api.py`) | [Render](https://render.com) | Construite avec `Dockerfile.api` (offre gratuite) |
| **Interface** (Streamlit, `script/MyApp.py`) | [Streamlit Community Cloud](https://streamlit.io/cloud) | Déployée directement depuis le dépôt |

Les deux services se redéploient automatiquement à chaque `push` sur la branche `main`.

L'interface trouve l'API grâce au paramètre `API_URL`, lu dans cet ordre :

1. la variable d'environnement `API_URL`
2. le secret Streamlit `API_URL` (utilisé sur Streamlit Cloud)
3. une valeur par défaut : `http://127.0.0.1:8001`

## Prérequis

- Python 3.9 ou supérieur (3.12 recommandé)
- `pip` pour installer les dépendances

## Installation

1. Clonez le dépôt :

    ```bash
    git clone https://github.com/Linn2d/Enedis_prediction.git
    cd Enedis_prediction
    ```

2. Créez et activez un environnement virtuel (recommandé) :

    ```bash
    python -m venv .venv
    # Windows (cmd)
    .venv\Scripts\activate.bat
    # Mac / Linux
    source .venv/bin/activate
    ```

3. Installez les dépendances :

    ```bash
    pip install -r script/requirements.txt
    pip install uvicorn fastapi
    ```

## Utilisation en local

1. Assurez-vous que les fichiers de modèles suivants sont bien présents dans le dossier `models/` pour la prédiction locale :

- **etiquette_knn_model.pkl**
- **etiquette_arbre_de_decision_model.pkl**
- **etiquette_random_forest_model.pkl**
- **consommation_xgboost_model.pkl**
- **consommation_arbre_de_decision_model.pkl**
- **consommation_random_forest.pkl**

Si ces fichiers sont manquants, exécutez le notebook `script/create_and_save_model.ipynb` pour les générer.

2. Lancez l'API dans un premier terminal :

    ```bash
    cd script
    python -m uvicorn api:app --port 8001
    ```

3. Lancez l'application Streamlit dans un second terminal (avec l'environnement virtuel activé) :

    ```bash
    cd script
    python -m streamlit run MyApp.py
    ```

4. Ouvrez votre navigateur et accédez à l'URL suivante :

    ```
    http://localhost:8501
    ```

> Les versions de `scikit-learn` (1.5.2) et de `xgboost` sont fixées, car les modèles enregistrés ne se rechargent correctement qu'avec les versions utilisées pour les entraîner.

## Auteurs

- [Lansana CISSE](https://github.com/lansanacisse)
- [Quentin Lim](https://github.com/QL2111)
- [Linh Nhi LE DINH](https://github.com/Linn2d)

## Liens

- [Vidéo demo](https://www.canva.com/design/DAGWCCn4eGE/Yi-rUdOqfwgIEOLZ5MxKiQ/watch?utm_content=DAGWCCn4eGE&utm_campaign=designshare&utm_medium=link&utm_source=editor)
- [OpenData-InfoClimat(température)](https://www.infoclimat.fr/opendata/)
- [ADEME DPE Logements existants](https://data.ademe.fr/datasets/dpe-v2-logements-existants/api-doc)
- [ADEME DPE Logements neufs](https://data.ademe.fr/datasets/dpe-v2-logements-neufs)
