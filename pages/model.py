import streamlit as st
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import requests
import folium
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from datetime import timedelta
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest
from datetime import date
from datetime import timedelta
import google.auth
from datetime import datetime
from datetime import date
from sklearn.preprocessing import StandardScaler
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')
st.set_option('deprecation.showPyplotGlobalUse', False)


# Fonction pour récupérer les données depuis Google Analytics
def get_google_analytics_data(property_id, start_date, end_date):
    # Chemin vers le fichier de clé JSON
    KEY_PATH = "google_analytics_api_access_keys.json"
    # Authentification
    credentials, project = google.auth.load_credentials_from_file(KEY_PATH)
    # Créer un client GA4
    client = BetaAnalyticsDataClient(credentials=credentials)

    # Configuration de la requête
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[
            Dimension(name="date")
        ],
        metrics=[
            Metric(name="averageSessionDuration"),
            Metric(name="screenPageViews"),
            Metric(name="bounceRate"),
            Metric(name="transactions"),
        ],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],  
    )

    # Exécution de la requête
    response = client.run_report(request)

    # Extraction des données de la réponse
    rows = []
    for row in response.rows:
        rows.append([dimension_value.value for dimension_value in row.dimension_values] + 
                    [metric_value.value for metric_value in row.metric_values])

    # Création du DataFrame pandas
    columns = ['date', 'averageSessionDuration', 'screenPageViews', 'bounceRate', 'transactions']
    data = pd.DataFrame(rows, columns=columns)

    # Conversion des colonnes en types appropriés
    data['averageSessionDuration'] = data['averageSessionDuration'].astype(float)
    data['screenPageViews'] = data['screenPageViews'].astype(int)
    data['bounceRate'] = data['bounceRate'].astype(float)
    data['transactions'] = data['transactions'].astype(int)

    return data

# Affichage de l'application Streamlit

st.title("Application Google Analytics")

    # Sidebar pour la sélection de la plage de dates
st.sidebar.header("Sélection de la Plage de Dates")
date_debut = st.sidebar.date_input("Date de début", datetime.now().date() - pd.to_timedelta("30day"))
date_fin = st.sidebar.date_input("Date de fin", datetime.now().date())

    # Récupération des données Google Analytics
data = get_google_analytics_data(property_id='293700220', start_date=str(date_debut), end_date=str(date_fin))

    # Affichage des données
st.subheader("Données Google Analytics")
st.write(data.head(10))
# Sélection des colonnes pertinentes
features = data[['averageSessionDuration', 'screenPageViews', 'bounceRate', 'transactions']]
# Remplacement des valeurs manquantes par la moyenne de la colonne
features.fillna(features.mean(), inplace=True)
# Standardisation des données
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)
# Détermination du nombre optimal de clusters avec la méthode du coude
sse = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_features)
    sse.append(kmeans.inertia_)
plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), sse, '-o')
plt.xlabel('Nombre de clusters')
plt.ylabel('SSE')
plt.title('Méthode du coude')
st.pyplot()
# Application de K-Means pour la segmentation (choix de 4 clusters par exemple)
kmeans = KMeans(n_clusters=4, random_state=42)
kmeans.fit(scaled_features)
# Ajout des labels de clusters au DataFrame original
data['cluster'] = kmeans.labels_
st.write(data)
# Visualisation des clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(x=scaled_features[:, 0], y=scaled_features[:, 1], hue=data['cluster'], palette='viridis')
plt.xlabel('Durée moyenne de la session (standardisée)')
plt.ylabel('Pages vues (standardisées)')
plt.title('Visualisation des clusters')
st.pyplot()



# Chemin vers le fichier de clé JSON
KEY_PATH = "google_analytics_api_access_keys.json"

# Authentification
credentials, project = google.auth.load_credentials_from_file(KEY_PATH)

# Créer un client GA4
client = BetaAnalyticsDataClient(credentials=credentials)

# Paramètres de la requête
property_id = '293700220'  # Remplacez par l'ID de votre propriété GA4


# Définir les dates de début et de fin pour la plage de dates
date_debut = pd.to_datetime('2023-01-01')  # Exemple de date de début
date_fin = pd.to_datetime('2023-12-31')    # Exemple de date de fin
# La requete pour recuperer les pays par la durée d'engagement
request = RunReportRequest(
    property=f'properties/{property_id}',
    dimensions=[Dimension(name='city')],
    metrics=[Metric(name='userEngagementDuration'), Metric(name='activeUsers')],
        date_ranges=[DateRange(start_date=date_debut.strftime("%Y-%m-%d"), end_date=date_fin.strftime("%Y-%m-%d"))], )

    # Exécuter la requête
