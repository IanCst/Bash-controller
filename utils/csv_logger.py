
from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

from utils.config import LOGS_DIR


def save_prompt_to_csv(prompt: str) -> Path:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    filename = now.strftime("prompts_%Y%m%d_%H%M%S.csv")
    file_path = LOGS_DIR / filename

    with file_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["date", "prompt"])
        writer.writerow([now.isoformat(), prompt])
    return file_path
