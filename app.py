import streamlit as st

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="NEON-WALL TERMINAL", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono:wght@300;500&display=swap');
    
    .stApp { background-color: #0a0a0a; color: #ffff00; font-family: 'Roboto Mono', monospace; }
    
    /* Cores das barras */
    .stProgress > div > div > div > div { background-color: #00ff41; } /* Verde padrão */
    
    .stTextInput input { background-color: rgba(192, 192, 192, 0.1) !important; color: #C0C0C0 !important; border: 1px solid #C0C0C0 !important; }
    
    .stButton>button { border: 1px solid #00ff41 !important; background-color: #1a1a1a !important; color: #00ff41 !important; font-family: 'Orbitron', sans-serif !important; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE DADOS (SIMULANDO BANCO DE DADOS) ---
if "personagens" not in st.session_state:
    # Fichas iniciais para teste
    st.session_state.personagens = {
        "Jogador 1": {"nome": "Player 1", "ocupacao": "Runner", "hp": 20, "hp_max": 20, "strain": 0, "strain_max": 10},
        "Jogador 2": {"nome": "Player 2", "ocupacao": "Tech", "hp": 15, "hp_max": 15, "strain": 2, "strain_max": 8}
    }

if "perfil_logado" not in st.session_state:
    st.session_state.perfil_logado = None

# --- FLUXO DE ACESSO ---
if not st.session_state.perfil_logado:
    st.title("SISTEMA DE ACESSO CENTRAL")
    
    col_login, _ = st.columns([1, 2])
    with col_login:
        perfil = st.selectbox("SELECIONE O PERFIL:", ["JOGADOR", "MESTRE"])
        chave = st.text_input("CHAVE DE ACESSO:", type="password")
        
        if st.button("CONECTAR"):
            if perfil == "MESTRE" and chave == "mestre":
                st.session_state.perfil_logado = "MESTRE"
                st.rerun()
            elif perfil == "JOGADOR" and chave == "cyber2024":
                st.session_state.perfil_logado = "JOGADOR"
                st.rerun()
            else:
                st.error("CHAVE INVÁLIDA.")
else:
    # --- INTERFACE LOGADA ---
    st.sidebar.write(f"SESSÃO: {st.session_state.perfil_logado}")
    if st.sidebar.button("SAIR"):
        st.session_state.perfil_logado = None
        st.rerun()

    if st.session_state.perfil_logado == "MESTRE":
        abas = st.tabs(["CONTROLE GERAL", "CRIAR PERSONAGENS", "ROLAGEM"])
        
        with abas[0]: # CONTROLE GERAL
            st.header("🛰️ MONITORAMENTO DE SQUAD")
            for p_id, dados in st.session_state.personagens.items():
                with st.expander(f"{dados['nome']} ({dados['ocupacao']})"):
                    c1, c2, c3 = st.columns(3)
                    c1.metric("HP", f"{dados['hp']}/{dados['hp_max']}")
                    c2.metric("STRAIN", f"{dados['strain']}/{dados['strain_max']}")
                    # Permitir mestre editar rápido
                    if c3.button(f"CURAR {dados['nome']}"):
                        st.session_state.personagens[p_id]['hp'] = dados['hp_max']
                        st.rerun()

        with abas[1]: # CRIAR PERSONAGENS
            st.header("🧬 GERADOR DE PERFIS")
            novo_id = st.text_input("ID DO JOGADOR (Ex: Jogador 3)")
            n_nome = st.text_input("NOME DO PERSONAGEM")
            n_hp = st.number_input("HP MÁXIMO", value=20)
            n_st = st.number_input("STRAIN MÁXIMO", value=10)
            if st.button("CADASTRAR NO SISTEMA"):
                st.session_state.personagens[novo_id] = {
                    "nome": n_nome, "ocupacao": "Desconhecido", 
                    "hp": n_hp, "hp_max": n_hp, "strain": 0, "strain_max": n_st
                }
                st.success(f"{n_nome} adicionado!")

    else: # INTERFACE DO JOGADOR
        # Seleção de qual personagem este jogador está controlando
        p_id = st.selectbox("CONFIRME SEU PERFIL:", list(st.session_state.personagens.keys()))
        dados = st.session_state.personagens[p_id]

        abas = st.tabs(["STATUS", "COMBATE", "ROLAGEM"])
        
        with abas[0]: # ABA STATUS PEDIDA
            col_id, col_cyber = st.columns([1.5, 1])
            with col_id:
                # NOME E OCUPAÇÃO
                st.session_state.personagens[p_id]['nome'] = st.text_input("NOME:", value=dados['nome'])
                st.session_state.personagens[p_id]['ocupacao'] = st.text_input("OCUPAÇÃO:", value=dados['ocupacao'])
                
                st.markdown("---")
                
                # HP COM CLIQUE DUPLO NO MÁXIMO
                hp_max = st.number_input("HP MÁXIMO:", value=dados['hp_max'], step=1)
                st.session_state.personagens[p_id]['hp_max'] = hp_max
                
                st.write(f"INTEGRIDADE: {dados['hp']} / {hp_max}")
                st.progress(min(dados['hp']/max(1, hp_max), 1.0))
                
                c1, c2, c3, c4 = st.columns(4)
                if c1.button("--"): st.session_state.personagens[p_id]['hp'] -= 5
                if c2.button("-"): st.session_state.personagens[p_id]['hp'] -= 1
                if c3.button("+"): st.session_state.personagens[p_id]['hp'] += 1
                if c4.button("++"): st.session_state.personagens[p_id]['hp'] += 5

                st.markdown("---")

                # STRAIN COM CORES DINÂMICAS
                st_max = st.number_input("LIMITE DE STRAIN:", value=dados['strain_max'], step=1)
                st.session_state.personagens[p_id]['strain_max'] = st_max
                
                # Lógica de cor
                cor = "yellow"
                if dados['strain'] >= (st_max / 2): cor = "orange"
                if dados['strain'] >= (st_max - 2): cor = "red"
                
                st.markdown(f"SOBRECARGA: <span style='color:{cor};'>{dados['strain']} / {st_max}</span>", unsafe_allow_html=True)
                st.progress(min(dados['strain']/max(1, st_max), 1.0))
                
                sc1, sc2 = st.columns(2)
                if sc1.button("- STRAIN"): st.session_state.personagens[p_id]['strain'] -= 1
                if sc2.button("+ STRAIN"): st.session_state.personagens[p_id]['strain'] += 1

            with col_cyber:
                st.subheader("LISTA DE CYBERWARE")
                for i in range(5):
                    ca, cb = st.columns([3, 1])
                    ca.text_input(f"DESCRIÇÃO {i+1}", key=f"desc_{p_id}_{i}")
                    cb.text_input("ST", key=f"st_{p_id}_{i}")
