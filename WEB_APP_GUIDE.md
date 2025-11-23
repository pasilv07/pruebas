# 🌐 Guía de la Interfaz Web

Guía completa para usar Visual Audit App a través de la interfaz web.

---

## 🚀 Inicio Rápido

### 1. Iniciar la aplicación

```bash
# Opción 1: Script automático
./run_webapp.sh

# Opción 2: Manual
streamlit run app.py
```

### 2. Abrir en navegador

La aplicación se abrirá automáticamente en:
```
http://localhost:8501
```

Si no se abre automáticamente, copia y pega la URL en tu navegador.

---

## 📱 Navegación

### Menú Principal (Sidebar)

```
🏠 Inicio          → Introducción y guías
📸 Análisis Individual → Analizar una sola imagen
📊 Análisis por Lotes  → Procesar múltiples imágenes
🔍 Comparación         → Comparar 2 reportes
```

### Indicador de Estado

En el sidebar verás:
- ✅ **API Key configurada** → Listo para usar
- ❌ **API Key no encontrada** → Debes configurar .env

---

## 🏠 Página de Inicio

### Contenido

- **Hero Section**: Descripción de la app y características
- **Framework de 5 Fases**: Tabs interactivos explicando cada fase
- **Scores Cuantitativos**: Explicación de métricas 0-10
- **Botones de acción**: Enlaces rápidos a otras páginas

### Ideal para:

- ✅ Nuevos usuarios que quieren entender el framework
- ✅ Referencia rápida de metodología
- ✅ Comprender qué mide cada score

---

## 📸 Análisis Individual

### Paso 1: Subir Imagen

1. Haz clic en **"Drag and drop file here"**
2. O arrastra la imagen directamente
3. Formatos soportados: JPG, PNG, WEBP, GIF

### Paso 2: Revisar Preview

- Se mostrará la imagen original
- Información del archivo (nombre, tamaño, tipo)

### Paso 3: Analizar

1. Click en **"🚀 Analizar Imagen"**
2. Espera 30-60 segundos (se muestra spinner)
3. ✅ Verás "Análisis completado exitosamente!"

### Paso 4: Explorar Resultados

**5 Tabs principales:**

#### 📈 Resumen Ejecutivo
- **Identificación**: Institución, programa, convocatoria
- **Scores Cuantitativos**: 5 métricas principales
- **Gráfico de Radar**: Perfil visual
- **Resumen Estratégico**: Promesa, arquetipo, público objetivo
- **Palabras Clave**: Tags extraídos

#### 🔍 Análisis Completo
5 sub-tabs con las fases completas:
- **Fase 1: Técnica** → Autenticidad, carga cognitiva, cromática
- **Fase 2: Contenido** → Protagonistas, escenografía, props
- **Fase 3: Texto** → Headlines, CTAs, tono, propuesta de valor
- **Fase 4: Estrategia** → Promesas, arquetipos, posicionamiento
- **Fase 5: Contexto** → Localización, benchmark

#### 💡 Insights
- **Fortalezas**: Qué hace bien la campaña
- **Oportunidades**: Qué podría mejorar
- **Riesgos**: Debilidades detectadas

#### 🚀 Recomendaciones
- **Acciones de contraste**: Si compites contra esta campaña
- **Elementos a evitar**: Qué no replicar
- **Nichos desatendidos**: Oportunidades no capturadas

#### 📄 Exportar
- **Descargar JSON**: Datos estructurados
- **Descargar Markdown**: Reporte legible
- Previews expandibles del contenido

### Tips de Uso

✅ **Para análisis rápido**: Ve directo al tab "Resumen Ejecutivo"
✅ **Para análisis profundo**: Explora "Análisis Completo" fase por fase
✅ **Para decisiones**: Revisa "Insights" y "Recomendaciones"
✅ **Para compartir**: Usa "Exportar" y descarga Markdown

---

## 📊 Análisis por Lotes

### Paso 1: Subir Múltiples Imágenes

1. Click en **"Browse files"**
2. Selecciona múltiples imágenes (Ctrl/Cmd + Click)
3. O arrastra varias imágenes a la vez
4. Verás contador: "✅ 10 imagen(es) cargada(s)"

### Paso 2: Ver Previews

- Expande **"👀 Ver previews"**
- Se muestran hasta 8 thumbnails
- Si hay más, verás "... y X imágenes más"

### Paso 3: Configurar Procesamiento

**⚙️ Configuración:**

- **Procesamiento Paralelo**: ✅ Activado (recomendado)
  - Procesa varias imágenes simultáneamente
  - Más rápido pero consume más recursos

