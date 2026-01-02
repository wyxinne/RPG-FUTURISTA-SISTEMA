import streamlit as st
import random
import re

# --- 1. CONFIGURAÇÃO E IDENTIDADE VISUAL ---
st.set_page_config(page_title="NEON-WALL TERMINAL", layout="centered")

st.markdown("""
    <style>
    /* Importando as fontes */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono:wght@300;500&display=swap');

    /* --- CONFIGURAÇÃO DO FUNDO COM IMAGEM --- */
    .stApp {
        /* 1. COLOQUE O LINK DA SUA IMAGEM DENTRO DAS ASPAS ABAIXO */
        background-image: url("https://github.com/wyxinne/RPG-FUTURISTA-SISTEMA/blob/main/fundo%20cyberpunk.png");
        
        /* Ajusta a imagem para cobrir toda a tela sem distorcer */
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
        
        /* --- EFEITO DE OPACIDADE/ESCURECIMENTO --- */
        /* Cor preta com 70% de transparência (mude o 0.7 para mais ou menos escuro) */
        background-color: rgba(0, 0, 0, 0.7);
        /* Mistura a cor preta com a imagem para escurecê-la */
        background-blend-mode: overlay;
    }
    
    /* --- Resto do Estilo Neon (Títulos, Botões, etc.) --- */
    h1, h2, h3 {
        color: #00ff41 !important;
        text-shadow: 0 0 10px #00ff41, 0 0 20px #ff00ff;
        font-family: 'Orbitron', sans-serif !important;
    }
    
    label, p, span, div {
        color: #ffff00 !important;
        font-family: 'Roboto Mono', monospace !important;
    }

    /* Abas com fundo semi-transparente para ler sobre a imagem */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        color: #00ff41 !important;
        border: 1px solid #ff00ff !important;
        background-color: rgba(0, 0, 0, 0.8) !important; /* Mais escuro para contraste */
        font-family: 'Orbitron', sans-serif !important;
        border-radius: 4px 4px 0px 0px;
    }

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

    /* Estilos de Crítico e Falha com tamanhos diferentes */
    .num_critico { color: #00ff00 !important; font-weight: 800; text-shadow: 0 0 10px #00ff00; }
    .msg_critico { color: #00ff00 !important; font-size: 0.8em; font-weight: 400; }
    .num_falha { color: #ff0000 !important; font-weight: 800; text-shadow: 0 0 10px #ff0000; }
    .msg_falha { color: #ff0000 !important; font-size: 0.8em; font-style: italic; font-weight: 400; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SISTEMA DE ACESSO ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    
    if st.session_state["password_correct"]:
        return True

    st.title("📟 MURALHA DE SEGURANÇA")
    st.write("Insira a chave de criptografia para acessar o terminal.")
    password = st.text_input("CHAVE DA REDE:", type="password")
    
    if st.button("CONECTAR"):
        if password == "cyber2024":
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("ACESSO NEGADO: Assinatura digital inválida.")
    return False

# --- 3. CONTEÚDO PRINCIPAL ---
if check_password():
    if "pa" not in st.session_state: st.session_state["pa"] = 10

    tab_combate, tab_rolagem, tab_pericias = st.tabs(["⚔️ COMBATE", "🎲 ROLAGEM LIVRE", "📊 PERÍCIAS"])

    with tab_combate:
        st.subheader(f"ENERGIA: {st.session_state['pa']} / 10 PA")
        if st.button("🕒 RECARREGAR PA"):
            st.session_state["pa"] = 10
            st.rerun()
        st.write("Módulo de combate pronto.")

    with tab_rolagem:
        st.subheader("TERMINAL DE DADOS NEURAIS")
        entrada = st.text_input("COMANDO (Ex: 2d20+3):", value="2d20+3", key="roll_final")
        
        if st.button("🎲 PROCESSAR"):
            try:
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
                else: st.error("Erro de sintaxe.")
            except Exception: st.error("Falha no terminal.")

    with tab_pericias:
        st.subheader("PERÍCIAS")
        st.write("- Programação (Muralha)")
