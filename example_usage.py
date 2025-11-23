"""
Ejemplo de uso programático de Visual Audit App
"""
from visual_audit import VisualAuditAnalyzer, BatchProcessor
from visual_audit.reporter import ReportGenerator


def ejemplo_analisis_individual():
    """Ejemplo: Analizar una sola imagen"""
    print("="*60)
    print("EJEMPLO 1: Análisis Individual")
    print("="*60)

    # Crear analizador
    analyzer = VisualAuditAnalyzer()

    # Analizar imagen
    report = analyzer.analyze_image("examples/campaña.jpg", verbose=True)

    # Acceder a datos
    print(f"\n📊 Scores:")
    print(f"   Stockiness: {report.scores.stockiness}/10")
    print(f"   Hard-Sell: {report.scores.hard_sell}/10")
    print(f"   Innovación: {report.scores.innovacion_visual}/10")

    print(f"\n🎯 Estrategia:")
    print(f"   Promesa: {report.promesa_resumen}")
    print(f"   Arquetipo: {report.fase4_estrategia.arquetipo_principal}")
    print(f"   Público: {report.publico_objetivo}")

    print(f"\n💡 Insights:")
    for fortaleza in report.insights.fortalezas:
        print(f"   ✅ {fortaleza}")

    # Guardar reporte
    reporter = ReportGenerator(output_dir="output")
    json_path = reporter.save_json(report)
    md_path = reporter.save_markdown(report)

    print(f"\n💾 Reportes guardados:")
    print(f"   {json_path}")
    print(f"   {md_path}")


def ejemplo_batch():
    """Ejemplo: Procesar múltiples imágenes"""
    print("\n" + "="*60)
    print("EJEMPLO 2: Procesamiento por Lotes")
    print("="*60)

    # Crear procesador
    processor = BatchProcessor(max_workers=3, verbose=True)

    # Procesar directorio
    result = processor.process_directory(
        directory="examples/",
        recursive=True,
        parallel=True
    )

    print(f"\n📊 Resultados:")
    print(f"   Total: {result.total_imagenes}")
    print(f"   Exitosas: {result.exitosas}")
    print(f"   Tiempo: {result.tiempo_procesamiento:.2f}s")

    # Análisis comparativo
    if result.reportes:
        print(f"\n📈 Análisis Comparativo:")

        # Promedio de scores
        avg_stockiness = sum(r.scores.stockiness for r in result.reportes) / len(result.reportes)
        avg_hard_sell = sum(r.scores.hard_sell for r in result.reportes) / len(result.reportes)

        print(f"   Stockiness promedio: {avg_stockiness:.1f}/10")
        print(f"   Hard-Sell promedio: {avg_hard_sell:.1f}/10")

        # Arquetipos más comunes
        arquetipos = [r.fase4_estrategia.arquetipo_principal for r in result.reportes]
        print(f"\n   Arquetipos detectados:")
        for arq in set(arquetipos):
            count = arquetipos.count(arq)
            print(f"      {arq}: {count}")

    # Generar reportes
    reporter = ReportGenerator(output_dir="output")
    paths = reporter.save_all_formats(result, prefix="ejemplo_batch")

    print(f"\n💾 Reportes generados:")
    for format_name, path in paths.items():
        print(f"   {format_name}: {path}")


def ejemplo_comparacion_custom():
    """Ejemplo: Comparación personalizada"""
    print("\n" + "="*60)
    print("EJEMPLO 3: Comparación Personalizada")
    print("="*60)

    # Analizar dos campañas específicas
    analyzer = VisualAuditAnalyzer()

    campañas = [
        "examples/campaña_universidad_a.jpg",
        "examples/campaña_universidad_b.jpg",
    ]

    reportes = []
    for img in campañas:
        try:
            report = analyzer.analyze_image(img, verbose=False)
            reportes.append(report)
        except Exception as e:
            print(f"Error con {img}: {e}")

    if len(reportes) >= 2:
        print(f"\n🔍 Comparación A vs B:")

        # Comparar scores
        print("\n📊 Scores:")
        print(f"{'Métrica':<20} {'A':<10} {'B':<10} {'Diferencia':<10}")
        print("-" * 50)

        metrics = [
            ("Stockiness", "stockiness"),
            ("Carga Cognitiva", "carga_cognitiva"),
            ("Hard-Sell", "hard_sell"),
            ("Autenticidad", "autenticidad_percibida"),
            ("Innovación", "innovacion_visual"),
        ]

        for label, attr in metrics:
            score_a = getattr(reportes[0].scores, attr)
            score_b = getattr(reportes[1].scores, attr)
            diff = score_b - score_a

            diff_str = f"+{diff}" if diff > 0 else str(diff)
            print(f"{label:<20} {score_a:<10} {score_b:<10} {diff_str:<10}")

        # Comparar estrategias
        print(f"\n🎯 Estrategias:")
        print(f"   A: {reportes[0].fase4_estrategia.arquetipo_principal}")
        print(f"   B: {reportes[1].fase4_estrategia.arquetipo_principal}")

        print(f"\n💬 Mensajes:")
        print(f"   A: {reportes[0].fase3_texto.jerarquia_verbal.headline_principal[:60]}...")
        print(f"   B: {reportes[1].fase3_texto.jerarquia_verbal.headline_principal[:60]}...")


def ejemplo_filtrado():
    """Ejemplo: Filtrar y buscar en reportes"""
    print("\n" + "="*60)
    print("EJEMPLO 4: Filtrado y Búsqueda")
    print("="*60)

    # Procesar lote
    processor = BatchProcessor(verbose=False)
    result = processor.process_directory("examples/", recursive=True)

    if not result.reportes:
        print("No hay reportes para filtrar")
        return

    # Filtro 1: Campañas con Hard-Sell alto
    print("\n🔥 Campañas con Hard-Sell alto (>7):")
    hard_sell_altas = [r for r in result.reportes if r.scores.hard_sell > 7]

    for report in hard_sell_altas:
        print(f"   - {report.imagen_nombre}: {report.scores.hard_sell}/10")
        print(f"     CTA: {report.fase3_texto.jerarquia_verbal.cta_texto}")

    # Filtro 2: Campañas auténticas
    print("\n✨ Campañas auténticas (Stockiness <4):")
    autenticas = [r for r in result.reportes if r.scores.stockiness < 4]

    for report in autenticas:
        print(f"   - {report.imagen_nombre}: {report.scores.stockiness}/10")

    # Filtro 3: Por arquetipo
    print("\n🎭 Campañas tipo 'El Héroe':")
    heroes = [
        r for r in result.reportes
        if "Héroe" in str(r.fase4_estrategia.arquetipo_principal)
    ]

    for report in heroes:
        print(f"   - {report.imagen_nombre}")
        print(f"     Promesa: {report.promesa_resumen[:60]}...")


if __name__ == "__main__":
    print("\n🎓 VISUAL AUDIT APP - Ejemplos de Uso Programático\n")

    # Descomentar los ejemplos que quieras ejecutar:

    # ejemplo_analisis_individual()
    # ejemplo_batch()
    # ejemplo_comparacion_custom()
    # ejemplo_filtrado()

    print("\n" + "="*60)
    print("💡 Descomentar funciones en el código para ejecutar ejemplos")
    print("="*60 + "\n")
