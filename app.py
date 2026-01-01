import streamlit as st
import random
import re

# --- 1. CONFIGURAÇÃO E IDENTIDADE VISUAL ---
st.set_page_config(page_title="NEON-WALL TERMINAL", layout="centered")

# CSS para o visual: Roxo, Verde, Rosa e Amarelo Neon
st.markdown("""
    <style>
    /* Fundo degradê: Cidade/Muralha (Roxo/Preto) para Low-Life (Cinza Sucata) */
    .stApp {
        background: linear-gradient(180deg, #1a0033 0%, #05080a 70%, #2c2c2c 100%);
        background-attachment: fixed;
    }
    
    /* Estilo das Abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(0,0,0,0.5);
    }
    .stTabs [data-baseweb="tab"] {
        color: #00ff41 !important; /* Verde Neon */
        border: 1px solid #ff00ff !important; /* Rosa Neon */
        padding: 10px;
    }

    /* Títulos e Textos */
    h1, h2, h3 {
        color: #00ff41 !important;
        text-shadow: 0 0 10px #00ff41, 0 0 20px #ff00ff;
        font-family: 'Courier New', monospace;
    }
    
    label, p, span {
        color: #ffff00 !important; /* Amarelo Neon para detalhes */
        font-family: 'Courier New', monospace;
    }

    /* Botões estilo "Scrap Metal / Neon" */
    .stButton>button {
        width: 100%;
        border: 2px solid #00ff41 !important;
        background-color: #1a1a1a !important;
        color: #ff00ff !important; /* Rosa */
        border-radius: 2px !important;
        font-weight: bold;
        box-shadow: 4px 4px 0px #ffff00; /* Sombra Amarela */
    }
    .stButton>button:hover {
        background-color: #ff00ff !important;
        color: #000000 !important;
        box-shadow: 0px 0px 15px #ff00ff;
    }
    </style>
    """, unsafe_allow_index=True)

# --- 2. SISTEMA DE ACESSO ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]:
        return True

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
    # Inicialização de Variáveis
    if "pa" not in st.session_state: st.session_state["pa"] = 10

    # Banco de Dados
    armas = {
        "Faca / Punhal": {"dano": "1d4", "trauma": 6, "atrib": True},
        "Pistola Leve": {"dano": "1d6", "trauma": 6, "atrib": True},
        "Pistola Pesada": {"dano": "1d10", "trauma": 6, "atrib": True},
        "Fuzil de Assalto": {"dano": "2d8", "trauma": 8, "atrib": True},
        "Foice (Rhaast)": {"dano": "2d10", "trauma": 10, "atrib": True}
    }

    pericias = {
        "Atletismo": "Feitos físicos, escalar, correr.",
        "Mecânica": "Reparar sucata e cabos metálicos.",
        "Programação": "Hackear a muralha e sistemas.",
        "Combate Próximo": "Uso de armas brancas.",
        "Disparo": "Uso de armas de fogo."
    }

    # --- 3. INTERFACE DE ABAS ---
    tab_combate, tab_pericias, tab_lore = st.tabs(["⚔️ COMBATE", "📊 PERÍCIAS", "🌆 MUNDO"])

    with tab_combate:
        st.subheader(f"STATUS: {st.session_state['pa']} / 10 PA")
        st.progress(st.session_state['pa'] / 10)
        
        if st.button("🕒 RECARREGAR SISTEMA (+PA)"):
            st.session_state["pa"] = 10
            st.rerun()

        col1, col2 = st.columns(2)
        with col1:
            arma_sel = st.selectbox("ARMA:", list(armas.keys()))
        with col2:
            mod_atrib = st.number_input("MOD. ATRIBUTO:", value=0)

        if st.button("🔥 EXECUTAR ATAQUE (-2 PA)"):
            if st.session_state["pa"] >= 2:
                st.session_state["pa"] -= 2
                dados = armas[arma_sel]
                num, tipo = map(int, re.findall(r'\d+', dados['dano']))
                rolagem = sum([random.randint(1, tipo) for _ in range(num)])
                dano_final = rolagem + mod_atrib
                
                # Trauma x3
                trauma = random.randint(1, dados['trauma'])
                if trauma == dados['trauma']:
                    st.error(f"💥 CRÍTICO! DANO TRIPLO: {dano_final * 3}")
                else:
                    st.success(f"DANO: {dano_final}")
                st.rerun()
            else:
                st.warning("SEM ENERGIA!")

    with tab_pericias:
        st.subheader("BANCO DE DADOS: PERÍCIAS")
        for nome, desc in pericias.items():
            st.markdown(f"**{nome}**: {desc}")
        
        st.divider()
        p_sel = st.selectbox("TESTAR PERÍCIA:", list(pericias.keys()))
        if st.button("🎲 ROLAR 2d6"):
            r1, r2 = random.randint(1,6), random.randint(1,6)
            st.info(f"RESULTADO: {r1} + {r2} = {r1+r2}")

    with tab_lore:
        st.subheader("REDE DA MURALHA")
        st.write("A grande muralha separa o luxo corporativo da sucata inferior.")
        st.write("Cuidado com os cabos prateados expostos na zona de baixo.")
