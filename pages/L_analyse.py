import streamlit as st
import numpy as np
import pandas as pd
import os
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import google.auth
from datetime import datetime
from datetime import date
from datetime import timedelta
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest
from google.analytics.data_v1beta.types import OrderBy
from datetime import date
from datetime import timedelta
import collections



# _ nombre d'utilisateur actif par ville
# _ le temps d'engagement par ville
# _ l'hystogramme des 5 meilleurs villes aillant le plus d'utilisateurs actifs.
# _ l'hystogramme des 5 dernieres villes aillant le moins d'utilisateurs actifs.
#_ diagramme circulaire du temps d'engagement par ville 

# statistique par trafic
# _ diagramme des 10 pages les plus visiter
# _ diagramme des 10 pages les moins visités

# Chemin vers le fichier de clé JSON
KEY_PATH = "google_analytics_api_access_keys.json"
# Authentification
credentials, project = google.auth.load_credentials_from_file(KEY_PATH)
# Créer un client GA4
client = BetaAnalyticsDataClient(credentials=credentials)
# Paramètres de la requête l'ID de votre propriété GA4
property_id = '293700220'




# le titre de la page data
st.header('LES DONNEES  sur GA4')


# Widgets de sélection de date dans la barre latérale
st.sidebar.header("Sélection de la Plage de Dates")
date_debut = st.sidebar.date_input("Date de début", datetime.now().date() - pd.to_timedelta("30day"))
date_fin = st.sidebar.date_input("Date de fin", datetime.now().date())




def display_histograms(data, dimension_col, metric_col, dimension_name, top_n, bottom_n, min_users):
    if not isinstance(data, pd.DataFrame):
        st.error("Les données fournies ne sont pas sous forme de DataFrame.")
        return

    # Supprimer les lignes où le nombre d'utilisateurs actifs est inférieur au seuil minimal
    data = data[data[metric_col] > min_users]

    # Trier les données par nombre d'utilisateurs actifs
    sorted_data = data.sort_values(by=metric_col, ascending=False)

    # Sélectionner les top_n et bottom_n
    top_data = sorted_data.head(top_n)
    bottom_data = sorted_data.tail(bottom_n)

    # Créer deux colonnes pour les histogrammes
    col1, col2 = st.columns(2)

    # Afficher l'histogramme des top_n dans la première colonne
    with col1:
        st.subheader(f"Top {top_n} {dimension_name} ayant le plus d'utilisateurs actifs")
        fig, ax = plt.subplots()
        ax.bar(top_data[dimension_col], top_data[metric_col], color='green')
        ax.set_xlabel(dimension_col.capitalize())
        ax.set_ylabel('Nombre d\'utilisateurs actifs')
        ax.set_title(f'Top {top_n} {dimension_name}')
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # Afficher l'histogramme des bottom_n dans la deuxième colonne
    with col2:
        st.subheader(f"Bottom {bottom_n} {dimension_name} ayant le moins d'utilisateurs actifs")
        fig, ax = plt.subplots()
        ax.bar(bottom_data[dimension_col], bottom_data[metric_col], color='red')
        ax.set_xlabel(dimension_col.capitalize())
        ax.set_ylabel('Nombre d\'utilisateurs actifs')
        ax.set_title(f'Bottom {bottom_n} {dimension_name}')
        plt.xticks(rotation=45)
        st.pyplot(fig)

# fonction d'affichage de donnée sur l'application streamlit 
def display_data_side_by_side(df1, df2, dimension_name, min_users, min_engagement):
    # Widgets interactifs pour choisir les seuils de suppression
    min_users_widget = st.slider("Supprimer les lignes avec utilisateurs <= ", min_value=0, max_value=int(df1['activeUsers'].max()), value=min_users)
    min_engagement_widget = st.slider("Supprimer les lignes avec engagement <= ", min_value=0, max_value=int(df2['averageEngagementTime'].max()), value=min_engagement)
    
    # Filtrer les données en fonction des widgets interactifs
    df1_filtered = df1[df1['activeUsers'] > min_users_widget]
    df2_filtered = df2[df2['averageEngagementTime'] > min_engagement_widget]
    
    # Afficher les DataFrames côte à côte
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"utilisateurs par {dimension_name}")
        st.write(df1_filtered)
    
    with col2:
        st.subheader(f"Engagement par {dimension_name}")
        st.write(df2_filtered)