- **Workers Paralelos**: 3 (ajustable 1-10)
  - Número de imágenes procesadas al mismo tiempo
  - Recomendado: 3-5 workers
  - Si hay errores de rate limit, reduce a 1-2

- **Tiempo estimado**: Cálculo automático
  - Basado en cantidad de imágenes y workers
  - ~45s por imagen promedio

### Paso 4: Procesar

1. Click en **"🚀 Procesar Lote"**
2. Se muestra:
   - Progress bar
   - Status text ("Analizando con Claude AI...")
3. Al finalizar: "✅ Completado en Xs"

### Paso 5: Explorar Resultados

**4 Tabs de resultados:**

#### 📈 Estadísticas

- **Métricas generales**:
  - Total imágenes, exitosas, fallidas, tiempo
  - Promedio por imagen

- **Scores Promedio**:
  - 5 métricas promediadas de todas las campañas
  - Útil para ver tendencias generales

- **Distribución de Arquetipos**:
  - Gráfico circular interactivo
  - Muestra qué arquetipos dominan en el lote

#### 📋 Tabla Comparativa

- **DataFrame interactivo**:
  - Todas las campañas en filas
  - Scores y datos clave en columnas
  - Ordenable y filtrable

- **Top Performers**:
  - **Más Auténtica**: Menor Stockiness
  - **Más Innovadora**: Mayor Innovación
  - **Más Hard-Sell**: Mayor Hard-Sell

#### 📊 Visualizaciones

- **Gráfico de barras agrupadas**:
  - Compara todas las métricas de todas las campañas
  - Colores diferentes por métrica
  - Interactivo (hover para detalles)

- **Scatter Plot: Autenticidad vs Innovación**:
  - Cada punto = una campaña
  - Color = nivel de Hard-Sell
  - Hover para ver nombre
  - Ideal para detectar outliers y patrones

#### 📄 Exportar

- **Excel Comparativo**:
  - 3 hojas: Comparativa, Scores, Insights
  - Listo para presentaciones

- **CSV Comparativo**:
  - Para análisis en Excel/Python/R

- **JSON Completo**:
  - Todos los datos estructurados
  - Para procesamiento programático

### Escenarios de Uso

**Scenario 1: Auditoría competitiva (5-10 campañas)**
```
1. Recolecta imágenes de competidores principales
2. Nómbralas descriptivamente (universidad_x_ingenieria.jpg)
3. Sube todas juntas
4. Usa 3-5 workers
5. Descarga Excel para presentar a stakeholders
```

**Scenario 2: Análisis histórico (30+ campañas)**
```
1. Organiza campañas por período/tipo
2. Procesamiento paralelo activado, 3 workers (seguro)
3. Revisa primero Estadísticas generales
4. Luego Visualizaciones para detectar tendencias
5. Descarga CSV para análisis estadístico adicional
```

**Scenario 3: A/B Testing (2-5 variantes)**
```
1. Sube las variantes de tu campaña
2. Procesa con 2-3 workers
3. Ve directo a Tabla Comparativa
4. Identifica cuál tiene mejor balance de scores
5. Revisa Insights para decisión final
```

---

## 🔍 Comparación

### Paso 1: Verificar Reportes Disponibles

- La app busca automáticamente en `output/`
- Solo muestra reportes individuales (excluye batch files)
- Si no hay reportes: "📭 No hay reportes..."

### Paso 2: Seleccionar Campañas

**Dos selectboxes:**
- **Campaña A**: Primer reporte
- **Campaña B**: Segundo reporte

**Nota:** Deben ser diferentes. Si seleccionas el mismo, verás advertencia.

### Paso 3: Explorar Comparación

**5 Tabs comparativos:**

#### 📈 Scores

- **Tabla de 3 columnas**:
  - Métrica | Campaña A | Campaña B
  - Cada score con delta calculado (diferencia)

- **Gráfico de radar superpuesto**:
  - Ambas campañas en el mismo gráfico
  - Colores diferentes para cada una
  - Fácil ver fortalezas/debilidades relativas

#### 🎯 Estrategia

**Lado a lado:**
- Arquetipo principal
- Promesas centrales
- Posicionamiento competitivo
- Hard-Sell score

**Análisis de diferencias automático:**
- ✅ Si usan mismo arquetipo
- ⚠️ Si son diferentes
- Promesas compartidas vs exclusivas

#### 💬 Mensajes

**Comparación textual:**
- **Headlines**: Transcripción exacta + longitud
- **CTAs**: Texto + nivel de urgencia
- **Tono**: Registro + frames semánticos
- **Propuesta de valor**: Tabla comparativa (precio, modalidad, etc.)

#### 🎨 Visual

