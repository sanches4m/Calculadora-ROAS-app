import streamlit as st

def aplicar_estilo_visual():
    st.markdown("""
        <style>
        /* --- IMPORTANDO FONTES (Google Fonts) --- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* --- ESTILIZANDO OS CARTÕES DE MÉTRICAS (KPIs) --- */
        [data-testid="stMetric"] {
            background-color: #ffffff;
            border: 1px solid #f0f2f6;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }
        
        /* Efeito ao passar o mouse sobre o cartão */
        [data-testid="stMetric"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
            border-color: #e0e0e0;
        }

        /* Cor do rótulo da métrica (Label) */
        [data-testid="stMetricLabel"] {
            color: #6c757d;
            font-size: 14px;
            font-weight: 600;
        }

        /* Cor do valor da métrica */
        [data-testid="stMetricValue"] {
            color: #1f2937;
            font-weight: 700;
        }

        /* --- BOTÕES --- */
        /* Botão Primário (Calcular/Ação) */
        button[kind="primary"] {
            background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
            border: none;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-weight: 600;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        button[kind="primary"]:hover {
            box-shadow: 0 6px 12px rgba(75, 108, 183, 0.4);
            transform: scale(1.02);
        }

        /* Botão Secundário (Resetar) */
        button[kind="secondary"] {
            border: 1px solid #d1d5db;
            color: #374151;
            border-radius: 8px;
        }

        /* --- BARRA LATERAL (SIDEBAR) --- */
        [data-testid="stSidebar"] {
            background-color: #f8f9fa;
            border-right: 1px solid #e5e7eb;
        }

        /* Estilo dos Expanders na barra lateral */
        .streamlit-expanderHeader {
            background-color: #ffffff;
            border-radius: 6px;
            border: 1px solid #e5e7eb;
            font-weight: 600;
        }

        /* --- TÍTULOS --- */
        h1 {
            color: #111827;
            font-weight: 800;
            letter-spacing: -0.025em;
        }
        h2, h3 {
            color: #374151;
        }

        /* Linhas divisórias */
        hr {
            margin: 2em 0;
            border-color: #e5e7eb;
        }
        </style>
    """, unsafe_allow_html=True)