# fonction du calcul de la boite à Moustache
def clean_and_visualize_data(data, column_name):
    # Suppression des utilisateurs inférieurs à 5
    data_cleaned = data[data['activeUsers'] > 5]
    
    # Nettoyage des données
    # Suppression des valeurs aberrantes
    Q1 = data_cleaned[column_name].quantile(0.25)
    Q3 = data_cleaned[column_name].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    data_cleaned = data_cleaned[(data_cleaned[column_name] >= lower_bound) & (data_cleaned[column_name] <= upper_bound)]
    
    # Suppression des valeurs manquantes
    data_cleaned = data_cleaned.dropna(subset=[column_name])
    
    # Utilisation des colonnes Streamlit pour afficher côte à côte
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Description statistique des données")
        st.write(data_cleaned.describe())
    
    with col2:
        st.subheader("Boîte à moustaches")
        fig, ax = plt.subplots()
        ax.boxplot(data_cleaned[column_name])
        ax.set_xlabel(column_name)
        st.pyplot(fig)


def plot_top_and_bottom_pages(data, column_name):
    # Vérification de l'existence des colonnes
    if 'pagePath' not in data.columns or column_name not in data.columns:
        st.error(f"Les colonnes 'pagePath' et '{column_name}' doivent exister dans les données.")
        return

    # Filtrer les 10 pages les plus visitées
    top_pages = data.nlargest(10, column_name)
    
    # Filtrer les 10 pages les moins visitées
    bottom_pages = data.nsmallest(10, column_name)
    
    # Créer un diagramme à barres pour les 10 pages les plus visitées
    fig_top = px.bar(top_pages, x='pagePath', y=column_name, title='Top 10 Pages les Plus Visitées')
    
    # Créer un diagramme à barres pour les 10 pages les moins visitées
    fig_bottom = px.bar(bottom_pages, x='pagePath', y=column_name, title='Top 10 Pages les Moins Visitées')
    
    # Afficher les graphiques côte à côte
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(fig_top, use_container_width=True)
    
    with col2:
        st.plotly_chart(fig_bottom, use_container_width=True)



def generate_active_users_report(property_id):
    def format_report(request):
        response = client.run_report(request)
        
        # Row index
        row_index_names = [header.name for header in response.dimension_headers]
        row_header = []
        for i in range(len(row_index_names)):
            row_header.append([row.dimension_values[i].value for row in response.rows])

        row_index_named = pd.MultiIndex.from_arrays(np.array(row_header), names=np.array(row_index_names))
        # Row flat data
        metric_names = [header.name for header in response.metric_headers]
        data_values = []
        for i in range(len(metric_names)):
            data_values.append([row.metric_values[i].value for row in response.rows])

        output = pd.DataFrame(data=np.transpose(np.array(data_values, dtype='f')), 
                              index=row_index_named, columns=metric_names)
        return output

    request = RunReportRequest(
        property='properties/' + property_id,
        dimensions=[Dimension(name="month"), 
                    Dimension(name="sessionMedium")],
        metrics=[Metric(name="averageSessionDuration"), 
                 Metric(name="activeUsers")],
        order_bys=[OrderBy(dimension={'dimension_name': 'month'}),
                   OrderBy(dimension={'dimension_name': 'sessionMedium'})],
        date_ranges=[DateRange(start_date="2020-06-01", end_date="today")],
    )

    output_df = format_report(request)

    # Création du tableau pivot
    monthly_users_pivot = pd.pivot_table(output_df, 
                                         columns=['sessionMedium'], 
                                         index=['month'], 
                                         values=['activeUsers'], 
                                         aggfunc='sum',
                                         fill_value=0).droplevel(0, axis=1)

    # Configuration du thème Seaborn
    sns.set_theme()

    # Création du graphique
    fig, ax = plt.subplots(figsize=(7, 5))
    monthly_users_pivot.plot.bar(y=['(none)', 'organic', 'referral', '(not set)'], 
                                 stacked=True, 
                                 colormap='Dark2', 
                                 ax=ax)
    ax.legend(title='User Medium', bbox_to_anchor=(1.05, 0.5))
    ax.set_title('Active Users by Month', fontsize=15)
    ax.set_xlabel('Month')
    ax.set_ylabel('Active Users')

    # Affichage dans Streamlit
    st.title("Active Users by Month Report")
    st.pyplot(fig)


