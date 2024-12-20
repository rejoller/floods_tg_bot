from typing import Callable, Dict, Any, Awaitable, Optional
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker
from icecream import ic



class DataBaseSession(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool
      
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Optional[Dict[str, Any]]
    ) -> Any:
        async with self.session_pool() as session_:
            data['session_'] = session_
            return await handler(event, data)