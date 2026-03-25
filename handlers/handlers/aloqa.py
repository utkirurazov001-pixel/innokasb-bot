from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import get_settings

router = Router()


@router.message(Command("aloqa"))
async def aloqa_handler(message: Message) -> None:
    settings = get_settings()
    contacts_lines = [f"• {item['name']}: {item['phone']}" for item in settings.contacts]
    branches_lines = "\n".join([f"• {branch}" for branch in settings.registration_branch_options])
    text = (
        "INNO KASB MARKAZI aloqa ma'lumotlari:\n"
        f"{chr(10).join(contacts_lines)}\n\n"
        "Filiallar:\n"
        f"{branches_lines}\n\n"
        "Qulay filialni tanlab, /royxat orqali yoziling."
    )
    await message.answer(text)
