import streamlit as st
import numpy as np
import pandas as pd
import os
import matplotlib
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





# Chemin vers le fichier de clé JSON
KEY_PATH = "google_analytics_api_access_keys.json"
# Authentification
credentials, project = google.auth.load_credentials_from_file(KEY_PATH)
# Créer un client GA4
client = BetaAnalyticsDataClient(credentials=credentials)
# Paramètres de la requête l'ID de la propriété GA4
property_id = '293700220'




# le titre de la page data
st.header('LES DONNEES  sur GA4')


# Widgets de sélection de date dans la barre latérale
st.sidebar.header("Sélection de la Plage de Dates")
date_debut = st.sidebar.date_input("Date de début", datetime.now().date() - pd.to_timedelta("30day"))
date_fin = st.sidebar.date_input("Date de fin", datetime.now().date())




## Format Report - run_report method
def format_report(request):
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

menu = st.sidebar.selectbox("DATA", ('Pays', 'Villes', 'Pages Vues', 'Sessions', 'lesDimension'))



# Logique pour afficher les données en fonction du choix de menu
if menu == 'Pays':
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

    # Afficher le DataFrame dans Streamlit
    st.subheader('Le nombre d utilisateurs par pays')
    st.write(nbres_users_by_country)
        
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

    # Afficher le DataFrame dans Streamlit
    st.subheader('Le temps d engagement par pays')
    st.write(temps_engagement_by_country)


    request = RunReportRequest(
        property='properties/'+property_id,
        dimensions=[Dimension(name="month"), 
                    Dimension(name="country")],
        metrics=[Metric(name="averageSessionDuration"), 
                 Metric(name="activeUsers")],
        order_bys = [OrderBy(dimension = {'dimension_name': 'month'}),
                    OrderBy(dimension = {'dimension_name': 'country'})],
        date_ranges=[DateRange(start_date=date_debut.strftime("%Y-%m-%d"), end_date=date_fin.strftime("%Y-%m-%d"))], )

    pays_mois = format_report(request)
    # Afficher le DataFrame dans Streamlit
    st.subheader('Nombre d tilisateur des pays par mois')
    st.write(pays_mois)


    country_users_pivot = pd.pivot_table(pays_mois, 
                                        columns=['country'],  
                                        index=['month'], 
                                        values=['activeUsers'], 
                                        aggfunc = 'sum',
                                        fill_value=0).droplevel(0, axis=1)
    st.subheader('Nombre d tilisateur des pays regroupe  par mois')
    st.write(country_users_pivot)



        
if menu == 'Villes':

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

    # Afficher le DataFrame dans Streamlit
    st.subheader('Le nombre d utilisateurs par ville')
    st.write(nbres_users_by_city)
        
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

    # Afficher le DataFrame dans Streamlit
    st.subheader('Le temps d engagement par ville')
    st.write(temps_engagement_by_city)

    request = RunReportRequest(
        property='properties/'+property_id,
        dimensions=[Dimension(name="month"), 
                    Dimension(name="city")],
        metrics=[Metric(name="averageSessionDuration"), 
                 Metric(name="activeUsers")],
        order_bys = [OrderBy(dimension = {'dimension_name': 'month'}),
                    OrderBy(dimension = {'dimension_name': 'city'})],
       date_ranges=[DateRange(start_date=date_debut.strftime("%Y-%m-%d"), end_date=date_fin.strftime("%Y-%m-%d"))],)

    ville_mois = format_report(request)
    # Afficher le DataFrame dans Streamlit
    st.subheader('Nombre d tilisateur des villes par mois')
    st.write(ville_mois)


    city_users_pivot = pd.pivot_table(ville_mois, 
                                        columns=['city'],  
                                        index=['month'], 
                                        values=['activeUsers'], 
                                        aggfunc = 'sum',
                                        fill_value=0).droplevel(0, axis=1)
    st.subheader('Nombre d tilisateur des villes regroupe  par mois')
    st.write(city_users_pivot)



