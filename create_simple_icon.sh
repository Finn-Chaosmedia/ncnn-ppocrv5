#!/bin/bash
echo "🎨 Erstelle einfache Brillanten-Icons mit ImageMagick..."

# Größen für Android
sizes=("48:mdpi" "72:hdpi" "96:xhdpi" "144:xxhdpi" "192:xxxhdpi")

for size_pair in "${sizes[@]}"; do
    size="${size_pair%%:*}"
    density="${size_pair##*:}"
    
    echo "  • Erstelle $density (${size}x${size})..."
    
    # Temporäre SVG erstellen
    cat > /tmp/diamond_${size}.svg << SVGEOF
<svg width="${size}" height="${size}" xmlns="http://www.w3.org/2000/svg">
  <!-- Hintergrund transparent -->
  <rect width="100%" height="100%" fill="transparent"/>
  
  <!-- Brillant/Diamant (Raute) -->
  <polygon points="${size/2},${size/6} ${size*5/6},${size/2} ${size/2},${size*5/6} ${size/6},${size/2}" 
           fill="#007AFF" stroke="#FFFFFF" stroke-width="2"/>
  
  <!-- Innere Highlights -->
  <polygon points="${size/2},${size/3} ${size*2/3},${size/2} ${size/2},${size*2/3} ${size/3},${size/2}" 
           fill="#64D2FF"/>
  
  <!-- Scanner-Strahlen (4 Linien) -->
  <line x1="${size/2}" y1="${size/6-5}" x2="${size/2}" y2="5" stroke="#FFFFFF" stroke-width="3"/>
  <line x1="${size*5/6+5}" y1="${size/2}" x2="${size-5}" y2="${size/2}" stroke="#FFFFFF" stroke-width="3"/>
  <line x1="${size/2}" y1="${size*5/6+5}" x2="${size/2}" y2="${size-5}" stroke="#FFFFFF" stroke-width="3"/>
  <line x1="${size/6-5}" y1="${size/2}" x2="5" y2="${size/2}" stroke="#FFFFFF" stroke-width="3"/>
</svg>
SVGEOF
    
    # SVG zu PNG konvertieren
    output_dir="app/src/main/res/drawable-${density}"
    mkdir -p "$output_dir"
    
    if command -v convert &> /dev/null; then
        convert /tmp/diamond_${size}.svg "${output_dir}/ic_launcher.png"
        echo "    ✓ PNG erstellt mit ImageMagick"
    elif command -v rsvg-convert &> /dev/null; then
        rsvg-convert -w ${size} -h ${size} /tmp/diamond_${size}.svg -o "${output_dir}/ic_launcher.png"
        echo "    ✓ PNG erstellt mit rsvg-convert"
    else
        # Fallback: Einfaches Icon mit Text (falls keine Konvertierung verfügbar)
        echo "    ⚠️ Kein ImageMagick/rsvg-convert gefunden, erstelle Text-Icon"
        cat > "${output_dir}/ic_launcher.png.txt" << TXTEOF
Einfaches Brillanten-Icon für OCR Scanner
Größe: ${size}x${size}
Farben: Blau (#007AFF) mit weißen Scanner-Strahlen
TXTEOF
        # Platzhalter-Icon erstellen (einfaches blaues Quadrat)
        echo "P1 ${size} ${size}" > "${output_dir}/ic_launcher.pbm"
        for ((i=0; i<size*size; i++)); do
            echo $((i % 2)) >> "${output_dir}/ic_launcher.pbm"
        done
    fi
done

echo -e "\n✅ Icons erstellt in:"
for density in mdpi hdpi xhdpi xxhdpi xxxhdpi; do
    if [ -f "app/src/main/res/drawable-${density}/ic_launcher.png" ]; then
        echo "  • drawable-${density}/ic_launcher.png"
    fi
done
