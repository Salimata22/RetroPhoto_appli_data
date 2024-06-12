import streamlit as st

def documentation_analyse():
    st.title("Documentation de l'application")

    st.header("Analyse")
    st.write("""
    ## Description
    La page Analyse de l'application fournit des outils interactifs pour explorer et comprendre les données de Google Analytics 4 (GA4). 
    Elle permet aux utilisateurs de visualiser les données à l'aide de graphiques et de générer des statistiques descriptives pour mieux saisir les tendances et les comportements des utilisateurs.
    """)

    st.subheader("Fonctionnalités")

    st.write("""
    ### Histogramme des utilisateurs actifs
    **Objectif**: L'histogramme des utilisateurs actifs permet de visualiser la distribution du nombre d'utilisateurs actifs par ville.
    
    **Utilité**: Cette visualisation est utile pour identifier la fréquence des différentes valeurs d'utilisateurs actifs, ce qui peut aider à repérer les villes avec des niveaux d'activité exceptionnellement élevés ou bas.
    """)

    st.write("""
    ### Statistiques descriptives des utilisateurs actifs par ville
    **Objectif**: Les statistiques descriptives fournissent un résumé statistique des données d'utilisateurs actifs.
    
    **Utilité**: Ces statistiques comprennent des mesures telles que la moyenne, la médiane, l'écart-type, les valeurs minimales et maximales. 
    Elles aident à comprendre la dispersion et la tendance centrale des données, offrant ainsi une vue d'ensemble rapide et efficace des utilisateurs actifs par ville.
    """)

    st.write("""
    Les statistiques descriptives incluent :
    - **Count** : Le nombre total d'observations (villes) dans les données.
    - **Mean** : La moyenne du nombre d'utilisateurs actifs par ville.
    - **Standard Deviation (std)** : Une mesure de la dispersion des valeurs par rapport à la moyenne.
    - **Min** : La valeur minimale d'utilisateurs actifs.
    - **25% (1er quartile)** : Le 25ème percentile des utilisateurs actifs.
    - **50% (médiane)** : La valeur médiane, séparant la moitié inférieure des valeurs de la moitié supérieure.
    - **75% (3ème quartile)** : Le 75ème percentile des utilisateurs actifs.
    - **Max** : La valeur maximale d'utilisateurs actifs.
    """)

    st.write("""
    ### Bar chart des utilisateurs actifs par ville
    **Objectif**: Le bar chart présente le nombre d'utilisateurs actifs pour chaque ville sous forme de barres.
    
    **Utilité**: Ce graphique est particulièrement utile pour comparer le nombre d'utilisateurs actifs entre différentes villes. 
    Il met en évidence les villes avec le plus et le moins d'utilisateurs actifs, facilitant ainsi l'identification des principaux marchés ou des zones nécessitant une attention particulière.
    """)


