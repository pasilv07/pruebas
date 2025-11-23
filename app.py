"""
Visual Audit App - Web Interface
Interfaz web con Streamlit para auditoría visual competitiva
"""
import streamlit as st
from pathlib import Path
import sys

# Añadir path del proyecto
sys.path.insert(0, str(Path(__file__).parent))

from web_app.pages import home, analyze, batch, compare


# Configuración de la página
st.set_page_config(
    page_title="Visual Audit App",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Visual Audit App - Auditoría Visual Competitiva para Campañas Educativas"
    }
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }

    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }

    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 5px;
        font-weight: bold;
        transition: all 0.3s;
    }

    .stButton>button:hover {
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
        transform: translateY(-2px);
    }

    .score-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        margin: 0.25rem;
    }

    .score-low {
        background: #fee;
        color: #c00;
    }

    .score-medium {
        background: #ffd;
        color: #880;
    }

    .score-high {
        background: #dfd;
        color: #080;
    }

    div[data-testid="stSidebarNav"] {
        background-image: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        padding-top: 2rem;
    }

    div[data-testid="stSidebarNav"] a {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Aplicación principal con navegación"""

    # Sidebar con navegación
    with st.sidebar:
        st.markdown("# 🎓 Visual Audit")
        st.markdown("---")

        page = st.radio(
            "Navegación",
            ["🏠 Inicio", "📸 Análisis Individual", "📊 Análisis por Lotes", "🔍 Comparación"],
            label_visibility="collapsed"
        )

        st.markdown("---")

        # Info en sidebar
        with st.expander("ℹ️ Acerca de"):
            st.markdown("""
            **Visual Audit App v1.0**

            Herramienta de auditoría visual competitiva para campañas educativas.

            Utiliza IA (Claude de Anthropic) para análisis exhaustivo.
            """)

        # Verificar API key
        import os
        from dotenv import load_dotenv
        load_dotenv()

        api_key = os.getenv('ANTHROPIC_API_KEY')

        if api_key:
            st.success("✅ API Key configurada")
        else:
            st.error("❌ API Key no encontrada")
            st.info("Configura ANTHROPIC_API_KEY en el archivo .env")

    # Routing a páginas
    if page == "🏠 Inicio":
        home.show()
    elif page == "📸 Análisis Individual":
        analyze.show()
    elif page == "📊 Análisis por Lotes":
        batch.show()
    elif page == "🔍 Comparación":
        compare.show()


if __name__ == "__main__":
    main()
