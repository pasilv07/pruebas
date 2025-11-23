"""
Página de análisis individual
"""
import streamlit as st
import os
import tempfile
from pathlib import Path
import plotly.graph_objects as go
import json

from visual_audit import VisualAuditAnalyzer
from visual_audit.reporter import ReportGenerator


def show():
    """Muestra la página de análisis individual"""

    st.markdown("# 📸 Análisis Individual")
    st.markdown("Sube una imagen de campaña educativa para análisis exhaustivo")

    # Verificar API key
    if not os.getenv('ANTHROPIC_API_KEY'):
        st.error("❌ API Key no configurada. Por favor configura ANTHROPIC_API_KEY en el archivo .env")
        st.info("💡 Obtén tu API key en: https://console.anthropic.com/")
        st.stop()

    # Upload de imagen
    st.markdown("### 📤 Subir Imagen")

    uploaded_file = st.file_uploader(
        "Arrastra una imagen o haz click para seleccionar",
        type=['jpg', 'jpeg', 'png', 'webp', 'gif'],
        help="Formatos soportados: JPG, PNG, WEBP, GIF (máx 10MB)"
    )

    if uploaded_file is not None:
        # Mostrar imagen
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("#### 🖼️ Imagen Original")
            st.image(uploaded_file, use_container_width=True)

        with col2:
            st.markdown("#### ℹ️ Información del Archivo")
            st.write(f"**Nombre:** {uploaded_file.name}")
            st.write(f"**Tamaño:** {uploaded_file.size / 1024:.2f} KB")
            st.write(f"**Tipo:** {uploaded_file.type}")

        st.markdown("---")

        # Botón de análisis
        if st.button("🚀 Analizar Imagen", type="primary", use_container_width=True):
            # Guardar archivo temporalmente
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name

            try:
                # Crear analizador
                with st.spinner("🤖 Analizando con Claude AI... Esto puede tomar 30-60 segundos..."):
                    analyzer = VisualAuditAnalyzer()
                    report = analyzer.analyze_image(tmp_path, verbose=False)

                st.success("✅ Análisis completado exitosamente!")

                # Guardar en session_state
                st.session_state['current_report'] = report

                # Mostrar resultados
                show_report(report, uploaded_file.name)

            except Exception as e:
                st.error(f"❌ Error durante el análisis: {str(e)}")
                st.info("💡 Verifica que la imagen sea válida y que tu API key esté configurada correctamente")

            finally:
                # Limpiar archivo temporal
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

    else:
        # Placeholder cuando no hay imagen
        st.info("👆 Sube una imagen de campaña educativa para comenzar el análisis")

        with st.expander("💡 Tips para mejores resultados"):
            st.markdown("""
            ### Imágenes ideales:

            ✅ **Alta resolución** (mejor análisis de texto)
            ✅ **Texto visible** (headlines, CTAs legibles)
            ✅ **Campañas reales** (Facebook Ads, Instagram, Display Ads)
            ✅ **Contenido educativo** (universidades, institutos, cursos)

            ### Evitar:

            ❌ Imágenes borrosas o muy comprimidas
            ❌ Solo logos sin contexto
            ❌ Screenshots con demasiado ruido visual

            ### Ejemplos de fuentes:
            - Capturas de Facebook/Instagram Ads
            - Banners de sitios web educativos
            - Material impreso digitalizado (folletos, afiches)
            - Posts en redes sociales de instituciones
            """)


def show_report(report, filename):
    """Muestra el reporte de análisis"""

    st.markdown("---")
    st.markdown("# 📊 Reporte de Auditoría Visual")

    # Tabs principales
    tabs = st.tabs([
        "📈 Resumen Ejecutivo",
        "🔍 Análisis Completo",
        "💡 Insights",
        "🚀 Recomendaciones",
        "📄 Exportar"
    ])

    # TAB 1: Resumen Ejecutivo
    with tabs[0]:
        show_executive_summary(report, filename)

    # TAB 2: Análisis Completo
    with tabs[1]:
        show_full_analysis(report)

    # TAB 3: Insights
    with tabs[2]:
        show_insights(report)

    # TAB 4: Recomendaciones
    with tabs[3]:
        show_recommendations(report)

    # TAB 5: Exportar
    with tabs[4]:
        show_export_options(report)