def documentation_data():
    st.write("Cette application permet d'afficher les données de Google Analytics 4 (GA4) pour la  propriété rétro photo donnée. Vous pouvez sélectionner différentes plages de dates et visualiser les données en fonction de plusieurs dimensions et métriques.")
    
    st.header("Choix du Menu")
    st.write("Vous pouvez choisir parmi les options suivantes pour afficher les données :")
    st.write("- **Pays**: Affiche le nombre d'utilisateurs actifs, le temps d'engagement moyen et les utilisateurs actifs par mois pour chaque pays.")
    st.write("- **Villes**: Affiche le nombre d'utilisateurs actifs, le temps d'engagement moyen et les utilisateurs actifs par mois pour chaque ville.")
    st.write("- **Pages Vues**: Affiche le temps d'engagement par page, les pages vues par scroll, les pages vues par utilisateurs et les pages vues par utilisateurs regroupées par ville et pays.")
    st.write("- **Sessions**: Affiche les sessions par utilisateur, le temps d'engagement par session, les sessions par mois, et les sessions par utilisateur regroupées par ville et pays.")
    st.write("- **lesDimension**: Affiche toutes les dimensions disponibles avec les métriques sélectionnées.")
    
    st.header("Détails des Requêtes")
    
    st.subheader("Pays")
    st.write("1. **Nombre d'utilisateurs par pays**: Affiche le nombre d'utilisateurs actifs pour chaque pays sur la période sélectionnée.")
    st.write("2. **Temps d'engagement par pays**: Affiche le temps d'engagement moyen par utilisateur pour chaque pays.")
    st.write("3. **Utilisateurs par pays et mois**: Affiche le nombre d'utilisateurs actifs par mois pour chaque pays.")
    
    st.subheader("Villes")
    st.write("1. **Nombre d'utilisateurs par ville**: Affiche le nombre d'utilisateurs actifs pour chaque ville sur la période sélectionnée.")
    st.write("2. **Temps d'engagement par ville**: Affiche le temps d'engagement moyen par utilisateur pour chaque ville.")
    st.write("3. **Utilisateurs par ville et mois**: Affiche le nombre d'utilisateurs actifs par mois pour chaque ville.")
    
    st.subheader("Pages Vues")
    st.write("1. **Temps d'engagement par page**: Affiche le temps d'engagement moyen par utilisateur pour chaque page.")
    st.write("2. **Pages vues par scroll**: Affiche le nombre de pages vues pour chaque page.")
    st.write("3. **Pages vues par utilisateurs**: Affiche le nombre de pages vues par utilisateur pour chaque page.")
    st.write("4. **Pages vues par utilisateur regroupées par ville**: Affiche les pages vues par utilisateur regroupées par ville.")
    st.write("5. **Pages vues par utilisateur regroupées par pays**: Affiche les pages vues par utilisateur regroupées par pays.")
    
    st.subheader("Sessions")
    st.write("1. **Sessions par utilisateur**: Affiche le nombre de sessions pour chaque utilisateur.")
    st.write("2. **Temps d'engagement par session**: Affiche le temps d'engagement moyen par session.")
    st.write("3. **Sessions par mois**: Affiche le nombre de sessions par mois.")
    st.write("4. **Sessions par utilisateur regroupées par ville**: Affiche les sessions par utilisateur regroupées par ville.")
    st.write("5. **Sessions par utilisateur regroupées par pays**: Affiche les sessions par utilisateur regroupées par pays.")
    
    st.subheader("lesDimension")
    st.write("Affiche toutes les dimensions disponibles avec les métriques sélectionnées :")
    st.write("- **Country**: Pays de l'utilisateur")
    st.write("- **City**: Ville de l'utilisateur")
    st.write("- **Session Medium**: Source de la session")
    st.write("- **Page Path**: Chemin de la page visitée")
    st.write("- **Operating System**: Système d'exploitation de l'utilisateur")
    st.write("- **Operating System Version**: Version du système d'exploitation de l'utilisateur")
    st.write("Avec les métriques suivantes :")
    st.write("- **Sessions**: Nombre de sessions")
    st.write("- **Engagement Rate**: Taux d'engagement")
    st.write("- **User Engagement Duration**: Durée d'engagement de l'utilisateur")
    st.write("- **Active Users**: Nombre d'utilisateurs actifs")




def display_user_predictions_documentation():
    st.write("""
    ## Prédictions du nombre d'utilisateurs par ville

    Cette section utilise les données de Google Analytics pour prédire le nombre d'utilisateurs actifs dans différentes villes pendant une période spécifiée. Voici comment cela fonctionne :

    1. **Sélection de la Plage de Dates** : Vous pouvez sélectionner la période de temps pour laquelle vous souhaitez effectuer les prédictions en utilisant les widgets dans la barre latérale. Par défaut, la période est définie sur les 30 derniers jours jusqu'à la date actuelle.

    2. **Extraction des Données d'Engagement** : Les données d'engagement sont extraites de Google Analytics pour la plage de dates sélectionnée. Cela comprend le temps d'engagement moyen des utilisateurs dans différentes villes ainsi que le nombre total d'utilisateurs actifs.

    3. **Préparation des Données pour la Régression Linéaire** : Les données sont préparées pour la régression linéaire. Cela implique de diviser les données en ensembles d'entraînement et de test, d'encoder les villes comme des variables catégorielles, et de séparer la variable cible (le temps d'engagement moyen) des autres caractéristiques.

    4. **Entraînement du Modèle** : Un modèle de régression linéaire est entraîné sur l'ensemble d'entraînement pour prédire le temps d'engagement moyen des utilisateurs.

    5. **Évaluation du Modèle** : L'erreur quadratique moyenne (MSE) est calculée pour évaluer les performances du modèle sur l'ensemble de test. Cela permet de quantifier la précision des prédictions par rapport aux valeurs réelles.

    6. **Prédictions** : Les prédictions sont effectuées sur l'ensemble de test à l'aide du modèle entraîné. Les valeurs prédites du temps d'engagement moyen sont affichées dans un DataFrame.

    7. **Affichage des Résultats** : Les résultats, y compris le MSE et les prédictions, sont affichés sur l'interface Streamlit pour permettre une analyse interactive des données prédites.

    Cette approche fournit des informations précieuses sur le comportement des utilisateurs dans différentes villes, ce qui peut être utile pour optimiser les stratégies de marketing et d'engagement.
    """)





# Appeler la fonction display_documentation dans le code principal de l'application
documentation_data()

# Pour intégrer cette page dans votre application, vous pouvez modifier votre fichier app.py comme suit:

documentation_analyse()

display_user_predictions_documentation()