def calc_start_date(end_date, no_days):
    if end_date == "today":
        start_date = date.today() - timedelta(days=no_days)
    else:
        start_date = date.fromisoformat(end_date) - timedelta(days=no_days)
        
    return start_date.strftime("%Y-%m-%d")


def format_report(request, client):
    response = client.run_report(request)
    
    # Row index
    row_index_names = [header.name for header in response.dimension_headers]
    row_header = []
    for i in range(len(row_index_names)):
        row_header.append([row.dimension_values[i].value for row in response.rows])

    row_index_named = pd.MultiIndex.from_arrays(np.array(row_header), names = np.array(row_index_names))
    # Row flat data
    metric_names = [header.name for header in response.metric_headers]
    data_values = []
    for i in range(len(metric_names)):
        data_values.append([row.metric_values[i].value for row in response.rows])

    output = pd.DataFrame(data = np.transpose(np.array(data_values, dtype = 'f')), 
                          index = row_index_named, columns = metric_names)
    return output


def produce_traffic_report(end_date, no_days, property_id=property_id, client=client):
    daily_traffic_request = RunReportRequest(
            property='properties/'+property_id,
            dimensions=[Dimension(name="date"), 
                        Dimension(name="sessionMedium")],
            metrics=[Metric(name="activeUsers")],
            order_bys=[OrderBy(dimension={'dimension_name': 'date'}),
                      OrderBy(dimension={'dimension_name': 'sessionMedium'})],
            date_ranges=[DateRange(start_date=calc_start_date(end_date, no_days), end_date=end_date)],
        )

    daily_traffic = format_report(daily_traffic_request, client).reset_index()
    active_users_pivot = pd.pivot_table(daily_traffic, 
                                        columns=['sessionMedium'], 
                                        index=['date'], 
                                        values=['activeUsers'], 
                                        aggfunc='sum',
                                        fill_value=0).droplevel(0, axis=1)
    active_users_pivot.index = active_users_pivot.index.str.slice(start=4)
    
    # Produire les graphiques en secteurs et en ligne
    fig, (axs1, axs2) = plt.subplots(1, 2, figsize=(14, 4), gridspec_kw={'width_ratios': [1, 2]})
    pie_data = daily_traffic.groupby(by=['sessionMedium']).sum().sort_values(by=['activeUsers'], ascending=False)
    
    # Modifier l'index name
    pie_data.index.name = 'sessionMedium'
    
    pie_data.plot.pie(ax=axs1,
                      colormap='Dark2',
                      y='activeUsers',  # Utilisez directement une chaîne de caractères ici
                      title='Active Users by Medium',
                      legend=False,
                      label=False,
                      startangle=0,
                      autopct=lambda p: f'{p:.0f}%').set_ylabel('')

    active_users_pivot.plot.line(ax=axs2,
                                 colormap='Dark2',
                                 title='Active Users by Day')

    axs2.legend(title='User Medium', bbox_to_anchor=(1.05, 0.6))

    return fig, active_users_pivot


