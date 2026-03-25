from __future__ import annotations

import logging

from openai import AsyncOpenAI

from config import Settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "Siz INNO KASB MARKAZI virtual yordamchisisiz. "
    "Faqat o'zbek tilida, qisqa, aniq va professional javob bering. "
    "Faqat markaz, kurslar, ro'yxatdan o'tish, voucher va filiallar mavzusida gapiring. "
    "Agar mavzu aloqasiz bo'lsa, muloyim tarzda markaz mavzusiga qaytaring va /royxat ga yo'naltiring. "
    "Huquqiy yoki moliyaviy kafolat bermang. "
    "Voucher haqida gapirganda 'amaldagi tartib va tegishli toifa asosida' iborasini saqlang. "
    "Imkon qadar foydalanuvchini /royxat ga yo'naltiring."
)

FALLBACK_AI_TEXT = (
    "Hozir javob berishda kichik texnik uzilish bor. "
    "INNO KASB MARKAZI bo'yicha tezkor ma'lumot uchun /yordam yoki /royxat dan foydalaning."
)


class AIHelper:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = AsyncOpenAI(api_key=settings.openai_api_key, timeout=20)

    async def answer(self, user_text: str) -> str:
        try:
            response = await self.client.responses.create(
                model=self.settings.openai_model,
                input=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_text},
                ],
                max_output_tokens=self.settings.openai_max_tokens,
                temperature=self.settings.openai_temperature,
            )
            text = response.output_text.strip()
            return text or FALLBACK_AI_TEXT
        except Exception:
            logger.exception("OpenAI so'rovida xatolik")
            return FALLBACK_AI_TEXT