if menu == 'Pages Vues':

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

    # Afficher le DataFrame dans Streamlit
    st.subheader('Le temps d engagement par pagePath')
    st.write(temps_engagement_by_pagePath)



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

    # Afficher le DataFrame dans Streamlit
    st.subheader('Les pages vue par scroll ')
    st.write(page_view)



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
    st.subheader('Les pages vue par utilisateurs')
    st.write(users_view)




    # Requetes sur Les pages vue par utilisateurs et ville

    request = RunReportRequest(
        property='properties/'+property_id,
        dimensions=[Dimension(name="city"), 
                    Dimension(name="pagePath")],
        metrics=[Metric(name="averageSessionDuration"), 
                 Metric(name="activeUsers")],
        order_bys = [OrderBy(dimension = {'dimension_name': 'city'}),
                    OrderBy(dimension = {'dimension_name': 'pagePath'})],
       date_ranges=[DateRange(start_date=date_debut.strftime("%Y-%m-%d"), end_date=date_fin.strftime("%Y-%m-%d"))],)

    output_df = format_report(request)
    # Afficher le DataFrame dans Streamlit
    st.subheader('Pages Vues par utilisateurs en fonction de la ville')
    st.write(output_df)

   # Requetes sur Les pages vue par la somme de chaque ville
    monhtly_users_pivot = pd.pivot_table(output_df, 
                                     columns=['city'], 
                                     index=['pagePath'], 
                                     values=['activeUsers'], 
                                     aggfunc = 'sum',
                                     fill_value=0).droplevel(0, axis=1)
    st.subheader('Pages Vues par utilisateur regroupe par ville')
    st.write(monhtly_users_pivot)



     # Requetes sur Les pages vue par utilisateurs et pays

    request = RunReportRequest(
        property='properties/'+property_id,
        dimensions=[Dimension(name="country"), 
                    Dimension(name="pagePath")],
        metrics=[Metric(name="averageSessionDuration"), 
                 Metric(name="activeUsers")],
        order_bys = [OrderBy(dimension = {'dimension_name': 'country'}),
                    OrderBy(dimension = {'dimension_name': 'pagePath'})],
        date_ranges=[DateRange(start_date=date_debut.strftime("%Y-%m-%d"), end_date=date_fin.strftime("%Y-%m-%d"))], )

    output_df = format_report(request)
    # Afficher le DataFrame dans Streamlit
    st.subheader('Pages Vues par utilisateurs en fonction du pays')
    st.write(output_df)

   # Requetes sur Les pages vue par la somme de chaque pays
    monhtly_users_pivot = pd.pivot_table(output_df, 
                                     columns=['country'], 
                                     index=['pagePath'], 
                                     values=['activeUsers'], 
                                     aggfunc = 'sum',
                                     fill_value=0).droplevel(0, axis=1)
    st.subheader('Pages Vues par utilisateur regroupe par pays')
    st.write(monhtly_users_pivot)



