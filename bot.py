from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from config import get_settings, validate_settings
from handlers.ai_chat import router as ai_router
from handlers.aloqa import router as aloqa_router
from handlers.kurslar import router as kurslar_router
from handlers.royxat import router as royxat_router
from handlers.start import router as start_router
from handlers.voucher import router as voucher_router
from handlers.yordam import router as yordam_router


async def set_default_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="start", description="Boshlash"),
        BotCommand(command="kurslar", description="Kurs yo'nalishlari"),
        BotCommand(command="royxat", description="Ro'yxatdan o'tish"),
        BotCommand(command="voucher", description="Voucher tartibi"),
        BotCommand(command="aloqa", description="Filiallar va aloqa"),
        BotCommand(command="yordam", description="Botdan foydalanish"),
    ]
    await bot.set_my_commands(commands)


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    settings = get_settings()
    validate_settings(settings)

    bot = Bot(settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start_router)
    dp.include_router(kurslar_router)
    dp.include_router(voucher_router)
    dp.include_router(aloqa_router)
    dp.include_router(yordam_router)
    dp.include_router(royxat_router)
    dp.include_router(ai_router)

    await set_default_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
