from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from utils.text import VOUCHER_TEXT

router = Router()


@router.message(Command("voucher"))
async def voucher_handler(message: Message) -> None:
    await message.answer(VOUCHER_TEXT)
