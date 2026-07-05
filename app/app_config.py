from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class AppConfig:
    auto_select_sources: set[str]
    auto_select_source_items: set[str]
    auto_select_targets: set[str]
    auto_capture: bool = False
    auto_streaming: bool = False


def _config_path() -> Path:
    home = Path.home()
    config_dir = home / ".config"
    if config_dir.exists() and config_dir.is_dir():
        target_dir = config_dir / "beamie"
    else:
        target_dir = home / ".beamie"
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir / "config.json"


def load_config() -> AppConfig:
    path = _config_path()
    if not path.exists():
        return AppConfig(
            auto_select_sources=set(),
            auto_select_source_items=set(),
            auto_select_targets=set(),
            auto_capture=False,
            auto_streaming=False,
        )

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return AppConfig(
            auto_select_sources=set(),
            auto_select_source_items=set(),
            auto_select_targets=set(),
            auto_capture=False,
            auto_streaming=False,
        )

    src = data.get("auto_select_sources", [])
    src_items = data.get("auto_select_source_items", [])
    dst = data.get("auto_select_targets", [])
    auto_cap = data.get("auto_capture", False)
    auto_stream = data.get("auto_streaming", False)
    return AppConfig(
        auto_select_sources={s for s in src if isinstance(s, str)},
        auto_select_source_items={s for s in src_items if isinstance(s, str)},
        auto_select_targets={s for s in dst if isinstance(s, str)},
        auto_capture=bool(auto_cap),
        auto_streaming=bool(auto_stream),
    )


def save_config(cfg: AppConfig) -> None:
    path = _config_path()
    payload = {
        "auto_select_sources": sorted(cfg.auto_select_sources),
        "auto_select_source_items": sorted(cfg.auto_select_source_items),
        "auto_select_targets": sorted(cfg.auto_select_targets),
        "auto_capture": cfg.auto_capture,
        "auto_streaming": cfg.auto_streaming,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
