import streamlit as st
import sys
import os

# Importação dos estilos visuais
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from estilos import aplicar_estilo_visual

aplicar_estilo_visual()

st.title("🎯 Calculadora de Preço por Meta")
st.markdown("Defina quanto você quer lucrar (em R$ ou %) e descubra o preço de venda exato.")

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

# --- Entradas (Inputs) na Barra Lateral ---
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

# --- ÁREA PRINCIPAL: ABAS PARA ESCOLHER O TIPO DE META ---
st.write("") # Espaçamento
tab_valor, tab_porc = st.tabs(["💲 Meta em Valor (R$)", "📊 Meta em Porcentagem (%)"])

# --- ABA 1: META EM VALOR (R$) ---
with tab_valor:
    st.info("Use esta opção se você quer garantir um valor fixo no bolso (ex: Lucrar R$ 10,00).")
    
    col_v1, col_v2 = st.columns([2, 1])
    with col_v1:
        lucro_alvo_valor = st.number_input(
            "Lucro Líquido Desejado (R$):", 
            min_value=0.0, value=5.00, step=1.00, format="%.2f",
            key=f"alvo_valor_{run_id}"
        )

    if st.button("Calcular por Valor (R$)", type="primary", use_container_width=True, key="btn_valor"):
        
        # Fórmula: Preço = (Custos + TaxasFixas + LucroDesejado) / (1 - TaxasPercentuais)
        custos_fixos_absolutos = custo_produto + custo_embalagem + lucro_alvo_valor + taxa_plataforma_fixa
        denominador = 1 - (taxa_imposto + taxa_plataforma_percentual)

        if denominador <= 0:
             st.error("Erro: As taxas somadas são maiores que 100%. Impossível calcular.")
        else:
            preco_sugerido = custos_fixos_absolutos / denominador
            
            # Conferência
            comissao_total = (preco_sugerido * taxa_plataforma_percentual) + taxa_plataforma_fixa
            imposto_total = preco_sugerido * taxa_imposto
            margem_real = (lucro_alvo_valor / preco_sugerido) * 100

            st.divider()
            st.markdown(f"### ✅ Venda por:")
            st.metric(label="Preço Sugerido", value=f"R$ {preco_sugerido:.2f}", delta=f"Margem: {margem_real:.1f}%")
            
            with st.expander("Ver detalhes da conta"):
                st.write(f"**Custos (Prod+Emb):** R$ {custo_produto+custo_embalagem:.2f}")
                st.write(f"**Comissão:** R$ {comissao_total:.2f}")
                st.write(f"**Imposto:** R$ {imposto_total:.2f}")
                st.success(f"**Lucro Líquido:** R$ {lucro_alvo_valor:.2f}")

# --- ABA 2: META EM PORCENTAGEM (%) ---
with tab_porc:
    st.info("Use esta opção se você quer garantir uma margem saudável (ex: Lucrar 20%).")
    
    col_p1, col_p2 = st.columns([2, 1])
    with col_p1:
        margem_alvo_perc = st.slider(
            "Margem de Lucro Desejada (%):", 
            min_value=1.0, max_value=50.0, value=15.0, step=0.5,
            key=f"alvo_perc_{run_id}"
        ) / 100

    if st.button("Calcular por Porcentagem (%)", type="primary", use_container_width=True, key="btn_perc"):
        
        # Fórmula: Preço = (Custos + TaxasFixas) / (1 - TaxasPercentuais - MargemDesejada)
        custos_fixos_absolutos = custo_produto + custo_embalagem + taxa_plataforma_fixa
        total_taxas_perc = taxa_imposto + taxa_plataforma_percentual
        
        # O "divisor" é o que sobra do preço (100%) depois de tirar impostos, comissão e a sua margem
        denominador = 1 - (total_taxas_perc + margem_alvo_perc)

        if denominador <= 0:
            st.error(f"Impossível! Taxas ({total_taxas_perc*100:.1f}%) + Margem ({margem_alvo_perc*100:.1f}%) somam mais de 100%.")
        else:
            preco_sugerido = custos_fixos_absolutos / denominador
            
            # Conferência
            lucro_em_reais = preco_sugerido * margem_alvo_perc
            comissao_total = (preco_sugerido * taxa_plataforma_percentual) + taxa_plataforma_fixa
            imposto_total = preco_sugerido * taxa_imposto

            st.divider()
            st.markdown(f"### ✅ Venda por:")
            st.metric(label="Preço Sugerido", value=f"R$ {preco_sugerido:.2f}", delta=f"Lucro: R$ {lucro_em_reais:.2f}")
            
            with st.expander("Ver detalhes da conta"):
                st.write(f"**Custos (Prod+Emb):** R$ {custo_produto+custo_embalagem:.2f}")
                st.write(f"**Comissão:** R$ {comissao_total:.2f}")
                st.write(f"**Imposto:** R$ {imposto_total:.2f}")
                st.success(f"**Lucro Líquido ({margem_alvo_perc*100:.1f}%):** R$ {lucro_em_reais:.2f}")