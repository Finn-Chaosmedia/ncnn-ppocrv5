#!/usr/bin/env python3
"""
Einfaches Brillanten-Icon für OCR Scanner App erstellen
"""

from PIL import Image, ImageDraw
import os

# Farben
BLUE_PRIMARY = (0, 122, 255)      # iOS Blau
BLUE_LIGHT = (100, 210, 255)      # Helles Blau
WHITE = (255, 255, 255)
TRANSPARENT = (0, 0, 0, 0)

# Größen für Android
sizes = {
    'mdpi': 48,
    'hdpi': 72,
    'xhdpi': 96,
    'xxhdpi': 144,
    'xxxhdpi': 192
}

def create_diamond_icon(size):
    """Erstelle ein Brillanten/Diamant Icon"""
    img = Image.new('RGBA', (size, size), TRANSPARENT)
    draw = ImageDraw.Draw(img)
    
    # Zentrum und Radius
    center = size // 2
    radius = size // 3
    
    # Brillanten-Form: Raute mit 4 Ecken
    points = [
        (center, center - radius),      # Oben
        (center + radius, center),      # Rechts
        (center, center + radius),      # Unten
        (center - radius, center)       # Links
    ]
    
    # Brillanten zeichnen (gefüllt)
    draw.polygon(points, fill=BLUE_PRIMARY)
    
    # Innere Highlights für 3D-Effekt
    inner_radius = radius // 2
    inner_points = [
        (center, center - inner_radius),
        (center + inner_radius, center),
        (center, center + inner_radius),
        (center - inner_radius, center)
    ]
    draw.polygon(inner_points, fill=BLUE_LIGHT)
    
    # Scanner-Strahlen (4 kleine Linien)
    ray_length = radius // 3
    for angle in [0, 90, 180, 270]:
        # Startpunkt am äußeren Rand des Brillanten
        start_x = center + int((radius + 5) * (1 if angle == 0 else -1 if angle == 180 else 0))
        start_y = center + int((radius + 5) * (1 if angle == 90 else -1 if angle == 270 else 0))
        
        # Endpunkt weiter außen
        end_x = center + int((radius + ray_length) * (1 if angle == 0 else -1 if angle == 180 else 0))
        end_y = center + int((radius + ray_length) * (1 if angle == 90 else -1 if angle == 270 else 0))
        
        draw.line([start_x, start_y, end_x, end_y], fill=WHITE, width=max(2, size//48))
    
    return img

def main():
    print("🎨 Erstelle Brillanten-Icons für OCR Scanner App...")
    
    # Icons für alle Größen erstellen
    for density, size in sizes.items():
        print(f"  • Erstelle {density} ({size}x{size})...")
        icon = create_diamond_icon(size)
        
        # Speichern
        output_dir = f"app/src/main/res/drawable-{density}"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "ic_launcher.png")
        icon.save(output_path, "PNG")
        
        print(f"    ✓ Gespeichert: {output_path}")
    
    print("\n✅ Alle Icons erstellt!")
    print("\n📁 Ordner-Struktur:")
    for density in sizes.keys():
        print(f"  • drawable-{density}/ic_launcher.png")

if __name__ == "__main__":
    main()