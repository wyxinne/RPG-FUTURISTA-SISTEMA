import streamlit as st
import random
import re

# --- 1. CONFIGURAÇÃO E IDENTIDADE VISUAL ---
st.set_page_config(page_title="NEON-WALL TERMINAL", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono:wght@300;500&display=swap');

    .stApp {
        background-image: url("https://raw.githubusercontent.com/wyxinne/RPG-FUTURISTA-SISTEMA/main/fundo%20cyberpunk.png");
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    html, body, [data-testid="stAppViewContainer"], button, input, .stTabs {
        text-transform: uppercase !important; font-family: 'Roboto Mono', monospace !important;
    }
    h1, h2, h3 { color: #00ff41 !important; text-shadow: 0 0 10px #00ff41; font-family: 'Orbitron', sans-serif !important; }
    label, p, span, div { color: #ffff00 !important; }

    /* Caixas de Cyberware Prateadas */
    div[data-testid="stTextInput"] input {
        background-color: rgba(192, 192, 192, 0.2) !important;
        border: 1px solid #C0C0C0 !important; color: #C0C0C0 !important;
    }
    .stButton>button {
        border: 1px solid #00ff41 !important; background-color: #1a1a1a !important;
        color: #00ff41 !important; font-family: 'Orbitron', sans-serif !important;
    }
    .stButton>button:hover { border: 1px solid #ff00ff !important; color: #ff00ff !important; box-shadow: 0 0 15px #ff00ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ÁUDIO DE AMBIÊNCIA (FIXO) ---
st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3")

# --- 3. BANCO DE DADOS (SESSION STATE) ---
if "personagens" not in st.session_state:
    st.session_state.personagens = {
        "P1": {"nome": "OPERADOR_01", "ocupacao": "RUNNER", "hp": 20, "hp_max": 20, "strain": 0, "strain_max": 10}
    }
if "perfil_logado" not in st.session_state:
    st.session_state.perfil_logado = None

# --- 4. SISTEMA DE LOGIN ---
if not st.session_state.perfil_logado:
    st.title("ACESSO À MURALHA")
    col_l, _ = st.columns([1, 2])
    with col_l:
        perf = st.selectbox("IDENTIFIQUE-SE:", ["JOGADOR", "MESTRE"])
        pw = st.text_input("CHAVE DE ACESSO:", type="password")
        if st.button("CONECTAR"):
            if perf == "MESTRE" and pw == "mestre":
                st.session_state.perfil_logado = "MESTRE"
                st.rerun()
            elif perf == "JOGADOR" and pw == "cyber2024":
                st.session_state.perfil_logado = "JOGADOR"
                st.rerun()
            else: st.error("ACESSO NEGADO.")
else:
    # Sidebar de Logout
    if st.sidebar.button("DESCONECTAR"):
        st.session_state.perfil_logado = None
        st.rerun()

    # --- 5. PERFIL MESTRE ---
    if st.session_state.perfil_logado == "MESTRE":
        t_mestre = st.tabs(["🛰️ CONTROLE GERAL", "🧬 CRIAR PERFIS"])
        with t_mestre[0]:
            st.header("STATUS DE TODOS OS JOGADORES")
            for pid, pdata in st.session_state.personagens.items():
                st.markdown(f"**{pdata['nome']}** | HP: {pdata['hp']}/{pdata['hp_max']} | STRAIN: {pdata['strain']}/{pdata['strain_max']}")
        with t_mestre[1]:
            st.header("CADASTRAR NOVO JOGADOR")
            new_id = st.text_input("ID DE LOGIN")
            new_n = st.text_input("NOME DO PERSONAGEM")
            if st.button("CADASTRAR"):
                st.session_state.personagens[new_id] = {"nome": new_n, "ocupacao": "N/A", "hp": 20, "hp_max": 20, "strain": 0, "strain_max": 10}
                st.success("REGISTRADO.")

    # --- 6. PERFIL JOGADOR ---
    else:
        p_id = st.selectbox("CONFIRME SUA IDENTIDADE:", list(st.session_state.personagens.keys()))
        char = st.session_state.personagens[p_id]
        tab_stat, tab_roll = st.tabs(["STATUS", "ROLAGEM LIVRE"])

        with tab_stat:
            col_id, col_cyber = st.columns([1.5, 1])
            with col_id:
                # Topo Esquerdo
                st.session_state.personagens[p_id]['nome'] = st.text_input("NOME:", value=char['nome'])
                st.session_state.personagens[p_id]['ocupacao'] = st.text_input("OCUPAÇÃO:", value=char['ocupacao'])
                st.markdown("---")
                # HP
                hp_m = st.number_input("HP MÁXIMO:", value=char['hp_max'], step=1)
                st.session_state.personagens[p_id]['hp_max'] = hp_m
                st.write(f"INTEGRIDADE: {char['hp']} / {hp_m}")
                st.progress(min(max(char['hp']/max(1, hp_m), 0.0), 1.0))
                c1, c2, c3, c4 = st.columns(4)
                if c1.button("--", key="h1"): st.session_state.personagens[p_id]['hp'] -= 5
                if c2.button("-", key="h2"): st.session_state.personagens[p_id]['hp'] -= 1
                if c3.button("+", key="h3"): st.session_state.personagens[p_id]['hp'] += 1
                if c4.button("++", key="h4"): st.session_state.personagens[p_id]['hp'] += 5
                st.markdown("---")
                # STRAIN
                st_m = st.number_input("LIMITE DE STRAIN:", value=char['strain_max'], step=1)
                st.session_state.personagens[p_id]['strain_max'] = st_m
                cor = "#ffff00" # Amarelo
                if char['strain'] >= (st_m / 2): cor = "#ffa500" # Laranja
                if char['strain'] >= (st_m - 2): cor = "#ff0000" # Vermelho
                st.markdown(f"SOBRECARGA: <span style='color:{cor}; font-weight:bold;'>{char['strain']} / {st_m}</span>", unsafe_allow_html=True)
                st.progress(min(max(char['strain']/max(1, st_m), 0.0), 1.0))
                sc1, sc2 = st.columns(2)
                if sc1.button("- STRAIN", key="s1"): st.session_state.personagens[p_id]['strain'] -= 1
                if sc2.button("+ STRAIN",
