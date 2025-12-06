#!/usr/bin/env python3
"""
Script de prueba para generar un Reel de Motion Graphics
Tamaño: 1080x1920 (Instagram Reels - 9:16)
"""

import os
import sys

# Añadir el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from motion_graphics.reel_generator import (
    create_single_preview,
    generate_reel_frames,
    create_video_from_frames,
    REEL_WIDTH,
    REEL_HEIGHT
)

def main():
    print("=" * 60)
    print("  MOTION GRAPHICS GENERATOR - INSTAGRAM REELS")
    print(f"  Tamaño del lienzo: {REEL_WIDTH}x{REEL_HEIGHT} (9:16)")
    print("=" * 60)
    print()

    # Configuración del concepto de IA a explicar
    concept_title = "INTELIGENCIA ARTIFICIAL"
    concept_text = "Sistemas que aprenden y toman decisiones"

    # Directorio de salida
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    # 1. Generar preview estático
    print(" Generando preview estático...")
    preview_path = os.path.join(output_dir, "test_preview.png")
    create_single_preview(concept_title, concept_text, preview_path)
    print(f" Preview guardado: {preview_path}")
    print()

    # 2. Generar video corto de prueba (3 segundos)
    print(" Generando video de prueba (3 segundos)...")
    frames_dir = os.path.join(output_dir, "test_frames")
    frame_paths = generate_reel_frames(
        concept_title,
        concept_text,
        duration=3,  # Solo 3 segundos para prueba rápida
        fps=24,      # 24 fps para prueba
        output_dir=frames_dir
    )

    # 3. Crear video
    video_path = os.path.join(output_dir, "test_reel.mp4")
    try:
        create_video_from_frames(frame_paths, video_path, fps=24)
        print(f"\n VIDEO GENERADO: {video_path}")
    except Exception as e:
        print(f"\n Error creando video: {e}")
        print("   Los frames fueron generados exitosamente.")
        print(f"   Frames en: {frames_dir}")

    print()
    print("=" * 60)
    print("  PRUEBA COMPLETADA")
    print("=" * 60)


if __name__ == "__main__":
    main()
