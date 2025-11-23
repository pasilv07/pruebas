# 📁 Carpeta de Ejemplos

Coloca aquí las imágenes de campañas educativas que quieres analizar.

## 📸 ¿Qué tipo de imágenes?

### Imágenes ideales para análisis:

✅ **Capturas de campañas publicitarias** de:
- Facebook Ads
- Instagram Ads
- LinkedIn Ads
- Google Display Ads
- Stories (Instagram, Facebook)
- Banners web
- Material impreso digitalizado

✅ **Contenido de instituciones educativas:**
- Universidades
- Institutos técnicos
- Plataformas de cursos online
- Programas de posgrado
- Cursos profesionales
- Bootcamps

### Características importantes:

- **Formato**: JPG, PNG, WEBP, GIF
- **Tamaño**: Hasta ~10MB (Claude API limit)
- **Resolución**: Preferible alta resolución para mejor análisis de texto
- **Contenido**: Debe incluir elementos visuales + texto (headlines, CTAs)

### Ejemplos de nombres de archivos:

```
universidad_x_ingenieria_2024.jpg
instituto_y_cursos_verano.png
plataforma_z_bootcamp_data.jpg
competidor_a_campaña_facebook.png
```

## 🗂️ Organización sugerida

Puedes organizar por:

### Por institución:
```
examples/
├── universidad_a/
│   ├── campaña1.jpg
│   └── campaña2.jpg
├── universidad_b/
│   └── campaña1.jpg
```

### Por período:
```
examples/
├── 2023/
│   └── campaña_marzo.jpg
├── 2024/
│   └── campaña_enero.jpg
```

### Por tipo:
```
examples/
├── facebook_ads/
├── instagram_stories/
└── display_banners/
```

## 🚀 Uso

Una vez que tengas imágenes aquí:

### Analizar una imagen específica:
```bash
python main.py analyze examples/campaña.jpg
```

### Analizar todas las imágenes:
```bash
python main.py batch examples/
```

### Analizar solo un subdirectorio:
```bash
python main.py batch examples/universidad_a/
```

## 📋 Checklist antes de analizar

- [ ] Las imágenes están en formato JPG, PNG, WEBP o GIF
- [ ] Las imágenes no están corruptas (se pueden abrir)
- [ ] El texto en las imágenes es legible (no muy pequeño)
- [ ] Configuraste tu API key en `.env`

## 💡 Tips

1. **Calidad del análisis depende de la calidad de la imagen**
   - Imágenes borrosas → análisis menos preciso
   - Texto ilegible → no se podrá analizar contenido verbal

2. **Contexto importa**
   - Incluye información de contexto en el nombre del archivo
   - Ejemplo: `universidad_x_ingenieria_sistemas_marzo2024.jpg`

3. **Variedad para comparación**
   - Recolecta campañas de diferentes competidores
   - Diferentes períodos temporales
   - Diferentes programas (grado, posgrado, cursos)

## 🔒 Privacidad

- Las imágenes procesadas se envían a la API de Claude (Anthropic)
- No se almacenan permanentemente en servidores de Anthropic
- Ver política de privacidad: https://www.anthropic.com/privacy

## ❓ Troubleshooting

**"No se encontraron imágenes"**
- Verifica que los archivos tengan extensión válida (.jpg, .png, etc.)
- Verifica permisos de lectura

**"Imagen inválida o corrupta"**
- Intenta abrir la imagen con un visor de imágenes
- Reconvierte la imagen si es necesario

---

¡Listo! Coloca tus imágenes aquí y comienza a analizar 🚀
