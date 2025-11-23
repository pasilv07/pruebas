"""
Página de comparación
"""
import streamlit as st
import json
from pathlib import Path
import plotly.graph_objects as go

from visual_audit.models import AuditReport


def show():
    """Muestra la página de comparación"""

    st.markdown("# 🔍 Comparación de Campañas")
    st.markdown("Compara reportes guardados lado a lado")

    # Buscar reportes JSON en output/
    output_dir = Path("output")

    if not output_dir.exists():
        st.warning("📁 La carpeta 'output/' no existe aún. Genera algunos reportes primero.")
        return

    json_files = list(output_dir.glob("*.json"))
    json_files = [f for f in json_files if not f.name.startswith("batch_")]  # Excluir batch files

    if not json_files:
        st.info("📭 No hay reportes individuales guardados en output/")
        st.write("💡 Genera reportes usando 'Análisis Individual' o 'Análisis por Lotes'")
        return

    st.success(f"✅ {len(json_files)} reporte(s) disponible(s)")

    # Selector de reportes a comparar
    st.markdown("### 📋 Seleccionar Reportes")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Campaña A")
        report_a_file = st.selectbox(
            "Selecciona primera campaña",
            options=json_files,
            format_func=lambda x: x.stem,
            key="report_a"
        )

    with col2:
        st.markdown("#### Campaña B")
        report_b_file = st.selectbox(
            "Selecciona segunda campaña",
            options=json_files,
            format_func=lambda x: x.stem,
            key="report_b"
        )

    if report_a_file and report_b_file:
        if report_a_file == report_b_file:
            st.warning("⚠️ Selecciona dos reportes diferentes para comparar")
            return

        # Cargar reportes
        try:
            with open(report_a_file) as f:
                report_a_data = json.load(f)
            report_a = AuditReport(**report_a_data)

            with open(report_b_file) as f:
                report_b_data = json.load(f)
            report_b = AuditReport(**report_b_data)

            st.markdown("---")

            # Mostrar comparación
            show_comparison(report_a, report_b)

        except Exception as e:
            st.error(f"❌ Error cargando reportes: {str(e)}")


def show_comparison(report_a, report_b):
    """Muestra comparación de dos reportes"""

    st.markdown("# 📊 Comparación Detallada")

    # Tabs
    tabs = st.tabs([
        "📈 Scores",
        "🎯 Estrategia",
        "💬 Mensajes",
        "🎨 Visual",
        "💡 Insights"
    ])

    # TAB 1: Scores
    with tabs[0]:
        show_scores_comparison(report_a, report_b)

    # TAB 2: Estrategia
    with tabs[1]:
        show_strategy_comparison(report_a, report_b)

    # TAB 3: Mensajes
    with tabs[2]:
        show_messages_comparison(report_a, report_b)

    # TAB 4: Visual
    with tabs[3]:
        show_visual_comparison(report_a, report_b)

    # TAB 5: Insights
    with tabs[4]:
        show_insights_comparison(report_a, report_b)


