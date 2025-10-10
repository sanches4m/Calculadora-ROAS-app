import streamlit as st

# --- INICIALIZAÇÃO DO ESTADO DE SESSÃO (COM NOVAS VARIÁVEIS) ---
# Usado para forçar o reset dos widgets de input
if 'run_id' not in st.session_state:
    st.session_state.run_id = 0
# Usado para controlar a exibição dos resultados
if 'calculation_done' not in st.session_state:
    st.session_state.calculation_done = False
# Usado para armazenar os resultados
if 'results' not in st.session_state:
    st.session_state.results = {}

# --- FUNÇÃO DE RESET ---
def reset_calculator():
    """ Reseta os inputs e limpa os resultados da memória. """
    st.session_state.run_id += 1
    st.session_state.calculation_done = False
    st.session_state.results = {}

# --- Interface do App ---
st.set_page_config(page_title="Calculadora de ROAS e Lucro", layout="centered")
st.title("📈 Calculadora de ROAS e Lucratividade")
st.write("Calcule o ponto de equilíbrio e o ROAS ideal para atingir sua meta de lucro.")

# --- Dicionários e Constantes ---
PLATFORMAS = ["Shopee", "Mercado Livre", "Amazon", "Shein", "Magalu"]
TAXA_SHEIN = 0.20
TAXA_MAGALU_PERCENTUAL = 0.18
TAXA_MAGALU_FIXA = 5.00

# --- Entradas do Usuário (Inputs) na barra lateral ---
st.sidebar.header("Passo 1: Insira os Dados da Venda")
valor_venda = st.sidebar.number_input("Valor da Venda (R$)", min_value=0.01, format="%.2f", key=f"valor_venda_{st.session_state.run_id}")
custo_produto = st.sidebar.number_input("Custo do Produto (R$)", min_value=0.0, format="%.2f", key=f"custo_produto_{st.session_state.run_id}")
custo_embalagem = st.sidebar.number_input("Custo da Embalagem (R$)", min_value=0.0, format="%.2f", key=f"custo_embalagem_{st.session_state.run_id}")
plataforma_nome = st.sidebar.selectbox("Plataforma", options=PLATFORMAS, key=f"plataforma_{st.session_state.run_id}")

# --- INPUTS CONDICIONAIS POR PLATAFORMA ---
comissao_percentual_manual = 0.0
if plataforma_nome == "Shopee":
    participa_frete_gratis = st.sidebar.radio("Faz parte do Frete Grátis?", ("Sim", "Não"), index=1, key=f"shopee_frete_{st.session_state.run_id}")
elif plataforma_nome in ["Mercado Livre", "Amazon"]:
    comissao_percentual_manual = st.sidebar.number_input(f"Taxa de comissão da {plataforma_nome} (%)", 0.0, 100.0, 17.0, 0.5, key=f"manual_comissao_{st.session_state.run_id}") / 100
taxa_imposto = st.sidebar.slider("Alíquota do Imposto (%)", 0.0, 30.0, 0.0, 0.5, help="MEI isento? Pode deixar em 0%.", key=f"imposto_{st.session_state.run_id}") / 100

# --- BOTÕES DE AÇÃO ---
col1, col2 = st.sidebar.columns(2)
calculate_button = col1.button("Calcular", use_container_width=True, type="primary")
reset_button = col2.button("Resetar", on_click=reset_calculator, use_container_width=True)

