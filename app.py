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
    html, body, [data-testid="stAppViewContainer"], button, input, .stTabs {
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

    /* TEXTO RESULTADO (DESTAQUE PRINCIPAL) */
    .destaque-neon {
        color: #ff00ff !important;
        text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 1.8em;
        font-weight: bold;
        margin-bottom: 0px;
    }

    /* TEXTO TOTAL (MENOS DESTAQUE) */
    .sub-destaque-neon {
        color: #ff00ff !important;
        text-shadow: 0 0 5px #ff00ff;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 1.1em;
        font-weight: normal;
        margin-top: 10px;
    }

    /* --- ESTILIZAÇÃO DAS ABAS (TABS) --- */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }

    .stTabs [data-baseweb="tab"] {
        color: #00ff41 !important;
        background-color: rgba(0, 0, 0, 0.8) !important;
        border: 1px solid #ff00ff !important;
        font-family: 'Press Start 2P', cursive !important;
        font-size: 10px !important;
        padding: 10px 15px !important;
        border-radius: 4px 4px 0px 0px;
        font-weight: 400;
    }

    .stTabs [aria-selected="true"] {
        background-color: #6a0dad !important; /* ROXO CHAPADO */
        color: #ff00ff !important; /* ROSA NEON */
        font-weight: 900 !important;
        border: 1px solid #ff00ff !important;
        text-shadow: none !important;
    }

    /* BOTÕES NEON */
    .stButton>button {
        width: 100%;
        border: 2px solid #00ff41 !important;
        background-color: #1a1a1a !important;
        color: #ff00ff !important;
        font-family: 'Orbitron', sans-serif !important;
        box-shadow: 4px 4px 0px #ffff00;
    }

    /* CRÍTICO E FALHA */
    .num_critico { color: #00ff00 !important; font-weight: 800; text-shadow: 0 0 15px #00ff00; font-size: 1.2em; }
    .msg_critico { color: #00ff00 !important; font-size: 0.75em; }
    .num_falha { color: #ff0000 !important; font-weight: 800; text-shadow: 0 0 15px #ff0000; font-size: 1.2em; }
    .msg_falha { color: #ff0000 !important; font-size: 0.75em; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

def play_dice_sound():
    url_audio = "https://raw.githubusercontent.com/wyxinne/RPG-FUTURISTA-SISTEMA/main/dados%202.m4a"
    audio_html = f"""<audio autoplay style="display:none;"><source src="{url_audio}?t={time.time()}" type="audio/mp4"></audio>"""
    st.markdown(audio_html, unsafe_allow_html=True)

def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
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
    if "pa" not in st.session_state: st.session_state["pa"] = 10

    tab_combate, tab_rolagem, tab_pericias = st.tabs(["COMBATE", "ROLAGEM LIVRE", "PERÍCIAS"])

    with tab_rolagem:
        st.subheader("TERMINAL DE DADOS INDEPENDENTES")
        entrada = st.text_input("COMANDO DE DADOS:", value="2D20+3", key="roll_main")
        
        if st.button("🎲 ROLAR"):
            play_dice_sound()
            
            try:
                match = re.match(r'(\d+)D(\d+)([+-]\d+)?', entrada.replace(" ", "").upper())
                if match:
                    qtd, faces = int(match.group(1)), int(match.group(2))
                    bonus = int(match.group(3)) if match.group(3) else 0
                    
                    rolagens = [random.randint(1, faces) for _ in range(qtd)]
                    maior_dado = max(rolagens)
                    resultado_final = maior_dado + bonus
                    soma_total = sum(rolagens) + bonus
                    
                    html_dados = []
                    for r in rolagens:
                        if r == faces:
                            html_dados.append(f"<span class='num_critico'>{r}</span> <span class='msg_critico'>(CRÍTICO!)</span>")
                        elif r == 1:
                            html_dados.append(f"<span class='num_falha'>{r}</span> <span class='msg_falha'>(VISH...)</span>")
                        else:
                            html_dados.append(str(r))
                    
                    # EXIBIÇÃO
                    st.markdown(f"<p class='destaque-neon'>RESULTADO: {resultado_final}</p>", unsafe_allow_html=True)
                    st.write(f"**LÓGICA:** MAIOR DADO ({maior_dado}) + BÔNUS ({bonus})")
                    
                    st.markdown(f"**DADOS ROLADOS:** {', '.join(html_dados)}", unsafe_allow_html=True)
                    
                    st.markdown(f"<p class='sub-destaque-neon'>TOTAL: {soma_total}</p>", unsafe_allow_html=True)
                    st.write(f"**LÓGICA:** SOMA DE TODOS OS DADOS + BÔNUS")
                    
                else: st.error("SINTAXE INVÁLIDA.")
            except Exception: st.error("ERRO NO PROCESSADOR.")

    with tab_combate:
        st.subheader(f"PONTOS DE AÇÃO: {st.session_state['pa']} / 10")
        if st.button("RECARREGAR PA"):
            st.session_state["pa"] = 10
            st.rerun()

    with tab_pericias:
        st.subheader("PERÍCIAS CADASTRADAS")
        st.write("● HACKEAMENTO")
        st.write("● MECÂNICA DE SUCATA")
