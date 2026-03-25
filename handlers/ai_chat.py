from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from ai_helper import AIHelper
from config import get_settings

router = Router()
ai_helper = AIHelper(get_settings())


@router.message(StateFilter(None), F.text, ~F.text.startswith("/"))
async def ai_chat_handler(message: Message) -> None:
    response = await ai_helper.answer(message.text)
    await message.answer(response)
