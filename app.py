import streamlit as st
import random
import re
import time

# --- 1. CONFIGURAÇÃO E IDENTIDADE VISUAL ---
st.set_page_config(page_title="NEON-WALL TERMINAL", layout="wide")

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
        text-shadow: 0 0 10px #00ff41, 0 0 20px #ff00ff;
        font-family: 'Orbitron', sans-serif !important;
    }
    
    label, p, span, div {
        color: #ffff00 !important;
        font-family: 'Roboto Mono', monospace !important;
    }

    .destaque-neon {
        color: #ff00ff !important;
        text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 1.8em;
        font-weight: bold;
    }

    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        color: #00ff41 !important;
        background-color: rgba(0, 0, 0, 0.8) !important;
        border: 1px solid #ff00ff !important;
        font-family: 'Press Start 2P', cursive !important;
        font-size: 10px !important;
        padding: 10px 15px !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #6a0dad !important;
        color: #ff00ff !important;
    }

    div[data-testid="stTextInput"] input {
        background-color: rgba(192, 192, 192, 0.1) !important;
        border: 1px solid #C0C0C0 !important;
        color: #C0C0C0 !important;
    }

    .stButton>button {
        width: 100%;
        border: 2px solid #00ff41 !important;
        background-color: #1a1a1a !important;
        color: #ff00ff !important;
        font-family: 'Orbitron', sans-serif !important;
        box-shadow: 4px 4px 0px #ffff00;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FUNÇÕES DE SUPORTE ---
def play_dice_sound():
    url_audio = "https://raw.githubusercontent.com/wyxinne/RPG-FUTURISTA-SISTEMA/main/dados%202.m4a"
    audio_html = f"""<audio autoplay style="display:none;"><source src="{url_audio}?t={time.time()}" type="audio/mp4"></audio>"""
    st.markdown(audio_html, unsafe_allow_html=True)

# --- 3. BANCO DE DADOS EM SESSÃO ---
if "personagens" not in st.session_state:
    st.session_state.personagens = {
        "P1": {"nome": "NOME DO PERSONAGEM", "ocupacao": "OCUPAÇÃO", "hp": 20, "hp_max": 20, "strain": 0, "strain_max": 10},
    }
if "perfil_logado" not in st.session_state: st.session_state.perfil_logado = None

# --- 4. CONTROLE DE ACESSO ---
if not st.session_state.perfil_logado:
    st.title("MURALHA DE SEGURANÇA")
    col_log, _ = st.columns([1, 2])
    with col_log:
        perf_sel = st.selectbox("IDENTIFIQUE-SE:", ["JOGADOR", "MESTRE"])
        senha = st.text_input("CHAVE DA REDE:", type="password")
        if st.button("CONECTAR"):
            if perf_sel == "MESTRE" and senha == "mestre":
                st.session_state.perfil_logado = "MESTRE"
                st.rerun()
            elif perf_sel == "JOGADOR" and senha == "cyber2024":
                st.session_state.perfil_logado = "JOGADOR"
                st.rerun()
            else: st.error("ACESSO NEGADO.")
else:
    # Sidebar Logout
    if st.sidebar.button("DESCONECTAR"):
        st.session_state.perfil_logado = None
        st.rerun()

    # --- 5. INTERFACE MESTRE ---
    if st.session_state.perfil_logado == "MESTRE":
        t_mestre = st.tabs(["🛰️ CONTROLE GERAL", "🧬 CRIAR PERFIS"])
        with t_mestre[0]:
            st.header("STATUS GLOBAL DOS AGENTES")
            for pid, pdata in st.session_state.personagens.items():
                st.markdown(f"**{pdata['nome']}** | HP: {pdata['hp']}/{pdata['hp_max']} | STRAIN: {pdata['strain']}/{pdata['strain_max']}")
        with t_mestre[1]:
            st.header("CADASTRAR NOVO PERFIL")
            n_id = st.text_input("ID DE LOGIN")
            n_nome = st.text_input("NOME DO PERSONAGEM")
            if st.button("CADASTRAR"):
                st.session_state.personagens[n_id] = {"nome": n_nome, "ocupacao": "N/A", "hp": 20, "hp_max": 20, "strain": 0, "strain_max": 10}
                st.success("REGISTRO CRIADO.")

    # --- 6. INTERFACE JOGADOR ---
    else:
        p_id = st.selectbox("CONFIRME SUA IDENTIDADE:", list(st.session_state.personagens.keys()))
        char = st.session_state.personagens[p_id]
        tab_stat, tab_roll, tab_comb = st.tabs(["STATUS", "ROLAGEM LIVRE", "COMBATE"])

        with tab_stat:
            col_l, col_r = st.columns([1.5, 1])
            with col_l:
                st.session_state.personagens[p_id]['nome'] = st.text_input("PERSONAGEM:", value=char['nome'])
                st.session_state.personagens[p_id]['ocupacao'] = st.text_input("OCUPAÇÃO:", value=char['ocupacao'])
                st.markdown("---")
                # HP
                m_hp = st.number_input("HP MÁXIMO:", value=char['hp_max'])
                st.session_state.personagens[p_id]['hp_max'] = m_hp
                st.write(f"INTEGRIDADE: {char['hp']} / {m_hp}")
                st.progress(min(max(char['hp']/max(1, m_hp), 0.0), 1.0))
                c1, c2, c3, c4 = st.columns(4)
                if c1.button("--", key="h1"): st.session_state.personagens[p_id]['hp'] -= 5
                if c2.button("-", key="h2"): st.session_state.personagens[p_id]['hp'] -= 1
                if c3.button("+", key="h3"): st.session_state.personagens[p_id]['hp'] += 1
                if c4.button("++", key="h4"): st.session_state.personagens[p_id]['hp'] += 5
                st.markdown("---")
                # STRAIN
                m_st = st.number_input("LIMITE DE STRAIN:", value=char['strain_max'])
                st.session_state.personagens[p_id]['strain_max'] = m_st
                cor = "#ffff00" # Amarelo
                if char['strain'] >= (m_st / 2): cor = "#ffa500" # Laranja
                if char['strain'] >= (m_st - 2): cor = "#ff0000" # Vermelho
                st.markdown(f"SOBRECARGA: <span style='color:{cor}; font-weight:bold;'>{char['strain']} / {m_st}</span>", unsafe_allow_html=True)
                st.progress(min(max(char['strain']/max(1, m_st), 0.0), 1.0))
                sc1, sc2 = st.columns(2)
                if sc1.button("- STRAIN", key="s1"): st.session_state.personagens[p_id]['strain'] -= 1
                if sc2.button("+ STRAIN", key="s2"): st.session_state.personagens[p_id]['strain'] += 1

            with col_r:
                st.subheader("LISTA DE CYBERWARE")
                for i in range(6):
                    ca, cb = st.columns([3, 1])
                    ca.text_input(f"DESC {i}", key=f"d_{p_id}_{i}", label_visibility="collapsed")
                    cb.text_input(f"ST {i}", key=f"s_{p_id}_{i}", label_visibility="collapsed")

        with tab_roll:
            st.subheader("TERMINAL DE DADOS")
            entrada = st.text_input("COMANDO:", value="2D20+3", key="roll_main")
            if st.button("🎲 ROLAR"):
                play_dice_sound()
                # A lógica de processamento de re.match do seu código original entraria aqui
                st.markdown(f"<p class='destaque-neon'>RESULTADO: {random.randint(1,20)}</p>", unsafe_allow_html=True)

        with tab_combate:
            st.info(f"STATUS RÁPIDO: HP {char['hp']} | STRAIN {char['strain']}")
