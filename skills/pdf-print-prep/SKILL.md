---
name: "PDF Print Prep"
description: "Prepare two print-friendly PDFs: preserve original appearance with -flatten, and remove separate colored drawing overlays before flattening with -clean. Inspect first and ask if the expected overlay structure is absent or ambiguous."
---

# PDF Print Prep

Help Eureka prepare PDFs for a Canon MF641C that has stalled while processing
large transparency-masked image layers. This is a compatibility workaround,
not a guarantee against printer faults.

## 1. Inspect first; ask if the pattern does not match

Use the available PDF skill/tooling to inspect page dimensions, text, image
placements, soft masks (`/SMask`), drawing commands, and annotations. Render
representative pages to understand which content belongs to the base document.

The expected pattern is separate, page-sized or near-page-sized colored
handwriting/drawing image overlays with transparency masks, placed over base
text and original diagrams. A previously edited version may hide those same
overlays behind entirely transparent masks.

A soft mask, large image, or colored object alone is **not** proof that it is an
unwanted drawing. Confirm the overlay's role from its placement and appearance.
Do not classify printed colored text, original diagrams, or scanned page content
as removable handwriting merely because they are colored.

If the pattern is absent, only some pages match, the drawings are baked into a
scan, or removal could damage required content, **stop before creating output
files and ask**. Explain the finding briefly and ask whether to flatten only or
how the user wants the clean version handled. Do not silently substitute
grayscale, remove all colored content, or create two identical versions.

## 2. Create exactly two result PDFs

Use all pages in original order unless the user specifies a page range. Preserve
the exact original basename, including spaces and non-English characters. Insert
the suffix before `.pdf`:

- `<original-stem>-flatten.pdf`: original appearance, including colorful
  drawings, flattened to opaque page images.
- `<original-stem>-clean.pdf`: only the confirmed added drawing overlays removed,
  then flattened to opaque page images. Preserve base text and original diagrams.

Example: `Lesson Answers.pdf` produces `Lesson Answers-flatten.pdf` and
`Lesson Answers-clean.pdf`. Do not add a third unflattened copy unless requested.

Before generating files, create `pdf-print-prep_YYYYMMDD_HHMMSS/` in the working
directory. Put both results and all supporting files, temporary files, and any
new dependency caches inside that folder. It is their final location; do not
copy or move outputs afterward. Leave the source file unchanged.

## 3. Remove first, flatten second

For the clean version, actually remove the confirmed overlay drawing commands
and associated unused image resources, then discard unreachable PDF objects.
Do not merely zero their masks, hide them, or cover them with white rectangles.
Remove only the confirmed overlays, including nested ones if present; do not
indiscriminately delete every image with a soft mask.

For both outputs, fit the chosen pages onto A4 with matching portrait/landscape
orientation, keeping proportions and the entire page visible. Composite onto an
opaque white background at **300 dpi in RGB**. Build a new PDF with one opaque
image per page, preferably using lossless compression. The finished flattened
PDFs must have no transparency masks or font dependencies. Do not convert to
grayscale unless explicitly requested.

## 4. Verify and deliver

- Check output page count, order, requested source-page selection, and A4 size.
- Compare the original-preserving render against the source. Check the clean
  render to ensure only intended drawings disappeared and base content remains.
- Verify embedded raster images match the intended page renders and contain no
  alpha channels/soft masks. Check for cropping, blank pages, or missing content.
- Report file sizes and provide absolute clickable links and one `MEDIA:` line
  per result. Explain that flattened text is no longer selectable and subsequent
  drawing removal is harder because text and drawings share the same pixels.
- Do not print, cancel jobs, restart the printer, or change settings unless the
  user separately authorizes that action. Never claim print performance was
  verified without an actual print test.
