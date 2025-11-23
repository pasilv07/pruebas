"""
Generador de reportes en múltiples formatos
"""
import json
from pathlib import Path
from typing import List, Optional
from datetime import datetime

import pandas as pd

from .models import AuditReport, BatchAuditResult


class ReportGenerator:
    """Generador de reportes de auditoría visual"""

    def __init__(self, output_dir: str = "output"):
        """
        Inicializa el generador de reportes

        Args:
            output_dir: Directorio donde guardar los reportes
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)

    def save_json(
        self,
        report: AuditReport,
        filename: Optional[str] = None,
        indent: int = 2
    ) -> Path:
        """
        Guarda reporte individual en JSON

        Args:
            report: Reporte a guardar
            filename: Nombre del archivo (si None, usa id_reporte)
            indent: Indentación del JSON

        Returns:
            Path al archivo guardado
        """
        if filename is None:
            filename = f"{report.id_reporte}.json"

        output_path = self.output_dir / filename

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report.model_dump(mode="json"), f, indent=indent, ensure_ascii=False)

        return output_path

    def save_batch_json(
        self,
        batch_result: BatchAuditResult,
        filename: str = "batch_audit_results.json",
        indent: int = 2
    ) -> Path:
        """
        Guarda resultado de batch en JSON

        Args:
            batch_result: Resultado del batch
            filename: Nombre del archivo
            indent: Indentación del JSON

        Returns:
            Path al archivo guardado
        """
        output_path = self.output_dir / filename

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(batch_result.model_dump(mode="json"), f, indent=indent, ensure_ascii=False)

        return output_path

    def generate_markdown(self, report: AuditReport) -> str:
        """
        Genera reporte en formato Markdown

        Args:
            report: Reporte a convertir

        Returns:
            String con contenido Markdown
        """
        md = f"""# AUDITORÍA VISUAL COMPETITIVA

