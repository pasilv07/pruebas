"""
Página de inicio
"""
import streamlit as st


def show():
    """Muestra la página de inicio"""

    # Header principal
    st.markdown('<h1 class="main-header">🎓 Visual Audit App</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Auditoría Visual Competitiva para Campañas Educativas</p>',
        unsafe_allow_html=True
    )

    # Hero section
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        ## 🚀 ¿Qué hace esta aplicación?

        **Visual Audit App** analiza imágenes de campañas educativas (universidades, institutos, cursos online)
        y extrae insights estratégicos usando **Inteligencia Artificial**.

        ### ✨ Características principales:

        - 📊 **Análisis en 5 fases**: Decodificación técnica, inventario de contenido, análisis de texto, estrategia inferida y contexto cultural
        - 🎯 **Scores cuantitativos**: Métricas 0-10 (Stockiness, Carga Cognitiva, Hard-Sell, Autenticidad, Innovación)
        - 💡 **Insights competitivos**: Fortalezas, oportunidades de diferenciación, riesgos
        - 🚀 **Recomendaciones tácticas**: Acciones accionables para optimizar tu estrategia
        - 📁 **Procesamiento por lotes**: Analiza múltiples campañas simultáneamente
        - 📈 **Visualizaciones comparativas**: Dashboards interactivos con gráficos
        - 📄 **Exportación multi-formato**: JSON, Markdown, Excel, CSV
        """)

    with col2:
        st.info("### 🎯 Casos de uso\n\n"
                "✅ Analizar competidores\n\n"
                "✅ Comparar estrategias\n\n"
                "✅ Optimizar campañas\n\n"
                "✅ Benchmarking visual\n\n"
                "✅ Auditar histórico")

    st.markdown("---")

    # Framework de análisis
    st.markdown("## 📋 Framework de Análisis de 5 Fases")

    tabs = st.tabs([
        "🔍 Fase 1: Técnica",
        "📦 Fase 2: Contenido",
        "💬 Fase 3: Texto",
        "🎯 Fase 4: Estrategia",
        "🌎 Fase 5: Contexto"
    ])

    with tabs[0]:
        st.markdown("""
        ### Decodificación Técnica

        Analiza la **física de la atención** en la imagen:

        - **Autenticidad Visual (Stockiness 0-10)**
          - ¿Es auténtico o parece stock?
          - Iluminación, expresiones, props
          - Diversidad representativa

        - **Carga Cognitiva (0-10)**
          - Complejidad visual
          - Jerarquía de atención
          - Ubicación del CTA

        - **Sistema Cromático**
          - Paletas dominantes
          - Temperatura emocional
          - Colores específicos
        """)

    with tabs[1]:
        st.markdown("""
        ### Inventario de Contenido

        **¿Qué se muestra?**

        - **Protagonistas y Roles**
          - Tipo de sujeto (estudiante, profesional, grupo)
          - Dirección de mirada
          - Lenguaje corporal

        - **Escenografía**
          - Tipo de instalación (tradicional, tecnológica, social)
          - Señales de estatus
          - Materiales nobles

        - **Props y Símbolos**
          - Objetos visibles
          - Badges y sellos
          - Tecnología mostrada
        """)

    with tabs[2]:
        st.markdown("""
        ### Análisis de Texto

        **¿Qué se dice?**

        - **Jerarquía Verbal**
          - Headlines principales
          - Subheadlines y body
          - CTAs (urgencia)

        - **Tono Lingüístico**
          - Registro comunicativo
          - Frames semánticos
          - Ejemplos clave

        - **Propuesta de Valor**
          - Precio visible
          - Descuentos
          - Modalidad y duración
        """)

    with tabs[3]:
        st.markdown("""
        ### Estrategia Inferida

        **¿Qué significa?**

        - **Promesas Centrales**
          - Transformación personal
          - Empleabilidad
          - Prestigio/Status
          - Experiencia universitaria
          - Rigor académico
          - Accesibilidad
          - Innovación/Modernidad

        - **Arquetipo de Marca**
          - El Sabio, El Héroe, El Cuidador
          - El Creador, El Gobernante, El Amigo

        - **Posicionamiento Competitivo**
          - Aspiracional vs Accesible
          - Tradicional vs Innovador

        - **Hard-Sell Score (0-10)**
          - Agresividad de venta
        """)

    with tabs[4]:
        st.markdown("""
        ### Análisis Contextual

        **Contexto cultural y competitivo**

        - **Localización Cultural**
          - Adaptación a Paraguay/Latam
          - Modelos étnicos regionales
          - Referencias locales

        - **Benchmark Competitivo**
          - Similitud con competidores
          - Universidad estatal vs privada
          - Elite vs masivo
          - Tradicional vs online
        """)

    st.markdown("---")

    # Métricas explicadas
    st.markdown("## 📊 Scores Cuantitativos (0-10)")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ### 📸 Stockiness
        **¿Qué mide?** Autenticidad vs artificialidad

        - **0-3**: Auténtico (fotos reales, UGC-like)
        - **4-6**: Híbrido profesional
        - **7-10**: Stock puro (poses artificiales)
        """)

    with col2:
        st.markdown("""
        ### 🧠 Carga Cognitiva
        **¿Qué mide?** Complejidad visual

        - **0-3**: Minimalista (fácil de procesar)
        - **4-6**: Balanceado
        - **7-10**: Saturado (muchos elementos)
        """)

    with col3:
        st.markdown("""
        ### 💰 Hard-Sell
        **¿Qué mide?** Agresividad de venta

        - **0-2**: Soft-sell (branding, lifestyle)
        - **5**: Balanceado
        - **8-10**: Hard-sell (precio, urgencia)
        """)

    col4, col5 = st.columns(2)

    with col4:
        st.markdown("""
        ### ✨ Autenticidad
        **¿Qué mide?** Credibilidad y confianza transmitida

        Evaluación holística de todos los elementos que contribuyen a la autenticidad percibida.
        """)

    with col5:
        st.markdown("""
        ### 🚀 Innovación Visual
        **¿Qué mide?** Originalidad y modernidad del diseño

        Evaluación de creatividad, vanguardia y diferenciación visual.
        """)

    st.markdown("---")

    # Call to action
    st.markdown("## 🎬 Comienza Ahora")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📸 Analizar una imagen", use_container_width=True):
            st.switch_page("app.py")
            # Nota: en Streamlit 1.28+ se usaría st.switch_page, pero por compatibilidad usamos session_state

    with col2:
        if st.button("📊 Procesamiento por lotes", use_container_width=True):
            st.switch_page("app.py")

    with col3:
        if st.button("🔍 Ver comparaciones", use_container_width=True):
            st.switch_page("app.py")

    st.markdown("---")

    # Footer
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p><strong>Visual Audit App v1.0</strong></p>
        <p>Powered by Claude AI (Anthropic) • Hecho con ❤️ para marketing educativo</p>
    </div>
    """, unsafe_allow_html=True)
