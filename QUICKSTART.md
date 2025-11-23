# 🚀 Quick Start Guide

Guía rápida para empezar a usar Visual Audit App en menos de 5 minutos.

---

## 1️⃣ Instalación (2 minutos)

### Opción A: Instalación automatizada (Linux/Mac)
```bash
./install.sh
```

### Opción B: Instalación manual
```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
nano .env  # Añade tu API key

# Permisos
chmod +x main.py
```

## 2️⃣ Obtener API Key (1 minuto)

1. Ve a: https://console.anthropic.com/
2. Crea cuenta o inicia sesión
3. Ve a "API Keys"
4. Crea una nueva key
5. Cópiala en `.env`:

```bash
ANTHROPIC_API_KEY=sk-ant-api03-tu_key_aqui
```

## 3️⃣ Preparar imágenes (1 minuto)

Coloca imágenes de campañas educativas en `examples/`:

```bash
# Ejemplo: descargar imagen de campaña
# Guardarla como: examples/campaña_test.jpg
```

## 4️⃣ Primer análisis (1 minuto)

### Analizar una imagen:
```bash
python main.py analyze examples/campaña_test.jpg
```

**Salida:**
- `output/audit_..._campaña_test.json` (datos estructurados)
- `output/audit_..._campaña_test.md` (reporte legible)

### Ver resultados:
```bash
# Ver reporte Markdown
cat output/*.md

# O abrir en editor
code output/*.md  # VS Code
nano output/*.md  # Terminal
```

---

## 5️⃣ Análisis por lotes (opcional)

Si tienes múltiples imágenes:

```bash
# Colocar varias imágenes en examples/
# Luego ejecutar:
python main.py batch examples/
```

**Salida:**
- Excel comparativo: `output/batch_audit_..._comparativa.xlsx`
- CSV: `output/batch_audit_..._comparativa.csv`
- JSON batch: `output/batch_audit_...batch.json`
- Reportes individuales (JSON + Markdown)

---

## 📊 Entender los resultados

### Scores principales (0-10):

| Score | Qué mide |
|-------|----------|
| **Stockiness** | 0=Auténtico, 10=Stock artificial |
| **Carga Cognitiva** | 0=Simple, 10=Saturado |
| **Hard-Sell** | 0=Branding suave, 10=Venta agresiva |
| **Autenticidad** | Credibilidad percibida |
| **Innovación** | Originalidad del diseño |

### Secciones clave del reporte:

1. **Scores Cuantitativos**: Métricas 0-10
2. **Decodificación Técnica**: Autenticidad, colores, complejidad
3. **Inventario de Contenido**: Qué se muestra (personas, lugares, objetos)
4. **Análisis de Texto**: Headlines, CTAs, tono
5. **Estrategia Inferida**: Promesas, arquetipos, posicionamiento
6. **Insights Competitivos**: Fortalezas, oportunidades, riesgos
7. **Recomendaciones**: Acciones tácticas

---

## 🎯 Casos de uso rápidos

### Caso 1: Analizar competidor
```bash
# Descargar imagen de campaña de competidor
# Guardar como competidor_x.jpg

python main.py analyze competidor_x.jpg

# Revisar insights en output/*.md
```

### Caso 2: Comparar múltiples competidores
```bash
# Crear carpeta
mkdir competidores

# Añadir imágenes de 5-10 competidores
# competidores/universidad_a.jpg
# competidores/universidad_b.jpg
# etc.

python main.py batch competidores/ -w 5

# Abrir: output/batch_audit_*_comparativa.xlsx
```

### Caso 3: Analizar campaña propia
```bash
python main.py analyze mi_campaña.jpg

# Revisar:
# - Score de Hard-Sell (¿muy agresivo?)
# - Autenticidad (¿parece stock?)
# - Insights > Riesgos/Debilidades
```

---

## 💡 Tips para mejores resultados

### ✅ HACER:
- Usar imágenes de alta resolución
- Incluir campañas con texto visible
- Analizar múltiples versiones para comparar
- Organizar imágenes por categoría (competidor, período, etc.)

### ❌ EVITAR:
- Imágenes borrosas o comprimidas
- Archivos corruptos
- Imágenes sin texto (solo logos)
- Procesar 100+ imágenes en paralelo (rate limits)

---

## 🐛 Solución rápida de problemas

| Error | Solución |
|-------|----------|
| "API key no configurada" | Verifica `.env` tiene `ANTHROPIC_API_KEY=...` |
| "Rate limit exceeded" | Reduce workers: `-w 2` o usa `--no-parallel` |
| "No se encontraron imágenes" | Verifica extensiones: .jpg, .png, .webp, .gif |
| "Imagen inválida" | Verifica que la imagen se puede abrir |

---

## 📚 Siguientes pasos

1. **Leer README.md completo**: Detalles de todas las funcionalidades
2. **Ver example_usage.py**: Uso programático en Python
3. **Experimentar con options**: `python main.py batch --help`
4. **Explorar reportes Excel**: Comparativas multi-hoja

---

## ❓ Ayuda

```bash
# Ayuda general
python main.py --help

# Ayuda por comando
python main.py analyze --help
python main.py batch --help

# Información de la app
python main.py info

# Configuración inicial
python main.py setup
```

---

## 🎉 ¡Listo!

Ya puedes analizar campañas educativas y obtener insights competitivos en minutos.

**¿Preguntas?** Ver README.md o crear un issue en GitHub.

---

**Happy analyzing! 🎓📊**
