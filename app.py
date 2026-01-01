import streamlit as st
import random
import re

# --- 1. CONFIGURAÇÃO E IDENTIDADE VISUAL ---
st.set_page_config(page_title="NEON-WALL TERMINAL", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono:wght@300;500&display=swap');

    .stApp {
        background: linear-gradient(180deg, #1a0033 0%, #05080a 60%, #2c2c2c 100%);
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

    .stTabs [data-baseweb="tab"] {
        color: #00ff41 !important;
        border: 1px solid #ff00ff !important;
        background-color: rgba(0,0,0,0.7);
        font-family: 'Orbitron', sans-serif !important;
    }

    .stButton>button {
        width: 100%;
        border: 2px solid #00ff41 !important;
        background-color: #1a1a1a !important;
        color: #ff00ff !important;
        font-family: 'Orbitron', sans-serif !important;
        box-shadow: 4px 4px 0px #ffff00;
    }

    /* ESTILOS DE CRÍTICO E FALHA SOLICITADOS */
    .critico_vibrante { 
        color: #00ff00 !important; /* Verde Totalmente Vibrante */
        font-weight: 800; 
        text-shadow: 0 0 12px #00ff00;
    }
    .falha_vibrante { 
        color: #ff0000 !important; /* Vermelho Totalmente Vibrante */
        font-weight: 800; 
        font-style: italic;
        text-shadow: 0 0 12px #ff0000;
    }
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

    with tab_combate:
        st.subheader(f"PA: {st.session_state['pa']} / 10")
        st.write("Módulo de combate pronto.")

    with tab_rolagem:
        st.subheader("TERMINAL DE DADOS NEURAIS")
        entrada = st.text_input("INPUT:", value="2d20+3", key="roll_in")
        
        if st.button("🎲 PROCESSAR ROLAGEM"):
            try:
                match = re.match(r'(\d+)d(\d+)([+-]\d+)?', entrada.replace(" ", "").lower())
                if match:
                    qtd, faces = int(match.group(1)), int(match.group(2))
                    bonus = int(match.group(3)) if match.group(3) else 0
                    
                    rolagens = [random.randint(1, faces) for _ in range(qtd)]
                    maior_valor = max(rolagens)
                    resultado_final = maior_valor + bonus
                    
                    # Formatação Vibrante
                    html_dados = []
                    for r in rolagens:
                        if r == faces:
                            html_dados.append(f"<span class='critico_vibrante'>{r} Crítico!</span>")
                        elif r == 1:
                            html_dados.append(f"<span class='falha_vibrante'>{r} Vish...</span>")
                        else:
                            html_dados.append(str(r))
                    
                    st.markdown(f"### 🚀 Total: **{resultado_final}**")
                    st.write(f"**Cálculo:** {maior_valor} + ({bonus})")
                    st.markdown(f"**Dados:** {', '.join(html_dados)}", unsafe_allow_html=True)
                else: st.error("Erro de sintaxe.")
            except Exception: st.error("Falha no sistema.")

    with tab_pericias:
        st.subheader("PERÍCIAS")
        st.write("Consulte o Mestre.")
