import streamlit as st
import random
import re

# --- 1. CONFIGURAÇÃO E IDENTIDADE VISUAL (RESTALRAÇÃO TOTAL) ---
st.set_page_config(page_title="NEON-WALL TERMINAL", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono:wght@300;500&display=swap');

    /* Fundo com a sua imagem cyberpunk */
    .stApp {
        background-image: url("https://raw.githubusercontent.com/wyxinne/RPG-FUTURISTA-SISTEMA/main/fundo%20cyberpunk.png");
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
    }
    
    /* Títulos Verde Neon com Glow Rosa */
    h1, h2, h3 {
        color: #00ff41 !important;
        text-shadow: 0 0 10px #00ff41, 0 0 20px #ff00ff;
        font-family: 'Orbitron', sans-serif !important;
    }
    
    /* Textos Gerais Amarelo Neon */
    label, p, span, div {
        color: #ffff00 !important;
        font-family: 'Roboto Mono', monospace !important;
    }

    /* Estilo das Abas */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        color: #00ff41 !important;
        border: 1px solid #ff00ff !important;
        background-color: rgba(0, 0, 0, 0.85) !important;
        font-family: 'Orbitron', sans-serif !important;
        border-radius: 4px 4px 0px 0px;
    }

    /* Botões Neon com Sombra */
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

    /* Configurações Vibrantes de Crítico e Falha */
    .num_critico { color: #00ff00 !important; font-weight: 800; text-shadow: 0 0 15px #00ff00; font-size: 1.2em; }
    .msg_critico { color: #00ff00 !important; font-size: 0.85em; font-weight: 400; }
    
    .num_falha { color: #ff0000 !important; font-weight: 800; text-shadow: 0 0 15px #ff0000; font-size: 1.2em; }
    .msg_falha { color: #ff0000 !important; font-size: 0.85em; font-style: italic; font-weight: 400; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO DE ÁUDIO ---
def play_dice_sound():
    url_audio = "https://raw.githubusercontent.com/wyxinne/RPG-FUTURISTA-SISTEMA/main/dados%202.m4a"
    audio_html = f"""
        <audio autoplay style="display:none;">
            <source src="{url_audio}" type="audio/mp4">
        </audio>
    """
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

    tab_combate, tab_rolagem, tab_pericias = st.tabs(["⚔️ COMBATE", "🎲 ROLAGEM LIVRE", "📊 PERÍCIAS"])

    with tab_rolagem:
        st.subheader("TERMINAL DE DADOS INDEPENDENTES")
        entrada = st.text_input("DIGITE SEUS DADOS E BÔNUS (Ex: 2d20+3):", value="2d20+3", key="roll_main")
        
        if st.button("🎲 ROLAR"):
            play_dice_sound() # Som disparado no clique
            
            try:
                # Processamento da string (ex: 2d20+5)
                match = re.match(r'(\d+)d(\d+)([+-]\d+)?', entrada.replace(" ", "").lower())
                if match:
                    qtd, faces = int(match.group(1)), int(match.group(2))
                    bonus = int(match.group(3)) if match.group(3) else 0
                    
                    rolagens = [random.randint(1, faces) for _ in range(qtd)]
                    maior_valor = max(rolagens)
                    resultado_final = maior_valor + bonus
                    
                    # Montagem do HTML dos dados individuais
                    html_dados = []
                    for r in rolagens:
                        if r == faces:
                            html_dados.append(f"<span class='num_critico'>{r}</span> <span class='msg_critico'>(Crítico!)</span>")
                        elif r == 1:
                            html_dados.append(f"<span class='num_falha'>{r}</span> <span class='msg_falha'>(Vish...)</span>")
                        else:
                            html_dados.append(str(r))
                    
                    st.markdown(f"### 🚀 TOTAL: **{resultado_final}**")
                    st.write(f"**Lógica:** Maior Dado ({maior_valor}) + Bônus ({bonus})")
                    st.markdown(f"**Dados rolados:** {', '.join(html_dados)}", unsafe_allow_html=True)
                else: st.error("Sintaxe inválida, operador.")
            except Exception: st.error("Erro no processador neural.")

    with tab_combate:
        st.subheader(f"PONTOS DE AÇÃO: {st.session_state['pa']} / 10")
        if st.button("🕒 RECARREGAR SISTEMA (PA)"):
            st.session_state["pa"] = 10
            st.rerun()

    with tab_pericias:
        st.subheader("BANCO DE DADOS: PERÍCIAS")
        st.write("● Hackeamento de Sistemas")
        st.write("● Sobrevivência Urbana")
