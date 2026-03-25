from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards import main_menu_keyboard
from utils.text import START_TEXT

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    await message.answer(START_TEXT, reply_markup=main_menu_keyboard())
