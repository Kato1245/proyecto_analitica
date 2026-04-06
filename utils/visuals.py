import streamlit as st

def load_custom_css():
    """
    Carga el sistema de diseño premium para todo el proyecto.
    Define colores, tipografía y estilos de tarjetas.
    """
    st.markdown("""
    <style>
    /* Importar tipografía moderna */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Outfit', sans-serif;
    }

    /* Fondo principal con sutil gradiente */
    .stApp {
        background: linear-gradient(135deg, #f8f9fc 0%, #eef2f7 100%);
    }

    /* Estilo de Tarjetas (Cards) */
    .premium-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border-left: 5px solid #00c6ff;
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }

    .premium-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.1);
    }

    /* Hero Section */
    .hero-container {
        background: linear-gradient(90deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        padding: 3rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }

    .hero-title {
        font-size: 3rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.5rem !important;
        background: -webkit-linear-gradient(#fff, #aaa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Sidebar personalizado */
    .css-1d391kg {
        background-color: #161b22 !important;
    }

    /* Botones Premium */
    .stButton>button {
        border-radius: 10px;
        border: none;
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
        color: white;
        font-weight: 600;
        padding: 0.6rem 2rem;
        transition: all 0.3s;
    }

    .stButton>button:hover {
        opacity: 0.9;
        transform: scale(1.02);
        color: white;
    }

    /* Métricas */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #0072ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

def card(title, content, emoji="📊"):
    """Renderiza una tarjeta estilo premium."""
    st.markdown(f"""
    <div class="premium-card">
        <h3 style="margin-top:0;">{emoji} {title}</h3>
        <p style="color: #444;">{content}</p>
    </div>
    """, unsafe_allow_html=True)
