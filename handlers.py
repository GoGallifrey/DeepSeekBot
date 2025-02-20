from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.generate import AI_GEN


router = Router()


class Gen(StatesGroup):
    wait = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Мише соболезнуем, остальным привет")


@router.message(Command("stop"))
async def cmd_stop(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Нет активных запросов.")
        return
    await state.clear()
    await message.answer("Запрос отменен.")


@router.message(Gen.wait)
async def stop_flood(message: Message):
    await message.answer("Запрос уже обрабатывается, подождите...")


@router.message()
async def generating(message: Message, state: FSMContext):
    # Проверяем, не находится ли пользователь уже в состоянии ожидания
    current_state = await state.get_state()
    if current_state == Gen.wait:
        await message.answer("Запрос уже обрабатывается, подождите...")
        return

    # Устанавливаем состояние "ожидание"
    await state.set_state(Gen.wait)

    try:
        # Генерируем ответ
        response = await AI_GEN(message.text)
        await message.answer(response)
    except Exception as e:
        # Если произошла ошибка, уведомляем пользователя
        await message.answer(f"Произошла ошибка: {e}")
    finally:
        # Очищаем состояние
        await state.clear()