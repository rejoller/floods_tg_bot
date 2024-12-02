from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert

from database.models import Municipalities, MunicSubscriptions

from utils import delete_munsub, add_munsub
from typing import Optional, Any
from datetime import datetime as dt






async def button4_clicked(
    callback: CallbackQuery, session_: AsyncSession, dialog_manager: DialogManager, data_: Optional[Any]=None):
    from database.engine import session_maker
    from bot import bot
    user_id = callback.from_user.id
    multiselect = dialog_manager.find("munsub")
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    
    
    allmunic_query = select(
        Municipalities.map_id, Municipalities.id_r_omsu
    ).order_by(Municipalities.caption_full)
    async with session_maker() as session_:
        result = await session_.execute(allmunic_query)
    response = result.all()
    municipality_ids = [item[1] for item in response]
    
    
    query = select(MunicSubscriptions.municipality_id, MunicSubscriptions.user_id).where(MunicSubscriptions.user_id == user_id)
    async with session_maker() as session_:
        result = await session_.execute(query)
    user_subs = result.all()
    user_subs = [item[0] for item in user_subs]
    
    query = select(Municipalities.id_r_omsu).where(Municipalities.id_r_omsu.in_(user_subs))
    async with session_maker() as session_:
        result = await session_.execute(query)
    response = result.all()
    
    if callback.data == 'all':
        to_subscribe = list(set(municipality_ids) - set(user_subs))
        for municipality_id in to_subscribe:
            async with session_maker() as session_:
                query = (insert(MunicSubscriptions)
                        .values(user_id=user_id, municipality_id=municipality_id, date_subscribed = dt.now())).on_conflict_do_nothing()
                await session_.execute(query)
                await session_.commit()
        return
        
    if callback.data == 'noall':
        query = delete(MunicSubscriptions).where(MunicSubscriptions.user_id == user_id)
        async with session_maker() as session_:
            await session_.execute(query)
            await session_.commit()
            return
    
    
    municipality_id = callback.data.split(":")[1]
    municipality_id = int(municipality_id)

    if multiselect.is_checked(municipality_id):
        await multiselect.set_checked(municipality_id, True)
        async with session_maker() as session_:
            await delete_munsub(session_, user_id=user_id, municipality_id=municipality_id)
            

    if not multiselect.is_checked(municipality_id):
        await multiselect.set_checked(municipality_id, False)
        async with session_maker() as session_:
            await add_munsub(session_, user_id=user_id, municipality_id=municipality_id)