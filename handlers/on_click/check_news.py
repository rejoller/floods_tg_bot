from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.engine import session_maker
from database.models import DFloodKrudor

import pandas as pd
from utils import decline_phrase, split_message



async def check_news(callback: CallbackQuery, session: AsyncSession, dialog_manager: DialogManager):
    async with session_maker() as session_:
    
        query = select(DFloodKrudor.municipality, DFloodKrudor.date_event, DFloodKrudor.type_flood, DFloodKrudor.road, DFloodKrudor.f_location, DFloodKrudor.f_road_l,
                       DFloodKrudor.f_road_q, DFloodKrudor.f_water_level, DFloodKrudor.f_closing_date, DFloodKrudor.f_opening_date, DFloodKrudor.oper_mode,
                       DFloodKrudor.f_detour)
        response = await session_.execute(query)
        flood_districts = response.all()
        
        df = pd.DataFrame(flood_districts)
        
        response = ''
        df['danger_icon'] = df.apply(lambda row: '🔴' if row['oper_mode'] in ('Чрезвычайная ситуация', 'Режим повышенной готовности') else '🟢', axis=1)
        df['date_event'] = df['date_event'].apply(lambda x: x.strftime('%d.%m.%Y') if pd.notnull(x) else x)
        df['f_closing_date'] = df['f_closing_date'].apply(lambda x: x.strftime('%d.%m.%Y') if pd.notnull(x) else x)
        df['f_opening_date'] = df['f_opening_date'].apply(lambda x: x.strftime('%d.%m.%Y') if pd.notnull(x) else x)
        
        for i in df.iterrows():
            declined_roads = await decline_phrase(int(i[1]['f_road_q']))
            
            response += f"{i[1]['danger_icon']} {i[1]['municipality']} " + \
                        f"{i[1]['date_event']}.\n"
            if i[1]['danger_icon'] == '🔴':
                response += "ПЕРЕЛИВ ДОРОГИ. "

            response += f"{i[1]['type_flood']} \n" +\
            f"А/Д: {i[1]['road']}. Местоположение {i[1]['f_location']}\n" + \
            f"Общая протяженность: {i[1]['f_road_l']} м на {declined_roads} \n" + \
            f"Текущий уровень воды над проезжей частью: {i[1]['f_water_level']} см\n" + \
            f"Дорога закрыта с {i[1]['f_closing_date']}\n"
            if i[1]['f_detour'] == 'Да':
                response += "Есть объездная дорога\n"
            else:
                response += "Нет объездной дороги\n"
            
            response += f"{i[1]['oper_mode']}. "
            if i[1]['danger_icon'] == '🟢':
                response += "НЕТ УГРОЗЫ\n\n"
            else:
                response += "\n\n"
    msg_parts = await split_message(response)
    for msg_part in msg_parts:
        await callback.message.answer(text=msg_part)