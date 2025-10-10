import streamlit as st

st.title("🏷️ Calculadora de Descontos Estratégicos")
st.write("Planeje suas promoções descobrindo o preço de vitrine, o preço final ou a porcentagem de desconto.")

# --- Estado de Sessão e Reset ---
if 'desc_run_id' not in st.session_state:
    st.session_state.desc_run_id = 0
def reset_desc_calculator():
    st.session_state.desc_run_id += 1

st.sidebar.button("Resetar Calculadora de Descontos", on_click=reset_desc_calculator, use_container_width=True)
run_id = st.session_state.desc_run_id

# --- Abas para cada modo de cálculo ---
tab_c, tab_a, tab_b = st.tabs([
    "🎯 Modo C: Descobrir Preço de Vitrine",
    "📊 Modo A: Descobrir a % de Desconto",
    "🧮 Modo B: Calcular Preço Final"
])


# MODO C: Achar o Preço de Vitrine (O mais importante para você)
with tab_c:
    st.header("Planejar Preço de Vitrine")
    st.info("Use este modo quando você sabe por quanto quer vender e qual desconto quer anunciar.")
    
    preco_final_c = st.number_input(
        "Preço Final que o cliente deve pagar (R$)", 
        min_value=0.01, format="%.2f", key=f"c_preco_final_{run_id}"
    )
    desconto_c = st.number_input(
        "Porcentagem de desconto que você quer anunciar (%)", 
        min_value=0.1, max_value=99.9, value=20.0, step=0.5, key=f"c_desconto_{run_id}"
    )

    if st.button("Calcular Preço de Vitrine", key="btn_c"):
        if desconto_c >= 100:
            st.error("O desconto não pode ser de 100% ou mais.")
        else:
            preco_vitrine = preco_final_c / (1 - (desconto_c / 100))
            st.subheader("Resultado:")
            st.metric(
                label="Você deve anunciar o produto por:",
                value=f"R$ {preco_vitrine:.2f}"
            )
            st.success(f"Anunciando por **R$ {preco_vitrine:.2f}** e aplicando um desconto de **{desconto_c}%**, o preço final para o cliente será de **R$ {preco_final_c:.2f}**.")

# MODO A: Achar a Porcentagem de Desconto
with tab_a:
    st.header("Descobrir a Porcentagem de Desconto")
    st.info("Use este modo para saber qual foi o desconto real aplicado em uma venda.")
    
    preco_cheio_a = st.number_input(
        "Preço 'Cheio' anunciado (R$)", 
        min_value=0.01, format="%.2f", key=f"a_preco_cheio_{run_id}"
    )
    preco_final_a = st.number_input(
        "Preço Final pago pelo cliente (R$)", 
        min_value=0.01, format="%.2f", key=f"a_preco_final_{run_id}"
    )

    if st.button("Calcular % de Desconto", key="btn_a"):
        if preco_final_a > preco_cheio_a:
            st.warning("O preço final é maior que o preço anunciado. Isso é um aumento, não um desconto.")
        elif preco_cheio_a <= 0:
            st.error("O preço anunciado deve ser maior que zero.")
        else:
            valor_desconto = preco_cheio_a - preco_final_a
            percentual_desconto = (valor_desconto / preco_cheio_a) * 100
            st.subheader("Resultado:")
            st.metric(
                label="A porcentagem de desconto aplicada foi de:",
                value=f"{percentual_desconto:.2f}%"
            )
            st.success(f"Um produto que custava **R$ {preco_cheio_a:.2f}** e foi vendido por **R$ {preco_final_a:.2f}** teve um desconto de **R$ {valor_desconto:.2f}**.")
            
# MODO B: Achar o Preço Final
with tab_b:
    st.header("Calcular o Preço Final")
    st.info("Use este modo para simular rapidamente o preço final aplicando um desconto.")

    preco_cheio_b = st.number_input(
        "Preço 'Cheio' anunciado (R$)", 
        min_value=0.01, format="%.2f", key=f"b_preco_cheio_{run_id}"
    )
    desconto_b = st.number_input(
        "Porcentagem de desconto a aplicar (%)", 
        min_value=0.1, max_value=99.9, value=15.0, step=0.5, key=f"b_desconto_{run_id}"
    )

    if st.button("Calcular Preço Final", key="btn_b"):
        valor_desconto = preco_cheio_b * (desconto_b / 100)
        preco_final = preco_cheio_b - valor_desconto
        st.subheader("Resultado:")
        st.metric(
            label="O preço final para o cliente será de:",
            value=f"R$ {preco_final:.2f}"
        )
        st.success(f"Aplicando **{desconto_b}%** de desconto em **R$ {preco_cheio_b:.2f}**, o valor do desconto é de **R$ {valor_desconto:.2f}**.")