def produce_top_pages_report(end_date, no_days, property_id=property_id, client=client):
    page_users_request = RunReportRequest(
            property='properties/'+property_id,
            dimensions=[Dimension(name="pagePath")],
            metrics=[Metric(name="activeUsers")],
            order_bys=[OrderBy(metric={'metric_name': 'activeUsers'}, desc=True)],
            date_ranges=[DateRange(start_date=calc_start_date(end_date, no_days), end_date=end_date)],
        )

    page_users_table = format_report(page_users_request, client)
    page_users_table['activeUsers'] = page_users_table['activeUsers'].astype('int')
    
    st.subheader('Top 10 Visited Pages')
    st.dataframe(page_users_table.head(10))








st.subheader('L_ANALYSE DES DONNEES')

menus = st.sidebar.radio("LES STATISTIQUES", ('statistique par pays', 'statistique par ville', 'statistique par trafic'))
# Logique pour afficher les données en fonction du choix de menu
if menus == 'statistique par pays':
    request = RunReportRequest(
        property=f'properties/{property_id}',
        dimensions=[Dimension(name='country')],
        metrics=[Metric(name='activeUsers')],
        date_ranges=[DateRange(start_date=date_debut.strftime("%Y-%m-%d"), end_date=date_fin.strftime("%Y-%m-%d"))],)

    # Exécuter la requête
    response = client.run_report(request)

    # Créer une liste pour stocker les données
    data = []

    # Extraire les données de la réponse et les stocker dans la liste
    for row in response.rows:
        data.append({
            'country': row.dimension_values[0].value,
            'activeUsers': int(row.metric_values[0].value)  # Convertir en entier
        })

    # Convertir la liste en DataFrame pandas
    nbres_users_by_country = pd.DataFrame(data)
    

    # La requete pour recuperer les pays par la durée d'engagement
    request = RunReportRequest(
        property=f'properties/{property_id}',
        dimensions=[Dimension(name='country')],
        metrics=[Metric(name='userEngagementDuration'), Metric(name='activeUsers')],
        date_ranges=[DateRange(start_date=date_debut.strftime("%Y-%m-%d"), end_date=date_fin.strftime("%Y-%m-%d"))], )

    # Exécuter la requête
    response = client.run_report(request)

    # Créer une liste pour stocker les données
    data = []

    # Extraire les données de la réponse et les stocker dans la liste
    for row in response.rows:
        country = row.dimension_values[0].value
        engagement_duration = float(row.metric_values[0].value)  # userEngagementDuration
        active_users = int(row.metric_values[1].value)  # activeUsers
        
        # Calculer la durée d'engagement moyenne
        average_engagement_time = engagement_duration / active_users if active_users > 0 else 0

        data.append({
            'country': country,
            'averageEngagementTime': average_engagement_time  # En secondes
        })

    # Convertir la liste en DataFrame pandas
    temps_engagement_by_country = pd.DataFrame(data)

    # Afficher les DataFrames côte à côte de manière interactive
    display_data_side_by_side(nbres_users_by_country, temps_engagement_by_country, dimension_name="pays", min_users=5, min_engagement=10)
    

    # Statistiques descriptives
    clean_and_visualize_data(nbres_users_by_country,'activeUsers')
    # Widgets interactifs pour choisir le nombre de top et bottom éléments
    top_n = st.slider("Nombre de top éléments à afficher", min_value=1, max_value=20, value=5)
    bottom_n = st.slider("Nombre de bottom éléments à afficher", min_value=1, max_value=20, value=5)
        
    # Widget interactif pour choisir le seuil minimal d'utilisateurs actifs
    min_users = st.slider("Seuil minimal d'utilisateurs actifs", min_value=0, max_value=100, value=5)

    display_histograms(nbres_users_by_country, 'country', 'activeUsers','Pays',top_n,bottom_n,min_users)

      
