import streamlit as st
import random
import re

# --- 1. CONFIGURAÇÃO E IDENTIDADE VISUAL ---
st.set_page_config(page_title="NEON-WALL TERMINAL", layout="centered")

# Injeção de Fontes e CSS Customizado
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono:wght@300;500&display=swap');

    /* Background: Roxo Neon/Muralha (Top) para Cinza Sucata/Low-life (Bottom) */
    .stApp {
        background: linear-gradient(180deg, #1a0033 0%, #05080a 60%, #2c2c2c 100%);
        background-attachment: fixed;
    }
    
    /* Títulos em Verde Neon com Brilho Rosa */
    h1, h2, h3 {
        color: #00ff41 !important;
        text-shadow: 0 0 10px #00ff41, 0 0 20px #ff00ff;
        font-family: 'Orbitron', sans-serif !important;
    }
    
    /* Textos Gerais em Amarelo Neon */
    label, p, span, div {
        color: #ffff00 !important;
        font-family: 'Roboto Mono', monospace !important;
    }

    /* Estilização das Abas */
    .stTabs [data-baseweb="tab-list"] { gap: 12px; }
    .stTabs [data-baseweb="tab"] {
        color: #00ff41 !important;
        border: 1px solid #ff00ff !important;
        background-color: rgba(0,0,0,0.7);
        font-family: 'Orbitron', sans-serif !important;
        border-radius: 4px 4px 0px 0px;
    }

    /* Botões Neon com Sombra Amarela */
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
        box-shadow: 0px 0px 15px #ff00ff;
    }

    /* Cores Específicas para Críticos e Falhas */
    .critico { color: #00ff41; font-weight: bold; text-shadow: 0 0 8px #00ff41; }
    .falha { color: #ff3131; font-weight: bold; font-style: italic; text-shadow: 0 0 8px #ff3131; }
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
    # Inicialização de Variáveis de Estado
    if "pa" not in st.session_state: 
        st.session_state["pa"] = 10

    # Banco de Dados de Combate
    armas = {
        "Faca / Punhal": {"dano": "1d4", "trauma": 6},
        "Pistola Leve": {"dano": "1d6", "trauma": 6},
        "Pistola Pesada": {"dano": "1d10", "trauma": 6},
        "Fuzil de Assalto": {"dano": "2d8", "trauma": 8},
        "Foice (Rhaast)": {"dano": "2d10", "trauma": 10}
    }

    # Definição das Abas
    tab_combate, tab_rolagem, tab_pericias = st.tabs(["⚔️ COMBATE", "🎲 ROLAGEM LIVRE", "📊 PERÍCIAS"])

    # ABA 1: COMBATE
    with tab_combate:
        st.subheader(f"STATUS DE ENERGIA: {st.session_state['pa']} / 10 PA")
        st.progress(st.session_state['pa'] / 10)
        
        col1, col2 = st.columns(2)
        with col1:
            arma_sel = st.selectbox("EQUIPAMENTO ATIVO:", list(armas.keys()))
        with col2:
            mod_atrib = st.number_input("MOD. ATRIBUTO:", value=0, key="comb_mod")

        if st.button("🔥 EXECUTAR PROTOCOLO DE ATAQUE (-2 PA)"):
            if st.session_state["pa"] >= 2:
                st.session_state["pa"] -= 2
                d = armas[arma_sel]
                n, t = map(int, re.findall(r'\d+', d['dano']))
                roladas = [random.randint(1, t) for _ in range(n)]
                total = sum(roladas) + mod_atrib
                
                st.success(f"Dano Causado: {total} (Dados: {roladas})")
                st.rerun()
            else:
                st.warning("ENERGIA INSUFICIENTE. RECARREGUE O SISTEMA.")
        
        if st.button("🕒 RECARREGAR PONTOS DE AÇÃO"):
            st.session_state["pa"] = 10
            st.rerun()

    # ABA 2: ROLAGEM LIVRE (MAIOR DADO + BÔNUS)
    with tab_rolagem:
        st.subheader("TERMINAL DE DADOS NEURAIS")
        st.write("Sintaxe aceita: **2d20+3**, **1d10-1**, etc.")
        entrada = st.text_input("INPUT DE COMANDO:", value="2d20+3", key="roll_input")
        
        if st.button("🎲 PROCESSAR ROLAGEM"):
            try:
                # Limpa espaços e extrai valores
                limpo = entrada.replace(" ", "").lower()
                match = re.match(r'(\d+)d(\d+)([+-]\d+)?', limpo)
                
                if match:
                    qtd = int(match.group(1))
                    faces = int(match.group(2))
                    bonus = int(match.group(3)) if match.group(3) else 0
                    
                    rolagens = [random.randint(1, faces) for _ in range(qtd)]
                    maior_valor = max(rolagens)
                    resultado_final = maior_valor + bonus
                    
                    # Formatação de Críticos e Falhas com HTML
                    html_dados = []
                    for r in rolagens:
                        if r == faces:
                            html_dados.append(f"<span class='critico'>{r} (Crítico!)</span>")
                        elif r == 1:
                            html_dados.append(f"<span class='falha'>{r} (Vish...)</span>")
                        else:
                            html_dados.append(str(r))
                    
                    # Interface de Resultado
                    st.toast(f"Resultados brutos: {rolagens}", icon="🎲")
                    st.markdown(f"### 🚀 Resultado Total: **{resultado_final}**")
                    st.write(f"**Cálculo:** {maior_valor} (Maior Dado) + ({bonus}) (Bônus)")
                    st.markdown(f"**Análise dos Dados:** {', '.join(html_dados)}", unsafe_allow_html=True)
                else:
                    st.error("ERRO DE SINTAXE: Use o formato '2d20+5'.")
            except Exception:
                st.error("FALHA NO PROCESSAMENTO NEURAL.")

    # ABA 3: PERÍCIAS
    with tab_pericias:
        st.subheader("BANCO DE DADOS: PERÍCIAS")
        pericias_lista = {
            "Programação": "Interação com a Muralha e terminais.",
            "Mecânica": "Manuseio de sucata e cabos metálicos.",
            "Atletismo": "Movimentação em ambientes low-life.",
            "Furtividade": "Passar despercebido pelas luzes da cidade."
        }
        for p, d in pericias_lista.items():
            st.markdown(f"● **{p}**: {d}")
