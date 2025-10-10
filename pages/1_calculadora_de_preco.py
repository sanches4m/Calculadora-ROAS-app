import streamlit as st

st.title("💰 Calculadora de Preço e Margem de Lucro")
st.write("Analise a lucratividade do seu preço atual e simule novos preços para atingir sua meta de margem de lucro.")

# --- Estado de Sessão Isolado para esta Calculadora ---
if 'preco_run_id' not in st.session_state:
    st.session_state.preco_run_id = 0
if 'preco_calculation_done' not in st.session_state:
    st.session_state.preco_calculation_done = False
if 'preco_results' not in st.session_state:
    st.session_state.preco_results = {}

def reset_preco_calculator():
    st.session_state.preco_run_id += 1
    st.session_state.preco_calculation_done = False
    st.session_state.preco_results = {}

# --- Dicionários e Constantes ---
PLATFORMAS = ["Shopee", "Mercado Livre", "Amazon", "Shein", "Magalu"]
TAXA_SHEIN = 0.20
TAXA_MAGALU_PERCENTUAL = 0.18
TAXA_MAGALU_FIXA = 5.00

# --- Entradas do Usuário na Barra Lateral ---
st.sidebar.header("Dados do Produto e Venda")
run_id = st.session_state.preco_run_id

# Inputs de Custo
custo_produto = st.sidebar.number_input("Custo do Produto (R$)", 0.01, key=f"preco_cp_{run_id}")
custo_embalagem = st.sidebar.number_input("Custo da Embalagem (R$)", 0.0, key=f"preco_ce_{run_id}")
taxa_imposto = st.sidebar.slider("Alíquota do Imposto (%)", 0.0, 30.0, 0.0, 0.5, help="MEI isento? Pode deixar em 0%.", key=f"preco_imp_{run_id}") / 100

# Inputs da Plataforma
plataforma_nome = st.sidebar.selectbox("Plataforma de Venda", PLATFORMAS, key=f"preco_plat_{run_id}")

comissao_percentual_manual = 0.0
if plataforma_nome == "Shopee":
    participa_frete_gratis = st.sidebar.radio("Faz parte do Frete Grátis?", ("Sim", "Não"), index=1, key=f"preco_shopee_frete_{run_id}")
elif plataforma_nome in ["Mercado Livre", "Amazon"]:
    comissao_percentual_manual = st.sidebar.number_input(f"Taxa de comissão da {plataforma_nome} (%)", 0.0, 100.0, 17.0, 0.5, key=f"preco_manual_comissao_{run_id}") / 100

# Input do Preço de Venda
preco_venda_atual = st.sidebar.number_input("Preço de Venda do Anúncio (R$)", 0.01, key=f"preco_pv_{run_id}")

# Botões de Ação
calculate_button = st.sidebar.button("Analisar Preço", use_container_width=True, type="primary")
st.sidebar.button("Resetar Calculadora de Preço", on_click=reset_preco_calculator, use_container_width=True)

# --- Lógica de Cálculo ---
if calculate_button:
    # Cálculo da comissão
    detalhe_comissao, comissao = "", 0.0
    if plataforma_nome == "Shopee":
        taxa_fixa_shopee = 4.00
        taxa_percentual = 0.20 if participa_frete_gratis == "Sim" else 0.14
        comissao = (preco_venda_atual * taxa_percentual) + taxa_fixa_shopee
        detalhe_comissao = f"Comissão Shopee ({taxa_percentual*100}% + R$ {taxa_fixa_shopee:.2f})"
    elif plataforma_nome in ["Mercado Livre", "Amazon"]:
        comissao = preco_venda_atual * comissao_percentual_manual
        detalhe_comissao = f"Comissão {plataforma_nome} ({comissao_percentual_manual*100:.1f}%)"
    elif plataforma_nome == "Shein":
        comissao = preco_venda_atual * TAXA_SHEIN
        detalhe_comissao = f"Comissão Shein ({TAXA_SHEIN*100}%)"
    elif plataforma_nome == "Magalu":
        comissao = (preco_venda_atual * TAXA_MAGALU_PERCENTUAL) + TAXA_MAGALU_FIXA
        detalhe_comissao = f"Comissão Magalu ({TAXA_MAGALU_PERCENTUAL*100}% + R$ {TAXA_MAGALU_FIXA:.2f})"

    # Cálculos de custos e lucro
    custo_total_produto = custo_produto + custo_embalagem
    valor_imposto = preco_venda_atual * taxa_imposto
    total_taxas = comissao + valor_imposto
    lucro_liquido = preco_venda_atual - custo_total_produto - total_taxas
    margem_lucro = (lucro_liquido / preco_venda_atual) * 100 if preco_venda_atual > 0 else 0

    # Armazenando na memória
    st.session_state.preco_calculation_done = True
    st.session_state.preco_results = {
        "preco_venda": preco_venda_atual, "custo_total_produto": custo_total_produto,
        "total_taxas": total_taxas, "lucro_liquido": lucro_liquido,
        "margem_lucro": margem_lucro, "detalhe_comissao": detalhe_comissao,
        "comissao": comissao, "valor_imposto": valor_imposto
    }

