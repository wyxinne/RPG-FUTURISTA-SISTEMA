import streamlit as st
import random
import re

# --- 1. CONFIGURAÇÃO E IDENTIDADE VISUAL COM FONTES ---
st.set_page_config(page_title="NEON-WALL TERMINAL", layout="centered")

# Importando fontes do Google e aplicando o estilo
st.markdown("""
    <style>
    /* Importando as fontes */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono:wght@300;500&display=swap');

    /* Fundo degradê conforme sua descrição */
    .stApp {
        background: linear-gradient(180deg, #1a0033 0%, #05080a 70%, #2c2c2c 100%);
        background-attachment: fixed;
    }
    
    /* TÍTULOS (Orbitron - Futurista) */
    h1, h2, h3 {
        color: #00ff41 !important;
        text-shadow: 0 0 10px #00ff41, 0 0 20px #ff00ff;
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 2px;
    }
    
    /* TEXTOS E LABELS (Roboto Mono - Terminal) */
    label, p, span, div {
        color: #ffff00 !important; /* Amarelo Neon */
        font-family: 'Roboto Mono', monospace !important;
    }

    /* Estilo das Abas */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        color: #00ff41 !important;
        border: 1px solid #ff00ff !important;
        background-color: rgba(0,0,0,0.6);
        font-family: 'Orbitron', sans-serif !important;
    }

    /* Botões Neon */
    .stButton>button {
        width: 100%;
        border: 2px solid #00ff41 !important;
        background-color: #1a1a1a !important;
        color: #ff00ff !important;
        font-family: 'Orbitron', sans-serif !important;
        box-shadow: 4px 4px 0px #ffff00;
    }

    /* Cores de Crítico e Falha */
    .critico { color: #00ff41; font-weight: bold; text-shadow: 0 0 8px #00ff41; }
    .falha { color: #ff3131; font-weight: bold; font-style: italic; text-shadow: 0 0 8px #ff3131; }
    </style>
    """, unsafe_allow_html=True)

# --- RESTO DO CÓDIGO (check_password e abas) CONTINUA IGUAL ---
