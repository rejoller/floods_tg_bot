import logging
from config import BOT_TOKEN, REDIS_URL
import asyncio
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from logging_config import setup_logging
from logging_middleware import LoggingMiddleware
from database.db import DataBaseSession
from database.engine import session_maker
from handlers import setup_routers
from users_middleware import UsersMiddleware
from aiogram import Bot, Dispatcher




bot = Bot(BOT_TOKEN)

storage = RedisStorage.from_url(REDIS_URL, key_builder=DefaultKeyBuilder(with_destiny=True, with_bot_id=True))

async def on_startup():
    from database.engine import create_db, drop_db
    # await drop_db()
    # await create_db()
        

async def main():
    setup_logging()
    await on_startup()
    dp = Dispatcher(storage = storage)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    router = setup_routers()
    dp.include_router(router)
    dp.message.middleware(LoggingMiddleware())
    dp.message.middleware(UsersMiddleware())
    print('Бот запущен и готов к приему сообщений')
    logging.info('--------------------Бот запущен и готов к приему сообщений------------------------------')

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), skip_updates=True)
    

if __name__ == "__main__":
    asyncio.run(main())