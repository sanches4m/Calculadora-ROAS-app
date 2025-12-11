import streamlit as st

st.title("📈 Calculadora de ROAS e Lucratividade")
st.markdown("Descubra seu **Ponto de Equilíbrio** e o **ROAS Ideal** para atingir suas metas.")

# --- Estado de Sessão (Mantendo isolamento com prefixo 'roas_') ---
if 'roas_run_id' not in st.session_state:
    st.session_state.roas_run_id = 0
if 'roas_calculation_done' not in st.session_state:
    st.session_state.roas_calculation_done = False
if 'roas_results' not in st.session_state:
    st.session_state.roas_results = {}

def reset_roas_calculator():
    st.session_state.roas_run_id += 1
    st.session_state.roas_calculation_done = False
    st.session_state.roas_results = {}

# --- Dicionários ---
PLATFORMAS = ["Shopee", "Mercado Livre", "Amazon", "Shein", "Magalu"]
TAXA_SHEIN = 0.20
TAXA_MAGALU_PERCENTUAL = 0.18
TAXA_MAGALU_FIXA = 5.00

# --- Barra Lateral Moderna ---
st.sidebar.header("⚙️ Configuração da Venda")
run_id = st.session_state.roas_run_id

# Grupo 1: Dados Financeiros
with st.sidebar.expander("💰 Dados do Produto", expanded=True):
    valor_venda = st.number_input("Valor da Venda (R$)", min_value=0.01, format="%.2f", key=f"roas_vv_{run_id}")
    custo_produto = st.number_input("Custo do Produto (R$)", min_value=0.0, format="%.2f", key=f"roas_cp_{run_id}")
    custo_embalagem = st.number_input("Custo da Embalagem (R$)", min_value=0.0, format="%.2f", key=f"roas_ce_{run_id}")
    taxa_imposto = st.slider("Imposto (MEI/Simples) %", 0.0, 30.0, 0.0, 0.5, key=f"roas_imp_{run_id}") / 100

# Grupo 2: Plataforma
with st.sidebar.expander("🛒 Plataforma e Taxas", expanded=True):
    plataforma_nome = st.selectbox("Plataforma", PLATFORMAS, key=f"roas_plat_{run_id}")
    
    comissao_percentual_manual = 0.0
    if plataforma_nome == "Shopee":
        participa_frete_gratis = st.radio("Frete Grátis?", ("Sim", "Não"), index=1, horizontal=True, key=f"roas_shopee_frete_{run_id}")
    elif plataforma_nome in ["Mercado Livre", "Amazon"]:
        comissao_percentual_manual = st.number_input(f"Taxa % {plataforma_nome}", 0.0, 100.0, 17.0, 0.5, key=f"roas_manual_comissao_{run_id}") / 100

st.sidebar.divider()
calculate_button = st.sidebar.button("🚀 Calcular Indicadores", type="primary", use_container_width=True)
st.sidebar.button("🔄 Resetar", on_click=reset_roas_calculator, use_container_width=True)

