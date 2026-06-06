#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
from pathlib import Path

import generate_gocalf_codex_pet as codex


OUT_DIR = Path(__file__).resolve().parent
STAGING_DIR = OUT_DIR / "eureka-pet"
STICKERS_DIR = STAGING_DIR / "stickers"
FRAME_DIR = STAGING_DIR / "frames"
TARGET = 352

STATE_SOURCES = {
    "idle": ("idle", 6, 140),
    "thinking": ("running", 6, 95),
    "needs_input": ("waiting", 6, 130),
    "complete": ("jumping", 5, 95),
    "error": ("failed", 8, 130),
    "steer": ("review", 6, 120),
}

STICKER_MAP = {
    "idle": {"stickers": ["idle-1.webp"], "rotateInterval": 60000},
    "thinking": {"stickers": ["thinking-1.webp"], "rotateInterval": 10000},
    "needs_input": {"stickers": ["needs_input-1.webp"], "rotateInterval": 10000},
    "complete": {"stickers": ["complete-1.webp"], "rotateInterval": 10000},
    "error": {"stickers": ["error-1.webp"], "rotateInterval": 10000},
    "steer": {"stickers": ["steer-1.webp"], "rotateInterval": 10000},
}

SOURCE_TEXT = (
    "\"Go\" 意味着前进或开始，\"Calf\" 指小牛，通常象征年轻、活力、力量和成长。"
    "“Go Calf” 寓意一种年轻、有活力、积极向上的精神，鼓励我们勇往直前，不畏挑战。"
    "同时也代表不断学习、提升并以此实现自我价值。"
)

PERSONA = {
    "description": "Gocalf 是一只年轻有活力的小牛伙伴，代表前进、开始、成长与力量。它鼓励 Calf 勇往直前、不畏挑战，在持续学习和提升中实现自我价值。",
    "tone": ["元气", "积极", "温柔", "坚定", "成长", "鼓励"],
    "catchphrases": ["Go Calf!", "向前一步", "小牛冲呀", "继续成长", "不怕挑战", "学一点，强一点"],
    "addressUser": "Calf",
}

CHATTER_SEEDS = {
    "complete": [
        "{summary}，向前一步！",
        "好，{summary} 完成啦。",
        "{summary} 搞定，小牛冲！",
        "完成 {summary}，继续长大。",
        "{summary} 已拿下。",
        "漂亮，{summary} 过关。",
    ],
    "title": [
        "新目标：{title}。",
        "从「{title}」开始。",
        "这步叫「{title}」。",
        "{title}，出发。",
        "把它标成「{title}」。",
        "下一站：{title}。",
    ],
    "tool": [
        "用 {tool} 往前推。",
        "我跑一下 {tool}。",
        "{tool} 来帮忙。",
        "接上 {tool}。",
        "让 {tool} 出力。",
        "用 {tool} 开路。",
    ],
    "thinking": [
        "我先蓄力一下。",
        "向前想一想。",
        "正在整理路径。",
        "小牛思考中。",
        "我确认细节。",
        "一步一步来。",
    ],
}


def sticker_svg(frame: dict[str, float | str]) -> str:
    scale = 0.305
    sx = scale * float(frame.get("sx", 1.0))
    sy = scale * float(frame.get("sy", 1.0))
    dx = float(frame.get("dx", 0.0)) * 1.55
    dy = float(frame.get("dy", 0.0)) * 1.55
    rot = float(frame.get("rot", 0.0))
    blink = float(frame.get("blink", 0.0))
    pupil_dx = float(frame.get("pupil_dx", 18.0))
    pupil_dy = float(frame.get("pupil_dy", 17.0))
    brow = str(frame.get("brow", "friendly"))
    mouth_kind = str(frame.get("mouth", "smile"))
    eye_shift_y = float(frame.get("eye_shift_y", 0.0))
    art = f"""
      <g transform="translate({TARGET / 2 + dx:.1f} {TARGET / 2 + dy:.1f}) rotate({rot:.1f}) scale({sx:.4f} {sy:.4f}) translate(-512 -512)">
        {codex.body_svg()}
        {codex.face_svg(pupil_dx, pupil_dy, blink, brow, mouth_kind, eye_shift_y)}
      </g>
    """
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {TARGET} {TARGET}" width="{TARGET}" height="{TARGET}" role="img" aria-label="Gocalf desktop pet sticker frame">
  <defs>
    <style>
      .body-rim {{ fill: none; stroke: #f8fbff; stroke-width: 1.7; stroke-linejoin: round; stroke-linecap: round; }}
      .body {{ fill: #3370ff; fill-rule: nonzero; }}
    </style>
  </defs>
  {art}
</svg>
"""


def pet_json() -> dict[str, object]:
    return {
        "id": "gocalf",
        "name": "Gocalf",
        "stickerMap": STICKER_MAP,
        "persona": PERSONA,
        "chatterSeeds": CHATTER_SEEDS,
        "sourceText": SOURCE_TEXT,
        "size": 120,
        "stickerSize": 100,
    }


def install_dir() -> Path:
    home = Path.home()
    if (home / ".craft-agent" / "config.json").exists():
        return home / ".craft-agent" / "pets" / "gocalf"
    return home / ".eureka" / "pets" / "gocalf"


def main() -> None:
    if STAGING_DIR.exists():
        shutil.rmtree(STAGING_DIR)
    STICKERS_DIR.mkdir(parents=True)
    FRAME_DIR.mkdir(parents=True)

    for state, (source_state, used_count, _duration) in STATE_SOURCES.items():
        frames = codex.frames_for_state(source_state)
        assert len(frames) == used_count
        state_dir = FRAME_DIR / state
        state_dir.mkdir()
        for idx, frame in enumerate(frames, 1):
            (state_dir / f"{idx:02d}.svg").write_text(sticker_svg(frame), encoding="utf-8")

    manifest = pet_json()
    (STAGING_DIR / "pet.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    target_dir = install_dir()
    target_dir.parent.mkdir(parents=True, exist_ok=True)
    target_dir.mkdir(exist_ok=True)
    (target_dir / "stickers").mkdir(exist_ok=True)
    (target_dir / "pet.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (STAGING_DIR / "install-path.txt").write_text(str(target_dir) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
