# Eureka Pet

Eureka desktop pet generated from the Eureka logo, with tracked source files for future adjustment.

## Install

Copy this folder to the local Eureka pets directory:

```bash
cp -R pets/eureka ~/.eureka/pets/eureka
```

Then select `Eureka` in Settings > Appearance > Desktop Pet. If it is already selected, restart Eureka to reload cached stickers.

## Contents

- `pet.json` and `stickers/` are the installable Eureka desktop pet files.
- `preview.png` shows the first frame for each desktop pet state.
- `source/generate_codex_pet.py` generates the Codex-style spritesheet source.
- `source/generate_eureka_pet.py` generates the Eureka desktop pet frame SVGs and manifest.
- `source/concepts/` keeps the editable face concept and comparison render.
- `source/codex-pet/` keeps the Codex pet spritesheet package.

## Regenerate

From this directory:

```bash
cd source
python3 generate_codex_pet.py
rsvg-convert -w 1536 -h 1872 codex-pet/spritesheet.svg | magick png:- -define webp:lossless=true codex-pet/spritesheet.webp

python3 generate_eureka_pet.py
for state in idle thinking needs_input complete error steer; do
  for svg in eureka-pet-eureka/frames/$state/*.svg; do
    rsvg-convert -w 352 -h 352 "$svg" -o "${svg%.svg}.png"
  done
done
magick -delay 14 -loop 0 eureka-pet-eureka/frames/idle/*.png -define webp:lossless=true ../stickers/idle-1.webp
magick -delay 10 -loop 0 eureka-pet-eureka/frames/thinking/*.png -define webp:lossless=true ../stickers/thinking-1.webp
magick -delay 13 -loop 0 eureka-pet-eureka/frames/needs_input/*.png -define webp:lossless=true ../stickers/needs_input-1.webp
magick -delay 10 -loop 0 eureka-pet-eureka/frames/complete/*.png -define webp:lossless=true ../stickers/complete-1.webp
magick -delay 13 -loop 0 eureka-pet-eureka/frames/error/*.png -define webp:lossless=true ../stickers/error-1.webp
magick -delay 12 -loop 0 eureka-pet-eureka/frames/steer/*.png -define webp:lossless=true ../stickers/steer-1.webp
cp eureka-pet-eureka/pet.json ../pet.json
```

Dependencies: Python 3, `rsvg-convert`, and ImageMagick with WebP support.
