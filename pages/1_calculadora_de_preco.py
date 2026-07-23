import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from estilos import aplicar_estilo_visual

# aplicar_estilo_visual()

st.title("💰 Calculadora de Preço e Margem")
st.markdown("Analise a saúde do seu preço atual e simule cenários para aumentar sua margem.")

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

PLATFORMAS = ["Shopee", "Mercado Livre", "Amazon", "Shein", "Magalu"]
TAXA_SHEIN = 0.20
TAXA_MAGALU_PERCENTUAL = 0.18
TAXA_MAGALU_FIXA = 5.00

st.sidebar.header("📝 Dados da Venda")
run_id = st.session_state.preco_run_id

with st.sidebar.expander("💸 Custos do Produto", expanded=True):
    custo_produto = st.number_input("Custo do Produto (R$)", 0.01, key=f"preco_cp_{run_id}")
    custo_embalagem = st.number_input("Custo da Embalagem (R$)", 0.0, key=f"preco_ce_{run_id}")
    taxa_imposto = st.slider("Imposto (%)", 0.0, 30.0, 0.0, 0.5, key=f"preco_imp_{run_id}") / 100

with st.sidebar.expander("🏪 Plataforma", expanded=True):
    plataforma_nome = st.selectbox("Canal de Venda", PLATFORMAS, key=f"preco_plat_{run_id}")
    
    comissao_percentual_manual = 0.0
    if plataforma_nome == "Shopee":
        participa_frete_gratis = st.radio("Frete Grátis?", ("Sim", "Não"), index=1, horizontal=True, key=f"preco_shopee_frete_{run_id}")
    elif plataforma_nome in ["Mercado Livre", "Amazon"]:
        comissao_percentual_manual = st.number_input(f"Taxa % {plataforma_nome}", 0.0, 100.0, 17.0, 0.5, key=f"preco_manual_comissao_{run_id}") / 100

with st.sidebar.expander("🏷️ Preço Atual", expanded=True):
    preco_venda_atual = st.number_input("Preço de Venda (R$)", 0.01, key=f"preco_pv_{run_id}")

st.sidebar.divider()
calculate_button = st.sidebar.button("📊 Analisar Lucratividade", type="primary", use_container_width=True)
st.sidebar.button("🔄 Resetar", on_click=reset_preco_calculator, use_container_width=True)

if calculate_button:
    detalhe_comissao, comissao = "", 0.0
    if plataforma_nome == "Shopee":
        taxa_fixa_shopee = 4.00
        taxa_percentual = 0.20 if participa_frete_gratis == "Sim" else 0.14
        comissao = (preco_venda_atual * taxa_percentual) + taxa_fixa_shopee
        detalhe_comissao = f"Shopee ({taxa_percentual*100}% + R$4)"
    elif plataforma_nome in ["Mercado Livre", "Amazon"]:
        comissao = preco_venda_atual * comissao_percentual_manual
        detalhe_comissao = f"{plataforma_nome} ({comissao_percentual_manual*100:.1f}%)"
    elif plataforma_nome == "Shein":
        comissao = preco_venda_atual * TAXA_SHEIN
        detalhe_comissao = f"Shein ({TAXA_SHEIN*100}%)"
    elif plataforma_nome == "Magalu":
        comissao = (preco_venda_atual * TAXA_MAGALU_PERCENTUAL) + TAXA_MAGALU_FIXA
        detalhe_comissao = f"Magalu ({TAXA_MAGALU_PERCENTUAL*100}% + R$5)"

    custo_total_produto = custo_produto + custo_embalagem
    valor_imposto = preco_venda_atual * taxa_imposto
    total_taxas = comissao + valor_imposto
    lucro_liquido = preco_venda_atual - custo_total_produto - total_taxas
    margem_lucro = (lucro_liquido / preco_venda_atual) * 100 if preco_venda_atual > 0 else 0

    st.session_state.preco_calculation_done = True
    st.session_state.preco_results = {
        "preco_venda": preco_venda_atual, "custo_total_produto": custo_total_produto,
        "total_taxas": total_taxas, "lucro_liquido": lucro_liquido,
        "margem_lucro": margem_lucro, "detalhe_comissao": detalhe_comissao,
        "comissao": comissao, "valor_imposto": valor_imposto
    }

if st.session_state.preco_calculation_done:
    res = st.session_state.preco_results
    
    st.divider()
    st.subheader("🔎 Resultado da Análise")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Preço Analisado", f"R$ {res['preco_venda']:.2f}")
    col2.metric("Lucro Líquido", f"R$ {res['lucro_liquido']:.2f}", delta_color="normal")
    
    cor_delta = "normal"
    if res['margem_lucro'] < 10: cor_delta = "inverse"
    if res['margem_lucro'] > 20: cor_delta = "off"
    
    col3.metric("Margem Real", f"{res['margem_lucro']:.2f}%", delta=f"{res['margem_lucro']:.1f}%", delta_color=cor_delta)

    with st.expander("🧾 Extrato detalhado da operação"):
        st.write(f"**Receita Bruta:** R$ {res['preco_venda']:.2f}")
        st.write(f"(-) Custos (Prod+Emb): R$ {res['custo_total_produto']:.2f}")
        st.write(f"(-) {res['detalhe_comissao']}: R$ {res['comissao']:.2f}")
        st.write(f"(-) Impostos: R$ {res['valor_imposto']:.2f}")
        st.write("---")
        if res['lucro_liquido'] > 0:
            st.success(f"**= Lucro Líquido: R$ {res['lucro_liquido']:.2f}**")
        else:
            st.error(f"**= Prejuízo: R$ {res['lucro_liquido']:.2f}**")

    st.divider()
    st.subheader("🎚️ Simulador de Cenários")
    st.markdown("Arraste para ver como o preço afeta sua margem em tempo real.")
    
    novo_preco = st.slider(
        "Novo Preço de Venda (R$)",
        min_value=float(res['custo_total_produto'] * 1.1),
        max_value=float(res['preco_venda'] * 2.5),
        value=float(res['preco_venda']),
        format="%.2f"
    )

    nova_comissao = 0.0
    if plataforma_nome == "Shopee":
        tx_fixa = 4.00
        tx_perc = 0.20 if participa_frete_gratis == "Sim" else 0.14
        nova_comissao = (novo_preco * tx_perc) + tx_fixa
    elif plataforma_nome in ["Mercado Livre", "Amazon"]:
        nova_comissao = novo_preco * comissao_percentual_manual
    elif plataforma_nome == "Shein":
        nova_comissao = novo_preco * TAXA_SHEIN
    elif plataforma_nome == "Magalu":
        nova_comissao = (novo_preco * TAXA_MAGALU_PERCENTUAL) + TAXA_MAGALU_FIXA

    novo_imposto = novo_preco * taxa_imposto
    novo_lucro = novo_preco - res['custo_total_produto'] - nova_comissao - novo_imposto
    nova_margem = (novo_lucro / novo_preco) * 100

    sc1, sc2 = st.columns(2)
    sc1.metric("Novo Lucro", f"R$ {novo_lucro:.2f}")
    sc2.metric("Nova Margem", f"{nova_margem:.2f}%")