def show_scores_comparison(report_a, report_b):
    """Compara scores"""

    st.markdown("### 📊 Comparación de Scores")

    # Tabla comparativa
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.markdown("**Métrica**")
    with col2:
        st.markdown(f"**A:** {report_a.imagen_nombre[:20]}...")
    with col3:
        st.markdown(f"**B:** {report_b.imagen_nombre[:20]}...")

    st.markdown("---")

    metrics = [
        ("📸 Stockiness", "stockiness"),
        ("🧠 Carga Cognitiva", "carga_cognitiva"),
        ("💰 Hard-Sell", "hard_sell"),
        ("✨ Autenticidad", "autenticidad_percibida"),
        ("🚀 Innovación", "innovacion_visual"),
    ]

    for label, attr in metrics:
        col1, col2, col3 = st.columns([2, 1, 1])

        score_a = getattr(report_a.scores, attr)
        score_b = getattr(report_b.scores, attr)
        diff = score_b - score_a

        with col1:
            st.write(label)

        with col2:
            st.metric("", f"{score_a}/10", delta=None)

        with col3:
            delta_label = f"{'+' if diff > 0 else ''}{diff}"
            st.metric("", f"{score_b}/10", delta=delta_label)

    st.markdown("---")

    # Gráfico de radar comparativo
    st.markdown("### 📊 Perfil Visual Comparativo")

    fig = go.Figure()

    categories = ['Stockiness', 'Carga<br>Cognitiva', 'Hard-Sell', 'Autenticidad', 'Innovación']

    fig.add_trace(go.Scatterpolar(
        r=[
            report_a.scores.stockiness,
            report_a.scores.carga_cognitiva,
            report_a.scores.hard_sell,
            report_a.scores.autenticidad_percibida,
            report_a.scores.innovacion_visual
        ],
        theta=categories,
        fill='toself',
        name='Campaña A',
        line_color='rgb(102, 126, 234)',
        fillcolor='rgba(102, 126, 234, 0.3)'
    ))

    fig.add_trace(go.Scatterpolar(
        r=[
            report_b.scores.stockiness,
            report_b.scores.carga_cognitiva,
            report_b.scores.hard_sell,
            report_b.scores.autenticidad_percibida,
            report_b.scores.innovacion_visual
        ],
        theta=categories,
        fill='toself',
        name='Campaña B',
        line_color='rgb(240, 147, 251)',
        fillcolor='rgba(240, 147, 251, 0.3)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=True,
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)


def show_strategy_comparison(report_a, report_b):
    """Compara estrategias"""

    st.markdown("### 🎯 Comparación Estratégica")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"#### Campaña A: {report_a.imagen_nombre[:25]}...")

        st.markdown("**Arquetipo Principal:**")
        st.info(report_a.fase4_estrategia.arquetipo_principal)

        st.markdown("**Promesas Centrales:**")
        for promesa in report_a.fase4_estrategia.promesas_centrales:
            st.write(f"- {promesa}")

        st.markdown("**Posicionamiento:**")
        st.code(report_a.fase4_estrategia.posicionamiento_cuadrante, language=None)

        st.metric("Hard-Sell Score", f"{report_a.fase4_estrategia.hard_sell_score}/10")

    with col2:
        st.markdown(f"#### Campaña B: {report_b.imagen_nombre[:25]}...")

        st.markdown("**Arquetipo Principal:**")
        st.info(report_b.fase4_estrategia.arquetipo_principal)

        st.markdown("**Promesas Centrales:**")
        for promesa in report_b.fase4_estrategia.promesas_centrales:
            st.write(f"- {promesa}")

        st.markdown("**Posicionamiento:**")
        st.code(report_b.fase4_estrategia.posicionamiento_cuadrante, language=None)

        st.metric("Hard-Sell Score", f"{report_b.fase4_estrategia.hard_sell_score}/10")

    st.markdown("---")

    # Análisis de diferencias
    st.markdown("### 🔍 Análisis de Diferencias")

    # Comparar arquetipos
    if report_a.fase4_estrategia.arquetipo_principal == report_b.fase4_estrategia.arquetipo_principal:
        st.success(f"✅ Ambas campañas usan el mismo arquetipo: **{report_a.fase4_estrategia.arquetipo_principal}**")
    else:
        st.warning(f"⚠️ Arquetipos diferentes:")
        st.write(f"- Campaña A: **{report_a.fase4_estrategia.arquetipo_principal}**")
        st.write(f"- Campaña B: **{report_b.fase4_estrategia.arquetipo_principal}**")

    # Comparar promesas
    promesas_a = set(report_a.fase4_estrategia.promesas_centrales)
    promesas_b = set(report_b.fase4_estrategia.promesas_centrales)

    promesas_comunes = promesas_a & promesas_b
    promesas_solo_a = promesas_a - promesas_b
    promesas_solo_b = promesas_b - promesas_a

    if promesas_comunes:
        st.info(f"🤝 **Promesas compartidas:** {', '.join(promesas_comunes)}")

    if promesas_solo_a:
        st.write(f"**Solo en A:** {', '.join(promesas_solo_a)}")

    if promesas_solo_b:
        st.write(f"**Solo en B:** {', '.join(promesas_solo_b)}")