if menus == 'statistique par ville':

    request = RunReportRequest(
        property=f'properties/{property_id}',
        dimensions=[Dimension(name='city')],
        metrics=[Metric(name='activeUsers')],
        date_ranges=[DateRange(start_date=date_debut.strftime("%Y-%m-%d"), end_date=date_fin.strftime("%Y-%m-%d"))],)

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
            'country': city,
            'averageEngagementTime': average_engagement_time  # En secondes
        })

    # Convertir la liste en DataFrame pandas
    temps_engagement_by_city = pd.DataFrame(data2)

    # Afficher les DataFrames côte à côte de manière interactive
    display_data_side_by_side(nbres_users_by_city, temps_engagement_by_city, dimension_name="ville", min_users=5, min_engagement=10)

     # Statistiques descriptives
    clean_and_visualize_data(nbres_users_by_city,'activeUsers')
    # Widgets interactifs pour choisir le nombre de top et bottom éléments
    top_n = st.slider("Nombre de top éléments à afficher", min_value=1, max_value=20, value=5)
    bottom_n = st.slider("Nombre de bottom éléments à afficher", min_value=1, max_value=20, value=5)
        
    # Widget interactif pour choisir le seuil minimal d'utilisateurs actifs
    min_users = st.slider("Seuil minimal d'utilisateurs actifs", min_value=0, max_value=100, value=5)

    display_histograms(nbres_users_by_city, 'city', 'activeUsers','Ville',top_n,bottom_n,min_users)