def show_executive_summary(report, filename):
    """Muestra resumen ejecutivo"""

    st.markdown(f"### 📋 {filename}")

    # Identificación
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Institución", report.institucion or "No identificable")
    with col2:
        st.metric("Programa", report.programa or "No especificado")
    with col3:
        st.metric("Convocatoria", report.convocatoria or "N/A")

    st.markdown("---")

    # Scores principales
    st.markdown("### 📊 Scores Cuantitativos")

    col1, col2, col3, col4, col5 = st.columns(5)

    scores = [
        (col1, "Stockiness", report.scores.stockiness, "📸"),
        (col2, "Carga Cognitiva", report.scores.carga_cognitiva, "🧠"),
        (col3, "Hard-Sell", report.scores.hard_sell, "💰"),
        (col4, "Autenticidad", report.scores.autenticidad_percibida, "✨"),
        (col5, "Innovación", report.scores.innovacion_visual, "🚀"),
    ]

    for col, label, value, icon in scores:
        with col:
            # Color basado en valor
            if value <= 3:
                color = "🟢"
            elif value <= 6:
                color = "🟡"
            else:
                color = "🔴"

            st.metric(f"{icon} {label}", f"{value}/10", delta=None)

    # Gráfico de radar con scores
    st.markdown("#### 📊 Perfil Visual")

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[
            report.scores.stockiness,
            report.scores.carga_cognitiva,
            report.scores.hard_sell,
            report.scores.autenticidad_percibida,
            report.scores.innovacion_visual
        ],
        theta=['Stockiness', 'Carga<br>Cognitiva', 'Hard-Sell', 'Autenticidad', 'Innovación'],
        fill='toself',
        name='Scores',
        line_color='rgb(102, 126, 234)',
        fillcolor='rgba(102, 126, 234, 0.3)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=False,
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Resumen estratégico
    st.markdown("### 🎯 Resumen Estratégico")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Promesa Central:**")
        st.info(report.promesa_resumen)

        st.markdown("**Arquetipo de Marca:**")
        st.success(f"**Principal:** {report.fase4_estrategia.arquetipo_principal}")
        if report.fase4_estrategia.arquetipo_secundario:
            st.write(f"*Secundario:* {report.fase4_estrategia.arquetipo_secundario}")

    with col2:
        st.markdown("**Público Objetivo:**")
        st.info(report.publico_objetivo)

        st.markdown("**Palabras Clave:**")
        keywords_html = " ".join([f"<span style='background: #e3f2fd; padding: 0.25rem 0.5rem; border-radius: 5px; margin: 0.25rem; display: inline-block;'>{kw}</span>" for kw in report.palabras_clave])
        st.markdown(keywords_html, unsafe_allow_html=True)


