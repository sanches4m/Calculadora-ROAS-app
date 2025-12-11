import streamlit as st

st.set_page_config(layout="centered") # Opcional, caso queira forçar layout nesta pág

st.title("🎯 Calculadora de Preço por Meta de Lucro")
st.markdown("Defina quanto você quer lucrar (em R$) e descubra o preço de venda exato para cobrir todos os custos e taxas.")

# --- Estado de Sessão ---
if 'meta_run_id' not in st.session_state:
    st.session_state.meta_run_id = 0

def reset_meta_calculator():
    st.session_state.meta_run_id += 1

# --- Dicionários e Constantes ---
PLATFORMAS = ["Shopee", "Mercado Livre", "Amazon", "Shein", "Magalu"]
TAXA_SHEIN = 0.20
TAXA_MAGALU_PERCENTUAL = 0.18
TAXA_MAGALU_FIXA = 5.00

# --- Entradas (Inputs) ---
st.sidebar.header("📝 Configuração de Custos")
run_id = st.session_state.meta_run_id

# 1. Custos do Produto
with st.sidebar.expander("💰 Custos do Produto", expanded=True):
    custo_produto = st.number_input("Custo do Produto (R$)", 0.0, format="%.2f", key=f"meta_cp_{run_id}")
    custo_embalagem = st.number_input("Custo da Embalagem (R$)", 0.0, format="%.2f", key=f"meta_ce_{run_id}")
    taxa_imposto = st.slider("Imposto (MEI/Simples) %", 0.0, 30.0, 0.0, 0.5, key=f"meta_imp_{run_id}") / 100

# 2. Configuração da Plataforma
with st.sidebar.expander("🛒 Taxas da Plataforma", expanded=True):
    plataforma_nome = st.selectbox("Selecione a Plataforma", PLATFORMAS, key=f"meta_plat_{run_id}")
    
    # Lógica de taxas
    taxa_plataforma_percentual = 0.0
    taxa_plataforma_fixa = 0.0

    if plataforma_nome == "Shopee":
        frete_gratis = st.radio("Programa Frete Grátis?", ("Sim", "Não"), index=1, key=f"meta_frete_{run_id}")
        taxa_plataforma_percentual = 0.20 if frete_gratis == "Sim" else 0.14
        taxa_plataforma_fixa = 4.00
    elif plataforma_nome in ["Mercado Livre", "Amazon"]:
        taxa_plataforma_percentual = st.number_input(f"Taxa % {plataforma_nome}", 0.0, 100.0, 17.0, 0.5, key=f"meta_man_{run_id}") / 100
    elif plataforma_nome == "Shein":
        taxa_plataforma_percentual = TAXA_SHEIN
    elif plataforma_nome == "Magalu":
        taxa_plataforma_percentual = TAXA_MAGALU_PERCENTUAL
        taxa_plataforma_fixa = TAXA_MAGALU_FIXA

st.sidebar.divider()
st.sidebar.button("🔄 Resetar Calculadora", on_click=reset_meta_calculator, use_container_width=True)

# --- Área Principal: Definição da Meta ---
st.container()
col_meta, col_vazio = st.columns([2, 1])
with col_meta:
    st.subheader("Quanto você quer lucrar?")
    lucro_alvo = st.number_input(
        "Digite o valor do lucro líquido desejado (R$):", 
        min_value=0.0, value=5.00, step=1.00, format="%.2f",
        help="Este é o valor que vai sobrar limpo no seu bolso."
    )

if st.button("🚀 Calcular Preço de Venda Necessário", type="primary", use_container_width=True):
    
    # --- MATEMÁTICA REVERSA ---
    # Preço = (Custos + Lucro + TaxaFixa) / (1 - TaxaImposto - TaxaPlataforma%)
    
    custos_fixos_absolutos = custo_produto + custo_embalagem + lucro_alvo + taxa_plataforma_fixa
    denominador = 1 - (taxa_imposto + taxa_plataforma_percentual)

    if denominador <= 0:
        st.error("Erro: As taxas somadas (Plataforma + Imposto) são iguais ou maiores que 100%. É impossível lucrar assim.")
    else:
        preco_venda_necessario = custos_fixos_absolutos / denominador
        
        # Cálculos de conferência
        comissao_total = (preco_venda_necessario * taxa_plataforma_percentual) + taxa_plataforma_fixa
        imposto_total = preco_venda_necessario * taxa_imposto
        custo_total = custo_produto + custo_embalagem + comissao_total + imposto_total
        margem_percentual = (lucro_alvo / preco_venda_necessario) * 100

        # --- EXIBIÇÃO ---
        st.divider()
        st.markdown(f"### ✅ Para lucrar **R$ {lucro_alvo:.2f}**, anuncie por:")
        st.metric(label="Preço de Venda Sugerido", value=f"R$ {preco_venda_necessario:.2f}", delta=f"Margem: {margem_percentual:.1f}%")

        # Detalhes visuais
        st.write("---")
        st.write("**Detalhamento da Composição do Preço:**")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Produto+Emb.", f"R$ {custo_produto+custo_embalagem:.2f}")
        col2.metric("Comissão", f"R$ {comissao_total:.2f}")
        col3.metric("Imposto", f"R$ {imposto_total:.2f}")
        col4.metric("SEU LUCRO", f"R$ {lucro_alvo:.2f}")

        # Gráfico de barras simples com progress bar para visualização
        st.caption("Distribuição do valor de venda:")
        st.progress(int(margem_percentual) if margem_percentual < 100 else 100)