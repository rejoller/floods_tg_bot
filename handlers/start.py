from aiogram.types import Message
from aiogram.filters.command import CommandStart
from aiogram import Router


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer('Здравствуйте, я бот для телеграма. Напишите мне /help для получения списка команд')