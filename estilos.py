import streamlit as st

def aplicar_estilo_visual():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        [data-testid="stMetric"] {
            background-color: #262730; /* Fundo cinza escuro para o cartão */
            border: 1px solid #3d3d3d;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3); /* Sombra mais escura */
            transition: all 0.3s ease;
        }
        
        [data-testid="stMetric"]:hover {
            transform: translateY(-5px);
            border-color: #00ADB5; /* Borda ciano ao passar o mouse */
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.5);
        }

        [data-testid="stMetricLabel"] {
            color: #b0b0b0; /* Cinza claro para leitura fácil */
            font-size: 14px;
            font-weight: 600;
        }

        [data-testid="stMetricValue"] {
            color: #ffffff; /* Branco puro para destaque */
            font-weight: 700;
        }
        
        /* Cor do Delta (A setinha de porcentagem) */
        [data-testid="stMetricDelta"] svg {
            fill: #00ADB5 !important;
        }

        /* Vamos deixar o Streamlit controlar a cor base pelo config.toml 
           e apenas arredondar e dar estilo */
        
        div.stButton > button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
            height: auto;
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }

        button[kind="primary"] {
            box-shadow: 0 0 10px rgba(0, 173, 181, 0.3);
            border: none;
        }
        
        button[kind="primary"]:hover {
            box-shadow: 0 0 20px rgba(0, 173, 181, 0.6);
            transform: scale(1.02);
        }

        button[kind="secondary"] {
            border: 1px solid #4a4a4a;
            color: #e0e0e0;
        }
        button[kind="secondary"]:hover {
            border-color: #b0b0b0;
            color: #ffffff;
        }

        h1 {
            background: linear-gradient(90deg, #00ADB5 0%, #EEEEEE 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }
        
        h2, h3 {
            color: #e0e0e0;
        }

        hr {
            margin: 2em 0;
            border-color: #3d3d3d;
        }
        </style>
    """, unsafe_allow_html=True)'''