# --- Seção de Resultados ---
if st.session_state.preco_calculation_done:
    results = st.session_state.preco_results
    
    st.header("Análise do Preço Atual")
    
    col1, col2 = st.columns(2)
    col1.metric("Lucro Líquido por Venda", f"R$ {results['lucro_liquido']:.2f}")
    col2.metric("Margem de Lucro", f"{results['margem_lucro']:.2f}%")
    
    if results['lucro_liquido'] < 0:
        st.error("Atenção: Com este preço, você está tendo prejuízo na venda.")
    else:
        st.success("Este é o seu resultado com o preço de venda atual.")

    with st.expander("Ver detalhes da análise"):
        st.write(f"**Preço de Venda:** R$ {results['preco_venda']:.2f}")
        st.write(f"**Custo total (Produto + Embalagem):** R$ {results['custo_total_produto']:.2f}")
        st.write(f"**Taxas (Comissão + Imposto):** R$ {results['total_taxas']:.2f}")
        st.write(f"**Lucro Líquido:** R$ {results['lucro_liquido']:.2f}")
        st.write(f"**Margem de Lucro (%):** {results['margem_lucro']:.2f}%")
        st.caption(f"Detalhe taxas: {results['detalhe_comissao']} (R$ {results['comissao']:.2f}) + Imposto (R$ {results['valor_imposto']:.2f})")

    st.divider()

    # --- Passo 2: Simulador de Preço ---
    st.header("Passo 2: Simule um Novo Preço")
    
    # Define um range razoável para o slider, começando do preço atual
    min_slider = max(0.01, results['preco_venda'] * 0.8)
    max_slider = results['preco_venda'] * 2.0
    
    novo_preco = st.slider(
        "Arraste para encontrar o preço ideal:",
        min_value=min_slider,
        max_value=max_slider,
        value=results['preco_venda'],
        format="R$ %.2f"
    )

    # Recálculo em tempo real com o novo preço
    nova_comissao = 0.0
    if plataforma_nome == "Shopee":
        taxa_fixa_shopee = 4.00
        taxa_percentual = 0.20 if participa_frete_gratis == "Sim" else 0.14
        nova_comissao = (novo_preco * taxa_percentual) + taxa_fixa_shopee
    elif plataforma_nome in ["Mercado Livre", "Amazon"]:
        nova_comissao = novo_preco * comissao_percentual_manual
    elif plataforma_nome == "Shein":
        nova_comissao = novo_preco * TAXA_SHEIN
    elif plataforma_nome == "Magalu":
        nova_comissao = (novo_preco * TAXA_MAGALU_PERCENTUAL) + TAXA_MAGALU_FIXA

    novo_imposto = novo_preco * taxa_imposto
    novo_total_taxas = nova_comissao + novo_imposto
    novo_lucro = novo_preco - results['custo_total_produto'] - novo_total_taxas
    nova_margem = (novo_lucro / novo_preco) * 100 if novo_preco > 0 else 0
    
    st.subheader("Resultado da Simulação")
    sim_col1, sim_col2 = st.columns(2)
    sim_col1.metric("Novo Lucro Líquido", f"R$ {novo_lucro:.2f}")
    sim_col2.metric("Nova Margem de Lucro", f"{nova_margem:.2f}%")
