import streamlit as st
import requests
import cv2 
r = requests
cv = cv2
plot_placeholder = st.empty()

def main():
    # Ajout de CSS pour les styles et animations
    st.markdown("""
    <style>
    body {
        color: #fff;
        background-color: #000000; 
    }
    .big-font {
        font-size: 40px !important;
        font-weight: bold;
        color: #f9d342;  /* Couleur du titre en jaune */
    }
    @keyframes blinker {
        50% { opacity: 0; }
    }
    h2 {
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Contenu de la page
    st.markdown('<div class="big-font">Automatisation des données GA4 de Retro Photo</div>', unsafe_allow_html=True)
    st.markdown("""
    ## Description de l'application
    Cette application permet une **analyse approfondie des données GA4** pour Retro Photo, une entreprise spécialisée dans la vente de cartes postales d'anciennes photos. En exploitant les données de leur site web, cette application aide à visualiser et analyser le comportement des utilisateurs, l'engagement sur le site, et les performances des différentes pages.
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
