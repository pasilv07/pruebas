# 🎓 Visual Audit App

**Auditoría Visual Competitiva para Campañas Educativas**

Herramienta de análisis de inteligencia competitiva que transforma material visual de campañas de captación educativa en datos estructurados y insights accionables usando IA (Claude de Anthropic).

---

## 🎯 ¿Qué hace?

Analiza imágenes de campañas educativas (universidades, institutos, plataformas online) y extrae:

- **Decodificación técnica**: Autenticidad visual, carga cognitiva, sistema cromático
- **Inventario de contenido**: Protagonistas, escenografía, props y símbolos
- **Análisis de texto**: Jerarquía verbal, tono lingüístico, propuesta de valor
- **Estrategia inferida**: Promesas centrales, arquetipos de marca, posicionamiento
- **Análisis contextual**: Adaptación local, benchmark competitivo

### 📊 Outputs

- Scores cuantitativos (0-10) en 5 dimensiones
- Insights competitivos (fortalezas, oportunidades, riesgos)
- Recomendaciones tácticas accionables
- Reportes en JSON, Markdown, Excel y CSV

---

## 🚀 Instalación Rápida

### 1. Requisitos previos

- Python 3.8 o superior
- API Key de Anthropic (Claude)

### 2. Clonar o descargar el repositorio

```bash
git clone <tu-repo>
cd visual-audit-app
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar API Key

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env y añadir tu API key
# ANTHROPIC_API_KEY=sk-ant-api03-...
```

**Obtén tu API key en:** https://console.anthropic.com/

### 5. Configuración inicial

```bash
python main.py setup
```

---

## 📖 Uso

### Comando 1: Analizar una imagen individual

```bash
python main.py analyze ruta/a/imagen.jpg
```

**Opciones:**
- `-o, --output DIR`: Directorio de salida (default: `output`)
- `-f, --format`: Formato de reporte (`json`, `markdown`, `both`)
- `-m, --model`: Modelo de Claude (default: `claude-3-5-sonnet-20241022`)

**Ejemplo:**
```bash
python main.py analyze examples/campaña_universidad_x.jpg -f both
```

---

### Comando 2: Analizar múltiples imágenes (Batch)

```bash
python main.py batch directorio/con/imagenes/
```

**Opciones:**
- `-o, --output DIR`: Directorio de salida
- `--recursive/--no-recursive`: Buscar en subdirectorios (default: sí)
- `--parallel/--no-parallel`: Procesamiento paralelo (default: sí)
- `-w, --workers N`: Número de workers paralelos (default: 3)
- `-m, --model`: Modelo de Claude

**Ejemplo:**
```bash
# Analizar todas las imágenes en examples/ y subdirectorios
python main.py batch examples/ -w 5 -o resultados

# Analizar solo el directorio actual, sin recursión
python main.py batch campaña_octubre/ --no-recursive
```

⚠️ **Nota sobre paralelismo:**
- Usar 3-5 workers es recomendado para balancear velocidad y rate limits
- Si experimentas errores de rate limit, reduce workers o usa `--no-parallel`

---

### Comando 3: Información de la app

```bash
python main.py info
```

---

## 📁 Estructura del Proyecto

```
visual-audit-app/
├── visual_audit/              # Paquete principal
│   ├── __init__.py
│   ├── analyzer.py            # Analizador con Claude API
│   ├── batch_processor.py     # Procesamiento por lotes
│   ├── models.py              # Modelos de datos (Pydantic)
│   ├── prompts.py             # Sistema de prompts
│   └── reporter.py            # Generador de reportes
├── examples/                  # Coloca aquí tus imágenes de prueba
├── output/                    # Reportes generados (creado automáticamente)
├── main.py                    # CLI principal
├── requirements.txt           # Dependencias
├── .env.example              # Plantilla de configuración
├── .gitignore
└── README.md
```

---

## 📄 Formatos de Reporte

### 1. JSON Individual
Reporte completo estructurado con todas las fases de análisis.

**Ubicación:** `output/<id_reporte>.json`