**ID Reporte:** {report.id_reporte}
**Fecha:** {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
**Imagen:** {report.imagen_nombre}

---

## 📋 IDENTIFICACIÓN

- **Institución:** {report.institucion or 'No identificable'}
- **Programa:** {report.programa or 'No especificado'}
- **Convocatoria:** {report.convocatoria or 'No especificada'}

---

## 📊 SCORES CUANTITATIVOS

| Métrica | Score |
|---------|-------|
| **Stockiness** | {report.scores.stockiness}/10 |
| **Carga Cognitiva** | {report.scores.carga_cognitiva}/10 |
| **Hard-Sell** | {report.scores.hard_sell}/10 |
| **Autenticidad Percibida** | {report.scores.autenticidad_percibida}/10 |
| **Innovación Visual** | {report.scores.innovacion_visual}/10 |

---

## 🎯 RESUMEN EJECUTIVO

### Promesa Central
{report.promesa_resumen}

### Público Objetivo
{report.publico_objetivo}

### Palabras Clave
{', '.join(report.palabras_clave)}

---

## 🔍 FASE 1: DECODIFICACIÓN TÉCNICA

### Autenticidad Visual (Stockiness: {report.fase1_decodificacion.autenticidad.stockiness_score}/10)
- **Iluminación de estudio:** {'Sí' if report.fase1_decodificacion.autenticidad.tiene_iluminacion_estudio else 'No'}
- **Sonrisa genuina:** {'Sí' if report.fase1_decodificacion.autenticidad.sonrisa_genuina else 'No'}
- **Props reales:** {'Sí' if report.fase1_decodificacion.autenticidad.props_reales else 'No'}
- **Diversidad representativa:** {'Sí' if report.fase1_decodificacion.autenticidad.diversidad_representativa else 'No'}

**Notas:** {report.fase1_decodificacion.autenticidad.notas}

### Carga Cognitiva (Score: {report.fase1_decodificacion.carga_cognitiva.complejidad_score}/10)
- **Atención primero:** {report.fase1_decodificacion.carga_cognitiva.atencion_primero}
- **Atención después:** {report.fase1_decodificacion.carga_cognitiva.atencion_segundo}
- **Ubicación CTA:** {report.fase1_decodificacion.carga_cognitiva.ubicacion_cta}

### Sistema Cromático
- **Temperatura emocional:** {report.fase1_decodificacion.sistema_cromatico.temperatura_emocional}
- **Colores dominantes:** {', '.join(report.fase1_decodificacion.sistema_cromatico.colores_dominantes)}

**Distribución de paletas:**
- Institucional: {report.fase1_decodificacion.sistema_cromatico.paleta_institucional}%
- Tecnológica: {report.fase1_decodificacion.sistema_cromatico.paleta_tecnologica}%
- Vibrante: {report.fase1_decodificacion.sistema_cromatico.paleta_vibrante}%
- Minimalista: {report.fase1_decodificacion.sistema_cromatico.paleta_minimalista}%

---

## 👥 FASE 2: INVENTARIO DE CONTENIDO

### Protagonistas
- **Tipo:** {report.fase2_inventario.protagonistas.tipo_sujeto}
- **Dirección de mirada:** {report.fase2_inventario.protagonistas.direccion_mirada}
- **Lenguaje corporal:** {', '.join(report.fase2_inventario.protagonistas.lenguaje_corporal)}

{report.fase2_inventario.protagonistas.descripcion_detallada}

### Escenografía
- **Tipo:** {report.fase2_inventario.escenografia.tipo_instalacion}
- **Materiales nobles:** {'Sí' if report.fase2_inventario.escenografia.materiales_nobles else 'No'}
- **Tecnología visible:** {'Sí' if report.fase2_inventario.escenografia.tecnologia_visible else 'No'}

{report.fase2_inventario.escenografia.descripcion}

### Props y Símbolos
- **Libros físicos:** {'Sí' if report.fase2_inventario.props_simbolos.libros_fisicos else 'No'}
- **Laptops/Tablets:** {'Sí' if report.fase2_inventario.props_simbolos.laptops_tablets else 'No'}
- **Badges/Sellos:** {', '.join(report.fase2_inventario.props_simbolos.badges_sellos) if report.fase2_inventario.props_simbolos.badges_sellos else 'Ninguno'}

---

## 💬 FASE 3: ANÁLISIS DE TEXTO

### Jerarquía Verbal
**Headline principal:** "{report.fase3_texto.jerarquia_verbal.headline_principal}"
**CTA:** "{report.fase3_texto.jerarquia_verbal.cta_texto}"
**Urgencia:** {report.fase3_texto.jerarquia_verbal.cta_urgencia}

### Tono Lingüístico
- **Registro:** {report.fase3_texto.tono_linguistico.registro}
- **Frames semánticos:** {', '.join(report.fase3_texto.tono_linguistico.frame_semantico)}

### Propuesta de Valor
- **Precio:** {report.fase3_texto.propuesta_valor.precio_visible or 'No visible'}
- **Modalidad:** {report.fase3_texto.propuesta_valor.modalidad or 'No especificada'}

---

## 🎲 FASE 4: ESTRATEGIA INFERIDA

### Promesas Centrales
{chr(10).join(f'- {p}' for p in report.fase4_estrategia.promesas_centrales)}

### Arquetipo de Marca
- **Principal:** {report.fase4_estrategia.arquetipo_principal}
- **Secundario:** {report.fase4_estrategia.arquetipo_secundario or 'N/A'}

### Posicionamiento
{report.fase4_estrategia.posicionamiento_cuadrante}

**Hard-Sell Score:** {report.fase4_estrategia.hard_sell_score}/10

{report.fase4_estrategia.estrategia_descripcion}

---

## 🌎 FASE 5: ANÁLISIS CONTEXTUAL

- **Adaptación local:** {'Sí' if report.fase5_contextual.tiene_adaptacion_local else 'No'}
- **Modelos regionales:** {'Sí' if report.fase5_contextual.modelos_etnicos_regionales else 'No'}
- **Referencias Paraguay:** {'Sí' if report.fase5_contextual.referencias_paraguay else 'No'}

**Benchmark similar a:** {', '.join(report.fase5_contextual.benchmark_similar)}

{report.fase5_contextual.notas_culturales}

---

## 💡 INSIGHTS COMPETITIVOS

### ✅ Fortalezas
{chr(10).join(f'- {f}' for f in report.insights.fortalezas)}

### 🎯 Oportunidades de Diferenciación
{chr(10).join(f'- {o}' for o in report.insights.oportunidades_diferenciacion)}

### ⚠️ Riesgos/Debilidades
{chr(10).join(f'- {r}' for r in report.insights.riesgos_debilidades)}

---

## 🚀 RECOMENDACIONES TÁCTICAS

### Acciones de Contraste
{chr(10).join(f'{i+1}. {a}' for i, a in enumerate(report.recomendaciones.acciones_contraste))}

### Elementos a Evitar
{chr(10).join(f'{i+1}. {e}' for i, e in enumerate(report.recomendaciones.elementos_evitar))}

### Nichos Desatendidos
{chr(10).join(f'{i+1}. {n}' for i, n in enumerate(report.recomendaciones.nichos_desatendidos))}

---

*Generado por Visual Audit App*
"""
        return md

    def save_markdown(
        self,
        report: AuditReport,
        filename: Optional[str] = None
    ) -> Path:
        """
        Guarda reporte en Markdown

        Args:
            report: Reporte a guardar
            filename: Nombre del archivo

        Returns:
            Path al archivo guardado
        """
        if filename is None:
            filename = f"{report.id_reporte}.md"

        output_path = self.output_dir / filename

        md_content = self.generate_markdown(report)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        return output_path

    def generate_comparison_table(self, reports: List[AuditReport]) -> pd.DataFrame:
        """
        Genera tabla comparativa de múltiples reportes

        Args:
            reports: Lista de reportes

        Returns:
            DataFrame con comparación
        """
        rows = []

        for report in reports:
            row = {
                "ID": report.id_reporte,
                "Imagen": report.imagen_nombre,
                "Institución": report.institucion or "N/A",
                "Programa": report.programa or "N/A",

                # Scores
                "Stockiness": report.scores.stockiness,
                "Carga Cognitiva": report.scores.carga_cognitiva,
                "Hard-Sell": report.scores.hard_sell,
                "Autenticidad": report.scores.autenticidad_percibida,
                "Innovación": report.scores.innovacion_visual,

                # Estrategia
                "Arquetipo": report.fase4_estrategia.arquetipo_principal,
                "Promesa Principal": report.fase4_estrategia.promesas_centrales[0] if report.fase4_estrategia.promesas_centrales else "N/A",

                # Texto
                "Headline": report.fase3_texto.jerarquia_verbal.headline_principal[:50] + "...",
                "CTA": report.fase3_texto.jerarquia_verbal.cta_texto[:30] + "...",

                # Color
                "Temperatura": report.fase1_decodificacion.sistema_cromatico.temperatura_emocional,

                # Público
                "Público Objetivo": report.publico_objetivo[:50] + "...",
            }
            rows.append(row)

        return pd.DataFrame(rows)

    def save_comparison_excel(
        self,
        reports: List[AuditReport],
        filename: str = "comparativa_campañas.xlsx"
    ) -> Path:
        """
        Guarda comparativa en Excel con múltiples hojas

        Args:
            reports: Lista de reportes
            filename: Nombre del archivo

        Returns:
            Path al archivo guardado
        """
        output_path = self.output_dir / filename

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Hoja 1: Comparativa general
            df_comparison = self.generate_comparison_table(reports)
            df_comparison.to_excel(writer, sheet_name='Comparativa', index=False)

            # Hoja 2: Scores detallados
            scores_data = []
            for report in reports:
                scores_data.append({
                    "Imagen": report.imagen_nombre,
                    "Institución": report.institucion or "N/A",
                    "Stockiness": report.scores.stockiness,
                    "Carga Cognitiva": report.scores.carga_cognitiva,
                    "Hard-Sell": report.scores.hard_sell,
                    "Autenticidad": report.scores.autenticidad_percibida,
                    "Innovación": report.scores.innovacion_visual,
                    "Promedio": (
                        report.scores.stockiness +
                        report.scores.carga_cognitiva +
                        report.scores.hard_sell +
                        report.scores.autenticidad_percibida +
                        report.scores.innovacion_visual
                    ) / 5
                })

            pd.DataFrame(scores_data).to_excel(writer, sheet_name='Scores', index=False)

            # Hoja 3: Insights
            insights_data = []
            for report in reports:
                insights_data.append({
                    "Imagen": report.imagen_nombre,
                    "Institución": report.institucion or "N/A",
                    "Fortalezas": " | ".join(report.insights.fortalezas),
                    "Oportunidades": " | ".join(report.insights.oportunidades_diferenciacion),
                    "Riesgos": " | ".join(report.insights.riesgos_debilidades),
                })

            pd.DataFrame(insights_data).to_excel(writer, sheet_name='Insights', index=False)

        return output_path

    def save_comparison_csv(
        self,
        reports: List[AuditReport],
        filename: str = "comparativa_campañas.csv"
    ) -> Path:
        """
        Guarda comparativa en CSV

        Args:
            reports: Lista de reportes
            filename: Nombre del archivo

        Returns:
            Path al archivo guardado
        """
        output_path = self.output_dir / filename

        df = self.generate_comparison_table(reports)
        df.to_csv(output_path, index=False, encoding='utf-8')

        return output_path

    def save_all_formats(
        self,
        batch_result: BatchAuditResult,
        prefix: str = "audit"
    ) -> Dict[str, Path]:
        """
        Guarda todos los reportes en todos los formatos disponibles

        Args:
            batch_result: Resultado del batch
            prefix: Prefijo para nombres de archivos

        Returns:
            Dict con paths de archivos generados
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        paths = {}

        # JSON batch completo
        paths["batch_json"] = self.save_batch_json(
            batch_result,
            filename=f"{prefix}_{timestamp}_batch.json"
        )

        # JSON individuales
        for report in batch_result.reportes:
            self.save_json(report)

        # Markdown individuales
        for report in batch_result.reportes:
            self.save_markdown(report)

        if batch_result.reportes:
            # Excel comparativo
            paths["excel"] = self.save_comparison_excel(
                batch_result.reportes,
                filename=f"{prefix}_{timestamp}_comparativa.xlsx"
            )

            # CSV comparativo
            paths["csv"] = self.save_comparison_csv(
                batch_result.reportes,
                filename=f"{prefix}_{timestamp}_comparativa.csv"
            )

        return paths