**Elementos visuales:**
- **Sistema cromático**:
  - Temperatura emocional
  - Colores dominantes
  - Gráficos circulares de paletas (lado a lado)

- **Protagonistas**:
  - Tipo de sujeto
  - Dirección de mirada

- **Escenografía**:
  - Tipo de instalación
  - Descripción resumida

#### 💡 Insights

**Insights comparativos:**
- **Fortalezas** (lado a lado)
- **Oportunidades** (lado a lado)
- **Riesgos** (lado a lado)

**Conclusión estratégica:**
- Score promedio de cada campaña
- Diferencia calculada
- Recomendación automática

### Casos de Uso

**Caso 1: Benchmarking competitivo**
```
Objetivo: Comparar nuestra campaña vs competidor líder
1. Selecciona ambas campañas
2. Ve directo a tab "Scores" → radar superpuesto
3. Identifica en qué métricas te supera
4. Revisa "Estrategia" para entender su posicionamiento
5. Usa "Insights" para tu plan de acción
```

**Caso 2: A/B Testing interno**
```
Objetivo: Decidir entre 2 variantes de diseño
1. Compara ambas versiones
2. Revisa scores para balance general
3. Analiza "Mensajes" para consistencia
4. Verifica "Visual" para coherencia cromática
5. Decide basado en objetivos estratégicos
```

**Caso 3: Evolución temporal**
```
Objetivo: Ver cómo ha cambiado nuestra estrategia
1. Compara campaña actual vs hace 1 año
2. "Estrategia" → ¿Cambió el arquetipo?
3. "Scores" → ¿Más auténticos o más hard-sell?
4. "Insights" → ¿Nuevas oportunidades detectadas?
```

---

## 💡 Tips Generales de Uso

### Performance

- **Análisis individual**: ~30-60s por imagen
- **Batch pequeño (5 imgs, 3 workers)**: ~2-3 minutos
- **Batch grande (20 imgs, 5 workers)**: ~8-10 minutos

### Mejores Prácticas

✅ **Nombra archivos descriptivamente**
- `universidad_x_ingenieria_2024.jpg`
- `competidor_a_facebook_ad.jpg`

✅ **Usa imágenes de alta calidad**
- Mejor análisis de texto
- Colores más precisos

✅ **Organiza tus campañas**
- Por período: 2023/, 2024/
- Por competidor: competidor_a/, competidor_b/
- Por canal: facebook/, instagram/, web/

✅ **Guarda reportes importantes**
- JSON para procesamiento posterior
- Markdown para compartir con equipo
- Excel para presentaciones

✅ **Documenta tus hallazgos**
- Toma screenshots de gráficos clave
- Exporta comparativas en PDF
- Anota insights en notas aparte

### Troubleshooting

**"API Key no configurada"**
- Verifica que `.env` existe
- Que contiene `ANTHROPIC_API_KEY=sk-ant-...`
- Reinicia la web app

**"Rate limit exceeded"**
- Reduce workers a 1-2
- Espera 1 minuto y reintenta
- Considera batch más pequeño

**"Imagen inválida"**
- Verifica que la imagen se puede abrir
- Reconvierte a JPG si es necesario
- Verifica que no está corrupta

**"No hay reportes para comparar"**
- Genera reportes primero usando Análisis Individual/Lotes
- Verifica que están en `output/`
- Deben ser archivos JSON individuales (no batch)

**Página en blanco / Error de carga**
- Recarga la página (F5)
- Verifica la consola del navegador (F12)
- Revisa terminal donde corre streamlit
- Reinstala dependencias: `pip install -r requirements.txt`

---

## 🎨 Atajos y Funcionalidades Ocultas

### Atajos de Teclado (Streamlit)

- **R**: Reload app (útil durante desarrollo)
- **C**: Clear cache
- **Ctrl+Enter**: Re-ejecutar app completa

### Funcionalidades

**Expandir/Colapsar**
- Todos los `st.expander()` son colapsables
- Click para expandir secciones adicionales

**Copiar contenido**
- Todos los `st.code()` tienen botón de copiar
- Útil para headlines, CTAs, etc.

**Descargar gráficos**
- Hover sobre gráficos Plotly
- Aparece menú con opciones de export
- Descarga como PNG para presentaciones

**Ordenar tablas**
- Click en headers de columnas
- Ordena ascendente/descendente
- Filtra por valores

---

## 📚 Recursos Adicionales

- **README.md**: Documentación completa
- **QUICKSTART.md**: Guía de inicio en 5 minutos
- **examples/README.md**: Guía de preparación de imágenes
- **example_usage.py**: Uso programático (Python)

---

**¿Preguntas?** Revisa la documentación o crea un issue en GitHub.

**Happy analyzing! 🎓📊**
