import streamlit as st

# --- 1. CONFIGURAÇÃO DE TELA E ESTILO (O LOOK NEON) ---
st.set_page_config(page_title="NEON-WALL TERMINAL", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono:wght@300;500&family=Press+Start+2P&display=swap');

    /* FUNDO PERSONALIZADO */
    .stApp {
        background-image: url("https://raw.githubusercontent.com/wyxinne/RPG-FUTURISTA-SISTEMA/main/fundo%20cyberpunk.png");
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
    }

    /* ESTILO GLOBAL DE TEXTO */
    html, body, [data-testid="stAppViewContainer"], button, input, .stTabs {
        text-transform: uppercase !important;
        font-family: 'Roboto Mono', monospace !important;
    }

    h1, h2, h3 {
        color: #00ff41 !important; /* Verde Neon */
        text-shadow: 0 0 10px #00ff41;
        font-family: 'Orbitron', sans-serif !important;
    }
    
    label, p, span {
        color: #ffff00 !important; /* Amarelo Neon */
    }

    /* CAIXAS DE CYBERWARE PRATEADAS */
    .stTextInput input {
        background-color: rgba(192, 192, 192, 0.2) !important;
        border: 1px solid #C0C0C0 !important;
        color: #C0C0C0 !important;
    }

    /* BOTÕES CUSTOMIZADOS */
    .stButton>button {
        width: 100%;
        border: 1px solid #00ff41 !important;
        background-color: #1a1a1a !important;
        color: #00ff41 !important;
        font-family: 'Orbitron', sans-serif !important;
    }
    
    .stButton>button:hover {
        border: 1px solid #ff00ff !important; /* Rosa Neon */
        color: #ff00ff !important;
        box-shadow: 0 0 15px #ff00ff;
    }

    /* TABS (ROXO NEON) */
    .stTabs [data-baseweb="tab-list"] { background-color: rgba(0,0,0,0.7); }
    .stTabs [data-baseweb="tab"] { color: #bc13fe; border: 1px solid #bc13fe; margin: 5px; }
    .stTabs [aria-selected="true"] { background-color: #bc13fe !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ÁUDIO DE AMBIÊNCIA ---
st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3") 

# --- 3. BANCO DE DADOS EM MEMÓRIA ---
if "personagens" not in st.session_state:
    st.session_state.personagens = {
        "P1": {"nome": "OPERADOR_01", "ocupacao": "SCAVENGER", "hp": 20, "hp_max": 20, "strain": 0, "strain_max": 10},
    }

if "perfil_logado" not in st.session_state:
    st.session_state.perfil_logado = None

# --- 4. TELA DE LOGIN ---
if not st.session_state.perfil_logado:
    st.markdown("<h1 style='text-align: center;'>IDENTIFICAÇÃO NECESSÁRIA</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        perfil = st.selectbox("ACESSO:", ["JOGADOR", "MESTRE"])
        chave = st.text_input("CHAVE DE REDE:", type="password")
        if st.button("CONECTAR"):
            if perfil == "MESTRE" and chave == "mestre":
                st.session_state.perfil_logado = "MESTRE"
                st.rerun()
            elif perfil == "JOGADOR" and chave == "cyber2024":
                st.session_state.perfil_logado = "JOGADOR"
                st.rerun()
            else:
                st.error("CHAVE INCORRETA.")
else:
    # --- 5. INTERFACE DO MESTRE ---
    if st.session_state.perfil_logado == "MESTRE":
        abas_mestre = st.tabs(["🛰️ CONTROLE GERAL", "🧬 CRIAR PERSONAGENS", "🎲 ROLAGENS"])
        
        with abas_mestre[0]:
            st.header("PAINEL DE MONITORAMENTO GLOBAL")
            for p_id, dados in st.session_state.personagens.items():
                with st.expander(f"📡 {dados['nome']} | HP: {dados['hp']} | ST: {dados['strain']}"):
                    st.write(f"Ocupação: {dados['ocupacao']}")
                    if st.button(f"RESTAURAR SISTEMA DE {dados['nome']}", key=f"btn_{p_id}"):
                        st.session_state.personagens[p_id]['hp'] = dados['hp_max']
                        st.session_state.personagens[p_id]['strain'] = 0
                        st.rerun()

        with abas_mestre[1]:
            st.header("CADASTRAR NOVO PERFIL")
            n_id = st.text_input("ID DE LOGIN (Ex: Jogador 2)")
            n_nome = st.text_input("NOME DO PERSONAGEM")
            n_hp = st.number_input("HP MÁX", value=20)
            n_st = st.number_input("STRAIN MÁX", value=10)
            if st.button("SALVAR NA MURALHA"):
                st.session_state.personagens[n_id] = {"nome": n_nome, "ocupacao": "INDETERMINADO", "hp": n_hp, "hp_max": n_hp, "strain": 0, "strain_max": n_st}
                st.success("REGISTRO CRIADO.")

    # --- 6. INTERFACE DO JOGADOR ---
    else:
        p_id = st.selectbox("ASSUMIR IDENTIDADE:", list(st.session_state.personagens.keys()))
        dados = st.session_state.personagens[p_id]
        abas_jog = st.tabs(["STATUS", "COMBATE", "ROLAGEM LIVRE"])
        
        with abas_jog[0]: # ABA STATUS PEDIDA
            col_id, col_cyber = st.columns([1.5, 1])
            with col_id:
                st.session_state.personagens[p_id]['nome'] = st.text_input("NOME:", value=dados['nome'])
                st.session_state.personagens[p_id]['ocupacao'] = st.text_input("OCUPAÇÃO:", value=dados['ocupacao'])
                st.markdown("---")
                
                # HP LÓGICA
                hp_m = st.number_input("HP MÁXIMO (EDITÁVEL):", value=dados['hp_max'])
                st.session_state.personagens[p_id]['hp_max'] = hp_m
                st.write(f"VIDA: {dados['hp']} / {hp_m}")
                st.progress(min(max(dados['hp']/max(1, hp_m), 0.0), 1.0))
                
                c1, c2, c3, c4 = st.columns(4)
                if c1.button("--"): st.session_state.personagens[p_id]['hp'] -= 5
                if c2.button("-"): st.session_state.personagens[p_id]['hp'] -= 1
                if c3.button("+"): st.session_state.personagens[p_id]['hp'] += 1
                if c4.button("++"): st.session_state.personagens[p_id]['hp'] += 5

                st.markdown("---")

                # STRAIN LÓGICA CORES
                st_m = st.number_input("LIMITE DE SOBRECARGA:", value=dados['strain_max'])
                st.session_state.personagens[p_id]['strain_max'] = st_m
                
                cor_st = "#ffff00" # Amarelo
                if dados['strain'] >= (st_m / 2): cor_st = "#ffa500" # Laranja
                if dados['strain'] >= (st_m - 2): cor_st = "#ff0000" # Vermelho
                
                st.markdown(f"SOBRECARGA: <span style='color:{cor_st}; font-size:1.2em; font-weight:bold;'>{dados['strain']} / {st_m}</span>", unsafe_allow_html=True)
                st.progress(min(max(dados['strain']/max(1, st_m), 0.0), 1.0))
                
                sc1, sc2 = st.columns(2)
                if sc1.button("- STRAIN"): st.session_state.personagens[p_id]['strain'] -= 1
                if sc2.button("+
