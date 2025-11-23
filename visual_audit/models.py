"""
Modelos de datos para la auditoría visual competitiva
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class TipoSujeto(str, Enum):
    ESTUDIANTE_IDEAL = "Estudiante ideal (18-25, aspiracional)"
    PROFESIONAL = "Profesional en formación (25-35, upskilling)"
    GRUPO_DIVERSO = "Grupo diverso (comunidad/inclusión)"
    NINGUNO = "Ninguno (foco en producto/instalaciones)"


class DireccionMirada(str, Enum):
    A_CAMARA = "A cámara (demanda/interpelación directa)"
    AL_HORIZONTE = "Al horizonte (aspiración/futuro)"
    A_OBJETO = "A objeto/pantalla (acción/estudio)"
    INTERACCION_SOCIAL = "Interacción social (pertenencia)"


class TipoInstalacion(str, Enum):
    TRADICIONAL_PRESTIGIO = "Tradicional-Prestigio"
    TECNOLOGICO_INNOVACION = "Tecnológico-Innovación"
    SOCIAL_EXPERIENCIA = "Social-Experiencia"
    NEUTRO_GENERICO = "Neutro-Genérico"
    HIBRIDO = "Híbrido"


class ArquetipoMarca(str, Enum):
    EL_SABIO = "El Sabio (Conocimiento, investigación)"
    EL_HEROE = "El Héroe (Superación, logros)"
    EL_CUIDADOR = "El Cuidador (Apoyo, comunidad)"
    EL_CREADOR = "El Creador (Innovación, creatividad)"
    EL_GOBERNANTE = "El Gobernante (Prestigio, élite)"
    EL_AMIGO = "El Amigo (Cercanía, experiencia)"


class PromesaCentral(str, Enum):
    TRANSFORMACION_PERSONAL = "Transformación personal"
    EMPLEABILIDAD = "Empleabilidad"
    PRESTIGIO_STATUS = "Prestigio/Status"
    EXPERIENCIA_VIDA = "Experiencia/Vida universitaria"
    RIGOR_ACADEMICO = "Rigor académico"
    ACCESIBILIDAD = "Accesibilidad"
    INNOVACION_MODERNIDAD = "Innovación/Modernidad"


# FASE 1: DECODIFICACIÓN TÉCNICA
class AutenticidadVisual(BaseModel):
    stockiness_score: int = Field(ge=0, le=10, description="Escala de stock (0=auténtico, 10=stock puro)")
    tiene_iluminacion_estudio: bool
    sonrisa_genuina: bool
    props_reales: bool
    diversidad_representativa: bool
    notas: str = ""


class CargaCognitiva(BaseModel):
    complejidad_score: int = Field(ge=0, le=10, description="0=minimalista, 10=saturado")
    atencion_primero: str
    atencion_segundo: str
    ubicacion_cta: str
    notas: str = ""


class SistemaCromatico(BaseModel):
    paleta_institucional: int = Field(ge=0, le=100, description="% Azul marino/Rojo/Gris")
    paleta_tecnologica: int = Field(ge=0, le=100, description="% Azul eléctrico/Verde/Blanco")
    paleta_vibrante: int = Field(ge=0, le=100, description="% Amarillo/Cian/Magenta")
    paleta_minimalista: int = Field(ge=0, le=100, description="% Monocromático")
    temperatura_emocional: str = Field(description="Fría/Neutra/Cálida")
    colores_dominantes: List[str]


class DecodificacionTecnica(BaseModel):
    autenticidad: AutenticidadVisual
    carga_cognitiva: CargaCognitiva
    sistema_cromatico: SistemaCromatico


# FASE 2: INVENTARIO DE CONTENIDO
class ProtagonistasRoles(BaseModel):
    tipo_sujeto: TipoSujeto
    direccion_mirada: DireccionMirada
    lenguaje_corporal: List[str]
    descripcion_detallada: str


class Escenografia(BaseModel):
    tipo_instalacion: TipoInstalacion
    materiales_nobles: bool
    tecnologia_visible: bool
    amplitud_espacial: bool
    orden_extremo: bool
    descripcion: str


class PropsSimbolos(BaseModel):
    libros_fisicos: bool
    laptops_tablets: bool
    auriculares: bool
    instrumentos_profesionales: bool
    badges_sellos: List[str]
    otros_objetos: List[str]


class InventarioContenido(BaseModel):
    protagonistas: ProtagonistasRoles
    escenografia: Escenografia
    props_simbolos: PropsSimbolos


# FASE 3: ANÁLISIS DE TEXTO
class JerarquiaVerbal(BaseModel):
    headline_principal: str
    headline_longitud: int
    subheadlines: List[str]
    cta_texto: str
    cta_urgencia: str  # Alta/Media/Baja


class TonoLinguistico(BaseModel):
    registro: str  # Formal/Coloquial/Aspiracional/Racional
    frame_semantico: List[str]
    ejemplos_texto: List[str]


class PropuestaValor(BaseModel):
    precio_visible: Optional[str]
    descuentos: Optional[str]
    modalidad: Optional[str]
    duracion: Optional[str]
    fecha_limite: Optional[str]


class AnalisisTexto(BaseModel):
    jerarquia_verbal: JerarquiaVerbal
    tono_linguistico: TonoLinguistico
    propuesta_valor: PropuestaValor


# FASE 4: ESTRATEGIA INFERIDA
class EstrategiaInferida(BaseModel):
    promesas_centrales: List[PromesaCentral]
    arquetipo_principal: ArquetipoMarca
    arquetipo_secundario: Optional[ArquetipoMarca]
    posicionamiento_cuadrante: str
    hard_sell_score: int = Field(ge=0, le=10, description="0=soft sell, 10=hard sell")
    estrategia_descripcion: str


# FASE 5: ANÁLISIS CONTEXTUAL
class AnalisisContextual(BaseModel):
    tiene_adaptacion_local: bool
    modelos_etnicos_regionales: bool
    referencias_paraguay: bool
    benchmark_similar: List[str]
    notas_culturales: str


# FICHA TÉCNICA FINAL
class ScoresCuantitativos(BaseModel):
    stockiness: int = Field(ge=0, le=10)
    carga_cognitiva: int = Field(ge=0, le=10)
    hard_sell: int = Field(ge=0, le=10)
    autenticidad_percibida: int = Field(ge=0, le=10)
    innovacion_visual: int = Field(ge=0, le=10)


class InsightsCompetitivos(BaseModel):
    fortalezas: List[str]
    oportunidades_diferenciacion: List[str]
    riesgos_debilidades: List[str]


class RecomendacionesTacticas(BaseModel):
    acciones_contraste: List[str]
    elementos_evitar: List[str]
    nichos_desatendidos: List[str]


# MODELO PRINCIPAL
class AuditReport(BaseModel):
    """Reporte completo de auditoría visual competitiva"""

    # Metadata
    id_reporte: str
    timestamp: datetime = Field(default_factory=datetime.now)
    imagen_path: str
    imagen_nombre: str

    # Identificación
    institucion: Optional[str]
    programa: Optional[str]
    convocatoria: Optional[str]

    # 5 Fases del análisis
    fase1_decodificacion: DecodificacionTecnica
    fase2_inventario: InventarioContenido
    fase3_texto: AnalisisTexto
    fase4_estrategia: EstrategiaInferida
    fase5_contextual: AnalisisContextual

    # Ficha técnica
    scores: ScoresCuantitativos
    palabras_clave: List[str]
    promesa_resumen: str
    publico_objetivo: str

    # Insights y recomendaciones
    insights: InsightsCompetitivos
    recomendaciones: RecomendacionesTacticas

    # Análisis crudo (opcional)
    analisis_completo_raw: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id_reporte": "audit_001_universidad_x",
                "institucion": "Universidad X",
                "programa": "Ingeniería en Sistemas",
                "scores": {
                    "stockiness": 7,
                    "carga_cognitiva": 5,
                    "hard_sell": 8,
                    "autenticidad_percibida": 4,
                    "innovacion_visual": 6
                }
            }
        }


class BatchAuditResult(BaseModel):
    """Resultado de procesamiento por lotes"""
    total_imagenes: int
    exitosas: int
    fallidas: int
    reportes: List[AuditReport]
    errores: List[Dict[str, str]]
    tiempo_procesamiento: float
    timestamp: datetime = Field(default_factory=datetime.now)
