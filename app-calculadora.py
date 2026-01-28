# app_calculadora.py
import streamlit as st
from estilos import aplicar_estilo_visual

st.set_page_config(
    page_title="Hub de Ferramentas",
    page_icon="🛠️",
    layout="centered"
)

aplicar_estilo_visual()

st.title("🛠️ Hub de Ferramentas para E-commerce")
st.markdown("---")
st.header("Bem-vindo(a)!")
st.markdown(
    """
    Este é o seu centro de controle para cálculos essenciais de e-commerce.
    
    Navegue pelas ferramentas disponíveis utilizando o menu na barra lateral à esquerda.
    
    👈 **Selecione uma calculadora para começar!**
    
    **Ferramentas disponíveis:**
    - **Calculadora de Preço:** Calcule o preço de venda ideal para seus produtos com base nos custos e margem de lucro desejada.
    - **Calculadora de ROAS:** Descubra seu ponto de equilíbrio e o ROAS ideal para atingir suas metas de lucro com ads.
    """
    
)

st.sidebar.success("Selecione uma calculadora acima.")
