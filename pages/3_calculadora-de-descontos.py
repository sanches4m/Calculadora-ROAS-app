import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from estilos import aplicar_estilo_visual

# aplicar_estilo_visual()

st.title("🏷️ Calculadora de Descontos Estratégicos")
st.write("Ferramentas para planejar promoções e analisar descontos.")

if 'desc_run_id' not in st.session_state:
    st.session_state.desc_run_id = 0
def reset_desc_calculator():
    st.session_state.desc_run_id += 1

st.sidebar.button("🔄 Resetar Esta Calculadora", on_click=reset_desc_calculator, use_container_width=True)
run_id = st.session_state.desc_run_id

tab_vitrine, tab_final, tab_porc = st.tabs([
    "🎯 Modo A: Definir Preço de Vitrine",
    "💰 Modo B: Calcular Preço Final",
    "🔍 Modo C: Descobrir % Aplicada"
])

with tab_vitrine:
    st.header("Planejar Preço de Vitrine (Âncora)")
    st.info("Você sabe por quanto quer vender, mas quer anunciar um valor maior com desconto.")
    
    col1, col2 = st.columns(2)
    with col1:
        preco_final_a = st.number_input("Preço que o cliente VAI pagar (R$)", min_value=0.01, format="%.2f", key=f"a_pf_{run_id}")
    with col2:
        desconto_a = st.number_input("Desconto para anunciar (%)", 0.1, 99.0, 20.0, step=0.5, key=f"a_desc_{run_id}")

    if st.button("Calcular Preço de Vitrine", key="btn_a", use_container_width=True):
        preco_vitrine = preco_final_a / (1 - (desconto_a / 100))
        
        st.success("Resultado calculado!")
        st.metric(label="Anuncie o produto 'DE':", value=f"R$ {preco_vitrine:.2f}")
        st.caption(f"Anunciando por **R$ {preco_vitrine:.2f}** com **{desconto_a}% OFF**, o preço cai para **R$ {preco_final_a:.2f}**.")

with tab_final:
    st.header("Simular Preço Final")
    st.info("Tenho o preço cheio e quero ver quanto fica se der X% de desconto.")
    
    col1, col2 = st.columns(2)
    with col1:
        preco_cheio_b = st.number_input("Preço 'Cheio' atual (R$)", min_value=0.01, format="%.2f", key=f"b_pc_{run_id}")
    with col2:
        desconto_b = st.number_input("Desconto a aplicar (%)", 0.1, 100.0, 15.0, step=0.5, key=f"b_desc_{run_id}")

    if st.button("Calcular Novo Preço", key="btn_b", use_container_width=True):
        valor_desconto = preco_cheio_b * (desconto_b / 100)
        preco_final = preco_cheio_b - valor_desconto
        
        st.metric(label="Preço Final 'POR':", value=f"R$ {preco_final:.2f}", delta=f"- R$ {valor_desconto:.2f}")

with tab_porc:
    st.header("Descobrir a % Real")
    st.info("Qual foi o desconto real dado entre dois preços?")
    
    col1, col2 = st.columns(2)
    with col1:
        preco_cheio_c = st.number_input("Preço 'DE' (Anunciado)", min_value=0.01, format="%.2f", key=f"c_pc_{run_id}")
    with col2:
        preco_final_c = st.number_input("Preço 'POR' (Pago)", min_value=0.01, format="%.2f", key=f"c_pf_{run_id}")

    if st.button("Descobrir Porcentagem", key="btn_c", use_container_width=True):
        if preco_final_c >= preco_cheio_c:
            st.warning("O preço final é igual ou maior que o inicial. Não houve desconto.")
        else:
            diff = preco_cheio_c - preco_final_c
            porcentagem = (diff / preco_cheio_c) * 100
            st.metric(label="Desconto Real Aplicado", value=f"{porcentagem:.2f}%")