if menus == 'statistique par trafic':
    menuTrafic = st.sidebar.radio("LES TRAFICS", ('Sessions', 'Pages'))
    if menuTrafic == 'Sessions':
            # Requetes sur les 'Sessions' par utilisateur
        request = RunReportRequest(
            property=f'properties/{property_id}',
            dimensions=[Dimension(name='sessionMedium')],
            metrics=[Metric(name='activeUsers')],
            date_ranges=[DateRange(start_date=date_debut.strftime("%Y-%m-%d"), end_date=date_fin.strftime("%Y-%m-%d"))],)

    # Exécuter la requête
        response = client.run_report(request)

    # Créer une liste pour stocker les données
        data6 = []

    # Extraire les données de la réponse et les stocker dans la liste
        for row in response.rows:
            data6.append({
                'sessionMedium': row.dimension_values[0].value,
                'activeUsers': int(row.metric_values[0].value)  # Convertir en entier
            })

    # Convertir la liste en DataFrame pandas
        Sessions_view = pd.DataFrame(data6)
    # La requete pour recuperer les sessionMedium par la durée d'engagement
        request = RunReportRequest(
            property=f'properties/{property_id}',
            dimensions=[Dimension(name='sessionMedium')],
            metrics=[Metric(name='userEngagementDuration'), Metric(name='activeUsers')],
            date_ranges=[DateRange(start_date=date_debut.strftime("%Y-%m-%d"), end_date=date_fin.strftime("%Y-%m-%d"))], )

    # Exécuter la requête
        response = client.run_report(request)

    # Créer une liste pour stocker les données
        data7 = []

    # Extraire les données de la réponse et les stocker dans la liste
        for row in response.rows:
            city = row.dimension_values[0].value
            engagement_duration = float(row.metric_values[0].value)  # userEngagementDuration
            active_users = int(row.metric_values[1].value)  # activeUsers
        
        # Calculer la durée d'engagement moyenne
            average_engagement_time = engagement_duration / active_users if active_users > 0 else 0

            data7.append({
                'pagePath': city,
                'averageEngagementTime': average_engagement_time  # En secondes
            })

    # Convertir la liste en DataFrame pandas
        temps_engagement_by_sessionMedium = pd.DataFrame(data7)

    # Afficher le DataFrame dans Streamlit
        # Afficher les DataFrames de manière interactive
        display_data_side_by_side(Sessions_view, temps_engagement_by_sessionMedium, dimension_name="session", min_users=5, min_engagement=10)
        # Statistiques descriptives
        clean_and_visualize_data(Sessions_view,'activeUsers')
        generate_active_users_report(property_id)
        
        ## Report dates
        end_date = 'today' ## ("today" or "yyyy-mm-dd")
        no_days = 90
        # Appel à la fonction pour produire le rapport de trafic
        fig, active_users_pivot = produce_traffic_report(end_date, no_days, property_id, client)
        # Affichage des graphiques dans l'application Streamlit
        st.pyplot(fig)

        # Affichage du tableau de données dans l'application Streamlit
        st.write("Tableau de données :")
        st.write(active_users_pivot)
       



        
    if menuTrafic == 'Pages':
        # La requete pour recuperer les pagePath par la durée d'engagement
        request = RunReportRequest(
            property=f'properties/{property_id}',
            dimensions=[Dimension(name='pagePath')],
            metrics=[Metric(name='userEngagementDuration'), Metric(name='activeUsers')],
            date_ranges=[DateRange(start_date=date_debut.strftime("%Y-%m-%d"), end_date=date_fin.strftime("%Y-%m-%d"))], )

    # Exécuter la requête
        response = client.run_report(request)

    # Créer une liste pour stocker les données
        data3 = []

    # Extraire les données de la réponse et les stocker dans la liste
        for row in response.rows:
            city = row.dimension_values[0].value
            engagement_duration = float(row.metric_values[0].value)  # userEngagementDuration
            active_users = int(row.metric_values[1].value)  # activeUsers
        
        # Calculer la durée d'engagement moyenne
            average_engagement_time = engagement_duration / active_users if active_users > 0 else 0

            data3.append({
                'pagePath': city,
                'averageEngagementTime': average_engagement_time  # En secondes
            })

    # Convertir la liste en DataFrame pandas
        temps_engagement_by_pagePath = pd.DataFrame(data3)
        # Requetes sur les pages vue et les scroll
        request = RunReportRequest(
            property=f'properties/{property_id}',
            dimensions=[Dimension(name='pagePath')],
            metrics=[Metric(name='screenPageViews')],
            date_ranges=[DateRange(start_date=date_debut.strftime("%Y-%m-%d"), end_date=date_fin.strftime("%Y-%m-%d"))],)

    # Exécuter la requête
        response = client.run_report(request)

    # Créer une liste pour stocker les données
        data4 = []

    # Extraire les données de la réponse et les stocker dans la liste
        for row in response.rows:
            data4.append({
                'pagePath': row.dimension_values[0].value,
                'screenPageViews': int(row.metric_values[0].value)  # Convertir en entier
            })

    # Convertir la liste en DataFrame pandas
        page_view = pd.DataFrame(data4)


    # Requetes sur Les pages vue par utilisateur
        request = RunReportRequest(
            property=f'properties/{property_id}',
            dimensions=[Dimension(name='pagePath')],
            metrics=[Metric(name='activeUsers')],
            date_ranges=[DateRange(start_date=date_debut.strftime("%Y-%m-%d"), end_date=date_fin.strftime("%Y-%m-%d"))],)

    # Exécuter la requête
        response = client.run_report(request)

    # Créer une liste pour stocker les données
        data5 = []

    # Extraire les données de la réponse et les stocker dans la liste
        for row in response.rows:
            data5.append({
                'pagePath': row.dimension_values[0].value,
                'activeUsers': int(row.metric_values[0].value)  # Convertir en entier
            })

    # Convertir la liste en DataFrame pandas
        users_view = pd.DataFrame(data5)

    # Afficher le DataFrame dans Streamlit
        display_data_side_by_side(users_view,temps_engagement_by_pagePath, dimension_name="Pages", min_users=5, min_engagement=10)
        # Statistiques descriptives
        clean_and_visualize_data(users_view,'activeUsers')
        # Utilisation
        end_date = 'today' ## ("today" or "yyyy-mm-dd")
        no_days = 90
        produce_top_pages_report(end_date, no_days, property_id, client)
        plot_top_and_bottom_pages(users_view,'activeUsers')
        
       
      






    
    








