# --- Lógica de Cálculo ---
if calculate_button:
    detalhe_comissao, comissao = "", 0.0
    
    # Regras de Plataforma
    if plataforma_nome == "Shopee":
        taxa_fixa_shopee = 4.00
        taxa_percentual = 0.20 if participa_frete_gratis == "Sim" else 0.14
        comissao = (valor_venda * taxa_percentual) + taxa_fixa_shopee
        detalhe_comissao = f"Shopee ({taxa_percentual*100}% + R$4)"
    elif plataforma_nome in ["Mercado Livre", "Amazon"]:
        taxa_percentual = comissao_percentual_manual
        comissao = valor_venda * taxa_percentual
        detalhe_comissao = f"{plataforma_nome} ({taxa_percentual*100:.1f}%)"
    elif plataforma_nome == "Shein":
        comissao = valor_venda * TAXA_SHEIN
        detalhe_comissao = f"Shein ({TAXA_SHEIN*100}%)"
    elif plataforma_nome == "Magalu":
        comissao = (valor_venda * TAXA_MAGALU_PERCENTUAL) + TAXA_MAGALU_FIXA
        detalhe_comissao = f"Magalu ({TAXA_MAGALU_PERCENTUAL*100}% + R$5)"
    
    valor_imposto = valor_venda * taxa_imposto
    custos_totais_sem_ads = custo_produto + custo_embalagem + comissao + valor_imposto
    lucro_bruto_por_venda = valor_venda - custos_totais_sem_ads

    # Salva no Session State
    st.session_state.roas_calculation_done = True
    st.session_state.roas_results = {
        "lucro_bruto": lucro_bruto_por_venda, "valor_venda": valor_venda,
        "detalhe_custos": {
            "detalhe_comissao": detalhe_comissao, "comissao": comissao,
            "valor_imposto": valor_imposto, "custo_produto_embalagem": custo_produto + custo_embalagem,
            "custos_totais_sem_ads": custos_totais_sem_ads
        }
    }

# --- Exibição dos Resultados ---
if st.session_state.roas_calculation_done:
    results = st.session_state.roas_results
    lucro_bruto = results["lucro_bruto"]
    
    # 1. Seção Ponto de Equilíbrio
    st.divider()
    st.subheader("📊 Resultado do Ponto de Equilíbrio")
    
    c1, c2 = st.columns(2)
    c1.metric("Lucro Líquido (sem Ads)", f"R$ {lucro_bruto:.2f}")

    if lucro_bruto <= 0:
        st.error("❌ Prejuízo Operacional. Não é possível rodar Ads.")
        c2.metric("ROAS Mínimo", "N/A")
    else:
        roas_equilibrio = results["valor_venda"] / lucro_bruto
        c2.metric("ROAS de Equilíbrio (Break-Even)", f"{roas_equilibrio:.2f}")
        
        # Barra de progresso visual para custos
        custos = results["detalhe_custos"]
        total_custos = custos['custos_totais_sem_ads']
        perc_custos = (total_custos / results['valor_venda'])
        st.caption(f"Os custos consomem {perc_custos*100:.1f}% do valor da venda.")
        st.progress(min(perc_custos, 1.0))

        with st.expander("🔎 Ver detalhe dos custos descontados"):
            st.write(f"**Venda:** R$ {results['valor_venda']:.2f}")
            st.write(f"- Produto + Emb.: R$ {custos['custo_produto_embalagem']:.2f}")
            st.write(f"- {custos['detalhe_comissao']}: R$ {custos['comissao']:.2f}")
            st.write(f"- Imposto: R$ {custos['valor_imposto']:.2f}")
            st.write("---")
            st.write(f"**Sobra Limpa:** R$ {lucro_bruto:.2f}")

    # 2. Seção ROAS Ideal
    st.divider()
    st.subheader("🎯 Planejamento: ROAS Ideal")
    
    if lucro_bruto > 0:
        st.info("Quanto você quer lucrar por venda para valer a pena?")
        
        col_input, col_result = st.columns([1, 2])
        
        with col_input:
            lucro_desejado = st.number_input(
                "Lucro Meta (R$)", 
                min_value=0.0, max_value=float(lucro_bruto), 
                value=max(0.0, lucro_bruto / 2), format="%.2f",
                key="roas_lucro_desejado_input"
            )

        verba_maxima_ads = lucro_bruto - lucro_desejado
        
        with col_result:
            if verba_maxima_ads > 0:
                roas_ideal = results["valor_venda"] / verba_maxima_ads
                st.metric("Seu ROAS Ideal deve ser:", f"{roas_ideal:.2f}")
                st.caption(f"Verba máx. de Ads: R$ {verba_maxima_ads:.2f}/venda")
            else:
                st.warning("Sem margem para Ads com esse lucro desejado.")