**Contenido:**
```json
{
  "id_reporte": "audit_20250123_143022_campana_x",
  "institucion": "Universidad X",
  "programa": "Ingeniería en Sistemas",
  "scores": {
    "stockiness": 7,
    "carga_cognitiva": 5,
    "hard_sell": 8,
    "autenticidad_percibida": 4,
    "innovacion_visual": 6
  },
  "fase1_decodificacion": {...},
  "insights": {...},
  ...
}
```

### 2. Markdown Individual
Reporte legible en formato Markdown con todas las secciones.

**Ubicación:** `output/<id_reporte>.md`

### 3. Excel Comparativo (Batch)
Archivo Excel con múltiples hojas:
- **Comparativa**: Tabla con todos los reportes lado a lado
- **Scores**: Scores detallados + promedios
- **Insights**: Fortalezas, oportunidades, riesgos

**Ubicación:** `output/batch_audit_<timestamp>_comparativa.xlsx`

### 4. CSV Comparativo (Batch)
Tabla comparativa en formato CSV.

**Ubicación:** `output/batch_audit_<timestamp>_comparativa.csv`

### 5. JSON Batch
Archivo JSON con todos los reportes + metadata del batch.

**Ubicación:** `output/batch_audit_<timestamp>_batch.json`

---

## 🔍 Framework de Análisis

### Fase 1: Decodificación Técnica
- **Autenticidad Visual (Stockiness 0-10)**
  - Iluminación, expresiones, props, diversidad
- **Carga Cognitiva (Complejidad 0-10)**
  - Jerarquía visual, puntos de atención, CTA
- **Sistema Cromático**
  - Paletas dominantes, temperatura emocional, colores

### Fase 2: Inventario de Contenido
- **Protagonistas y Roles**
  - Tipo de sujeto, dirección de mirada, lenguaje corporal
- **Escenografía**
  - Tipo de instalación, señales de estatus
- **Props y Símbolos**
  - Objetos visibles, badges, sellos de calidad

### Fase 3: Análisis de Texto
- **Jerarquía Verbal**
  - Headlines, subheadlines, CTAs
- **Tono Lingüístico**
  - Registro comunicativo, frames semánticos
- **Propuesta de Valor**
  - Precio, modalidad, urgencia

### Fase 4: Estrategia Inferida
- **Promesas Centrales**
  - Transformación, empleabilidad, prestigio, etc.
- **Arquetipo de Marca**
  - El Sabio, El Héroe, El Cuidador, etc.
- **Posicionamiento Competitivo**
  - Cuadrante estratégico (Aspiracional/Accesible × Tradicional/Innovador)
- **Hard-Sell Score (0-10)**

### Fase 5: Análisis Contextual
- **Localización Cultural**
  - Adaptación regional (Paraguay/Latam)
- **Benchmark Competitivo**
  - Similitud con competidores

---

## 💡 Ejemplos de Uso

### Caso 1: Analizar campaña de competidor

```bash
# Descargar imagen de campaña de LinkedIn/Facebook
# Guardarla como "competidor_a.jpg"

python main.py analyze competidor_a.jpg

# Revisar: output/audit_..._competidor_a.md
```

**Resultado:** Reporte detallado con insights sobre estrategia del competidor.

### Caso 2: Comparar múltiples campañas de la competencia

```bash
# Crear directorio con imágenes
mkdir competencia_octubre
# Añadir 10 imágenes de diferentes instituciones

python main.py batch competencia_octubre/ -w 5

# Revisar: output/batch_audit_..._comparativa.xlsx
```

**Resultado:** Excel con comparativa de 10 campañas, promedios de scores, insights.

### Caso 3: Auditar histórico de campañas propias

```bash
# Organizar por período
mkdir campañas_propias
mkdir campañas_propias/2023
mkdir campañas_propias/2024

# Añadir imágenes históricas

python main.py batch campañas_propias/ --recursive

# Comparar evolución temporal
```

---

## 🛠️ Uso Programático (Python)

También puedes usar la librería directamente en tu código:

