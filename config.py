from __future__ import annotations

import json
import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

from dotenv import load_dotenv

load_dotenv()


DEFAULT_COURSE_OPTIONS = [
    "IT",
    "Ingliz tili",
    "Rus tili",
    "Nemis tili",
    "SMM",
    "Grafik dizayn",
    "Tikuvchilik",
    "Oshpazlik",
    "Boshqa",
]

DEFAULT_TIME_OPTIONS = ["Ertalab", "Kunduzgi", "Kechqurun", "Farqi yo'q"]

DEFAULT_REG_BRANCH_OPTIONS = [
    "Angor tuman",
    "Termiz shahar",
    "Jizzax shahar",
    "Jizzax Sh.Rashidov",
    "Zangiota tuman",
    "Bekobod",
]

DEFAULT_CONTACTS = [
    {"name": "Angor filial", "phone": "+998937610200"},
]


@dataclass(frozen=True)
class Settings:
    bot_token: 8723704134:AAHWwg671Q0KfmQg08WWTkO3OqWWk3NeVio
    openai_api_key: str
    manager_chat_id: int
    google_sheet_name: str
    google_creds_json: str
    openai_model: str
    openai_max_tokens: int
    openai_temperature: float
    course_options: tuple[str, ...]
    time_options: tuple[str, ...]
    registration_branch_options: tuple[str, ...]
    contacts: tuple[dict[str, str], ...]

    @property
    def google_creds_dict(self) -> dict[str, Any]:
        try:
            return json.loads(self.google_creds_json)
        except json.JSONDecodeError:
            with open(self.google_creds_json, "r", encoding="utf-8") as f:
                return json.load(f)



def _parse_json_list(raw: str | None, default: list[Any]) -> list[Any]:
    if not raw:
        return default
    try:
        parsed = json.loads(raw)
        return parsed if isinstance(parsed, list) and parsed else default
    except json.JSONDecodeError:
        return default


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings(
        bot_token=os.getenv("BOT_TOKEN", "").strip(),
        openai_api_key=os.getenv("OPENAI_API_KEY", "").strip(),
        manager_chat_id=int(os.getenv("MANAGER_CHAT_ID", "0")),
        google_sheet_name=os.getenv("GOOGLE_SHEET_NAME", "").strip(),
        google_creds_json=os.getenv("GOOGLE_CREDS_JSON", "{}").strip(),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip(),
        openai_max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "220")),
        openai_temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.4")),
        course_options=tuple(_parse_json_list(os.getenv("COURSE_OPTIONS_JSON"), DEFAULT_COURSE_OPTIONS)),
        time_options=tuple(_parse_json_list(os.getenv("TIME_OPTIONS_JSON"), DEFAULT_TIME_OPTIONS)),
        registration_branch_options=tuple(
            _parse_json_list(os.getenv("REG_BRANCH_OPTIONS_JSON"), DEFAULT_REG_BRANCH_OPTIONS)
        ),
        contacts=tuple(_parse_json_list(os.getenv("CONTACTS_JSON"), DEFAULT_CONTACTS)),
    )
    return settings


def validate_settings(settings: Settings) -> None:
    required = {
        "BOT_TOKEN": settings.bot_token,
        "OPENAI_API_KEY": settings.openai_api_key,
        "GOOGLE_SHEET_NAME": settings.google_sheet_name,
        "GOOGLE_CREDS_JSON": settings.google_creds_json,
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        missing_str = ", ".join(missing)
        raise ValueError(f"Majburiy env qiymatlar yo'q: {missing_str}")

    if settings.openai_max_tokens < 32:
        raise ValueError("OPENAI_MAX_TOKENS kamida 32 bo'lishi kerak")

    if not 0 <= settings.openai_temperature <= 1.2:
        raise ValueError("OPENAI_TEMPERATURE 0 va 1.2 oralig'ida bo'lishi kerak")
