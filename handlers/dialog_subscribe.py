
import logging
import operator
from typing import Optional
from datetime import datetime as dt
import pandas as pd

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message


from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.kbd import Back, Group, Multiselect, Select, Button
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.media import DynamicMedia

from sqlalchemy import and_, delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Subscriptions, Sub_categories, Users, DFloodKrudor
from database.engine import session_maker

from utils.decline_phrase import decline_phrase



from icecream import ic

class MySG(StatesGroup):
    window1 = State()
    window2 = State()
    window3 = State()


router = Router()

@router.message(CommandStart(), F.chat.type == "private")
async def handle_subscribe(message: Message, session_: AsyncSession, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.window1, mode=StartMode.RESET_STACK)


async def window2_get_data(session_: AsyncSession, dialog_manager: DialogManager, **kwargs):

    user_id = dialog_manager.event.from_user.id

    check_query = select(Subscriptions.category_id).where(
        Subscriptions.user_id == user_id
    )
    check_response = await session_.execute(check_query)
    users_subscriptions = check_response.all()

    users_subscriptions = [i[0] for i in users_subscriptions]

    multiselect = dialog_manager.find("sub")
    
    for category_id in users_subscriptions:
        await multiselect.set_checked(category_id, True)
    
    query = select(
        Sub_categories.category_name, Sub_categories.category_id)
    
    response = await session_.execute(query)
    result = response.all()

    return {"subcategories": result}


async def delete_sub(session_: AsyncSession, user_id, category_id):
    print("delete_sub")
    user_id = int(user_id)
    category_id = int(category_id)
    query = (delete(Subscriptions).where(
        and_(
            Subscriptions.user_id == user_id, Subscriptions.category_id == category_id
        )
    ))
    try:
        await session_.execute(query)
        await session_.commit()
    except Exception as e:
        logging.error(e)


async def add_sub(session_: Optional[AsyncSession], user_id, category_id):
    user_id = int(user_id)
    category_id = int(category_id)
    insert_query = (insert(Subscriptions).values(user_id=user_id, category_id=category_id, date_subscribed = dt.now()))

    try:
        await session_.execute(insert_query)
        await session_.commit()
        print('inserted')
    except Exception as e:
        logging.error(e)


async def button1_clicked(
        callback: CallbackQuery,
        session_: AsyncSession,
        dialog_manager: DialogManager
    ):
    clicked_button = callback.data
    if clicked_button == '1':
        await dialog_manager.switch_to(MySG.window2)
        return
    
    if clicked_button == '2':
        await dialog_manager.switch_to(MySG.window3)
        return
    
    
    if clicked_button == '3':
        flood_districts = dialog_manager.start_data['flood_districts']
        
        
        await callback.message.answer(text=flood_districts)
        
    
    await dialog_manager.next()
    
    



async def button2_clicked(
    callback: CallbackQuery,
    session_: AsyncSession,
    dialog_manager: DialogManager,
    data: Optional[dict],
):
    from database.engine import session_maker
    category_id = callback.data.split(":")[1]
    user_id = callback.from_user.id

    multiselect = dialog_manager.find("sub")
    
    category_id = int(category_id)
    if multiselect.is_checked(category_id):
        await multiselect.set_checked(category_id, True)
        async with session_maker() as session_:

            await delete_sub(session_, user_id=user_id, category_id=category_id)

    if not multiselect.is_checked(category_id):
        await multiselect.set_checked(category_id, False)
        async with session_maker() as session_:
            await add_sub(session_, user_id=user_id, category_id=category_id)


async def button3_clicked(
        callback: CallbackQuery,
        session_: AsyncSession,
        dialog_manager: DialogManager
    ):
    clicked_button = callback.data
    if clicked_button == '3':
        await dialog_manager.switch_to(MySG.window1)
        return

    
    await dialog_manager.next()



async def check_news(callback: CallbackQuery, session: AsyncSession, dialog_manager: DialogManager):
    async with session_maker() as session_:
    
        query = select(DFloodKrudor.district, DFloodKrudor.date_event, DFloodKrudor.type, DFloodKrudor.road, DFloodKrudor.f_location, DFloodKrudor.f_road_l,
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
            
            response += f"{i[1]['danger_icon']} {i[1]['district']} " + \
                        f"{i[1]['date_event']}.\n"
            if i[1]['danger_icon'] == '🔴':
                response += "ПЕРЕЛИВ ДОРОГИ. "

            response += f"{i[1]['type']} \n" +\
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
        
    await callback.message.answer(text=response)
        
    
    
    
    





multi2 = Multiselect(
    Format("✅ {item[0]}"),
    Format("☑️{item[0]}"),
    id="sub",
    item_id_getter=operator.itemgetter(1),
    items="subcategories",
    on_click=button2_clicked,
)



dialog = Dialog(
    Window(
        Format("Добро пожаловать"),
        Button(Const("Выбрать категорию"), id="1", on_click=button1_clicked),
        Button(Const("Помощь"), id="2", on_click=button1_clicked),
        Button(Const("Получить новости"), id="3", on_click=check_news),
        state=MySG.window1),
    
    
    Window(
        Format("Выберите подкатегории для оформления подписки"),
        Group(multi2, width=1),
        Back(text=Const("Главное меню")),
        Button(Const("Помощь"), id="2", on_click=button1_clicked),
        state=MySG.window2,
        getter=window2_get_data, 
    ),
    Window(
        Format("Если нужна помощь то не звоните"),
        Button(Const("К выбору категорий"), id="1", on_click=button1_clicked),
        Button(Const("Главное меню"), id="3", on_click=button3_clicked),
        state=MySG.window3,
    )
    
)