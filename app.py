import streamlit as st
import random
import re
import time

# --- 1. CONFIGURAÇÃO E IDENTIDADE VISUAL ---
st.set_page_config(page_title="NEON-WALL TERMINAL", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono:wght@300;500&family=Press+Start+2P&display=swap');

    html, body, [data-testid="stAppViewContainer"], button, input, .stTabs {
        text-transform: uppercase !important;
    }

    .stApp {
        background-image: url("https://raw.githubusercontent.com/wyxinne/RPG-FUTURISTA-SISTEMA/main/fundo%20cyberpunk.png");
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
    }
    
    h1, h2, h3 {
        color: #00ff41 !important;
        text-shadow: 0 0 10px #00ff41;
        font-family: 'Orbitron', sans-serif !important;
    }
    
    label, p, span, div {
        color: #ffff00 !important;
        font-family: 'Roboto Mono', monospace !important;
    }

    .destaque-neon {
        color: #ff00ff !important;
        text-shadow: 0 0 10px #ff00ff;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 1.8em;
        font-weight: bold;
    }

    .sub-destaque-neon {
        color: #ff00ff !important;
        text-shadow: 0 0 5px #ff00ff;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 1.1em;
    }

    /* ESTILO DAS CAIXAS DE CYBERWARE PRATEADAS */
    .stTextInput input {
        background-color: rgba(192, 192, 192, 0.1) !important;
        border: 1px solid #C0C0C0 !important;
        color: #C0C0C0 !important;
    }

    /* BOTÕES */
    .stButton>button {
        width: 100%;
        border: 1px solid #00ff41 !important;
        background-color: #1a1a1a !important;
        color: #00ff41 !important;
        font-family: 'Orbitron', sans-serif !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Inicialização de variáveis de estado
if "hp_atual" not in st.session_state: st.session_state.hp_atual = 20
if "hp_max" not in st.session_state: st.session_state.hp_max = 20
if "strain_atual" not in st.session_state: st.session_state.strain_atual = 0
if "strain_max" not in st.session_state: st.session_state.strain_max = 10

def check_password():
    if "password_correct" not in st.session_state: st.session_state["password_correct"] = False
    if st.session_state["password_correct"]: return True
    st.title("MURALHA DE SEGURANÇA")
    password = st.text_input("CHAVE DA REDE:", type="password")
    if st.button("CONECTAR"):
        if password == "cyber2024":
            st.session_state["password_correct"] = True
            st.rerun()
        else: st.error("ACESSO NEGADO.")
    return False

if check_password():
    tab_status, tab_combate, tab_rolagem = st.tabs(["STATUS", "COMBATE", "ROLAGEM LIVRE"])

    with tab_status:
        col_id, col_cyber = st.columns([1.5, 1])

        with col_id:
            # Identificação
            st.text_input("PERSONAGEM:", placeholder="NOME DO OPERADOR")
            st.text_input("OCUPAÇÃO:", placeholder="EX: HACKER / MERCENÁRIO")
            
            st.markdown("---")

            # Gerenciamento de HP
            st.write(f"INTEGRIDADE (HP): {st.session_state.hp_atual} / {st.session_state.hp_max}")
            new_hp_max = st.number_input("HP MÁXIMO (CLIQUE DUPLO P/ EDITAR)", value=st.session_state.hp_max, step=1)
            st.session_state.hp_max = new_hp_max
            
            # Barra de HP (Verde)
            progresso_hp = min(st.session_state.hp_atual / max(1, st.session_state.hp_max), 1.0)
            st.progress(progresso_hp)
            
            c1, c2, c3, c4 = st.columns(4)
            if c1.button("--", help="Remove 5 HP"): st.session_state.hp_atual -= 5
            if c2.button("-", help="Remove 1 HP"): st.session_state.hp_atual -= 1
            if c3.button("+", help="Adiciona 1 HP"): st.session_state.hp_atual += 1
            if c4.button("++", help="Adiciona 5 HP"): st.session_state.hp_atual += 5

            st.markdown("---")

            # Gerenciamento de Strain
            new_strain_max = st.number_input("LIMITE DE SOBRECARGA (STRAIN)", value=st.session_state.strain_max, step=1)
            st.session_state.strain_max = new_strain_max
            
            # Lógica de Cor da Barra de Strain
            atual = st.session_state.strain_atual
            maximo = st.session_state.strain_max
            
            cor_strain = "yellow" # Amarela (Inicial)
            if atual >= (maximo / 2): cor_strain = "orange" # Laranja (Metade)
            if atual >= (maximo - 2) and atual > 0: cor_strain = "red" # Vermelha (Faltam 2)

            st.markdown(f"SOBRECARGA: <span style='color:{cor_strain}; font-weight:bold;'>{atual} / {maximo}</span>", unsafe_allow_html=True)
            progresso_strain = min(atual / max(1, maximo), 1.0)
            st.progress(progresso_strain)
            
            # Botões Strain
            sc1, sc2 = st.columns(2)
            if sc1.button("- STRAIN"): st.session_state.strain_atual -= 1
            if sc2.button("+ STRAIN"): st.session_state.strain_atual += 1

        with col_cyber:
            st.subheader("LISTA DE CYBERWARE")
            for i in range(6): # Cria 6 fileiras de implantes
                ca, cb = st.columns([3, 1])
                with ca:
                    st.text_input(f"IMPLANTE {i+1}", key=f"cyber_{i}", placeholder="DETALHE O HARDWARE")
                with cb:
                    st.text_input("ST", key=f"st_{i}", placeholder="ST")

    with tab_rolagem:
        st.subheader("TERMINAL DE DADOS INDEPENDENTES")
        entrada = st.text_input("COMANDO:", value="2D20+3")
        if st.button("🎲 ROLAR"):
            # Lógica de rolagem simplificada para o exemplo
            st.markdown(f"<p class='destaque-neon'>RESULTADO: 18</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='sub-destaque-neon'>TOTAL: 25</p>", unsafe_allow_html=True)

    with tab_combate:
        st.subheader("INTERFACE DE ATAQUE")
        st.write("STATUS RÁPIDO:")
        st.info(f"HP: {st.session_state.hp_atual} | STRAIN: {st.session_state.strain_atual}")
