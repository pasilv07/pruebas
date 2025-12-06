"""
Motion Graphics Generator for Instagram Reels
Estilo cinematográfico tipo After Effects para explicar conceptos de IA

Tamaño del lienzo: 1080x1920 (Instagram Reels - 9:16)
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

# Configuración del lienzo para Instagram Reels
REEL_WIDTH = 1080
REEL_HEIGHT = 1920
FPS = 30
DURATION = 10  # segundos por defecto

# Paleta de colores cinematográfica para IA
COLORS = {
    "background_dark": "#0a0a0f",
    "background_gradient_top": "#0f0f1a",
    "background_gradient_bottom": "#1a0a20",
    "primary": "#00d4ff",      # Cyan brillante
    "secondary": "#8b5cf6",    # Púrpura
    "accent": "#ff006e",       # Magenta
    "text_white": "#ffffff",
    "text_gray": "#a0a0a0",
    "glow_blue": "#00d4ff",
    "glow_purple": "#8b5cf6",
    "neural_green": "#00ff88",
}


def hex_to_rgb(hex_color):
    """Convierte color hex a RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def create_gradient_background(width=REEL_WIDTH, height=REEL_HEIGHT):
    """Crea un fondo con gradiente cinematográfico"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)

    top_color = hex_to_rgb(COLORS["background_gradient_top"])
    bottom_color = hex_to_rgb(COLORS["background_gradient_bottom"])

    for y in range(height):
        ratio = y / height
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * ratio)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * ratio)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    return img


def add_particle_grid(img, progress=0.5, density=20):
    """Añade una grilla de partículas tipo matrix/neural network"""
    draw = ImageDraw.Draw(img, 'RGBA')
    width, height = img.size

    # Dibujar puntos de la grilla
    spacing_x = width // density
    spacing_y = height // density

    for i in range(density + 1):
        for j in range(density + 1):
            x = i * spacing_x
            y = j * spacing_y

            # Animación basada en progress
            offset_x = int(math.sin(progress * math.pi * 2 + i * 0.5) * 5)
            offset_y = int(math.cos(progress * math.pi * 2 + j * 0.5) * 5)

            # Tamaño variable
            size = 2 + int(math.sin(progress * math.pi * 2 + i + j) * 2)

            # Color con transparencia
            alpha = int(50 + 50 * math.sin(progress * math.pi * 2 + i * 0.3 + j * 0.3))
            color = hex_to_rgb(COLORS["primary"]) + (alpha,)

            draw.ellipse([
                x + offset_x - size,
                y + offset_y - size,
                x + offset_x + size,
                y + offset_y + size
            ], fill=color)

    return img


def add_glowing_lines(img, progress=0.5):
    """Añade líneas brillantes tipo circuito/neural"""
    draw = ImageDraw.Draw(img, 'RGBA')
    width, height = img.size

    # Líneas horizontales animadas
    num_lines = 8
    for i in range(num_lines):
        y_base = (i + 1) * height // (num_lines + 1)

        # Animación de la línea
        start_x = int((progress * 2 - 1) * width * 0.3)
        end_x = start_x + int(width * 0.4)

        alpha = int(100 + 50 * math.sin(progress * math.pi * 2 + i))
        color = hex_to_rgb(COLORS["secondary"]) + (alpha,)

        # Línea principal
        draw.line([(max(0, start_x), y_base), (min(width, end_x), y_base)],
                  fill=color, width=2)

    return img


def add_neural_nodes(img, progress=0.5):
    """Añade nodos de red neuronal conectados"""
    draw = ImageDraw.Draw(img, 'RGBA')
    width, height = img.size

    # Definir nodos
    nodes = []
    num_nodes = 12
    for i in range(num_nodes):
        angle = (i / num_nodes) * math.pi * 2 + progress * math.pi
        radius = 200 + 100 * math.sin(progress * math.pi * 2)
        x = width // 2 + int(math.cos(angle) * radius)
        y = height // 2 + int(math.sin(angle) * radius)
        nodes.append((x, y))

    # Dibujar conexiones
    for i, node1 in enumerate(nodes):
        for j, node2 in enumerate(nodes):
            if i < j and abs(i - j) <= 3:
                alpha = int(30 + 20 * math.sin(progress * math.pi * 4 + i + j))
                color = hex_to_rgb(COLORS["primary"]) + (alpha,)
                draw.line([node1, node2], fill=color, width=1)

    # Dibujar nodos
    for i, (x, y) in enumerate(nodes):
        size = 8 + int(4 * math.sin(progress * math.pi * 2 + i))

        # Glow effect
        for glow_size in range(size + 10, size, -2):
            alpha = int(20 * (size + 10 - glow_size) / 10)
            glow_color = hex_to_rgb(COLORS["glow_blue"]) + (alpha,)
            draw.ellipse([x - glow_size, y - glow_size, x + glow_size, y + glow_size],
                        fill=glow_color)

        # Nodo principal
        node_color = hex_to_rgb(COLORS["primary"]) + (255,)
        draw.ellipse([x - size, y - size, x + size, y + size], fill=node_color)

    return img


def add_text_with_glow(img, text, position, font_size=80, color=None, glow_color=None):
    """Añade texto con efecto de glow cinematográfico"""
    if color is None:
        color = COLORS["text_white"]
    if glow_color is None:
        glow_color = COLORS["glow_blue"]

    # Crear capa para el glow
    glow_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)

    # Intentar cargar fuente, usar default si no existe
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # Dibujar glow (múltiples capas offset)
    glow_rgb = hex_to_rgb(glow_color)
    for offset in range(10, 0, -2):
        alpha = int(30 * (10 - offset) / 10)
        for dx in [-offset, 0, offset]:
            for dy in [-offset, 0, offset]:
                pos = (position[0] + dx, position[1] + dy)
                glow_draw.text(pos, text, font=font, fill=glow_rgb + (alpha,))

    # Aplicar blur al glow
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=5))

    # Combinar con imagen original
    img = img.convert('RGBA')
    img = Image.alpha_composite(img, glow_layer)

    # Dibujar texto principal
    draw = ImageDraw.Draw(img)
    text_color = hex_to_rgb(color) if isinstance(color, str) else color
    draw.text(position, text, font=font, fill=text_color)

    return img


def create_ai_concept_frame(concept_title, concept_text, progress=0.5, frame_num=0):
    """
    Crea un frame para explicar un concepto de IA

    Args:
        concept_title: Título del concepto (ej: "Machine Learning")
        concept_text: Texto explicativo corto
        progress: Progreso de la animación (0.0 a 1.0)
        frame_num: Número de frame actual

    Returns:
        PIL Image del frame
    """
    # Crear fondo
    img = create_gradient_background()

    # Añadir elementos visuales
    img = add_particle_grid(img, progress)
    img = add_glowing_lines(img, progress)
    img = add_neural_nodes(img, progress)

    # Calcular posiciones centradas
    title_y = 400
    text_y = 550

    # Efecto de aparición del texto
    if progress < 0.2:
        # Fade in del título
        alpha = int(255 * (progress / 0.2))
    else:
        alpha = 255

    # Añadir título
    img = add_text_with_glow(
        img,
        concept_title,
        (REEL_WIDTH // 2 - len(concept_title) * 20, title_y),
        font_size=72,
        glow_color=COLORS["glow_purple"]
    )

    # Añadir texto explicativo (si ya pasó el fade in del título)
    if progress > 0.3:
        text_progress = (progress - 0.3) / 0.7
        img = add_text_with_glow(
            img,
            concept_text,
            (100, text_y),
            font_size=36,
            color=COLORS["text_gray"],
            glow_color=COLORS["glow_blue"]
        )

    # Añadir indicador de progreso en la parte inferior
    draw = ImageDraw.Draw(img)
    progress_bar_y = REEL_HEIGHT - 100
    progress_width = int(REEL_WIDTH * 0.8 * progress)

    # Fondo de la barra
    draw.rectangle([
        (REEL_WIDTH * 0.1, progress_bar_y),
        (REEL_WIDTH * 0.9, progress_bar_y + 4)
    ], fill=hex_to_rgb(COLORS["text_gray"]))

    # Barra de progreso
    if progress_width > 0:
        draw.rectangle([
            (REEL_WIDTH * 0.1, progress_bar_y),
            (REEL_WIDTH * 0.1 + progress_width, progress_bar_y + 4)
        ], fill=hex_to_rgb(COLORS["primary"]))

    return img.convert('RGB')


def generate_reel_frames(concept_title, concept_text, duration=DURATION, fps=FPS, output_dir="output"):
    """
    Genera todos los frames para un Reel

    Args:
        concept_title: Título del concepto
        concept_text: Texto explicativo
        duration: Duración en segundos
        fps: Frames por segundo
        output_dir: Directorio de salida

    Returns:
        Lista de paths a los frames generados
    """
    total_frames = duration * fps
    frame_paths = []

    os.makedirs(output_dir, exist_ok=True)

    print(f"Generando {total_frames} frames para Reel de {duration}s...")

    for frame_num in range(total_frames):
        progress = frame_num / total_frames

        frame = create_ai_concept_frame(
            concept_title,
            concept_text,
            progress,
            frame_num
        )

        frame_path = os.path.join(output_dir, f"frame_{frame_num:04d}.png")
        frame.save(frame_path, quality=95)
        frame_paths.append(frame_path)

        if frame_num % fps == 0:
            print(f"  Progreso: {frame_num}/{total_frames} frames ({progress*100:.1f}%)")

    print(f"Frames generados en: {output_dir}")
    return frame_paths


def create_video_from_frames(frame_paths, output_path, fps=FPS):
    """
    Crea un video MP4 a partir de los frames

    Args:
        frame_paths: Lista de paths a los frames
        output_path: Path del video de salida
        fps: Frames por segundo
    """
    try:
        # MoviePy 2.x usa moviepy directamente
        from moviepy import ImageSequenceClip

        print(f"Creando video: {output_path}")
        clip = ImageSequenceClip(frame_paths, fps=fps)
        clip.write_videofile(
            output_path,
            codec='libx264',
            audio=False,
            fps=fps,
            preset='medium',
            bitrate='8000k'
        )
        print(f"Video creado exitosamente: {output_path}")
        return output_path
    except ImportError as e:
        print(f"Error importando MoviePy: {e}")
        # Intentar con ffmpeg directamente como alternativa
        try:
            import subprocess
            frame_pattern = os.path.join(os.path.dirname(frame_paths[0]), "frame_%04d.png")
            cmd = [
                'ffmpeg', '-y',
                '-framerate', str(fps),
                '-i', frame_pattern,
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                '-b:v', '8000k',
                output_path
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"Video creado con ffmpeg: {output_path}")
            return output_path
        except Exception as ffmpeg_error:
            print(f"Error con ffmpeg: {ffmpeg_error}")
            raise


def create_single_preview(concept_title, concept_text, output_path="preview.png"):
    """
    Crea una imagen de preview estática
    """
    frame = create_ai_concept_frame(concept_title, concept_text, progress=0.5)
    frame.save(output_path)
    print(f"Preview guardado: {output_path}")
    return output_path


# ============================================================
# FUNCIÓN PRINCIPAL PARA GENERAR REEL COMPLETO
# ============================================================

def generate_ai_reel(
    concept_title="Machine Learning",
    concept_text="Algoritmos que aprenden de datos",
    duration=5,
    output_name="ai_reel"
):
    """
    Genera un Reel completo de Motion Graphics para Instagram

    Tamaño: 1080x1920 (Instagram Reels)

    Args:
        concept_title: Título del concepto de IA
        concept_text: Explicación corta
        duration: Duración en segundos
        output_name: Nombre base del archivo de salida

    Returns:
        Path al video generado
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "output", output_name)

    # Generar frames
    frame_paths = generate_reel_frames(
        concept_title,
        concept_text,
        duration=duration,
        output_dir=output_dir
    )

    # Crear video
    video_path = os.path.join(script_dir, "output", f"{output_name}.mp4")
    create_video_from_frames(frame_paths, video_path)

    # Crear preview
    preview_path = os.path.join(script_dir, "output", f"{output_name}_preview.png")
    create_single_preview(concept_title, concept_text, preview_path)

    return video_path


if __name__ == "__main__":
    # Ejemplo de uso
    video = generate_ai_reel(
        concept_title="REDES NEURONALES",
        concept_text="Sistemas inspirados en el cerebro humano",
        duration=5,
        output_name="neural_networks_reel"
    )
    print(f"\n Video generado: {video}")
