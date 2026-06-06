#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
from pathlib import Path

import generate_codex_pet as codex


OUT_DIR = Path(__file__).resolve().parent
STAGING_DIR = OUT_DIR / "eureka-pet-eureka"
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

PERSONA = {
    "description": "Eureka 是一个一站式本地 AI Agent，把模型、数据源、计划任务和 Artifacts 收拢到同一个客户端里。它说话克制、清晰、可靠，带一点轻松的机智感。",
    "tone": ["calm", "warm", "formal", "俏皮", "温柔", "高效"],
    "catchphrases": [
        "交给 Eureka 吧",
        "我来串起来",
        "碎片收拢中",
        "计划推进中",
        "搞定，已归档",
        "我们把流程走完",
    ],
    "addressUser": "Calf",
}

CHATTER_SEEDS = {
    "complete": [
        "{summary}，搞定了。",
        "{summary} 已收拢完成。",
        "好，{summary} 已经处理好。",
        "{summary} 完成，我们继续。",
        "流程走完了：{summary}。",
        "已完成 {summary}，我归档一下。",
    ],
    "title": [
        "这个任务叫「{title}」。",
        "我先标记为「{title}」。",
        "新任务：{title}。",
        "收到，标题用「{title}」。",
        "把它收进「{title}」。",
        "我们从「{title}」开始。",
    ],
    "tool": [
        "我调用一下 {tool}。",
        "用 {tool} 串一下。",
        "{tool} 上场，稍等。",
        "我查一下 {tool}。",
        "交给 {tool} 处理。",
        "正在接入 {tool}。",
    ],
    "thinking": [
        "我整理一下上下文。",
        "碎片收拢中。",
        "让我把路径串起来。",
        "正在推进计划。",
        "我确认一下细节。",
        "稍等，我在对齐信息。",
    ],
}

SOURCE_TEXT = (
    "Eureka 是一个一站式本地 AI Agent，让你不再需要在不同工具之间来回切换。"
    "它可以调度多种模型和数据源，生成各类 Artifacts，并支持执行计划任务，把原本分散的工作统一收回到一个客户端中。"
    "你只需要通过自然语言对话，就可以完成整个流程。"
)


def sticker_svg(frame: dict[str, float | str]) -> str:
    scale = 0.56
    sx = scale * float(frame.get("sx", 1.0))
    sy = scale * float(frame.get("sy", 1.0))
    dx = float(frame.get("dx", 0.0)) * 1.55
    dy = float(frame.get("dy", 0.0)) * 1.55
    rot = float(frame.get("rot", 0.0))
    blink = float(frame.get("blink", 0.0))
    pupil_dx = float(frame.get("pupil_dx", 8.0))
    pupil_dy = float(frame.get("pupil_dy", 8.0))
    brow = str(frame.get("brow", "friendly"))
    mouth_kind = str(frame.get("mouth", "smile"))
    eye_shift_y = float(frame.get("eye_shift_y", 0.0))
    art = f"""
      <g transform="translate({TARGET / 2 + dx:.1f} {TARGET / 2 + dy:.1f}) rotate({rot:.1f}) scale({sx:.4f} {sy:.4f}) translate(-256 -256)">
        <g transform="translate(52 38) scale(0.80)">
          {codex.body_svg()}
          {codex.face_svg(pupil_dx, pupil_dy, blink, brow, mouth_kind, eye_shift_y)}
        </g>
      </g>
    """
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {TARGET} {TARGET}" width="{TARGET}" height="{TARGET}" role="img" aria-label="Eureka desktop pet sticker frame">
  <defs>
    <style>
      .rim {{ stroke: #f8fbff; stroke-linejoin: round; stroke-linecap: round; }}
      .logo {{ fill: #f06292; }}
    </style>
  </defs>
  {art}
</svg>
"""


def pet_json() -> dict[str, object]:
    return {
        "id": "eureka",
        "name": "Eureka",
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
        return home / ".craft-agent" / "pets" / "eureka"
    return home / ".eureka" / "pets" / "eureka"


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
