"""
Procesador por lotes para múltiples imágenes
"""
import time
from pathlib import Path
from typing import List, Optional, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm

from .analyzer import VisualAuditAnalyzer
from .models import AuditReport, BatchAuditResult


class BatchProcessor:
    """Procesador de auditorías visuales en lote"""

    def __init__(
        self,
        analyzer: Optional[VisualAuditAnalyzer] = None,
        max_workers: int = 3,
        verbose: bool = True
    ):
        """
        Inicializa el procesador por lotes

        Args:
            analyzer: Instancia de VisualAuditAnalyzer (si None, crea una nueva)
            max_workers: Número de workers paralelos (por defecto 3, cuidado con rate limits)
            verbose: Si True, muestra progress bar
        """
        self.analyzer = analyzer or VisualAuditAnalyzer()
        self.max_workers = max_workers
        self.verbose = verbose

    def find_images(self, directory: str, recursive: bool = True) -> List[Path]:
        """
        Encuentra todas las imágenes en un directorio

        Args:
            directory: Directorio a escanear
            recursive: Si True, busca recursivamente en subdirectorios

        Returns:
            Lista de rutas de imágenes encontradas
        """
        directory_path = Path(directory)

        if not directory_path.exists():
            raise FileNotFoundError(f"Directorio no encontrado: {directory}")

        # Extensiones soportadas
        extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

        if recursive:
            images = [
                p for p in directory_path.rglob("*")
                if p.suffix.lower() in extensions
            ]
        else:
            images = [
                p for p in directory_path.glob("*")
                if p.suffix.lower() in extensions
            ]

        return sorted(images)

    def process_single(self, image_path: Path) -> tuple[Optional[AuditReport], Optional[str]]:
        """
        Procesa una sola imagen (wrapper para manejo de errores)

        Args:
            image_path: Ruta a la imagen

        Returns:
            tuple: (report o None, error_message o None)
        """
        try:
            report = self.analyzer.analyze_image(str(image_path), verbose=False)
            return report, None
        except Exception as e:
            error_msg = f"{image_path.name}: {str(e)}"
            return None, error_msg

    def process_batch(
        self,
        image_paths: List[Path],
        parallel: bool = True
    ) -> BatchAuditResult:
        """
        Procesa múltiples imágenes

        Args:
            image_paths: Lista de rutas de imágenes
            parallel: Si True, procesa en paralelo (cuidado con rate limits)

        Returns:
            BatchAuditResult con todos los reportes y estadísticas
        """
        start_time = time.time()

        reportes: List[AuditReport] = []
        errores: List[Dict[str, str]] = []

        total = len(image_paths)

        if self.verbose:
            print(f"\n🚀 Procesando {total} imágenes...")
            print(f"   Modo: {'Paralelo' if parallel else 'Secuencial'}")
            print(f"   Workers: {self.max_workers if parallel else 1}\n")

        if parallel and self.max_workers > 1:
            # Procesamiento paralelo
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {
                    executor.submit(self.process_single, img_path): img_path
                    for img_path in image_paths
                }

                with tqdm(total=total, disable=not self.verbose) as pbar:
                    for future in as_completed(futures):
                        img_path = futures[future]
                        report, error = future.result()

                        if report:
                            reportes.append(report)
                            pbar.set_description(f"✅ {img_path.name}")
                        else:
                            errores.append({
                                "imagen": str(img_path),
                                "error": error
                            })
                            pbar.set_description(f"❌ {img_path.name}")

                        pbar.update(1)
        else:
            # Procesamiento secuencial
            for img_path in tqdm(image_paths, disable=not self.verbose):
                report, error = self.process_single(img_path)

                if report:
                    reportes.append(report)
                else:
                    errores.append({
                        "imagen": str(img_path),
                        "error": error
                    })

        elapsed_time = time.time() - start_time

        result = BatchAuditResult(
            total_imagenes=total,
            exitosas=len(reportes),
            fallidas=len(errores),
            reportes=reportes,
            errores=errores,
            tiempo_procesamiento=elapsed_time
        )

        if self.verbose:
            print(f"\n{'='*60}")
            print(f"✅ Completado en {elapsed_time:.2f}s")
            print(f"   Exitosas: {result.exitosas}/{total}")
            print(f"   Fallidas: {result.fallidas}/{total}")
            print(f"{'='*60}\n")

            if errores:
                print("⚠️  Errores encontrados:")
                for err in errores:
                    print(f"   - {Path(err['imagen']).name}: {err['error']}")
                print()

        return result

    def process_directory(
        self,
        directory: str,
        recursive: bool = True,
        parallel: bool = True
    ) -> BatchAuditResult:
        """
        Procesa todas las imágenes en un directorio

        Args:
            directory: Directorio con imágenes
            recursive: Buscar recursivamente en subdirectorios
            parallel: Procesar en paralelo

        Returns:
            BatchAuditResult con todos los reportes
        """
        images = self.find_images(directory, recursive=recursive)

        if not images:
            print(f"⚠️  No se encontraron imágenes en: {directory}")
            return BatchAuditResult(
                total_imagenes=0,
                exitosas=0,
                fallidas=0,
                reportes=[],
                errores=[],
                tiempo_procesamiento=0.0
            )

        if self.verbose:
            print(f"📁 Directorio: {directory}")
            print(f"   Encontradas: {len(images)} imágenes")

        return self.process_batch(images, parallel=parallel)