if menu == 'Sessions':


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

    # Afficher le DataFrame dans Streamlit
    st.subheader('Les Sessions pas utilisateurs ')
    st.write(Sessions_view)


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
    st.subheader('Le temps d engagement par session')
    st.write(temps_engagement_by_sessionMedium)


    # Requetes sur les 'Sessions' par mois

    request = RunReportRequest(
        property='properties/'+property_id,
        dimensions=[Dimension(name="month"), 
                    Dimension(name="sessionMedium")],
        metrics=[Metric(name="averageSessionDuration"), 
                 Metric(name="activeUsers")],
        order_bys = [OrderBy(dimension = {'dimension_name': 'month'}),
                    OrderBy(dimension = {'dimension_name': 'sessionMedium'})],
        date_ranges=[DateRange(start_date=date_debut.strftime("%Y-%m-%d"), end_date=date_fin.strftime("%Y-%m-%d"))],)

    output_df = format_report(request)
    # Afficher le DataFrame dans Streamlit
    st.subheader('session par mois')
    st.write(output_df)



    # Requetes sur les 'Sessions' par utilisateurs et ville

    request = RunReportRequest(
        property='properties/'+property_id,
        dimensions=[Dimension(name="city"), 
                    Dimension(name="sessionMedium")],
        metrics=[Metric(name="averageSessionDuration"), 
                 Metric(name="activeUsers")],
        order_bys = [OrderBy(dimension = {'dimension_name': 'city'}),
                    OrderBy(dimension = {'dimension_name': 'sessionMedium'})],
       date_ranges=[DateRange(start_date=date_debut.strftime("%Y-%m-%d"), end_date=date_fin.strftime("%Y-%m-%d"))],)

    output_df = format_report(request)
    # Afficher le DataFrame dans Streamlit
    st.subheader('session par utilisateurs en fonction de la ville')
    st.write(output_df)

   # Requetes sur les 'Sessions' par la somme de chaque ville
    monhtly_users_pivot = pd.pivot_table(output_df, 
                                     columns=['sessionMedium'], 
                                     index=['city'], 
                                     values=['activeUsers'], 
                                     aggfunc = 'sum',
                                     fill_value=0).droplevel(0, axis=1)
    st.subheader('session par utilisateur regroupe par ville')
    st.write(monhtly_users_pivot)



     # Requetes sur les 'Sessions' par utilisateurs et pays

    request = RunReportRequest(
        property='properties/'+property_id,
        dimensions=[Dimension(name="country"), 
                    Dimension(name="sessionMedium")],
        metrics=[Metric(name="averageSessionDuration"), 
                 Metric(name="activeUsers")],
        order_bys = [OrderBy(dimension = {'dimension_name': 'country'}),
                    OrderBy(dimension = {'dimension_name': 'sessionMedium'})],
        date_ranges=[DateRange(start_date=date_debut.strftime("%Y-%m-%d"), end_date=date_fin.strftime("%Y-%m-%d"))], )

    output_df = format_report(request)
    # Afficher le DataFrame dans Streamlit
    st.subheader('session par utilisateurs en fonction du pays')
    st.write(output_df)

   # Requetes sur les 'Sessions' par la somme de chaque pays
    monhtly_users_pivot = pd.pivot_table(output_df, 
                                     columns=['sessionMedium'], 
                                     index=['country'], 
                                     values=['activeUsers'], 
                                     aggfunc = 'sum',
                                     fill_value=0).droplevel(0, axis=1)
    st.subheader('session par utilisateur regroupe par pays')
    st.write(monhtly_users_pivot)



if menu == 'lesDimension':
        # Définir les dimensions et les métriques que vous souhaitez récupérer
    dimensions = [
    #     Dimension(name='userPseudoId'),  # Utiliser userPseudoId à la place de clientId
        Dimension(name='country'),
        Dimension(name='city'),
        Dimension(name='sessionMedium'),
        Dimension(name='pagePath'),
        Dimension(name='operatingSystem'),
        Dimension(name='operatingSystemVersion')
    ]

    metrics = [
        Metric(name='sessions'),
        Metric(name='engagementRate'),
        Metric(name='userEngagementDuration'),
        Metric(name='activeUsers')
    ]

    request = RunReportRequest(
        property=f'properties/{property_id}',
        dimensions=dimensions,
        metrics=metrics,
    date_ranges=[DateRange(start_date=date_debut.strftime("%Y-%m-%d"), end_date=date_fin.strftime("%Y-%m-%d"))],)

    # Exécuter la requête
    response = client.run_report(request)

    # Créer une liste pour stocker les données
    data8 = []

    # Extraire les données de la réponse et les stocker dans la liste
    for row in response.rows:
        record = {dimension.name: row.dimension_values[idx].value for idx, dimension in enumerate(dimensions)}
        record.update({metric.name: float(row.metric_values[idx].value) for idx, metric in enumerate(metrics)})
        data8.append(record)

    # Convertir la liste en DataFrame pandas
    df = pd.DataFrame(data8)

    # Afficher le DataFrame dans Streamlit
    st.subheader('Toutes les dimension par metrics')
    st.write(df)





    
