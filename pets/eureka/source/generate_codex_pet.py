#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


OUT_DIR = Path(__file__).resolve().parent
PACKAGE_DIR = OUT_DIR / "codex-pet"
CELL_W = 192
CELL_H = 208
COLS = 8
ROWS = 9
SHEET_W = CELL_W * COLS
SHEET_H = CELL_H * ROWS

LOGO_PATH = (
    "M 252 2 L 211 26 L 210 36 L 428 165 L 427 242 L 391 264 L 382 263 "
    "L 374 196 L 154 69 L 141 66 L 35 129 L 34 379 L 72 405 L 82 401 "
    "L 83 165 L 120 141 L 128 141 L 133 147 L 133 438 L 259 509 L 476 382 "
    "L 477 336 L 470 328 L 354 393 L 317 375 L 312 363 L 476 265 L 477 132 "
    "L 431 101 Z M 187 150 L 194 150 L 324 227 L 330 234 L 330 269 L 326 275 "
    "L 318 276 L 234 227 L 226 228 L 223 233 L 224 270 L 286 306 L 292 312 "
    "L 292 318 L 288 323 L 260 339 L 256 339 L 233 326 L 227 327 L 223 332 "
    "L 224 373 L 230 378 L 291 412 L 297 420 L 292 429 L 259 448 L 248 446 "
    "L 189 412 L 181 404 L 181 157 Z"
)


def body_svg() -> str:
    return f"""
      <path class="rim" fill="none" stroke-width="23" d="{LOGO_PATH}"/>
      <path class="logo" fill-rule="evenodd" d="{LOGO_PATH}"/>
    """


def eye(cx: float, cy: float, pupil_dx: float, pupil_dy: float, blink: float = 0.0) -> str:
    if blink >= 0.95:
        return f"""
          <path d="M {cx - 40:.1f} {cy:.1f} C {cx - 16:.1f} {cy + 13:.1f} {cx + 16:.1f} {cy + 13:.1f} {cx + 40:.1f} {cy:.1f}"
            fill="none" stroke="#f8fbff" stroke-width="21" stroke-linecap="round"/>
          <path d="M {cx - 40:.1f} {cy:.1f} C {cx - 16:.1f} {cy + 13:.1f} {cx + 16:.1f} {cy + 13:.1f} {cx + 40:.1f} {cy:.1f}"
            fill="none" stroke="#15171d" stroke-width="13" stroke-linecap="round"/>
        """
    ry = 43 * (1.0 - blink * 0.72)
    pupil_r = max(6.0, 14 * (1.0 - blink * 0.55))
    return f"""
      <ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="38" ry="{ry:.1f}" fill="#f8fbff" stroke="#f8fbff" stroke-width="16"/>
      <ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="38" ry="{ry:.1f}" fill="#f8fbff" stroke="#15171d" stroke-width="13"/>
      <circle cx="{cx + pupil_dx:.1f}" cy="{cy + pupil_dy:.1f}" r="{pupil_r:.1f}" fill="#15171d"/>
      <circle cx="{cx + pupil_dx + 5:.1f}" cy="{cy + pupil_dy - 6:.1f}" r="{max(2.0, pupil_r * 0.4):.1f}" fill="#f8fbff"/>
    """


def brows(kind: str = "friendly") -> str:
    if kind == "focused":
        left = ("M 129 172 C 159 151 203 153 240 176", "M 305 210 C 341 193 385 205 415 236")
    elif kind == "sad":
        left = ("M 133 191 C 162 213 203 216 238 198", "M 310 225 C 344 244 385 237 411 207")
    elif kind == "alert":
        left = ("M 130 155 C 160 134 204 139 238 165", "M 308 190 C 343 175 386 190 416 220")
    else:
        left = ("M 134 163 C 161 143 202 146 236 168", "M 311 200 C 344 185 384 197 411 226")
    return f"""
      <path d="{left[0]}" fill="none" stroke="#f8fbff" stroke-width="20" stroke-linecap="round"/>
      <path d="{left[1]}" fill="none" stroke="#f8fbff" stroke-width="20" stroke-linecap="round"/>
      <path d="{left[0]}" fill="none" stroke="#15171d" stroke-width="13" stroke-linecap="round"/>
      <path d="{left[1]}" fill="none" stroke="#15171d" stroke-width="13" stroke-linecap="round"/>
    """