response = client.run_report(request)

    # Créer une liste pour stocker les données
data2 = []

    # Extraire les données de la réponse et les stocker dans la liste
for row in response.rows:
    city = row.dimension_values[0].value
    engagement_duration = float(row.metric_values[0].value)  # userEngagementDuration
    active_users = int(row.metric_values[1].value)  # activeUsers
        
        # Calculer la durée d'engagement moyenne
    average_engagement_time = engagement_duration / active_users if active_users > 0 else 0

    data2.append({
        'city': city,
        'averageEngagementTime': average_engagement_time  # En secondes
        })

    # Convertir la liste en DataFrame pandas
temps_engagement_by_city = pd.DataFrame(data2)

# Préparation des données
X = temps_engagement_by_city.drop(['averageEngagementTime'], axis=1)  # toutes les caractéristiques sauf le taux d'engagement
y_regression = temps_engagement_by_city['averageEngagementTime']  # taux d'engagement

# Encodage One-Hot sur la colonne 'city'
X_encoded = pd.get_dummies(X, columns=['city'])

# Division des données en ensembles d'entraînement et de test
X_train, X_test, y_train_regression, y_test_regression = train_test_split(X_encoded, y_regression, test_size=0.2, random_state=42)

# Modèle de régression pour prédire le taux d'engagement
regressor = LinearRegression()
regressor.fit(X_train, y_train_regression)
predictions_regression = regressor.predict(X_test)
mse = mean_squared_error(y_test_regression, predictions_regression)

st.write(f"MSE pour la régression : {mse}")

# Prédiction avec le modèle
predictions_regression = regressor.predict(X_test)

# Créer un DataFrame pour les prédictions
df_predictions = pd.DataFrame(predictions_regression, columns=['Predicted Engagement Time'])

# Afficher les prédictions sur l'interface Streamlit
st.write(df_predictions)

# Définir les dates de début et de fin pour la plage de dates
date_debut = pd.to_datetime('2023-01-01')  # Exemple de date de début
date_fin = pd.to_datetime('2023-12-31')    # Exemple de date de fin

# Récupérer les données GA4
request = RunReportRequest(
    property=f'properties/{property_id}',
    dimensions=[Dimension(name='city')],
    metrics=[Metric(name='activeUsers')],
    date_ranges=[DateRange(start_date=date_debut.strftime("%Y-%m-%d"), end_date=date_fin.strftime("%Y-%m-%d"))],
)

# Exécuter la requête
response = client.run_report(request)

# Créer une liste pour stocker les données
data1 = []

# Extraire les données de la réponse et les stocker dans la liste
for row in response.rows:
    data1.append({
        'city': row.dimension_values[0].value,
        'activeUsers': int(row.metric_values[0].value)  # Convertir en entier
    })

# Convertir la liste en DataFrame pandas
nbres_users_by_city = pd.DataFrame(data1)

# Filtrer les 100 premières villes avec le plus d'utilisateurs actifs
top_100_cities = nbres_users_by_city.nlargest(100, 'activeUsers')

# Préparation des données pour le modèle
# Ici, nous utilisons uniquement les villes comme caractéristiques car nous n'avons pas d'autres dimensions

# Encodage des villes
X = pd.get_dummies(top_100_cities['city'])

# Les cibles
y = top_100_cities['activeUsers']

# Division des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Création du modèle de régression linéaire
model = LinearRegression()

# Entraînement du modèle
model.fit(X_train, y_train)

# Prédiction sur l'ensemble de test
y_pred = model.predict(X_test)

# Calcul de l'erreur quadratique moyenne
mse = mean_squared_error(y_test, y_pred)

# Affichage des résultats dans Streamlit
print('Erreur quadratique moyenne:', mse)

# Faire des prédictions pour les 100 villes
top_100_cities['predictedActiveUsers'] = model.predict(X)

# Trier les villes par nombre d'utilisateurs actifs prédit
top_100_cities_sorted = top_100_cities.sort_values(by='predictedActiveUsers', ascending=False)

st.write(top_100_cities_sorted[['city', 'predictedActiveUsers']])

