from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from utils.text import YORDAM_TEXT

router = Router()


@router.message(Command("yordam"))
async def yordam_handler(message: Message) -> None:
    await message.answer(YORDAM_TEXT)
