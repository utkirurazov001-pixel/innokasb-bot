from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from utils.text import KURSLAR_TEXT

router = Router()


@router.message(Command("kurslar"))
async def kurslar_handler(message: Message) -> None:
    await message.answer(KURSLAR_TEXT)