def mouth(kind: str = "smile") -> str:
    if kind == "open":
        return """
          <path d="M 222 338 C 253 376 309 380 344 339" fill="none" stroke="#f8fbff" stroke-width="24" stroke-linecap="round"/>
          <path d="M 222 338 C 253 376 309 380 344 339" fill="none" stroke="#15171d" stroke-width="14" stroke-linecap="round"/>
          <ellipse cx="286" cy="354" rx="18" ry="11" fill="#15171d"/>
        """
    if kind == "frown":
        return """
          <path d="M 224 356 C 256 324 309 325 342 357" fill="none" stroke="#f8fbff" stroke-width="23" stroke-linecap="round"/>
          <path d="M 224 356 C 256 324 309 325 342 357" fill="none" stroke="#15171d" stroke-width="13" stroke-linecap="round"/>
        """
    if kind == "flat":
        return """
          <path d="M 229 343 C 260 351 307 350 339 341" fill="none" stroke="#f8fbff" stroke-width="22" stroke-linecap="round"/>
          <path d="M 229 343 C 260 351 307 350 339 341" fill="none" stroke="#15171d" stroke-width="13" stroke-linecap="round"/>
        """
    return """
      <path d="M 222 338 C 253 370 306 374 340 339" fill="none" stroke="#f8fbff" stroke-width="23" stroke-linecap="round"/>
      <path d="M 222 338 C 253 370 306 374 340 339" fill="none" stroke="#15171d" stroke-width="13" stroke-linecap="round"/>
    """


def face_svg(
    pupil_dx: float = 11,
    pupil_dy: float = 11,
    blink: float = 0.0,
    brow: str = "friendly",
    mouth_kind: str = "smile",
    eye_shift_y: float = 0.0,
) -> str:
    return f"""
      {eye(177, 219 + eye_shift_y, pupil_dx, pupil_dy, blink)}
      {eye(356, 260 + eye_shift_y, -pupil_dx, pupil_dy, blink)}
      {mouth(mouth_kind)}
      {brows(brow)}
    """


def pet_svg(frame: dict[str, float | str]) -> str:
    scale = 0.30
    sx = scale * float(frame.get("sx", 1.0))
    sy = scale * float(frame.get("sy", 1.0))
    dx = float(frame.get("dx", 0.0))
    dy = float(frame.get("dy", 0.0))
    rot = float(frame.get("rot", 0.0))
    blink = float(frame.get("blink", 0.0))
    pupil_dx = float(frame.get("pupil_dx", 8.0))
    pupil_dy = float(frame.get("pupil_dy", 8.0))
    brow = str(frame.get("brow", "friendly"))
    mouth_kind = str(frame.get("mouth", "smile"))
    eye_shift_y = float(frame.get("eye_shift_y", 0.0))
    return f"""
      <g transform="translate({CELL_W / 2 + dx:.1f} {CELL_H / 2 + dy:.1f}) rotate({rot:.1f}) scale({sx:.4f} {sy:.4f}) translate(-256 -256)">
        <g transform="translate(52 38) scale(0.80)">
          {body_svg()}
          {face_svg(pupil_dx, pupil_dy, blink, brow, mouth_kind, eye_shift_y)}
        </g>
      </g>
    """


