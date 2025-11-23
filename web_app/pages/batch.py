"""
Página de análisis por lotes
"""
import streamlit as st
import os
import tempfile
from pathlib import Path
import time
import io

from visual_audit import VisualAuditAnalyzer, BatchProcessor
from visual_audit.reporter import ReportGenerator


def show():
    """Muestra la página de análisis por lotes"""

    st.markdown("# 📊 Análisis por Lotes")
    st.markdown("Procesa múltiples imágenes simultáneamente y obtén reportes comparativos")

    # Verificar API key
    if not os.getenv('ANTHROPIC_API_KEY'):
        st.error("❌ API Key no configurada. Por favor configura ANTHROPIC_API_KEY en el archivo .env")
        st.info("💡 Obtén tu API key en: https://console.anthropic.com/")
        st.stop()

    # Upload múltiple
    st.markdown("### 📤 Subir Imágenes")

    uploaded_files = st.file_uploader(
        "Arrastra múltiples imágenes o haz click para seleccionar",
        type=['jpg', 'jpeg', 'png', 'webp', 'gif'],
        accept_multiple_files=True,
        help="Puedes seleccionar múltiples archivos. Formatos: JPG, PNG, WEBP, GIF"
    )

    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} imagen(es) cargada(s)")

        # Mostrar previews
        with st.expander(f"👀 Ver previews ({len(uploaded_files)} imágenes)"):
            cols = st.columns(min(4, len(uploaded_files)))
            for idx, file in enumerate(uploaded_files[:8]):  # Máximo 8 previews
                with cols[idx % 4]:
                    st.image(file, caption=file.name, use_container_width=True)

            if len(uploaded_files) > 8:
                st.info(f"... y {len(uploaded_files) - 8} imágenes más")

        st.markdown("---")

        # Configuración de procesamiento
        st.markdown("### ⚙️ Configuración de Procesamiento")

        col1, col2, col3 = st.columns(3)

        with col1:
            parallel = st.checkbox(
                "Procesamiento Paralelo",
                value=True,
                help="Procesa imágenes en paralelo (más rápido pero consume más recursos)"
            )

        with col2:
            workers = st.slider(
                "Workers Paralelos",
                min_value=1,
                max_value=10,
                value=min(3, len(uploaded_files)),
                disabled=not parallel,
                help="Número de imágenes a procesar simultáneamente (cuidado con rate limits)"
            )

        with col3:
            st.metric("Tiempo estimado", f"~{len(uploaded_files) * 45 / (workers if parallel else 1):.0f}s")

        st.markdown("---")

        # Botón de procesamiento
        if st.button("🚀 Procesar Lote", type="primary", use_container_width=True):
            process_batch(uploaded_files, parallel, workers)

    else:
        # Placeholder
        st.info("👆 Sube múltiples imágenes para comenzar el análisis por lotes")

        with st.expander("💡 Consejos para procesamiento por lotes"):
            st.markdown("""
            ### Recomendaciones:

            ✅ **Organización**
            - Nombra tus archivos descriptivamente (ej: `universidad_x_ingenieria.jpg`)
            - Agrupa por tipo de campaña o competidor

            ✅ **Cantidad óptima**
            - 5-10 imágenes: Ideal para comparación rápida
            - 10-30 imágenes: Análisis competitivo completo
            - 30+ imágenes: Auditoría exhaustiva (toma más tiempo)

            ✅ **Workers paralelos**
            - 1-3 workers: Seguro para cualquier cuenta
            - 3-5 workers: Recomendado si tienes buena conexión
            - 5+ workers: Solo si tienes rate limits altos

            ⚠️ **Rate Limits**
            - Si experimentas errores, reduce el número de workers
            - O desactiva procesamiento paralelo

            ### Reportes generados:

            📊 **Excel** - Comparativa con 3 hojas (General, Scores, Insights)
            📄 **CSV** - Datos tabulares para análisis en Excel/Python
            🗂️ **JSON** - Datos estructurados completos
            📝 **Markdown** - Reportes individuales legibles
            """)