```python
from visual_audit import VisualAuditAnalyzer, BatchProcessor
from visual_audit.reporter import ReportGenerator

# Analizar una imagen
analyzer = VisualAuditAnalyzer()
report = analyzer.analyze_image("imagen.jpg")

print(f"Stockiness: {report.scores.stockiness}/10")
print(f"Promesa: {report.promesa_resumen}")

# Batch processing
processor = BatchProcessor(max_workers=5)
batch_result = processor.process_directory("imagenes/")

# Generar reportes
reporter = ReportGenerator(output_dir="mis_reportes")
reporter.save_all_formats(batch_result)
```

---

## 📊 Métricas y Scores

### Stockiness (0-10)
**¿Qué mide?** Nivel de autenticidad vs artificialidad de la imagen.

- **0-3**: Auténtico (fotos reales, UGC-like)
- **4-6**: Híbrido (profesional pero natural)
- **7-10**: Stock puro (poses artificiales)

### Carga Cognitiva (0-10)
**¿Qué mide?** Complejidad visual y saturación informativa.

- **0-3**: Minimalista (fácil de procesar)
- **4-6**: Balanceado
- **7-10**: Saturado (muchos elementos)

### Hard-Sell (0-10)
**¿Qué mide?** Agresividad de la venta.

- **0-2**: Soft-sell (branding, lifestyle)
- **5**: Balanceado
- **8-10**: Hard-sell (precio, urgencia, descuentos)

### Autenticidad Percibida (0-10)
**¿Qué mide?** Credibilidad y confianza transmitida.

### Innovación Visual (0-10)
**¿Qué mide?** Originalidad y modernidad del diseño.

---

## 🎨 Arquetipos de Marca

La app identifica arquetipos de Jung aplicados a marketing educativo:

- **El Sabio**: Conocimiento, investigación, pensamiento crítico
- **El Héroe**: Superación, logros, transformación
- **El Cuidador**: Apoyo, guía, comunidad
- **El Creador**: Innovación, emprendimiento
- **El Gobernante**: Prestigio, tradición, élite
- **El Amigo**: Cercanía, diversión, experiencia

---

## ⚙️ Configuración Avanzada

### Variables de entorno (.env)

```bash
# API Key (requerida)
ANTHROPIC_API_KEY=sk-ant-api03-...

# Modelo (opcional)
CLAUDE_MODEL=claude-3-5-sonnet-20241022

# Max tokens (opcional)
MAX_TOKENS=4000
```

### Modelos disponibles

- `claude-3-5-sonnet-20241022` (recomendado, balance precio/calidad)
- `claude-3-opus-20240229` (más potente, más caro)
- `claude-3-haiku-20240307` (más rápido, más económico)

---

## 🐛 Troubleshooting

### Error: "ANTHROPIC_API_KEY no configurada"
**Solución:**
1. Crea archivo `.env` desde `.env.example`
2. Añade tu API key de Anthropic

### Error: "Rate limit exceeded"
**Solución:**
- Reduce workers: `python main.py batch dir/ -w 2`
- O usa modo secuencial: `python main.py batch dir/ --no-parallel`

### Error: "Image too large"
**Solución:**
- Claude acepta imágenes hasta ~10MB
- Redimensiona imágenes muy grandes antes de procesar

### Error de parsing JSON
**Solución:**
- Verifica que la imagen sea legible (no corrupta)
- Prueba con otra imagen primero
- Revisa logs en consola

---

## 📈 Roadmap

- [ ] Soporte para videos (extraer frames clave)
- [ ] Análisis de carruseles (múltiples imágenes de una campaña)
- [ ] Dashboard web interactivo
- [ ] Integración con redes sociales (scraping automatizado)
- [ ] Modo "compare": comparar dos campañas lado a lado
- [ ] Exportar a PowerPoint con visualizaciones

---

## 🤝 Contribuciones

¡Contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo licencia MIT.

---

## 👤 Autor

Creado para análisis de inteligencia competitiva en marketing educativo.

---

## 🙏 Créditos

- **Claude AI** (Anthropic) - Motor de análisis visual
- **Pydantic** - Validación de datos
- **Click** - CLI framework
- **Rich** - Output beautification
- **Pandas** - Data processing

---

## 📞 Soporte

- **Issues**: Reporta bugs o solicita features en GitHub Issues
- **Documentación**: Este README
- **Ejemplos**: Ver carpeta `examples/`

---

**Made with ❤️ for competitive intelligence in educational marketing**
