import streamlit as st

# --- 1. CONFIGURAÇÃO DE TELA E ESTILO ---
st.set_page_config(page_title="NEON-WALL TERMINAL", layout="wide")

# CSS Refinado para evitar quebras
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono:wght@300;500&display=swap');

    .stApp {
        background-image: url("https://raw.githubusercontent.com/wyxinne/RPG-FUTURISTA-SISTEMA/main/fundo%20cyberpunk.png");
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
    }

    html, body, [data-testid="stAppViewContainer"], button, input, .stTabs {
        text-transform: uppercase !important;
        font-family: 'Roboto Mono', monospace !important;
    }

    h1, h2, h3 {
        color: #00ff41 !important;
        text-shadow: 0 0 10px #00ff41;
        font-family: 'Orbitron', sans-serif !important;
    }
    
    label, p, span, div {
        color: #ffff00 !important;
    }

    /* Estilo das caixinhas de Cyberware */
    div[data-testid="stTextInput"] input {
        background-color: rgba(192, 192, 192, 0.2) !important;
        border: 1px solid #C0C0C0 !important;
        color: #C0C0C0 !important;
    }

    .stButton>button {
        border: 1px solid #00ff41 !important;
        background-color: #1a1a1a !important;
        color: #00ff41 !important;
        font-family: 'Orbitron', sans-serif !important;
    }
    
    .stButton>button:hover {
        border: 1px solid #ff00ff !important;
        color: #ff00ff !important;
        box-shadow: 0 0 15px #ff00ff;
    }

    /* Tabs Neon Roxo */
    .stTabs [data-baseweb="tab-list"] { background-color: rgba(0,0,0,0.8); border-radius: 10px; }
    .stTabs [data-baseweb="tab"] { color: #bc13fe; }
    .stTabs [aria-selected="true"] { border-bottom-color: #bc13fe !important; color: #bc13fe !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Áudio de Ambiência
st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3")

# --- 2. BANCO DE DADOS EM SESSÃO ---
if "personagens" not in st.session_state:
    st.session_state.personagens = {
        "P1": {"nome": "OPERADOR_ZERO", "ocupacao": "SCAVENGER", "hp": 20, "hp_max": 20, "strain": 0, "strain_max": 10},
    }

if "perfil_logado" not in st.
