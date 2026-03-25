from __future__ import annotations

import logging
import time
from datetime import datetime, timezone

import gspread

from config import Settings

logger = logging.getLogger(__name__)


class SheetsClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._worksheet = None

    def _get_worksheet(self):
        if self._worksheet is None:
            gc = gspread.service_account_from_dict(self.settings.google_creds_dict)
            spreadsheet = gc.open(self.settings.google_sheet_name)
            self._worksheet = spreadsheet.sheet1
        return self._worksheet

    def append_lead(
        self,
        *,
        full_name: str,
        phone: str,
        course: str,
        study_time: str,
        branch: str,
        telegram_id: int,
        username: str | None,
    ) -> bool:
        row = [
            datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
            full_name,
            phone,
            course,
            study_time,
            branch,
            str(telegram_id),
            username or "",
        ]
        for attempt in range(1, 4):
            try:
                self._get_worksheet().append_row(row, value_input_option="USER_ENTERED")
                return True
            except Exception:
                logger.exception("Google Sheets ga yozishda xatolik. Urinish=%s", attempt)
                self._worksheet = None
                time.sleep(0.8)
        return False