# --- A lógica do botão agora SÓ CALCULA E ARMAZENA OS DADOS ---
if calculate_button:
    # --- Cálculos ---
    detalhe_comissao, comissao = "", 0.0
    if plataforma_nome == "Shopee":
        taxa_fixa_shopee = 4.00
        taxa_percentual = 0.20 if participa_frete_gratis == "Sim" else 0.14
        comissao = (valor_venda * taxa_percentual) + taxa_fixa_shopee
        detalhe_comissao = f"Comissão Shopee ({taxa_percentual*100}% + R$ {taxa_fixa_shopee:.2f})"
    elif plataforma_nome in ["Mercado Livre", "Amazon"]:
        taxa_percentual = comissao_percentual_manual
        comissao = valor_venda * taxa_percentual
        detalhe_comissao = f"Comissão {plataforma_nome} ({taxa_percentual*100:.1f}%)"
    elif plataforma_nome == "Shein":
        comissao = valor_venda * TAXA_SHEIN
        detalhe_comissao = f"Comissão Shein ({TAXA_SHEIN*100}%)"
    elif plataforma_nome == "Magalu":
        comissao = (valor_venda * TAXA_MAGALU_PERCENTUAL) + TAXA_MAGALU_FIXA
        detalhe_comissao = f"Comissão Magalu ({TAXA_MAGALU_PERCENTUAL*100}% + R$ {TAXA_MAGALU_FIXA:.2f})"
    
    valor_imposto = valor_venda * taxa_imposto
    custos_totais_sem_ads = custo_produto + custo_embalagem + comissao + valor_imposto
    lucro_bruto_por_venda = valor_venda - custos_totais_sem_ads

    # Armazenando os resultados na "memória"
    st.session_state.calculation_done = True
    st.session_state.results = {
        "lucro_bruto": lucro_bruto_por_venda,
        "valor_venda": valor_venda,
        "detalhe_custos": {
            "detalhe_comissao": detalhe_comissao,
            "comissao": comissao,
            "valor_imposto": valor_imposto,
            "custo_produto_embalagem": custo_produto + custo_embalagem,
            "custos_totais_sem_ads": custos_totais_sem_ads
        }
    }

# --- NOVA SEÇÃO: MOSTRA OS RESULTADOS SE ELES EXISTIREM NA MEMÓRIA ---
if st.session_state.calculation_done:
    results = st.session_state.results
    lucro_bruto = results["lucro_bruto"]
    
    st.header("Resultados do Ponto de Equilíbrio")
    col1, col2 = st.columns(2)
    col1.metric("Lucro Bruto por Venda (sem Ads)", f"R$ {lucro_bruto:.2f}")

    if lucro_bruto <= 0:
        st.error("AVISO: A venda já resulta em prejuízo antes dos anúncios.")
        col2.metric("ROAS de Equilíbrio", "PREJUÍZO")
    else:
        roas_equilibrio = results["valor_venda"] / lucro_bruto
        col2.metric("ROAS de Equilíbrio", f"{roas_equilibrio:.2f}")
        st.info("Este é o ROAS mínimo para não ter prejuízo.")

    with st.expander("Ver detalhes dos custos"):
        custos = results["detalhe_custos"]
        st.write(f"**Lucro Líquido (sem Ads): R$ {lucro_bruto:.2f}**")
        st.write(f"- {custos['detalhe_comissao']}: R$ {custos['comissao']:.2f}")
        st.write(f"- Valor do Imposto: R$ {custos['valor_imposto']:.2f}")
        st.write(f"- Custo Produto + Embalagem: R$ {custos['custo_produto_embalagem']:.2f}")
        st.write("---")
        st.write(f"**Custos Totais (sem Ads): R$ {custos['custos_totais_sem_ads']:.2f}**")

    st.divider()
    st.header("Passo 2: Encontre o seu ROAS Ideal")

    if lucro_bruto > 0:
        lucro_desejado = st.number_input("Qual o lucro líquido desejado por venda (R$)?", 0.0, float(lucro_bruto), max(0.0, lucro_bruto / 2), format="%.2f")
        verba_maxima_ads = lucro_bruto - lucro_desejado
        if verba_maxima_ads > 0:
            roas_ideal = results["valor_venda"] / verba_maxima_ads
            st.subheader(f"Seu ROAS Ideal para começar é de: {roas_ideal:.2f}")
            st.success(f"Para obter um lucro de **R$ {lucro_desejado:.2f}**, você pode gastar até **R$ {verba_maxima_ads:.2f}** em anúncios, exigindo um ROAS de **{roas_ideal:.2f}**.")
        else:
            st.warning("O lucro desejado é muito alto. Não há margem para investir em anúncios e atingir essa meta.")
    else:
        st.warning("Não é possível calcular um ROAS ideal, pois a operação já está dando prejuízo.")