def frames_for_state(state: str) -> list[dict[str, float | str]]:
    if state == "idle":
        return [
            {"dy": 0},
            {"dy": -1, "sy": 1.01},
            {"dy": -2, "sy": 1.015},
            {"dy": -1, "blink": 1.0},
            {"dy": 0, "sy": 0.995},
            {"dy": 1},
        ]
    if state == "running-right":
        return [
            {"dx": -6, "dy": 2, "rot": -4, "pupil_dx": 11, "brow": "alert"},
            {"dx": -3, "dy": -4, "rot": -2, "pupil_dx": 11, "brow": "alert"},
            {"dx": 0, "dy": 1, "rot": 1, "pupil_dx": 12, "brow": "alert"},
            {"dx": 4, "dy": -5, "rot": 3, "pupil_dx": 12, "brow": "alert"},
            {"dx": 7, "dy": 1, "rot": 4, "pupil_dx": 11, "brow": "alert"},
            {"dx": 3, "dy": -3, "rot": 2, "pupil_dx": 11, "brow": "alert"},
            {"dx": -1, "dy": 2, "rot": -1, "pupil_dx": 10, "brow": "alert"},
            {"dx": -5, "dy": -2, "rot": -3, "pupil_dx": 11, "brow": "alert"},
        ]
    if state == "running-left":
        return [
            {"dx": 6, "dy": 2, "rot": 4, "pupil_dx": -11, "brow": "alert"},
            {"dx": 3, "dy": -4, "rot": 2, "pupil_dx": -11, "brow": "alert"},
            {"dx": 0, "dy": 1, "rot": -1, "pupil_dx": -12, "brow": "alert"},
            {"dx": -4, "dy": -5, "rot": -3, "pupil_dx": -12, "brow": "alert"},
            {"dx": -7, "dy": 1, "rot": -4, "pupil_dx": -11, "brow": "alert"},
            {"dx": -3, "dy": -3, "rot": -2, "pupil_dx": -11, "brow": "alert"},
            {"dx": 1, "dy": 2, "rot": 1, "pupil_dx": -10, "brow": "alert"},
            {"dx": 5, "dy": -2, "rot": 3, "pupil_dx": -11, "brow": "alert"},
        ]
    if state == "waving":
        return [
            {"rot": -5, "dy": 0, "mouth": "open", "brow": "alert"},
            {"rot": 6, "dy": -5, "mouth": "open", "brow": "alert", "pupil_dx": -4},
            {"rot": -4, "dy": -2, "mouth": "smile", "brow": "friendly", "blink": 0.2},
            {"rot": 4, "dy": -4, "mouth": "open", "brow": "alert", "pupil_dx": 12},
        ]
    if state == "jumping":
        return [
            {"dy": 12, "sx": 1.07, "sy": 0.92, "brow": "alert"},
            {"dy": -8, "sx": 0.95, "sy": 1.08, "mouth": "open", "brow": "alert"},
            {"dy": -22, "rot": -3, "mouth": "open", "brow": "alert"},
            {"dy": -8, "rot": 3, "mouth": "open", "brow": "alert"},
            {"dy": 8, "sx": 1.04, "sy": 0.95},
        ]
    if state == "failed":
        return [
            {"dy": 0, "brow": "sad", "mouth": "flat", "pupil_dy": 13},
            {"dy": 4, "rot": -2, "brow": "sad", "mouth": "frown", "pupil_dy": 14},
            {"dy": 7, "rot": 2, "brow": "sad", "mouth": "frown", "pupil_dy": 14, "blink": 0.2},
            {"dy": 10, "sx": 1.03, "sy": 0.96, "brow": "sad", "mouth": "frown", "pupil_dy": 15},
            {"dy": 8, "rot": -1, "brow": "sad", "mouth": "frown", "pupil_dy": 15},
            {"dy": 6, "rot": 1, "brow": "sad", "mouth": "flat", "pupil_dy": 14},
            {"dy": 8, "brow": "sad", "mouth": "frown", "pupil_dy": 15, "blink": 0.45},
            {"dy": 7, "brow": "sad", "mouth": "frown", "pupil_dy": 15},
        ]
    if state == "waiting":
        return [
            {"pupil_dx": -8, "dy": 0},
            {"pupil_dx": -4, "dy": -1},
            {"pupil_dx": 8, "dy": -1},
            {"pupil_dx": 12, "dy": 0},
            {"pupil_dx": 4, "dy": 1, "blink": 1.0},
            {"pupil_dx": -6, "dy": 1},
        ]
    if state == "running":
        return [
            {"dy": 2, "rot": -3, "brow": "focused", "mouth": "flat"},
            {"dy": -4, "rot": 2, "brow": "focused", "mouth": "flat", "pupil_dx": 10},
            {"dy": 1, "rot": 4, "brow": "focused", "mouth": "smile"},
            {"dy": -5, "rot": -2, "brow": "focused", "mouth": "flat", "pupil_dx": -4},
            {"dy": 0, "rot": -4, "brow": "focused", "mouth": "smile"},
            {"dy": -3, "rot": 1, "brow": "focused", "mouth": "flat"},
        ]
    if state == "review":
        return [
            {"pupil_dx": -8, "pupil_dy": 11, "brow": "focused", "mouth": "flat"},
            {"pupil_dx": -4, "pupil_dy": 12, "brow": "focused", "mouth": "flat"},
            {"pupil_dx": 2, "pupil_dy": 12, "brow": "focused", "mouth": "flat"},
            {"pupil_dx": 8, "pupil_dy": 11, "brow": "focused", "mouth": "flat"},
            {"pupil_dx": 4, "pupil_dy": 10, "brow": "focused", "mouth": "smile", "blink": 0.35},
            {"pupil_dx": -6, "pupil_dy": 11, "brow": "focused", "mouth": "flat"},
        ]
    raise ValueError(state)


STATES = [
    ("idle", 6),
    ("running-right", 8),
    ("running-left", 8),
    ("waving", 4),
    ("jumping", 5),
    ("failed", 8),
    ("waiting", 6),
    ("running", 6),
    ("review", 6),
]


def build_sheet() -> str:
    cells: list[str] = []
    for row, (state, used_count) in enumerate(STATES):
        state_frames = frames_for_state(state)
        assert len(state_frames) == used_count
        for col in range(COLS):
            x = col * CELL_W
            y = row * CELL_H
            content = pet_svg(state_frames[col]) if col < used_count else ""
            cells.append(f'<g transform="translate({x} {y})">{content}</g>')
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SHEET_W} {SHEET_H}" width="{SHEET_W}" height="{SHEET_H}" role="img" aria-label="Eureka Codex Pet spritesheet">
  <defs>
    <style>
      .rim {{ stroke: #f8fbff; stroke-linejoin: round; stroke-linecap: round; }}
      .logo {{ fill: #f06292; }}
    </style>
  </defs>
  {"".join(cells)}
</svg>
"""


def main() -> None:
    PACKAGE_DIR.mkdir(exist_ok=True)
    sprite_svg = PACKAGE_DIR / "spritesheet.svg"
    sprite_svg.write_text(build_sheet(), encoding="utf-8")
    manifest = {
        "id": "eureka",
        "displayName": "Eureka",
        "description": "A face-only Eureka logo companion for Codex Pet.",
        "spritesheetPath": "spritesheet.webp",
    }
    (PACKAGE_DIR / "pet.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
