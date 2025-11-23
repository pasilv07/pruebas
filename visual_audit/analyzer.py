"""
Analizador visual usando Claude API (Anthropic)
"""
import os
import json
import base64
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

import anthropic
from PIL import Image

from .models import AuditReport
from .prompts import get_system_prompt, get_analysis_prompt


class VisualAuditAnalyzer:
    """Analizador de auditoría visual competitiva usando Claude Vision"""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        """
        Inicializa el analizador

        Args:
            api_key: API key de Anthropic (si no se provee, lee de ANTHROPIC_API_KEY env var)
            model: Modelo de Claude a usar (por defecto claude-3-5-sonnet-20241022)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key no encontrada. "
                "Provee api_key o configura ANTHROPIC_API_KEY en .env"
            )

        self.model = model
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.max_tokens = int(os.getenv("MAX_TOKENS", "4000"))

    def _load_and_encode_image(self, image_path: str) -> tuple[str, str]:
        """
        Carga y codifica imagen en base64

        Args:
            image_path: Ruta a la imagen

        Returns:
            tuple: (base64_data, media_type)
        """
        image_path_obj = Path(image_path)

        if not image_path_obj.exists():
            raise FileNotFoundError(f"Imagen no encontrada: {image_path}")

        # Detectar media type
        suffix = image_path_obj.suffix.lower()
        media_type_map = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp"
        }

        media_type = media_type_map.get(suffix, "image/jpeg")

        # Leer y encodear
        with open(image_path, "rb") as img_file:
            image_data = base64.standard_b64encode(img_file.read()).decode("utf-8")

        return image_data, media_type

    def _validate_image(self, image_path: str) -> bool:
        """
        Valida que la imagen sea válida y legible

        Args:
            image_path: Ruta a la imagen

        Returns:
            bool: True si es válida
        """
        try:
            with Image.open(image_path) as img:
                img.verify()
            return True
        except Exception as e:
            print(f"⚠️  Imagen inválida {image_path}: {e}")
            return False

    def analyze_image(self, image_path: str, verbose: bool = False) -> AuditReport:
        """
        Analiza una imagen de campaña educativa

        Args:
            image_path: Ruta a la imagen a analizar
            verbose: Si True, imprime información de progreso

        Returns:
            AuditReport: Reporte completo de auditoría
        """
        if verbose:
            print(f"\n📸 Analizando: {Path(image_path).name}")

        # Validar imagen
        if not self._validate_image(image_path):
            raise ValueError(f"Imagen inválida o corrupta: {image_path}")

        # Cargar y encodear
        if verbose:
            print("   🔄 Cargando imagen...")

        image_data, media_type = self._load_and_encode_image(image_path)

        # Preparar mensaje para Claude
        if verbose:
            print(f"   🤖 Enviando a Claude ({self.model})...")

        message = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=get_system_prompt(),
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": get_analysis_prompt()
                        }
                    ],
                }
            ],
        )

        # Extraer respuesta
        response_text = message.content[0].text

        if verbose:
            print("   ✅ Análisis recibido, parseando JSON...")

        # Parsear JSON
        try:
            # Intentar extraer JSON si viene con markdown
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()

            analysis_data = json.loads(response_text)

        except json.JSONDecodeError as e:
            print(f"❌ Error parseando JSON: {e}")
            print(f"Respuesta recibida:\n{response_text[:500]}...")
            raise ValueError(f"Claude no retornó JSON válido: {e}")

        # Crear reporte
        image_path_obj = Path(image_path)

        report = AuditReport(
            id_reporte=f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{image_path_obj.stem}",
            timestamp=datetime.now(),
            imagen_path=str(image_path_obj.absolute()),
            imagen_nombre=image_path_obj.name,
            analisis_completo_raw=response_text,
            **analysis_data
        )

        if verbose:
            print(f"   ✅ Reporte generado: {report.id_reporte}")

        return report

    def get_usage_stats(self) -> Dict[str, Any]:
        """
        Retorna estadísticas de uso (futuro)

        Returns:
            Dict con estadísticas
        """
        return {
            "model": self.model,
            "max_tokens": self.max_tokens,
        }
