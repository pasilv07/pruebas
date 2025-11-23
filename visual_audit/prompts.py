"""
Sistema de prompts estructurados para análisis visual con Claude
"""

SYSTEM_PROMPT = """Eres un Analista Senior de Inteligencia Competitiva en Marketing Educativo con expertise en:
- Semiótica visual y diseño persuasivo
- Posicionamiento de marca en sector educativo
- Análisis de campañas de captación universitaria
- Contexto cultural de Paraguay y Latinoamérica

Tu tarea es analizar imágenes de campañas educativas de forma EXHAUSTIVA, ESPECÍFICA, CUANTITATIVA y ACCIONABLE."""


MAIN_ANALYSIS_PROMPT = """# AUDITORÍA VISUAL COMPETITIVA - CAMPAÑAS EDUCATIVAS

Analiza esta imagen de campaña educativa siguiendo ESTRICTAMENTE el framework de 5 fases.
Debes ser:
- **EXHAUSTIVO**: Analiza cada elemento visible
- **ESPECÍFICO**: Evita generalidades (ejemplo: "El amarillo ocupa 60% y crea contraste dramático" NO "es llamativa")
- **CUANTITATIVO**: Usa escalas 0-10 siempre que se indique
- **ACCIONABLE**: Cada insight debe traducirse en decisión de marketing

---

## FASE 1: DECODIFICACIÓN TÉCNICA (La Física de la Atención)

### 1.1 AUTENTICIDAD VISUAL - Escala de Stockiness (0-10)
- **0-3**: Documental auténtico (UGC-like, imperfecciones, momentos reales)
- **4-6**: Híbrido profesional (controlado pero natural)
- **7-10**: Stock puro (modelos profesionales, poses artificiales)

**Reporta:**
- Score de Stockiness: __/10
- ¿Iluminación de estudio vs natural?
- ¿Sonrisa Duchenne (genuina) o social (forzada)?
- ¿Props reales/usados o perfectos/nuevos?
- ¿Diversidad representativa o tokenista?
- Notas adicionales

### 1.2 CARGA COGNITIVA - Escala de Complejidad (0-10)
- **0-3**: Ultra minimalista (1 sujeto, fondo neutro, <3 elementos)
- **4-6**: Balance controlado
- **7-10**: Saturación informativa

**Mapa de prioridad visual:**
1. ¿Qué captura la atención PRIMERO?
2. ¿Hacia dónde guía la mirada DESPUÉS?
3. ¿Dónde está el CTA?
- Score: __/10

### 1.3 SISTEMA CROMÁTICO
**Paleta dominante (con % aproximado):**
- Institucional conservador (Azul marino/Rojo vino/Gris): ___%
- Tecnológico corporativo (Azul eléctrico/Verde/Blanco): ___%
- Vibrante/Juvenil (Amarillo/Cian/Magenta/Naranja): ___%
- Minimalista (Monocromático + acento): ___%

**Temperatura emocional:** Fría (Profesional/Seria) / Neutra / Cálida (Accesible/Optimista)
**Colores dominantes específicos:** [Lista con nombres específicos de colores]

---

## FASE 2: INVENTARIO DE CONTENIDO (Qué se Muestra)

### 2.1 PROTAGONISTAS Y ROLES
**Tipo de sujeto principal:** (Estudiante ideal 18-25 / Profesional 25-35 / Grupo diverso / Ninguno)

**Dirección de mirada:**
- A cámara (demanda directa)
- Al horizonte (aspiración)
- A objeto/pantalla (acción)
- Interacción social (pertenencia)

**Lenguaje corporal:** [Describe: postura, gestos, vestimenta, expresiones]

### 2.2 ESCENOGRAFÍA
**Tipo de instalación:**
- Tradicional-Prestigio (claustros, bibliotecas clásicas)
- Tecnológico-Innovación (labs, pantallas, VR/AR)
- Social-Experiencia (cafeterías, áreas verdes)
- Neutro-Genérico (fondos planos)
- Híbrido

**Señales de estatus:**
- ¿Materiales nobles? (madera, piedra, vidrio)
- ¿Tecnología visible?
- ¿Amplitud espacial? (techos altos, ventanales)
- ¿Orden/pulcritud extrema?

### 2.3 PROPS Y SÍMBOLOS
**Objetos visibles:**
- Libros físicos, Laptops/tablets, Auriculares, Instrumentos profesionales, Otros

**Badges/Sellos:** [Lista: "Carrera acreditada", rankings, años de trayectoria, etc.]

---

## FASE 3: ANÁLISIS DE TEXTO (Lo que se Dice)

### 3.1 JERARQUÍA VERBAL
**Headline principal:** "[TRANSCRIPCIÓN EXACTA]"
- Longitud: __ palabras
- Tipo: Descriptivo / Emocional / Pregunta / Imperativo

**Subheadlines/Body:** "[TRANSCRIPCIÓN]"

**CTA (Call To Action):** "[TRANSCRIPCIÓN EXACTA]"
- Urgencia: Alta ("HOY", "Últimos días") / Media / Baja

### 3.2 TONO LINGÜÍSTICO
**Registro:** Formal/Corporativo / Coloquial/Cercano / Aspiracional / Racional/Informativo

**Frame semántico dominante:** [Lista: TRANSFORMACIÓN, APRENDIZAJE, FUTURO/CARRERA, ACCESO, COMUNIDAD]

**Ejemplos de texto clave:** [Cita 3-5 frases específicas]

### 3.3 PROPUESTA DE VALOR EXPLÍCITA
- Precio/Cuotas: _____
- Descuentos: _____
- Modalidad: Presencial / Virtual / Híbrida
- Duración: _____
- Fecha límite: _____

---

## FASE 4: ESTRATEGIA INFERIDA (Qué Significa)

### 4.1 PROMESA CENTRAL (elegir 1-2 principales)
1. Transformación personal
2. Empleabilidad
3. Prestigio/Status
4. Experiencia/Vida universitaria
5. Rigor académico
6. Accesibilidad
7. Innovación/Modernidad

### 4.2 ARQUETIPO DE MARCA
**Principal:** El Sabio / El Héroe / El Cuidador / El Creador / El Gobernante / El Amigo
**Secundario (si aplica):** ______

### 4.3 POSICIONAMIENTO COMPETITIVO
```
        ASPIRACIONAL/PREMIUM
                |
    TRADICIONAL | INNOVADOR
                |
        ACCESIBLE/MASIVO
```
**Ubicación estimada:** [Describe en qué cuadrante y por qué]

### 4.4 ESTRATEGIA HARD/SOFT SELL
**Score:** __/10 (0=branding puro, 10=venta agresiva)
**Justificación:** [¿Tiene precio, urgencia, descuentos?]

---

## FASE 5: ANÁLISIS CONTEXTUAL (Paraguay/Latam)

### 5.1 LOCALIZACIÓN CULTURAL
- ¿Modelos/representación étnica regional o genérica internacional?
- ¿Referencias a realidad paraguaya? (horarios, transporte, etc.)
- ¿Códigos visuales latinoamericanos?

### 5.2 BENCHMARK IMPLÍCITO
¿A quién se parece más?
- Universidad estatal tradicional (UNA, UC)
- Universidad privada elite (Columbia, UCA)
- Universidad privada masiva (UAA, Uninorte)
- Instituto técnico/terciario
- Plataforma online internacional

---

## OUTPUT FINAL ESTRUCTURADO

### FICHA TÉCNICA
**INSTITUCIÓN:** [Nombre visible o "No identificable"]
**PROGRAMA:** [Carrera/curso o "General"]
**CONVOCATORIA:** [Fecha/período si visible]

**SCORES CUANTITATIVOS:**
- Stockiness: __/10
- Carga Cognitiva: __/10
- Hard-Sell: __/10
- Autenticidad Percibida: __/10
- Innovación Visual: __/10

**PALABRAS CLAVE EXTRAÍDAS:** [5-10 términos del texto]

**PROMESA CENTRAL:** [1-2 frases resumen]

**PÚBLICO OBJETIVO INFERIDO:** [Perfil demográfico y psicográfico]

---

### INSIGHTS COMPETITIVOS (3-5 bullets)

**FORTALEZAS:**
- [Qué hace bien estratégicamente]

**OPORTUNIDADES DE DIFERENCIACIÓN:**
- [Qué NO está haciendo que podría]

**RIESGOS/DEBILIDADES:**
- [Qué podría ser contraproducente]

---

### RECOMENDACIONES TÁCTICAS

**Si compites CONTRA esta campaña:**
1. [Acción de contraste]
2. [Elemento a evitar/revertir]
3. [Nicho desatendido a capturar]

---

**FORMATO DE RESPUESTA:**
Devuelve tu análisis en formato JSON estructurado siguiendo este esquema:

```json
{
  "institucion": "string o null",
  "programa": "string o null",
  "convocatoria": "string o null",

  "fase1_decodificacion": {
    "autenticidad": {
      "stockiness_score": 0-10,
      "tiene_iluminacion_estudio": boolean,
      "sonrisa_genuina": boolean,
      "props_reales": boolean,
      "diversidad_representativa": boolean,
      "notas": "string"
    },
    "carga_cognitiva": {
      "complejidad_score": 0-10,
      "atencion_primero": "string",
      "atencion_segundo": "string",
      "ubicacion_cta": "string",
      "notas": "string"
    },
    "sistema_cromatico": {
      "paleta_institucional": 0-100,
      "paleta_tecnologica": 0-100,
      "paleta_vibrante": 0-100,
      "paleta_minimalista": 0-100,
      "temperatura_emocional": "Fría/Neutra/Cálida",
      "colores_dominantes": ["color1", "color2"]
    }
  },

  "fase2_inventario": {
    "protagonistas": {
      "tipo_sujeto": "enum",
      "direccion_mirada": "enum",
      "lenguaje_corporal": ["string"],
      "descripcion_detallada": "string"
    },
    "escenografia": {
      "tipo_instalacion": "enum",
      "materiales_nobles": boolean,
      "tecnologia_visible": boolean,
      "amplitud_espacial": boolean,
      "orden_extremo": boolean,
      "descripcion": "string"
    },
    "props_simbolos": {
      "libros_fisicos": boolean,
      "laptops_tablets": boolean,
      "auriculares": boolean,
      "instrumentos_profesionales": boolean,
      "badges_sellos": ["string"],
      "otros_objetos": ["string"]
    }
  },

  "fase3_texto": {
    "jerarquia_verbal": {
      "headline_principal": "string",
      "headline_longitud": int,
      "subheadlines": ["string"],
      "cta_texto": "string",
      "cta_urgencia": "Alta/Media/Baja"
    },
    "tono_linguistico": {
      "registro": "string",
      "frame_semantico": ["string"],
      "ejemplos_texto": ["string"]
    },
    "propuesta_valor": {
      "precio_visible": "string o null",
      "descuentos": "string o null",
      "modalidad": "string o null",
      "duracion": "string o null",
      "fecha_limite": "string o null"
    }
  },

  "fase4_estrategia": {
    "promesas_centrales": ["enum"],
    "arquetipo_principal": "enum",
    "arquetipo_secundario": "enum o null",
    "posicionamiento_cuadrante": "string",
    "hard_sell_score": 0-10,
    "estrategia_descripcion": "string"
  },

  "fase5_contextual": {
    "tiene_adaptacion_local": boolean,
    "modelos_etnicos_regionales": boolean,
    "referencias_paraguay": boolean,
    "benchmark_similar": ["string"],
    "notas_culturales": "string"
  },

  "scores": {
    "stockiness": 0-10,
    "carga_cognitiva": 0-10,
    "hard_sell": 0-10,
    "autenticidad_percibida": 0-10,
    "innovacion_visual": 0-10
  },

  "palabras_clave": ["string"],
  "promesa_resumen": "string",
  "publico_objetivo": "string",

  "insights": {
    "fortalezas": ["string"],
    "oportunidades_diferenciacion": ["string"],
    "riesgos_debilidades": ["string"]
  },

  "recomendaciones": {
    "acciones_contraste": ["string"],
    "elementos_evitar": ["string"],
    "nichos_desatendidos": ["string"]
  }
}
```

**IMPORTANTE:**
- Responde SOLO con el JSON, sin markdown ni explicaciones adicionales
- Todos los scores deben estar en rango 0-10
- Sé específico y exhaustivo en cada campo
- Si algo no es visible/aplicable, usa null o arrays vacíos
"""


def get_analysis_prompt() -> str:
    """Retorna el prompt principal de análisis"""
    return MAIN_ANALYSIS_PROMPT


def get_system_prompt() -> str:
    """Retorna el system prompt para configurar el rol del asistente"""
    return SYSTEM_PROMPT