def show_messages_comparison(report_a, report_b):
    """Compara mensajes"""

    st.markdown("### 💬 Comparación de Mensajes")

    # Headlines
    st.markdown("#### 📣 Headlines")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Campaña A:**")
        st.code(report_a.fase3_texto.jerarquia_verbal.headline_principal, language=None)
        st.caption(f"Longitud: {report_a.fase3_texto.jerarquia_verbal.headline_longitud} palabras")

    with col2:
        st.markdown("**Campaña B:**")
        st.code(report_b.fase3_texto.jerarquia_verbal.headline_principal, language=None)
        st.caption(f"Longitud: {report_b.fase3_texto.jerarquia_verbal.headline_longitud} palabras")

    st.markdown("---")

    # CTAs
    st.markdown("#### 🎯 Calls to Action")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Campaña A:**")
        st.code(report_a.fase3_texto.jerarquia_verbal.cta_texto, language=None)
        st.caption(f"Urgencia: {report_a.fase3_texto.jerarquia_verbal.cta_urgencia}")

    with col2:
        st.markdown("**Campaña B:**")
        st.code(report_b.fase3_texto.jerarquia_verbal.cta_texto, language=None)
        st.caption(f"Urgencia: {report_b.fase3_texto.jerarquia_verbal.cta_urgencia}")

    st.markdown("---")

    # Tono
    st.markdown("#### 🗣️ Tono Lingüístico")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Campaña A:**")
        st.write(f"**Registro:** {report_a.fase3_texto.tono_linguistico.registro}")
        st.write(f"**Frames:** {', '.join(report_a.fase3_texto.tono_linguistico.frame_semantico)}")

    with col2:
        st.markdown("**Campaña B:**")
        st.write(f"**Registro:** {report_b.fase3_texto.tono_linguistico.registro}")
        st.write(f"**Frames:** {', '.join(report_b.fase3_texto.tono_linguistico.frame_semantico)}")

    st.markdown("---")

    # Propuesta de valor
    st.markdown("#### 💰 Propuesta de Valor")

    data = {
        "Elemento": ["Precio", "Descuentos", "Modalidad", "Duración", "Fecha límite"],
        "Campaña A": [
            report_a.fase3_texto.propuesta_valor.precio_visible or "No visible",
            report_a.fase3_texto.propuesta_valor.descuentos or "No",
            report_a.fase3_texto.propuesta_valor.modalidad or "No especificada",
            report_a.fase3_texto.propuesta_valor.duracion or "No especificada",
            report_a.fase3_texto.propuesta_valor.fecha_limite or "No especificada"
        ],
        "Campaña B": [
            report_b.fase3_texto.propuesta_valor.precio_visible or "No visible",
            report_b.fase3_texto.propuesta_valor.descuentos or "No",
            report_b.fase3_texto.propuesta_valor.modalidad or "No especificada",
            report_b.fase3_texto.propuesta_valor.duracion or "No especificada",
            report_b.fase3_texto.propuesta_valor.fecha_limite or "No especificada"
        ]
    }

    import pandas as pd
    df = pd.DataFrame(data)
    st.table(df)