def process_batch(uploaded_files, parallel, workers):
    """Procesa lote de imágenes"""

    # Crear directorio temporal
    temp_dir = tempfile.mkdtemp()

    try:
        # Guardar archivos temporalmente
        st.info(f"📁 Guardando {len(uploaded_files)} archivos...")
        temp_paths = []

        for uploaded_file in uploaded_files:
            temp_path = Path(temp_dir) / uploaded_file.name
            with open(temp_path, 'wb') as f:
                f.write(uploaded_file.getvalue())
            temp_paths.append(temp_path)

        # Crear procesador
        analyzer = VisualAuditAnalyzer()
        processor = BatchProcessor(analyzer=analyzer, max_workers=workers, verbose=False)

        # Procesar con progress bar
        st.markdown("### 🔄 Procesando...")

        progress_bar = st.progress(0)
        status_text = st.empty()

        start_time = time.time()

        # Procesar imágenes
        status_text.text(f"🤖 Analizando con Claude AI...")

        result = processor.process_batch(temp_paths, parallel=parallel)

        elapsed_time = time.time() - start_time

        progress_bar.progress(100)
        status_text.text(f"✅ Completado en {elapsed_time:.2f}s")

        # Mostrar resultados
        st.success(f"🎉 Procesamiento completado: {result.exitosas}/{result.total_imagenes} exitosas")

        if result.fallidas > 0:
            with st.expander(f"⚠️ {result.fallidas} imágenes fallidas"):
                for error in result.errores:
                    st.error(f"- {Path(error['imagen']).name}: {error['error']}")

        st.markdown("---")

        # Mostrar reportes
        show_batch_results(result)

    except Exception as e:
        st.error(f"❌ Error durante el procesamiento: {str(e)}")
        st.info("💡 Verifica que todas las imágenes sean válidas y que tu API key esté configurada")

    finally:
        # Limpiar archivos temporales
        import shutil
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def show_batch_results(result):
    """Muestra resultados del batch"""

    st.markdown("# 📊 Resultados del Lote")

    # Tabs
    tabs = st.tabs([
        "📈 Estadísticas",
        "📋 Tabla Comparativa",
        "📊 Visualizaciones",
        "📄 Exportar"
    ])

    # TAB 1: Estadísticas
    with tabs[0]:
        show_batch_stats(result)

    # TAB 2: Tabla comparativa
    with tabs[1]:
        show_comparison_table(result)

    # TAB 3: Visualizaciones
    with tabs[2]:
        show_batch_visualizations(result)

    # TAB 4: Exportar
    with tabs[3]:
        show_batch_export(result)


def show_batch_stats(result):
    """Muestra estadísticas del batch"""

    st.markdown("### 📊 Estadísticas Generales")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Imágenes", result.total_imagenes)

    with col2:
        st.metric("Exitosas", result.exitosas, delta=None)

    with col3:
        st.metric("Fallidas", result.fallidas, delta=None if result.fallidas == 0 else f"-{result.fallidas}")

    with col4:
        st.metric("Tiempo Total", f"{result.tiempo_procesamiento:.2f}s")

    if result.reportes:
        avg_time = result.tiempo_procesamiento / result.total_imagenes
        st.info(f"⏱️ Promedio por imagen: {avg_time:.2f}s")

    st.markdown("---")

    # Scores promedio
    if result.reportes:
        st.markdown("### 📊 Scores Promedio")

        avg_stockiness = sum(r.scores.stockiness for r in result.reportes) / len(result.reportes)
        avg_carga = sum(r.scores.carga_cognitiva for r in result.reportes) / len(result.reportes)
        avg_hard_sell = sum(r.scores.hard_sell for r in result.reportes) / len(result.reportes)
        avg_autenticidad = sum(r.scores.autenticidad_percibida for r in result.reportes) / len(result.reportes)
        avg_innovacion = sum(r.scores.innovacion_visual for r in result.reportes) / len(result.reportes)

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("📸 Stockiness", f"{avg_stockiness:.1f}/10")
        with col2:
            st.metric("🧠 Carga Cognitiva", f"{avg_carga:.1f}/10")
        with col3:
            st.metric("💰 Hard-Sell", f"{avg_hard_sell:.1f}/10")
        with col4:
            st.metric("✨ Autenticidad", f"{avg_autenticidad:.1f}/10")
        with col5:
            st.metric("🚀 Innovación", f"{avg_innovacion:.1f}/10")

        st.markdown("---")

        # Distribución de arquetipos
        st.markdown("### 🎭 Distribución de Arquetipos")

        arquetipos = {}
        for report in result.reportes:
            arq = str(report.fase4_estrategia.arquetipo_principal)
            arquetipos[arq] = arquetipos.get(arq, 0) + 1

        import plotly.graph_objects as go

        fig = go.Figure(data=[go.Pie(
            labels=list(arquetipos.keys()),
            values=list(arquetipos.values()),
            hole=0.3
        )])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)


