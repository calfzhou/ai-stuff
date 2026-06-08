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

C_BODY = (
    "M14,2.92 C16.5194671,2.92 18.8834923,3.58552618 20.9258646,4.75036765 "
    "C23.3266591,6.11963072 25.2829988,8.17883964 26.5249111,10.6580218 "
    "L21.157438,13.3424173 C19.8441878,10.7201917 17.1323226,8.92 14,8.92 "
    "C9.581722,8.92 6,12.501722 6,16.92 C6,21.338278 9.581722,24.92 14,24.92 "
    "C17.1319237,24.92 19.8434972,23.1202667 21.1569362,20.4985844 "
    "L26.524486,23.1828269 C24.2259103,27.770606 19.4807453,30.92 14,30.92 "
    "C6.26801351,30.92 0,24.6519865 0,16.92 C0,9.18801351 6.26801351,2.92 14,2.92 Z"
)
LEFT_TOP = (
    "M3.5,0.520000001 C4.0389319,0.520000001 4.51148102,0.804218481 "
    "4.77593471,1.23094279 L4.77757384,1.23002808 L4.78972262,1.25363724 "
    "C4.83633603,1.33191483 4.87602559,1.41479558 4.90794647,1.50143469 "
    "C5.66943921,2.98459361 7.21613917,4 9,4 C9.64019601,4 "
    "10.2498465,3.86921924 10.8036928,3.63291651 C11.4393516,5.12866795 "
    "12.1313531,6.88111103 12.5653953,7.94646894 C11.5210107,8.56452258 "
    "10.3020185,8.92 9,8.92 C5.17912337,8.92 2.07324819,5.85871493 "
    "2.00127666,2.05504698 L2,2.02 C2,1.19157288 2.67157288,0.520000001 3.5,0.520000001 Z"
)
RIGHT_TOP = (
    "M16.9,0.520000001 C17.4389319,0.520000001 17.911481,0.804218481 "
    "18.1759347,1.23094279 L18.1775738,1.23002808 L18.1897226,1.25363724 "
    "C18.236336,1.33191483 18.2760256,1.41479558 18.3079465,1.50143469 "
    "C19.0694392,2.98459361 20.6161392,4 22.4,4 C23.040196,4 "
    "23.6498465,3.86921924 24.2036928,3.63291651 C24.8393516,5.12866795 "
    "25.5313531,6.88111103 25.9653953,7.94646894 C24.9210107,8.56452258 "
    "23.7020185,8.92 22.4,8.92 C18.5791234,8.92 15.4732482,5.85871493 "
    "15.4012767,2.05504698 L15.4,2.02 C15.4,1.19157288 16.0715729,0.520000001 16.9,0.520000001 Z"
)


def body_svg() -> str:
    def paths(cls: str) -> str:
        return f"""
          <path class="{cls}" d="{C_BODY}"/>
          <path class="{cls}" d="{LEFT_TOP}"/>
          <path class="{cls}" transform="translate(20.682957, 4.720000) scale(-1, 1) translate(-20.682957, -4.720000)" d="{RIGHT_TOP}"/>
        """

    return f"""
      <g transform="scale(32)">
        <g transform="translate(2 0.3)">
          {paths("body-rim")}
          {paths("body")}
        </g>
      </g>
    """


def eye(cx: float, cy: float, look_x: float, look_y: float, blink: float = 0.0) -> str:
    if blink >= 0.95:
        return f"""
          <path d="M {cx - 51:.1f} {cy:.1f} C {cx - 18:.1f} {cy + 18:.1f} {cx + 18:.1f} {cy + 18:.1f} {cx + 51:.1f} {cy:.1f}"
            fill="none" stroke="#f8fbff" stroke-width="32" stroke-linecap="round"/>
          <path d="M {cx - 51:.1f} {cy:.1f} C {cx - 18:.1f} {cy + 18:.1f} {cx + 18:.1f} {cy + 18:.1f} {cx + 51:.1f} {cy:.1f}"
            fill="none" stroke="#15171d" stroke-width="21" stroke-linecap="round"/>
        """
    ry = 70 * (1.0 - blink * 0.74)
    pupil_r = max(8.0, 21 * (1.0 - blink * 0.55))
    return f"""
      <ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="58" ry="{ry:.1f}" fill="#f8fbff" stroke="#f8fbff" stroke-width="32"/>
      <ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="58" ry="{ry:.1f}" fill="#f8fbff" stroke="#15171d" stroke-width="25"/>
      <circle cx="{cx + look_x:.1f}" cy="{cy + look_y:.1f}" r="{pupil_r:.1f}" fill="#15171d"/>
      <circle cx="{cx + look_x + 9:.1f}" cy="{cy + look_y - 12:.1f}" r="{max(3.0, pupil_r * 0.38):.1f}" fill="#f8fbff"/>
    """