def show_full_analysis(report):
    """Muestra análisis completo de las 5 fases"""

    phases = st.tabs([
        "🔍 Fase 1: Técnica",
        "📦 Fase 2: Contenido",
        "💬 Fase 3: Texto",
        "🎯 Fase 4: Estrategia",
        "🌎 Fase 5: Contexto"
    ])

    # FASE 1
    with phases[0]:
        st.markdown("### Decodificación Técnica")

        # Autenticidad
        st.markdown("#### 📸 Autenticidad Visual")
        st.metric("Stockiness Score", f"{report.fase1_decodificacion.autenticidad.stockiness_score}/10")

        col1, col2 = st.columns(2)
        with col1:
            st.write("✅ **Iluminación de estudio:**", "Sí" if report.fase1_decodificacion.autenticidad.tiene_iluminacion_estudio else "No")
            st.write("✅ **Sonrisa genuina:**", "Sí" if report.fase1_decodificacion.autenticidad.sonrisa_genuina else "No")
        with col2:
            st.write("✅ **Props reales:**", "Sí" if report.fase1_decodificacion.autenticidad.props_reales else "No")
            st.write("✅ **Diversidad representativa:**", "Sí" if report.fase1_decodificacion.autenticidad.diversidad_representativa else "No")

        if report.fase1_decodificacion.autenticidad.notas:
            st.info(f"**Notas:** {report.fase1_decodificacion.autenticidad.notas}")

        st.markdown("---")

        # Carga cognitiva
        st.markdown("#### 🧠 Carga Cognitiva")
        st.metric("Complejidad Score", f"{report.fase1_decodificacion.carga_cognitiva.complejidad_score}/10")

        st.write(f"**Atención primero:** {report.fase1_decodificacion.carga_cognitiva.atencion_primero}")
        st.write(f"**Atención después:** {report.fase1_decodificacion.carga_cognitiva.atencion_segundo}")
        st.write(f"**Ubicación CTA:** {report.fase1_decodificacion.carga_cognitiva.ubicacion_cta}")

        st.markdown("---")

        # Sistema cromático
        st.markdown("#### 🎨 Sistema Cromático")

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Temperatura emocional:** {report.fase1_decodificacion.sistema_cromatico.temperatura_emocional}")
            st.write(f"**Colores dominantes:** {', '.join(report.fase1_decodificacion.sistema_cromatico.colores_dominantes)}")

        with col2:
            # Gráfico de paletas
            paletas = {
                'Institucional': report.fase1_decodificacion.sistema_cromatico.paleta_institucional,
                'Tecnológica': report.fase1_decodificacion.sistema_cromatico.paleta_tecnologica,
                'Vibrante': report.fase1_decodificacion.sistema_cromatico.paleta_vibrante,
                'Minimalista': report.fase1_decodificacion.sistema_cromatico.paleta_minimalista
            }

            fig = go.Figure(data=[go.Pie(
                labels=list(paletas.keys()),
                values=list(paletas.values()),
                hole=0.3
            )])
            fig.update_layout(height=250, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)

    # FASE 2
    with phases[1]:
        st.markdown("### Inventario de Contenido")

        # Protagonistas
        st.markdown("#### 👥 Protagonistas y Roles")
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Tipo de sujeto:** {report.fase2_inventario.protagonistas.tipo_sujeto}")
            st.write(f"**Dirección de mirada:** {report.fase2_inventario.protagonistas.direccion_mirada}")

        with col2:
            st.write(f"**Lenguaje corporal:** {', '.join(report.fase2_inventario.protagonistas.lenguaje_corporal)}")

        st.info(report.fase2_inventario.protagonistas.descripcion_detallada)

        st.markdown("---")

        # Escenografía
        st.markdown("#### 🏛️ Escenografía")
        st.write(f"**Tipo:** {report.fase2_inventario.escenografia.tipo_instalacion}")

        col1, col2 = st.columns(2)
        with col1:
            st.write("✅ **Materiales nobles:**", "Sí" if report.fase2_inventario.escenografia.materiales_nobles else "No")
            st.write("✅ **Tecnología visible:**", "Sí" if report.fase2_inventario.escenografia.tecnologia_visible else "No")
        with col2:
            st.write("✅ **Amplitud espacial:**", "Sí" if report.fase2_inventario.escenografia.amplitud_espacial else "No")
            st.write("✅ **Orden extremo:**", "Sí" if report.fase2_inventario.escenografia.orden_extremo else "No")

        st.info(report.fase2_inventario.escenografia.descripcion)

        st.markdown("---")

        # Props
        st.markdown("#### 🎒 Props y Símbolos")
        col1, col2 = st.columns(2)

        with col1:
            st.write("📚 **Libros físicos:**", "Sí" if report.fase2_inventario.props_simbolos.libros_fisicos else "No")
            st.write("💻 **Laptops/Tablets:**", "Sí" if report.fase2_inventario.props_simbolos.laptops_tablets else "No")

        with col2:
            st.write("🎧 **Auriculares:**", "Sí" if report.fase2_inventario.props_simbolos.auriculares else "No")
            st.write("🔬 **Instrumentos profesionales:**", "Sí" if report.fase2_inventario.props_simbolos.instrumentos_profesionales else "No")

        if report.fase2_inventario.props_simbolos.badges_sellos:
            st.write(f"**Badges/Sellos:** {', '.join(report.fase2_inventario.props_simbolos.badges_sellos)}")

        if report.fase2_inventario.props_simbolos.otros_objetos:
            st.write(f"**Otros objetos:** {', '.join(report.fase2_inventario.props_simbolos.otros_objetos)}")

    # FASE 3
    with phases[2]:
        st.markdown("### Análisis de Texto")

        # Jerarquía verbal
        st.markdown("#### 💬 Jerarquía Verbal")

        st.markdown(f"**Headline Principal:** `{report.fase3_texto.jerarquia_verbal.headline_principal}`")
        st.write(f"Longitud: {report.fase3_texto.jerarquia_verbal.headline_longitud} palabras")

        if report.fase3_texto.jerarquia_verbal.subheadlines:
            st.markdown("**Subheadlines:**")
            for sh in report.fase3_texto.jerarquia_verbal.subheadlines:
                st.write(f"- {sh}")

        st.markdown(f"**CTA:** `{report.fase3_texto.jerarquia_verbal.cta_texto}`")
        st.write(f"Urgencia: {report.fase3_texto.jerarquia_verbal.cta_urgencia}")

        st.markdown("---")

        # Tono
        st.markdown("#### 🗣️ Tono Lingüístico")
        st.write(f"**Registro:** {report.fase3_texto.tono_linguistico.registro}")
        st.write(f"**Frames semánticos:** {', '.join(report.fase3_texto.tono_linguistico.frame_semantico)}")

        if report.fase3_texto.tono_linguistico.ejemplos_texto:
            st.markdown("**Ejemplos clave:**")
            for ej in report.fase3_texto.tono_linguistico.ejemplos_texto:
                st.code(ej, language=None)

        st.markdown("---")

        # Propuesta de valor
        st.markdown("#### 💰 Propuesta de Valor")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Precio", report.fase3_texto.propuesta_valor.precio_visible or "No visible")
            st.metric("Descuentos", report.fase3_texto.propuesta_valor.descuentos or "No")
        with col2:
            st.metric("Modalidad", report.fase3_texto.propuesta_valor.modalidad or "No especificada")
            st.metric("Duración", report.fase3_texto.propuesta_valor.duracion or "No especificada")
        with col3:
            st.metric("Fecha límite", report.fase3_texto.propuesta_valor.fecha_limite or "No especificada")

    # FASE 4
    with phases[3]:
        st.markdown("### Estrategia Inferida")

        # Promesas
        st.markdown("#### 🎯 Promesas Centrales")
        for promesa in report.fase4_estrategia.promesas_centrales:
            st.write(f"- {promesa}")

        st.markdown("---")

        # Arquetipos
        st.markdown("#### 🎭 Arquetipos de Marca")
        st.success(f"**Principal:** {report.fase4_estrategia.arquetipo_principal}")
        if report.fase4_estrategia.arquetipo_secundario:
            st.info(f"**Secundario:** {report.fase4_estrategia.arquetipo_secundario}")

        st.markdown("---")

        # Posicionamiento
        st.markdown("#### 📊 Posicionamiento Competitivo")
        st.info(report.fase4_estrategia.posicionamiento_cuadrante)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Hard-Sell Score", f"{report.fase4_estrategia.hard_sell_score}/10")
        with col2:
            if report.fase4_estrategia.hard_sell_score <= 3:
                st.write("**Tipo:** Soft-sell (branding)")
            elif report.fase4_estrategia.hard_sell_score <= 6:
                st.write("**Tipo:** Balanceado")
            else:
                st.write("**Tipo:** Hard-sell (venta agresiva)")

        st.markdown(f"**Descripción:** {report.fase4_estrategia.estrategia_descripcion}")

    # FASE 5
    with phases[4]:
        st.markdown("### Análisis Contextual")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Adaptación Local",
                "Sí" if report.fase5_contextual.tiene_adaptacion_local else "No"
            )

        with col2:
            st.metric(
                "Modelos Regionales",
                "Sí" if report.fase5_contextual.modelos_etnicos_regionales else "No"
            )

        with col3:
            st.metric(
                "Referencias Paraguay",
                "Sí" if report.fase5_contextual.referencias_paraguay else "No"
            )

        st.markdown("---")

        st.markdown("#### 📊 Benchmark Competitivo")
        st.write("**Similar a:**")
        for bench in report.fase5_contextual.benchmark_similar:
            st.write(f"- {bench}")

        if report.fase5_contextual.notas_culturales:
            st.markdown("#### 📝 Notas Culturales")
            st.info(report.fase5_contextual.notas_culturales)


