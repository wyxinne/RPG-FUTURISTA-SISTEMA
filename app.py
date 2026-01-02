import streamlit as st
import random
import re
import time

# --- 1. CONFIGURAÇÃO E IDENTIDADE VISUAL ---
st.set_page_config(page_title="NEON-WALL TERMINAL", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono:wght@300;500&family=Press+Start+2P&display=swap');

    /* FORÇAR CAIXA ALTA GLOBAL */
    html, body, [data-testid="stAppViewContainer"], button, input {
        text-transform: uppercase !important;
    }

    /* FUNDO CYBERPUNK */
    .stApp {
        background-image: url("https://raw.githubusercontent.com/wyxinne/RPG-FUTURISTA-SISTEMA/main/fundo%20cyberpunk.png");
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
    }
    
    /* TÍTULOS VERDE NEON */
    h1, h2, h3 {
        color: #00ff41 !important;
        text-shadow: 0 0 10px #00ff41, 0 0 20px #ff00ff;
        font-family: 'Orbitron', sans-serif !important;
    }
    
    /* TEXTOS GERAIS */
    label, p, span, div {
        color: #ffff00 !important;
        font-family: 'Roboto Mono', monospace !important;
    }

    /* --- ESTILIZAÇÃO DAS ABAS (TABS) --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    /* Estilo de todas as abas (não selecionadas) */
    .stTabs [data-baseweb="tab"] {
        color: #00ff41 !important;
        background-color: rgba(0, 0, 0, 0.7) !important;
        border: 1px solid #ff00ff !important;
        font-family: 'Press Start 2P', cursive !important;
        font-size: 10px !important;
        padding: 10px 15px !important;
        border-radius: 4px 4px 0px 0px;
        transition: all 0.3s ease;
    }

    /* ABA SELECIONADA (FOCO ATIVO) */
    .stTabs [aria-selected="true"] {
        background-color: #300066 !important; /* Roxo Escuro */
        color: #ff00ff !important; /* Rosa Neon */
        text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff !important; /* Brilho Rosa */
        border-bottom: 2px solid #ff00ff !important;
    }

    /* BOTÕES NEON */
    .stButton>button {
        width: 100%;
        border: 2px solid #00ff41 !important;
        background-color: #1a1a1a !important;
        color: #ff00ff !important;
        font-family: 'Orbitron', sans-serif !important;
        box-shadow: 4px 4px 0px #ffff00;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff00ff !important;
        color: #000000 !important;
        box-shadow: 0px 0px 20px #ff00ff;
    }

    /* CRÍTICO E FALHA */
    .num_critico { color: #00ff00 !important; font-weight: 800; text-shadow: 0 0 15px #00ff00; font-size: 1.2em; }
    .msg_critico { color: #00ff00 !important; font-size: 0.75em; }
    .num_falha { color: #ff0000 !important; font-weight: 800; text-shadow: 0 0 15px #ff0000; font-size: 1.2em; }
    .msg_falha { color: #ff0000 !important; font-size: 0.75em; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO DE ÁUDIO ---
def play_dice_sound():
    url_audio = "https://raw.githubusercontent.com/wyxinne/RPG-FUTURISTA-SISTEMA/main/dados%202.m4a"
    audio_html = f"""<audio autoplay style="display:none;"><source src="{url_audio}?t={time.time()}" type="audio/mp4"></audio>"""
    st.markdown(audio_html, unsafe_allow_html=True)

# --- 2. SISTEMA DE ACESSO ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]: return True

    st.title("📟 MURALHA DE SEGURANÇA")
    password = st.text_input("CHAVE DA REDE:", type="password")
    if st.button("CONECTAR"):
        if password == "cyber2024":
            st.session_state["password_correct"] = True
            st.rerun()
        else: st.error("ACESSO NEGADO.")
    return False

# --- 3. CONTEÚDO PRINCIPAL ---
if check_password():
    if "pa" not in st.session_state: st.session_state["pa"] = 10

    tab_combate, tab_rolagem, tab_pericias = st.tabs(["COMBATE", "ROLAGEM LIVRE", "PERÍCIAS"])

    with tab_rolagem:
        st.subheader("TERMINAL DE DADOS NEURAIS")
        entrada = st.text_input("COMANDO DE DADOS (EX: 2D20+5):", value="2D20+3", key="roll_main")
        
        if st.button("🎲 ROLAR"):
            play_dice_sound()
            
            try:
                match = re.match(r'(\d+)D(\d+)([+-]\d+)?', entrada.replace(" ", "").upper())
                if match:
                    qtd, faces = int(match.group(1)), int(match.group(2))
                    bonus = int(match.group(3)) if match.group(3) else 0
                    
                    rolagens = [random.randint(1, faces) for _ in range(qtd)]
                    soma_dados = sum(rolagens)
                    resultado_final = soma_dados + bonus
                    
                    html_dados = []
                    for r in rolagens:
                        if r == faces:
                            html_dados.append(f"<span class='num_critico'>{r}</span> <span class='msg_critico'>(CRÍTICO!)</span>")
                        elif r == 1:
                            html_dados.append(f"<span class='num_falha'>{r}</span> <span class='msg_falha'>(VISH...)</span>")
                        else:
                            html_dados.append(str(r))
                    
                    st.markdown(f"### 🚀 TOTAL: **{resultado_final}**")
                    st.write(f"**LÓGICA:** SOMA ({soma_dados}) + BÔNUS ({bonus})")
                    st.markdown(f"**DADOS ROLADOS:** {', '.join(html_dados)}", unsafe_allow_html=True)
                else: st.error("SINTAXE INVÁLIDA.")
            except Exception: st.error("ERRO NO PROCESSADOR.")

    with tab_combate:
        st.subheader(f"PONTOS DE AÇÃO: {st.session_state['pa']} / 10")
        if st.button("🕒 RECARREGAR PA"):
            st.session_state["pa"] = 10
            st.rerun()

    with tab_pericias:
        st.subheader("PERÍCIAS CADASTRADAS")
        st.write("● HACKEAMENTO")
        st.write("● MECÂNICA DE SUCATA")