def show_visual_comparison(report_a, report_b):
    """Compara elementos visuales"""

    st.markdown("### 🎨 Comparación Visual")

    # Cromática
    st.markdown("#### 🌈 Sistema Cromático")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Campaña A:**")
        st.write(f"**Temperatura:** {report_a.fase1_decodificacion.sistema_cromatico.temperatura_emocional}")
        st.write(f"**Colores dominantes:** {', '.join(report_a.fase1_decodificacion.sistema_cromatico.colores_dominantes)}")

        # Gráfico de paletas A
        paletas_a = {
            'Institucional': report_a.fase1_decodificacion.sistema_cromatico.paleta_institucional,
            'Tecnológica': report_a.fase1_decodificacion.sistema_cromatico.paleta_tecnologica,
            'Vibrante': report_a.fase1_decodificacion.sistema_cromatico.paleta_vibrante,
            'Minimalista': report_a.fase1_decodificacion.sistema_cromatico.paleta_minimalista
        }

        fig_a = go.Figure(data=[go.Pie(
            labels=list(paletas_a.keys()),
            values=list(paletas_a.values()),
            hole=0.4
        )])
        fig_a.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0), showlegend=False)
        st.plotly_chart(fig_a, use_container_width=True)

    with col2:
        st.markdown("**Campaña B:**")
        st.write(f"**Temperatura:** {report_b.fase1_decodificacion.sistema_cromatico.temperatura_emocional}")
        st.write(f"**Colores dominantes:** {', '.join(report_b.fase1_decodificacion.sistema_cromatico.colores_dominantes)}")

        # Gráfico de paletas B
        paletas_b = {
            'Institucional': report_b.fase1_decodificacion.sistema_cromatico.paleta_institucional,
            'Tecnológica': report_b.fase1_decodificacion.sistema_cromatico.paleta_tecnologica,
            'Vibrante': report_b.fase1_decodificacion.sistema_cromatico.paleta_vibrante,
            'Minimalista': report_b.fase1_decodificacion.sistema_cromatico.paleta_minimalista
        }

        fig_b = go.Figure(data=[go.Pie(
            labels=list(paletas_b.keys()),
            values=list(paletas_b.values()),
            hole=0.4
        )])
        fig_b.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0), showlegend=False)
        st.plotly_chart(fig_b, use_container_width=True)

    st.markdown("---")

    # Protagonistas
    st.markdown("#### 👥 Protagonistas")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Campaña A:**")
        st.write(f"**Tipo:** {report_a.fase2_inventario.protagonistas.tipo_sujeto}")
        st.write(f"**Mirada:** {report_a.fase2_inventario.protagonistas.direccion_mirada}")

    with col2:
        st.markdown("**Campaña B:**")
        st.write(f"**Tipo:** {report_b.fase2_inventario.protagonistas.tipo_sujeto}")
        st.write(f"**Mirada:** {report_b.fase2_inventario.protagonistas.direccion_mirada}")

    st.markdown("---")

    # Escenografía
    st.markdown("#### 🏛️ Escenografía")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Campaña A:**")
        st.write(f"**Tipo:** {report_a.fase2_inventario.escenografia.tipo_instalacion}")
        st.info(report_a.fase2_inventario.escenografia.descripcion[:150] + "...")

    with col2:
        st.markdown("**Campaña B:**")
        st.write(f"**Tipo:** {report_b.fase2_inventario.escenografia.tipo_instalacion}")
        st.info(report_b.fase2_inventario.escenografia.descripcion[:150] + "...")


def show_insights_comparison(report_a, report_b):
    """Compara insights"""

    st.markdown("### 💡 Comparación de Insights")

    # Fortalezas
    st.markdown("#### ✅ Fortalezas")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Campaña A:**")
        for f in report_a.insights.fortalezas:
            st.success(f"✓ {f}")

    with col2:
        st.markdown("**Campaña B:**")
        for f in report_b.insights.fortalezas:
            st.success(f"✓ {f}")

    st.markdown("---")

    # Oportunidades
    st.markdown("#### 🎯 Oportunidades de Diferenciación")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Campaña A:**")
        for o in report_a.insights.oportunidades_diferenciacion:
            st.info(f"→ {o}")

    with col2:
        st.markdown("**Campaña B:**")
        for o in report_b.insights.oportunidades_diferenciacion:
            st.info(f"→ {o}")

    st.markdown("---")

    # Riesgos
    st.markdown("#### ⚠️ Riesgos/Debilidades")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Campaña A:**")
        for r in report_a.insights.riesgos_debilidades:
            st.warning(f"! {r}")

    with col2:
        st.markdown("**Campaña B:**")
        for r in report_b.insights.riesgos_debilidades:
            st.warning(f"! {r}")

    st.markdown("---")

    # Conclusión
    st.markdown("### 🎯 Conclusión Estratégica")

    # Score promedio
    avg_a = (
        report_a.scores.stockiness +
        report_a.scores.carga_cognitiva +
        report_a.scores.hard_sell +
        report_a.scores.autenticidad_percibida +
        report_a.scores.innovacion_visual
    ) / 5

    avg_b = (
        report_b.scores.stockiness +
        report_b.scores.carga_cognitiva +
        report_b.scores.hard_sell +
        report_b.scores.autenticidad_percibida +
        report_b.scores.innovacion_visual
    ) / 5

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Campaña A - Score Promedio", f"{avg_a:.2f}/10")

    with col2:
        diff = avg_b - avg_a
        st.metric("Campaña B - Score Promedio", f"{avg_b:.2f}/10", delta=f"{diff:+.2f}")

    if avg_a > avg_b:
        st.info(f"📊 La **Campaña A** tiene un score promedio superior en {avg_a - avg_b:.2f} puntos")
    elif avg_b > avg_a:
        st.info(f"📊 La **Campaña B** tiene un score promedio superior en {avg_b - avg_a:.2f} puntos")
    else:
        st.info("📊 Ambas campañas tienen scores promedio idénticos")
