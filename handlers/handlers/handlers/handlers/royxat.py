from __future__ import annotations

import asyncio
import logging
import re

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from config import get_settings
from keyboards import options_keyboard
from sheets import SheetsClient
from states import RegistrationState
from utils.text import REG_SUCCESS_TEXT

router = Router()
logger = logging.getLogger(__name__)

PHONE_RE = re.compile(r"^\+?\d{9,15}$")
settings = get_settings()
sheets_client = SheetsClient(settings)


def normalize_phone(raw_phone: str) -> str | None:
    phone = raw_phone.strip().replace(" ", "").replace("-", "")
    if phone.startswith("998"):
        phone = f"+{phone}"
    if PHONE_RE.match(phone):
        return phone
    return None


@router.message(Command("royxat"))
async def start_registration(message: Message, state: FSMContext) -> None:
    await state.set_state(RegistrationState.full_name)
    await message.answer("Ism va familiyangizni kiriting:", reply_markup=ReplyKeyboardRemove())


@router.message(RegistrationState.full_name)
async def get_full_name(message: Message, state: FSMContext) -> None:
    await state.update_data(full_name=message.text.strip())
    await state.set_state(RegistrationState.phone)
    await message.answer("Telefon raqamingizni kiriting. Masalan: +998901234567")


@router.message(RegistrationState.phone)
async def get_phone(message: Message, state: FSMContext) -> None:
    phone = normalize_phone(message.text)
    if not phone:
        await message.answer("Telefon format noto'g'ri. Iltimos, +998901234567 formatida yuboring.")
        return

    await state.update_data(phone=phone)
    await state.set_state(RegistrationState.course)
    await message.answer(
        "Kurs yo'nalishini tanlang:",
        reply_markup=options_keyboard(settings.course_options),
    )


@router.message(RegistrationState.course, F.text.in_(settings.course_options))
async def get_course(message: Message, state: FSMContext) -> None:
    await state.update_data(course=message.text.strip())
    await state.set_state(RegistrationState.study_time)
    await message.answer(
        "O'qish vaqtini tanlang:",
        reply_markup=options_keyboard(settings.time_options),
    )


@router.message(RegistrationState.course)
async def invalid_course(message: Message) -> None:
    await message.answer("Iltimos, tugmalardan birini tanlang.")


@router.message(RegistrationState.study_time, F.text.in_(settings.time_options))
async def get_study_time(message: Message, state: FSMContext) -> None:
    await state.update_data(study_time=message.text.strip())
    await state.set_state(RegistrationState.branch)
    await message.answer(
        "Filialni tanlang:",
        reply_markup=options_keyboard(settings.registration_branch_options),
    )


@router.message(RegistrationState.study_time)
async def invalid_time(message: Message) -> None:
    await message.answer("Iltimos, tugmalardan birini tanlang.")


@router.message(RegistrationState.branch, F.text.in_(settings.registration_branch_options))
async def complete_registration(message: Message, state: FSMContext) -> None:
    await state.update_data(branch=message.text.strip())
    data = await state.get_data()

    await asyncio.to_thread(
        sheets_client.append_lead,
        full_name=data["full_name"],
        phone=data["phone"],
        course=data["course"],
        study_time=data["study_time"],
        branch=data["branch"],
        telegram_id=message.from_user.id,
        username=message.from_user.username,
    )

    manager_text = (
        "🔥 YANGI LID\n\n"
        f"👤 Ism: {data['full_name']}\n"
        f"📞 Telefon: {data['phone']}\n"
        f"📚 Kurs: {data['course']}\n"
        f"⏰ Vaqt: {data['study_time']}\n"
        f"📍 Filial: {data['branch']}"
    )

    if settings.manager_chat_id:
        try:
            await message.bot.send_message(settings.manager_chat_id, manager_text)
        except Exception:
            logger.exception("Menejer chatga yuborishda xatolik")

    await message.answer(REG_SUCCESS_TEXT, reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(RegistrationState.branch)
async def invalid_branch(message: Message) -> None:
    await message.answer("Iltimos, tugmalardan birini tanlang.")
