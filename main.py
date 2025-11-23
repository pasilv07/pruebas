#!/usr/bin/env python3
"""
Visual Audit App - CLI Principal
Auditoría Visual Competitiva para Campañas Educativas
"""
import os
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from dotenv import load_dotenv

from visual_audit import VisualAuditAnalyzer, BatchProcessor
from visual_audit.reporter import ReportGenerator

# Cargar variables de entorno
load_dotenv()

console = Console()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    🎓 Visual Audit App - Auditoría Visual Competitiva

    Analiza campañas educativas usando IA para extraer insights estratégicos.
    """
    pass


@cli.command()
@click.argument('image_path', type=click.Path(exists=True))
@click.option('--output', '-o', default='output', help='Directorio de salida')
@click.option('--format', '-f',
              type=click.Choice(['json', 'markdown', 'both']),
              default='both',
              help='Formato de reporte')
@click.option('--model', '-m',
              default='claude-3-5-sonnet-20241022',
              help='Modelo de Claude a usar')
def analyze(image_path: str, output: str, format: str, model: str):
    """
    Analiza UNA imagen individual

    Ejemplo:
        python main.py analyze campaña.jpg
    """
    console.print("\n🎓 [bold cyan]Visual Audit App[/bold cyan]\n")

    # Verificar API key
    if not os.getenv('ANTHROPIC_API_KEY'):
        console.print("[bold red]❌ Error:[/bold red] ANTHROPIC_API_KEY no configurada")
        console.print("\n💡 Configura tu API key:")
        console.print("   1. Copia .env.example a .env")
        console.print("   2. Añade tu API key de Anthropic")
        console.print("   3. Obtén tu key en: https://console.anthropic.com/\n")
        sys.exit(1)

    try:
        # Crear analizador
        analyzer = VisualAuditAnalyzer(model=model)
        reporter = ReportGenerator(output_dir=output)

        # Analizar
        console.print(f"📸 Analizando: [cyan]{Path(image_path).name}[/cyan]")
        report = analyzer.analyze_image(image_path, verbose=True)

        # Guardar reportes
        console.print("\n💾 Guardando reportes...")

        if format in ['json', 'both']:
            json_path = reporter.save_json(report)
            console.print(f"   ✅ JSON: {json_path}")

        if format in ['markdown', 'both']:
            md_path = reporter.save_markdown(report)
            console.print(f"   ✅ Markdown: {md_path}")

        # Mostrar resumen
        console.print("\n" + "="*60)
        console.print("[bold green]✅ Análisis completado[/bold green]\n")

        table = Table(title="📊 Scores Cuantitativos")
        table.add_column("Métrica", style="cyan")
        table.add_column("Score", justify="center", style="magenta")

        table.add_row("Stockiness", f"{report.scores.stockiness}/10")
        table.add_row("Carga Cognitiva", f"{report.scores.carga_cognitiva}/10")
        table.add_row("Hard-Sell", f"{report.scores.hard_sell}/10")
        table.add_row("Autenticidad", f"{report.scores.autenticidad_percibida}/10")
        table.add_row("Innovación", f"{report.scores.innovacion_visual}/10")

        console.print(table)

        console.print(f"\n🎯 [bold]Promesa Central:[/bold] {report.promesa_resumen}")
        console.print(f"👥 [bold]Público Objetivo:[/bold] {report.publico_objetivo}")

        console.print("\n" + "="*60 + "\n")

    except Exception as e:
        console.print(f"\n[bold red]❌ Error:[/bold red] {e}\n")
        sys.exit(1)


@cli.command()
@click.argument('directory', type=click.Path(exists=True))
@click.option('--output', '-o', default='output', help='Directorio de salida')
@click.option('--recursive/--no-recursive', default=True, help='Buscar en subdirectorios')
@click.option('--parallel/--no-parallel', default=True, help='Procesamiento paralelo')
@click.option('--workers', '-w', default=3, help='Número de workers paralelos')
@click.option('--model', '-m',
              default='claude-3-5-sonnet-20241022',
              help='Modelo de Claude a usar')
def batch(directory: str, output: str, recursive: bool, parallel: bool, workers: int, model: str):
    """
    Analiza MÚLTIPLES imágenes en lote

    Ejemplo:
        python main.py batch ./campañas/ -o resultados
    """
    console.print("\n🎓 [bold cyan]Visual Audit App - Modo Lote[/bold cyan]\n")

    # Verificar API key
    if not os.getenv('ANTHROPIC_API_KEY'):
        console.print("[bold red]❌ Error:[/bold red] ANTHROPIC_API_KEY no configurada")
        console.print("\n💡 Configura tu API key:")
        console.print("   1. Copia .env.example a .env")
        console.print("   2. Añade tu API key de Anthropic\n")
        sys.exit(1)

    try:
        # Crear procesador
        analyzer = VisualAuditAnalyzer(model=model)
        processor = BatchProcessor(analyzer=analyzer, max_workers=workers)
        reporter = ReportGenerator(output_dir=output)

        # Procesar directorio
        result = processor.process_directory(
            directory=directory,
            recursive=recursive,
            parallel=parallel
        )

        if result.exitosas == 0:
            console.print("[yellow]⚠️  No se procesaron imágenes exitosamente[/yellow]\n")
            sys.exit(0)

        # Guardar reportes
        console.print("💾 Generando reportes comparativos...")
        paths = reporter.save_all_formats(result, prefix="batch_audit")

        console.print("\n[bold green]✅ Procesamiento completado[/bold green]\n")

        # Tabla de resultados
        table = Table(title="📊 Resultados del Lote")
        table.add_column("Métrica", style="cyan")
        table.add_column("Valor", style="magenta")

        table.add_row("Total de imágenes", str(result.total_imagenes))
        table.add_row("Exitosas", f"[green]{result.exitosas}[/green]")
        table.add_row("Fallidas", f"[red]{result.fallidas}[/red]")
        table.add_row("Tiempo total", f"{result.tiempo_procesamiento:.2f}s")
        table.add_row("Promedio por imagen", f"{result.tiempo_procesamiento/result.total_imagenes:.2f}s")

        console.print(table)

        # Archivos generados
        console.print("\n📁 [bold]Archivos generados:[/bold]")
        console.print(f"   📊 Excel: {paths.get('excel', 'N/A')}")
        console.print(f"   📄 CSV: {paths.get('csv', 'N/A')}")
        console.print(f"   🗂️  JSON batch: {paths.get('batch_json', 'N/A')}")
        console.print(f"   📝 Reportes individuales en: {output}/")

        # Estadísticas de scores
        if result.reportes:
            console.print("\n📊 [bold]Estadísticas de Scores:[/bold]")

            avg_stockiness = sum(r.scores.stockiness for r in result.reportes) / len(result.reportes)
            avg_hard_sell = sum(r.scores.hard_sell for r in result.reportes) / len(result.reportes)
            avg_innovacion = sum(r.scores.innovacion_visual for r in result.reportes) / len(result.reportes)

            console.print(f"   Stockiness promedio: {avg_stockiness:.1f}/10")
            console.print(f"   Hard-Sell promedio: {avg_hard_sell:.1f}/10")
            console.print(f"   Innovación promedio: {avg_innovacion:.1f}/10")

        console.print("\n" + "="*60 + "\n")

    except Exception as e:
        console.print(f"\n[bold red]❌ Error:[/bold red] {e}\n")
        sys.exit(1)


@cli.command()
def setup():
    """
    Configuración inicial de la aplicación
    """
    console.print("\n🎓 [bold cyan]Visual Audit App - Configuración[/bold cyan]\n")

    # Verificar si .env existe
    env_path = Path(".env")

    if env_path.exists():
        console.print("✅ Archivo .env encontrado")

        # Verificar si tiene API key
        load_dotenv()
        if os.getenv('ANTHROPIC_API_KEY'):
            console.print("✅ ANTHROPIC_API_KEY configurada")
            console.print("\n[green]Todo listo para usar la aplicación[/green]\n")
        else:
            console.print("[yellow]⚠️  ANTHROPIC_API_KEY no encontrada en .env[/yellow]")
            console.print("\n💡 Añade esta línea a tu .env:")
            console.print("   ANTHROPIC_API_KEY=tu_api_key_aqui\n")
    else:
        console.print("[yellow]⚠️  Archivo .env no encontrado[/yellow]")

        # Crear .env desde .env.example
        example_path = Path(".env.example")
        if example_path.exists():
            example_path.read_text()
            env_path.write_text(example_path.read_text())
            console.print("✅ .env creado desde .env.example")
            console.print("\n💡 Ahora edita .env y añade tu API key de Anthropic")
        else:
            console.print("[red]❌ .env.example no encontrado[/red]")

        console.print("\n📖 Para obtener tu API key:")
        console.print("   1. Ve a: https://console.anthropic.com/")
        console.print("   2. Crea una cuenta o inicia sesión")
        console.print("   3. Ve a API Keys y crea una nueva key")
        console.print("   4. Cópiala en el archivo .env\n")

    # Verificar directorios
    console.print("\n📁 Verificando directorios...")

    output_dir = Path("output")
    examples_dir = Path("examples")

    for dir_path in [output_dir, examples_dir]:
        if dir_path.exists():
            console.print(f"   ✅ {dir_path}/ existe")
        else:
            dir_path.mkdir(exist_ok=True)
            console.print(f"   ➕ {dir_path}/ creado")

    console.print("\n" + "="*60)
    console.print("[bold green]Configuración completada[/bold green]")
    console.print("\n📚 Próximos pasos:")
    console.print("   1. Coloca imágenes de campañas en examples/")
    console.print("   2. Ejecuta: python main.py analyze examples/imagen.jpg")
    console.print("   3. O modo lote: python main.py batch examples/")
    console.print("\n💡 Ayuda: python main.py --help")
    console.print("="*60 + "\n")


@cli.command()
def info():
    """
    Muestra información sobre la aplicación
    """
    console.print("\n🎓 [bold cyan]Visual Audit App v1.0.0[/bold cyan]\n")

    console.print("[bold]Descripción:[/bold]")
    console.print("Herramienta de análisis visual competitivo para campañas educativas.")
    console.print("Utiliza Claude AI (Anthropic) para auditorías exhaustivas.\n")

    console.print("[bold]Framework de Análisis:[/bold]")
    console.print("✓ Fase 1: Decodificación Técnica (autenticidad, carga cognitiva, cromática)")
    console.print("✓ Fase 2: Inventario de Contenido (protagonistas, escenografía, props)")
    console.print("✓ Fase 3: Análisis de Texto (jerarquía verbal, tono, propuesta valor)")
    console.print("✓ Fase 4: Estrategia Inferida (promesas, arquetipos, posicionamiento)")
    console.print("✓ Fase 5: Análisis Contextual (localización, benchmark)\n")

    console.print("[bold]Formatos de Salida:[/bold]")
    console.print("📄 JSON (individual y batch)")
    console.print("📝 Markdown (reportes detallados)")
    console.print("📊 Excel (comparativas con múltiples hojas)")
    console.print("📋 CSV (datos tabulares)\n")

    console.print("[bold]Comandos Disponibles:[/bold]")
    console.print("• setup    - Configuración inicial")
    console.print("• analyze  - Analizar una imagen")
    console.print("• batch    - Analizar múltiples imágenes")
    console.print("• info     - Esta información\n")

    console.print("[bold]Ejemplos:[/bold]")
    console.print("  python main.py setup")
    console.print("  python main.py analyze campaña.jpg")
    console.print("  python main.py batch ./imagenes/ -w 5\n")

    console.print("[bold]Más información:[/bold]")
    console.print("README.md para documentación completa\n")


if __name__ == '__main__':
    cli()