def brows(kind: str = "friendly") -> str:
    if kind == "focused":
        left = ("M 272 189 C 314 159 382 164 431 202", "M 511 205 C 555 172 622 182 670 228")
    elif kind == "sad":
        left = ("M 284 203 C 323 227 386 232 432 210", "M 516 222 C 564 244 629 232 668 196")
    elif kind == "alert":
        left = ("M 260 185 C 302 149 371 155 424 196", "M 520 197 C 565 158 633 168 684 219")
    else:
        left = ("M 260 185 C 302 149 371 155 424 196", "M 520 197 C 565 158 633 168 684 219")
    return f"""
      <path d="{left[0]}" fill="none" stroke="#f8fbff" stroke-width="34" stroke-linecap="round"/>
      <path d="{left[1]}" fill="none" stroke="#f8fbff" stroke-width="34" stroke-linecap="round"/>
      <path d="{left[0]}" fill="none" stroke="#15171d" stroke-width="21" stroke-linecap="round"/>
      <path d="{left[1]}" fill="none" stroke="#15171d" stroke-width="21" stroke-linecap="round"/>
    """


def mouth(kind: str = "smile") -> str:
    if kind == "open":
        return """
          <path d="M 355 868 C 421 927 544 909 613 842" fill="none" stroke="#f8fbff" stroke-width="38" stroke-linecap="round"/>
          <path d="M 355 868 C 421 927 544 909 613 842" fill="none" stroke="#15171d" stroke-width="23" stroke-linecap="round"/>
        """
    if kind == "frown":
        return """
          <path d="M 365 878 C 428 823 526 817 588 865" fill="none" stroke="#f8fbff" stroke-width="38" stroke-linecap="round"/>
          <path d="M 365 878 C 428 823 526 817 588 865" fill="none" stroke="#15171d" stroke-width="23" stroke-linecap="round"/>
        """
    if kind == "flat":
        return """
          <path d="M 366 858 C 430 872 523 861 586 837" fill="none" stroke="#f8fbff" stroke-width="36" stroke-linecap="round"/>
          <path d="M 366 858 C 430 872 523 861 586 837" fill="none" stroke="#15171d" stroke-width="22" stroke-linecap="round"/>
        """
    return """
      <path d="M 355 868 C 421 927 544 909 613 842" fill="none" stroke="#f8fbff" stroke-width="38" stroke-linecap="round"/>
      <path d="M 355 868 C 421 927 544 909 613 842" fill="none" stroke="#15171d" stroke-width="23" stroke-linecap="round"/>
    """


def face_svg(
    pupil_dx: float = 18,
    pupil_dy: float = 17,
    blink: float = 0.0,
    brow: str = "friendly",
    mouth_kind: str = "smile",
    eye_shift_y: float = 0.0,
) -> str:
    return f"""
      {eye(357, 304 + eye_shift_y, pupil_dx, pupil_dy, blink)}
      {eye(570, 310 + eye_shift_y, -pupil_dx, pupil_dy, blink)}
      {mouth(mouth_kind)}
      {brows(brow)}
    """


