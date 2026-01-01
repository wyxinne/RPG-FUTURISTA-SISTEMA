import streamlit as st
import random
import re

# --- 1. CONFIGURAÇÃO E IDENTIDADE VISUAL ---
st.set_page_config(page_title="NEON-WALL TERMINAL", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #1a0033 0%, #05080a 70%, #2c2c2c 100%);
        background-attachment: fixed;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        color: #00ff41 !important;
        border: 1px solid #ff00ff !important;
        background-color: rgba(0,0,0,0.6);
        padding: 10px;
    }
    h1, h2, h3 {
        color: #00ff41 !important;
        text-shadow: 0 0 10px #00ff41, 0 0 20px #ff00ff;
        font-family: 'Courier New', monospace;
    }
    label, p, span { color: #ffff00 !important; font-family: 'Courier New', monospace; }
    .stButton>button {
        width: 100%;
        border: 2px solid #00ff41 !important;
        background-color: #1a1a1a !important;
        color: #ff00ff !important;
        border-radius: 2px !important;
        font-weight: bold;
        box-shadow: 4px 4px 0px #ffff00;
    }
    .stButton>button:hover {
        background-color: #ff00ff !important;
        color: #000000 !important;
        box-shadow: 0px 0px 15px #ff00ff;
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
        else:
            st.error("ACESSO NEGADO.")
    return False

if check_password():
    if "pa" not in st.session_state: st.session_state["pa"] = 10

    # Banco de Dados Simples
    armas = {
        "Faca / Punhal": {"dano": "1d4", "trauma": 6},
        "Pistola Leve": {"dano": "1d6", "trauma": 6},
        "Pistola Pesada": {"dano": "1d10", "trauma": 6},
        "Fuzil de Assalto": {"dano": "2d8", "trauma": 8},
        "Foice (Rhaast)": {"dano": "2d10", "trauma": 10}
    }

    # --- 3. INTERFACE DE ABAS ---
    tab_combate, tab_rolagem, tab_pericias = st.tabs(["⚔️ COMBATE", "🎲 ROLAGEM LIVRE", "📊 PERÍCIAS"])

    with tab_combate:
        st.subheader(f"STATUS: {st.session_state['pa']} / 10 PA")
        st.progress(st.session_state['pa'] / 10)
        col1, col2 = st.columns(2)
        with col1: arma_sel = st.selectbox("ARMA:", list(armas.keys()))
        with col2: mod_atrib = st.number_input("MOD. ATRIBUTO:", value=0, key="atrib_combate")
        
        if st.button("🔥 ATACAR (-2 PA)"):
            if st.session_state["pa"] >= 2:
                st.session_state["pa"] -= 2
                d = armas[arma_sel]
                n, t = map(int, re.findall(r'\d+', d['dano']))
                roladas = [random.randint(1, t) for _ in range(n)]
                total = sum(roladas) + mod_atrib
                st.success(f"Dano: {total} {roladas}")
                st.rerun()
            else: st.warning("SEM ENERGIA!")

    with tab_rolagem:
        st.subheader("TERMINAL DE DADOS LIVRES")
        st.write("Digite no formato: **2d20+3** ou **1d10-1**")
        
        entrada = st.text_input("COMANDO DE VOZ (INPUT):", value="1d20+0")
        
        if st.button("🎲 PROCESSAR ROLAGEM"):
            try:
                # Regex para decompor 2d20+3
                match = re.match(r'(\d+)d(\d+)([+-]\d+)?', entrada.replace(" ", ""))
                if match:
                    qtd = int(match.group(1))
                    faces = int(match.group(2))
                    bonus = int(match.group(3)) if match.group(3) else 0
                    
                    rolagens = [random.randint(1, faces) for _ in range(qtd)]
                    maior_valor = max(rolagens)
                    resultado_final = maior_valor + bonus
                    
                    # Notificação visual (Toast no canto)
                    st.toast(f"Dados Rolados: {rolagens}", icon="🎲")
                    
                    st.markdown(f"""
                    ### Resultado Final: **{resultado_final}**
                    - **Dados**: {rolagens} (Maior: {maior_valor})
                    - **Bônus**: {bonus}
                    """)
                else:
                    st.error("Formato inválido! Use algo como '2d20+3'.")
            except Exception as e:
                st.error(f"Erro no processamento: {e}")

        st.divider()
        st.write("DADOS DISPONÍVEIS:")
        cols = st.columns(6)
        dados_padrao = [4, 6, 8, 10, 20, 100]
        for i, face in enumerate(dados_padrao):
            if cols[i].button(f"d{face}"):
                res = random.randint(1, face)
                st.info(f"d{face} rolado: {res}")

    with tab_pericias:
        st.subheader("PERÍCIAS CADASTRADAS")
        st.write("- **Programação**: Hackear a Muralha.")
        st.write("- **Mecânica**: Consertar cabos e sucata.")
