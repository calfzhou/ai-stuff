# Gocalf Pet

Gocalf desktop pet generated from the original `gocalf.svg` logo body.

The persona follows the logo concept: "Go" means moving forward or beginning, and "Calf" represents youth, energy, strength, and growth. The pet is meant to feel positive, forward-moving, and encouraging.

## Install

Copy this folder to the local Eureka pets directory:

```bash
cp -R pets/gocalf ~/.eureka/pets/gocalf
```

Then select `Gocalf` in Settings > Appearance > Desktop Pet. If it is already selected, restart Eureka to reload cached stickers and persona.

## Contents

- `pet.json` and `stickers/` are the installable Eureka desktop pet files.
- `source/generate_gocalf_codex_pet.py` generates the Codex-style spritesheet source.
- `source/generate_gocalf_eureka_pet.py` generates the Eureka desktop pet frame SVGs, manifest, and local install copy.
- `source/concepts/` keeps the approved concept and comparison render.
- `source/codex-pet/` keeps the Codex pet spritesheet package.

## Regenerate

From this directory:

```bash
cd source
python3 generate_gocalf_codex_pet.py
rsvg-convert -w 1536 -h 1872 codex-pet/spritesheet.svg | magick png:- -define webp:lossless=true codex-pet/spritesheet.webp

python3 generate_gocalf_eureka_pet.py
for state in idle thinking needs_input complete error steer; do
  for svg in eureka-pet/frames/$state/*.svg; do
    rsvg-convert -w 352 -h 352 "$svg" -o "${svg%.svg}.png"
  done
done
magick -delay 14 -loop 0 eureka-pet/frames/idle/*.png -define webp:lossless=true ../stickers/idle-1.webp
magick -delay 10 -loop 0 eureka-pet/frames/thinking/*.png -define webp:lossless=true ../stickers/thinking-1.webp
magick -delay 13 -loop 0 eureka-pet/frames/needs_input/*.png -define webp:lossless=true ../stickers/needs_input-1.webp
magick -delay 10 -loop 0 eureka-pet/frames/complete/*.png -define webp:lossless=true ../stickers/complete-1.webp
magick -delay 13 -loop 0 eureka-pet/frames/error/*.png -define webp:lossless=true ../stickers/error-1.webp
magick -delay 12 -loop 0 eureka-pet/frames/steer/*.png -define webp:lossless=true ../stickers/steer-1.webp
cp eureka-pet/pet.json ../pet.json
```

Dependencies: Python 3, `rsvg-convert`, and ImageMagick with WebP support.