def pet_svg(frame: dict[str, float | str]) -> str:
    scale = 0.164
    sx = scale * float(frame.get("sx", 1.0))
    sy = scale * float(frame.get("sy", 1.0))
    dx = float(frame.get("dx", 0.0))
    dy = float(frame.get("dy", 0.0))
    rot = float(frame.get("rot", 0.0))
    blink = float(frame.get("blink", 0.0))
    pupil_dx = float(frame.get("pupil_dx", 18.0))
    pupil_dy = float(frame.get("pupil_dy", 17.0))
    brow = str(frame.get("brow", "friendly"))
    mouth_kind = str(frame.get("mouth", "smile"))
    eye_shift_y = float(frame.get("eye_shift_y", 0.0))
    return f"""
      <g transform="translate({CELL_W / 2 + dx:.1f} {CELL_H / 2 + dy:.1f}) rotate({rot:.1f}) scale({sx:.4f} {sy:.4f}) translate(-512 -512)">
        {body_svg()}
        {face_svg(pupil_dx, pupil_dy, blink, brow, mouth_kind, eye_shift_y)}
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
            {"dx": -6, "dy": 2, "rot": -4, "pupil_dx": 22, "brow": "alert"},
            {"dx": -3, "dy": -4, "rot": -2, "pupil_dx": 22, "brow": "alert"},
            {"dx": 0, "dy": 1, "rot": 1, "pupil_dx": 24, "brow": "alert"},
            {"dx": 4, "dy": -5, "rot": 3, "pupil_dx": 24, "brow": "alert"},
            {"dx": 7, "dy": 1, "rot": 4, "pupil_dx": 22, "brow": "alert"},
            {"dx": 3, "dy": -3, "rot": 2, "pupil_dx": 22, "brow": "alert"},
            {"dx": -1, "dy": 2, "rot": -1, "pupil_dx": 20, "brow": "alert"},
            {"dx": -5, "dy": -2, "rot": -3, "pupil_dx": 22, "brow": "alert"},
        ]
    if state == "running-left":
        return [
            {"dx": 6, "dy": 2, "rot": 4, "pupil_dx": -22, "brow": "alert"},
            {"dx": 3, "dy": -4, "rot": 2, "pupil_dx": -22, "brow": "alert"},
            {"dx": 0, "dy": 1, "rot": -1, "pupil_dx": -24, "brow": "alert"},
            {"dx": -4, "dy": -5, "rot": -3, "pupil_dx": -24, "brow": "alert"},
            {"dx": -7, "dy": 1, "rot": -4, "pupil_dx": -22, "brow": "alert"},
            {"dx": -3, "dy": -3, "rot": -2, "pupil_dx": -22, "brow": "alert"},
            {"dx": 1, "dy": 2, "rot": 1, "pupil_dx": -20, "brow": "alert"},
            {"dx": 5, "dy": -2, "rot": 3, "pupil_dx": -22, "brow": "alert"},
        ]
    if state == "waving":
        return [
            {"rot": -5, "mouth": "open", "brow": "alert"},
            {"rot": 6, "dy": -5, "mouth": "open", "brow": "alert", "pupil_dx": -8},
            {"rot": -4, "dy": -2, "mouth": "smile", "brow": "friendly", "blink": 0.2},
            {"rot": 4, "dy": -4, "mouth": "open", "brow": "alert", "pupil_dx": 24},
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
            {"brow": "sad", "mouth": "flat", "pupil_dy": 23},
            {"dy": 4, "rot": -2, "brow": "sad", "mouth": "frown", "pupil_dy": 25},
            {"dy": 7, "rot": 2, "brow": "sad", "mouth": "frown", "pupil_dy": 25, "blink": 0.2},
            {"dy": 10, "sx": 1.03, "sy": 0.96, "brow": "sad", "mouth": "frown", "pupil_dy": 26},
            {"dy": 8, "rot": -1, "brow": "sad", "mouth": "frown", "pupil_dy": 26},
            {"dy": 6, "rot": 1, "brow": "sad", "mouth": "flat", "pupil_dy": 25},
            {"dy": 8, "brow": "sad", "mouth": "frown", "pupil_dy": 26, "blink": 0.45},
            {"dy": 7, "brow": "sad", "mouth": "frown", "pupil_dy": 26},
        ]
    if state == "waiting":
        return [
            {"pupil_dx": -18, "dy": 0},
            {"pupil_dx": -8, "dy": -1},
            {"pupil_dx": 18, "dy": -1},
            {"pupil_dx": 24, "dy": 0},
            {"pupil_dx": 8, "dy": 1, "blink": 1.0},
            {"pupil_dx": -12, "dy": 1},
        ]
    if state == "running":
        return [
            {"dy": 2, "rot": -3, "brow": "focused", "mouth": "flat"},
            {"dy": -4, "rot": 2, "brow": "focused", "mouth": "flat", "pupil_dx": 22},
            {"dy": 1, "rot": 4, "brow": "focused", "mouth": "smile"},
            {"dy": -5, "rot": -2, "brow": "focused", "mouth": "flat", "pupil_dx": -8},
            {"dy": 0, "rot": -4, "brow": "focused", "mouth": "smile"},
            {"dy": -3, "rot": 1, "brow": "focused", "mouth": "flat"},
        ]
    if state == "review":
        return [
            {"pupil_dx": -18, "pupil_dy": 17, "brow": "focused", "mouth": "flat"},
            {"pupil_dx": -8, "pupil_dy": 19, "brow": "focused", "mouth": "flat"},
            {"pupil_dx": 2, "pupil_dy": 19, "brow": "focused", "mouth": "flat"},
            {"pupil_dx": 18, "pupil_dy": 17, "brow": "focused", "mouth": "flat"},
            {"pupil_dx": 8, "pupil_dy": 15, "brow": "focused", "mouth": "smile", "blink": 0.35},
            {"pupil_dx": -12, "pupil_dy": 17, "brow": "focused", "mouth": "flat"},
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
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SHEET_W} {SHEET_H}" width="{SHEET_W}" height="{SHEET_H}" role="img" aria-label="Gocalf Codex Pet spritesheet">
  <defs>
    <style>
      .body-rim {{ fill: none; stroke: #f8fbff; stroke-width: 0.95; stroke-linejoin: round; stroke-linecap: round; }}
      .body {{ fill: #3370ff; fill-rule: nonzero; }}
    </style>
  </defs>
  {"".join(cells)}
</svg>
"""


def main() -> None:
    PACKAGE_DIR.mkdir(exist_ok=True)
    (PACKAGE_DIR / "spritesheet.svg").write_text(build_sheet(), encoding="utf-8")
    manifest = {
        "id": "gocalf",
        "displayName": "Gocalf",
        "description": "A gocalf logo companion for Codex Pet.",
        "spritesheetPath": "spritesheet.webp",
    }
    (PACKAGE_DIR / "pet.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