def show_comparison_table(result):
    """Muestra tabla comparativa"""

    st.markdown("### 📋 Tabla Comparativa")

    if not result.reportes:
        st.warning("No hay reportes para mostrar")
        return

    # Generar tabla con ReportGenerator
    reporter = ReportGenerator(output_dir=tempfile.gettempdir())
    df = reporter.generate_comparison_table(result.reportes)

    # Mostrar DataFrame
    st.dataframe(
        df,
        use_container_width=True,
        height=400
    )

    # Destacar top performers
    st.markdown("#### 🏆 Top Performers")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Más Auténtica**")
        min_stock = df.loc[df['Stockiness'].idxmin()]
        st.info(f"{min_stock['Imagen']}\nScore: {min_stock['Stockiness']}/10")

    with col2:
        st.markdown("**Más Innovadora**")
        max_innov = df.loc[df['Innovación'].idxmax()]
        st.info(f"{max_innov['Imagen']}\nScore: {max_innov['Innovación']}/10")

    with col3:
        st.markdown("**Más Hard-Sell**")
        max_hard = df.loc[df['Hard-Sell'].idxmax()]
        st.info(f"{max_hard['Imagen']}\nScore: {max_hard['Hard-Sell']}/10")


def show_batch_visualizations(result):
    """Muestra visualizaciones del batch"""

    st.markdown("### 📊 Visualizaciones Comparativas")

    if not result.reportes:
        st.warning("No hay datos para visualizar")
        return

    import plotly.graph_objects as go
    import pandas as pd

    # Preparar datos
    data = []
    for report in result.reportes:
        data.append({
            'Imagen': report.imagen_nombre[:20] + '...' if len(report.imagen_nombre) > 20 else report.imagen_nombre,
            'Stockiness': report.scores.stockiness,
            'Carga Cognitiva': report.scores.carga_cognitiva,
            'Hard-Sell': report.scores.hard_sell,
            'Autenticidad': report.scores.autenticidad_percibida,
            'Innovación': report.scores.innovacion_visual
        })

    df = pd.DataFrame(data)

    # Gráfico de barras agrupadas
    st.markdown("#### 📊 Comparación de Scores")

    fig = go.Figure()

    metrics = ['Stockiness', 'Carga Cognitiva', 'Hard-Sell', 'Autenticidad', 'Innovación']
    colors = ['#667eea', '#f093fb', '#4facfe', '#43e97b', '#fa709a']

    for idx, metric in enumerate(metrics):
        fig.add_trace(go.Bar(
            name=metric,
            x=df['Imagen'],
            y=df[metric],
            marker_color=colors[idx]
        ))

    fig.update_layout(
        barmode='group',
        height=500,
        xaxis_tickangle=-45,
        yaxis_title="Score (0-10)",
        legend_title="Métrica"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Scatter plot: Autenticidad vs Innovación
    st.markdown("#### 📊 Autenticidad vs Innovación")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['Autenticidad'],
        y=df['Innovación'],
        mode='markers+text',
        text=df['Imagen'],
        textposition="top center",
        marker=dict(
            size=12,
            color=df['Hard-Sell'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Hard-Sell")
        ),
        hovertemplate='<b>%{text}</b><br>Autenticidad: %{x}<br>Innovación: %{y}<extra></extra>'
    ))

    fig.update_layout(
        xaxis_title="Autenticidad (0-10)",
        yaxis_title="Innovación (0-10)",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info("💡 El tamaño y color de los puntos representa el nivel de Hard-Sell")


def show_batch_export(result):
    """Muestra opciones de exportación del batch"""

    st.markdown("### 📄 Exportar Reportes")

    if not result.reportes:
        st.warning("No hay reportes para exportar")
        return

    # Generar reportes
    reporter = ReportGenerator(output_dir=tempfile.gettempdir())

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📊 Excel Comparativo")
        st.write("Archivo Excel con 3 hojas:")
        st.write("- Comparativa general")
        st.write("- Scores detallados")
        st.write("- Insights")

        # Generar Excel
        excel_buffer = io.BytesIO()
        import pandas as pd

        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df_comparison = reporter.generate_comparison_table(result.reportes)
            df_comparison.to_excel(writer, sheet_name='Comparativa', index=False)

        excel_data = excel_buffer.getvalue()

        st.download_button(
            label="📥 Descargar Excel",
            data=excel_data,
            file_name=f"batch_audit_comparativa.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    with col2:
        st.markdown("#### 📄 CSV Comparativo")
        st.write("Tabla comparativa en formato CSV para análisis adicional")

        df = reporter.generate_comparison_table(result.reportes)
        csv = df.to_csv(index=False)

        st.download_button(
            label="📥 Descargar CSV",
            data=csv,
            file_name=f"batch_audit_comparativa.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.markdown("---")

    st.markdown("#### 🗂️ JSON Batch Completo")

    import json
    batch_json = json.dumps(result.model_dump(mode='json'), indent=2, ensure_ascii=False)

    st.download_button(
        label="📥 Descargar JSON Completo",
        data=batch_json,
        file_name=f"batch_audit_completo.json",
        mime="application/json",
        use_container_width=True
    )

    st.markdown("---")

    st.info("💡 **Tip:** Descarga el Excel para obtener una comparativa visual completa con gráficos")
