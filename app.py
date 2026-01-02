import streamlit as st
import random
import re

# --- FUNÇÃO PARA DISPARAR O ÁUDIO ---
def play_audio(url):
    # Injeta um HTML invisível que força o navegador a tocar o som uma vez
    # Usando type="audio/mp4" para compatibilidade com arquivos .m4a
    audio_html = f"""
        <audio autoplay style="display:none;">
            <source src="{url}" type="audio/mp4">
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# --- 1. CONFIGURAÇÃO E IDENTIDADE VISUAL ---
st.set_page_config(page_title="NEON-WALL TERMINAL", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono:wght@300;500&display=swap');

    /* Fundo com a sua imagem cyberpunk */
    .stApp {{
        background-image: url("https://raw.githubusercontent.com/wyxinne/RPG-FUTURISTA-SISTEMA/main/fundo%20cyberpunk.png");
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
    }}
    
    h1, h2, h3 {{
        color: #00ff41 !important;
        text-shadow: 0 0 10px #00ff41, 0 0 20px #ff00ff;
        font-family: 'Orbitron', sans-serif !important;
    }}
    
    label, p, span, div {{
        color: #ffff00 !important;
        font-family: 'Roboto Mono', monospace !important;
    }}

    .stTabs [data-baseweb="tab"] {{
        color: #00ff41 !important;
        border: 1px solid #ff00ff !important;
        background-color: rgba(0, 0, 0, 0.8) !important;
        font-family: 'Orbitron', sans-serif !important;
    }}

    .stButton>button {{
        width: 100%;
        border: 2px solid #00ff41 !important;
        background-color: #1a1a1a !important;
        color: #ff00ff !important;
        font-family: 'Orbitron', sans-serif !important;
        box-shadow: 4px 4px 0px #ffff00;
    }}

    /* Estilos de Crítico e Falha */
    .num_critico {{ color: #00ff00 !important; font-weight: 800; text-shadow: 0 0 10px #00ff00; }}
    .msg_critico {{ color: #00ff00 !important; font-size: 0.8em; font-weight: 400; }}
    .num_falha {{ color: #ff0000 !important; font-weight: 800; text-shadow: 0 0 10px #ff0000; }}
    .msg_falha {{ color: #ff0000 !important; font-size: 0.8em; font-style: italic; font-weight: 400; }}
    </style>
    """, unsafe_allow_html=True)

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
        st.subheader("TERMINAL DE DADOS NEURAIS")
        entrada = st.text_input("COMANDO (Ex: 2d20+3):", value="2d20+3", key="roll_final")
        
        # Link RAW do seu áudio m4a
        LINK_DO_AUDIO = "https://raw.githubusercontent.com/wyxinne/RPG-FUTURISTA-SISTEMA/main/dados%202.m4a"

        if st.button("🎲 PROCESSAR"):
            # O áudio dispara assim que clica no botão
            play_audio(LINK_DO_AUDIO)
            
            try:
                # Limpeza e processamento da string de dados
                match = re.match(r'(\d+)d(\d+)([+-]\d+)?', entrada.replace(" ", "").lower())
                if match:
                    qtd, faces = int(match.group(1)), int(match.group(2))
                    bonus = int(match.group(3)) if match.group(3) else 0
                    
                    rolagens = [random.randint(1, faces) for _ in range(qtd)]
                    maior_valor = max(rolagens)
                    resultado_final = maior_valor + bonus
                    
                    html_dados = []
                    for r in rolagens:
                        if r == faces:
                            html_dados.append(f"<span class='num_critico'>{r}</span> <span class='msg_critico'>(Crítico!)</span>")
                        elif r == 1:
                            html_dados.append(f"<span class='num_falha'>{r}</span> <span class='msg_falha'>(Vish...)</span>")
                        else:
                            html_dados.append(str(r))
                    
                    st.markdown(f"### 🚀 TOTAL: **{resultado_final}**")
                    st.write(f"**Cálculo:** {maior_valor} (Maior Dado) + ({bonus})")
                    st.markdown(f"**Dados Rolados:** {', '.join(html_dados)}", unsafe_allow_html=True)
                else: st.error("Erro de sintaxe. Use o formato: 2d20+3")
            except Exception: st.error("Falha no terminal neural.")

    with tab_combate:
        st.subheader(f"ENERGIA: {st.session_state['pa']} / 10 PA")
        if st.button("🕒 RECARREGAR PA"):
            st.session_state["pa"] = 10
            st.rerun()

    with tab_pericias:
        st.subheader("BANCO DE DADOS: PERÍCIAS")
        st.write("● Programação")
        st.write("● Mecânica")