def show_insights(report):
    """Muestra insights competitivos"""

    st.markdown("### 💡 Insights Competitivos")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### ✅ Fortalezas")
        for f in report.insights.fortalezas:
            st.success(f"✓ {f}")

    with col2:
        st.markdown("#### 🎯 Oportunidades")
        for o in report.insights.oportunidades_diferenciacion:
            st.info(f"→ {o}")

    with col3:
        st.markdown("#### ⚠️ Riesgos")
        for r in report.insights.riesgos_debilidades:
            st.warning(f"! {r}")


def show_recommendations(report):
    """Muestra recomendaciones tácticas"""

    st.markdown("### 🚀 Recomendaciones Tácticas")

    st.markdown("#### 🎯 Acciones de Contraste")
    st.markdown("*Si estuvieras compitiendo CONTRA esta campaña, harías:*")
    for i, accion in enumerate(report.recomendaciones.acciones_contraste, 1):
        st.write(f"{i}. {accion}")

    st.markdown("---")

    st.markdown("#### ⛔ Elementos a Evitar")
    for i, elem in enumerate(report.recomendaciones.elementos_evitar, 1):
        st.write(f"{i}. {elem}")

    st.markdown("---")

    st.markdown("#### 💎 Nichos Desatendidos")
    st.markdown("*Oportunidades que esta campaña NO está capturando:*")
    for i, nicho in enumerate(report.recomendaciones.nichos_desatendidos, 1):
        st.write(f"{i}. {nicho}")


def show_export_options(report):
    """Muestra opciones de exportación"""

    st.markdown("### 📄 Exportar Reporte")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### JSON")
        json_str = json.dumps(report.model_dump(mode='json'), indent=2, ensure_ascii=False)

        st.download_button(
            label="📥 Descargar JSON",
            data=json_str,
            file_name=f"{report.id_reporte}.json",
            mime="application/json",
            use_container_width=True
        )

        with st.expander("Ver JSON"):
            st.code(json_str, language='json')

    with col2:
        st.markdown("#### Markdown")

        # Generar markdown
        reporter = ReportGenerator(output_dir=tempfile.gettempdir())
        md_content = reporter.generate_markdown(report)

        st.download_button(
            label="📥 Descargar Markdown",
            data=md_content,
            file_name=f"{report.id_reporte}.md",
            mime="text/markdown",
            use_container_width=True
        )

        with st.expander("Ver Markdown"):
            st.code(md_content, language='markdown')

    st.markdown("---")

    st.info("💡 **Tip:** Para exportar a Excel o CSV con comparativas, usa el análisis por lotes")
