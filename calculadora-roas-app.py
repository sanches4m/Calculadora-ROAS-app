import streamlit as st

# --- INICIALIZAÇÃO DO ESTADO DE SESSÃO --- # <<< NOVO
# Usado para forçar o reset dos widgets
if 'run_id' not in st.session_state:
    st.session_state.run_id = 0

# --- FUNÇÃO DE RESET --- # <<< NOVO
def reset_calculator():
    st.session_state.run_id += 1

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

# Adicionamos o parâmetro 'key' a todos os widgets de input
valor_venda = st.sidebar.number_input(
    "Valor da Venda na Plataforma (R$)", min_value=0.01, format="%.2f",
    key=f"valor_venda_{st.session_state.run_id}"
)
custo_produto = st.sidebar.number_input(
    "Custo do Produto (R$)", min_value=0.0, format="%.2f",
    key=f"custo_produto_{st.session_state.run_id}"
)
custo_embalagem = st.sidebar.number_input(
    "Custo da Embalagem (R$)", min_value=0.0, format="%.2f",
    key=f"custo_embalagem_{st.session_state.run_id}"
)

plataforma_nome = st.sidebar.selectbox(
    "Plataforma", options=PLATFORMAS,
    key=f"plataforma_{st.session_state.run_id}"
)

# --- INPUTS CONDICIONAIS POR PLATAFORMA ---
comissao_percentual_manual = 0.0

if plataforma_nome == "Shopee":
    participa_frete_gratis = st.sidebar.radio(
        "Faz parte do Programa de Frete Grátis?", ("Sim", "Não"), index=1,
        help="A taxa de comissão da Shopee muda com base na sua participação no programa.",
        key=f"shopee_frete_{st.session_state.run_id}"
    )
elif plataforma_nome in ["Mercado Livre", "Amazon"]:
    comissao_percentual_manual = st.sidebar.number_input(
        f"Taxa de comissão da {plataforma_nome} (%)", min_value=0.0, max_value=100.0, value=17.0, step=0.5,
        key=f"manual_comissao_{st.session_state.run_id}"
    ) / 100

taxa_imposto = st.sidebar.slider(
    "Alíquota do Imposto (%)", 
    min_value=0.0, max_value=30.0, value=0.0, step=0.5,
    help="Se você é MEI e isento para esta venda, pode deixar em 0%.",
    key=f"imposto_{st.session_state.run_id}"
) / 100


# --- BOTÕES DE AÇÃO ---
col1, col2 = st.sidebar.columns(2)

# O botão de calcular continua como antes
calculate_button = col1.button("Calcular", use_container_width=True)

# <<< NOVO: BOTÃO DE RESET
reset_button = col2.button("Resetar", on_click=reset_calculator, use_container_width=True)


# --- Se o botão de calcular for pressionado, rodamos a lógica ---
if calculate_button:

    # --- LÓGICA DE CÁLCULO DA COMISSÃO ---
    comissao = 0.0
    detalhe_comissao = ""

    if plataforma_nome == "Shopee":
        taxa_fixa_shopee = 4.00
        taxa_percentual = 0.20 if participa_frete_gratis == "Sim" else 0.14
        comissao = (valor_venda * taxa_percentual) + taxa_fixa_shopee
        detalhe_comissao = f"Comissão Shopee ({taxa_percentual*100}% + R$ {taxa_fixa_shopee:.2f})"
    
    elif plataforma_nome in ["Mercado Livre", "Amazon"]:
        taxa_percentual = comissao_percentual_manual
        comissao = valor_venda * taxa_percentual
        detalhe_comissao = f"Comissão {plataforma_nome} ({taxa_percentual*100}%)"

    elif plataforma_nome == "Shein":
        taxa_percentual = TAXA_SHEIN
        comissao = valor_venda * taxa_percentual
        detalhe_comissao = f"Comissão Shein ({taxa_percentual*100}%)"

    elif plataforma_nome == "Magalu":
        comissao = (valor_venda * TAXA_MAGALU_PERCENTUAL) + TAXA_MAGALU_FIXA
        detalhe_comissao = f"Comissão Magalu ({TAXA_MAGALU_PERCENTUAL*100}% + R$ {TAXA_MAGALU_FIXA:.2f})"

    # --- RESTANTE DOS CÁLCULOS ---
    valor_imposto = valor_venda * taxa_imposto
    custos_totais_sem_ads = custo_produto + custo_embalagem + comissao + valor_imposto
    lucro_bruto_por_venda = valor_venda - custos_totais_sem_ads
    
    # --- Exibição dos Resultados do Ponto de Equilíbrio ---
    st.header("Resultados do Ponto de Equilíbrio")
    
    res_col1, res_col2 = st.columns(2)
    res_col1.metric("Lucro Bruto por Venda (Sem Ads)", f"R$ {lucro_bruto_por_venda:.2f}")
    
    if lucro_bruto_por_venda <= 0:
        st.error("AVISO: A venda deste produto já resulta em prejuízo antes dos anúncios.")
        res_col2.metric("ROAS de Equilíbrio", "PREJUÍZO")
    else:
        roas_equilibrio = valor_venda / lucro_bruto_por_venda
        res_col2.metric("ROAS de Equilíbrio", f"{roas_equilibrio:.2f}")
        st.info(f"Este é o ROAS mínimo para não ter prejuízo. Qualquer valor acima disso é lucro.")

    with st.expander("Ver detalhes dos custos"):
        st.write(f"**Lucro Líquido (sem Ads): R$ {lucro_bruto_por_venda:.2f}**")
        st.write(f"- {detalhe_comissao}: R$ {comissao:.2f}")
        st.write(f"- Valor do Imposto: R$ {valor_imposto:.2f}")
        st.write(f"- Custo do Produto + Embalagem: R$ {custo_produto + custo_embalagem:.2f}")
        st.write(f"---")
        st.write(f"**Custos Totais (sem Ads): R$ {custos_totais_sem_ads:.2f}**")

    st.divider()

    # --- SEÇÃO: CÁLCULO DO ROAS IDEAL ---
    st.header("Passo 2: Encontre o seu ROAS Ideal")
    
    if lucro_bruto_por_venda > 0:
        lucro_desejado = st.number_input(
            "Qual o lucro líquido desejado por venda (R$)?", 
            min_value=0.0, 
            max_value=float(lucro_bruto_por_venda),
            value=max(0.0, lucro_bruto_por_venda / 2),
            format="%.2f",
            # A key aqui não precisa do run_id, pois esta seção é recriada a cada cálculo
            key="lucro_desejado" 
        )

        verba_maxima_ads = lucro_bruto_por_venda - lucro_desejado

        if verba_maxima_ads > 0:
            roas_ideal = valor_venda / verba_maxima_ads
            
            st.subheader(f"Seu ROAS Ideal para começar é de: {roas_ideal:.2f}")
            st.success(f"Para obter um lucro de **R$ {lucro_desejado:.2f}** por venda, você pode gastar até **R$ {verba_maxima_ads:.2f}** em anúncios. Isso exige um ROAS de **{roas_ideal:.2f}**.")
        else:
            st.warning("O lucro desejado é muito alto. Com os custos atuais, não há margem para investir em anúncios e atingir essa meta de lucro.")
    else:
        st.warning("Não é possível calcular um ROAS ideal, pois a operação já está dando prejuízo.")
