import logging
import operator
from typing import Optional, Any
from datetime import datetime as dt
import pandas as pd

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message


from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.kbd import Back, Group, Multiselect, Button
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory

from sqlalchemy import and_, delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import FCategoriesSubscriptions, FCategories, DFloodKrudor, Municipalities, MunicSubscriptions, DFloodAggoAndChs
from database.engine import session_maker

from utils.text.decline_phrase import decline_phrase, choose_plural
from utils.text.msg_splitter import split_message
from icecream import ic


class MySG(StatesGroup):
    window1 = State()
    window2 = State()
    window3 = State()
    window4 = State()


router = Router()

@router.message(CommandStart(), F.chat.type == "private")
async def handle_subscribe(message: Message, session_: AsyncSession, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.window1, mode=StartMode.RESET_STACK)



async def window1_get_data(session_: AsyncSession, dialog_manager: DialogManager, **kwargs):

    user_id = dialog_manager.event.from_user.id
    chek_query = select(MunicSubscriptions.map_id).where(MunicSubscriptions.user_id == user_id)
    check_response = await session_.execute(chek_query)
    users_subscriptions = check_response.all()
    map_ids = [i[0] for i in users_subscriptions]
    
    query = select(Municipalities.municipality_id).where(Municipalities.map_id.in_(map_ids))
    response = await session_.execute(query)
    municipality_ids = response.all()
    municipality_ids = [i[0] for i in municipality_ids]

    multiselect = dialog_manager.find("munsub")
    for municipality_id in municipality_ids:
        await multiselect.set_checked(municipality_id, True)
        
    return {"user_subscriptions": users_subscriptions}





async def window2_get_data(session_: AsyncSession, dialog_manager: DialogManager, **kwargs):

    user_id = dialog_manager.event.from_user.id
    check_query = select(FCategoriesSubscriptions.category_id).where(
        FCategoriesSubscriptions.user_id == user_id
    )
    check_response = await session_.execute(check_query)
    users_subscriptions = check_response.all()
    users_subscriptions = [i[0] for i in users_subscriptions]
    multiselect = dialog_manager.find("sub")
    
    for category_id in users_subscriptions:
        await multiselect.set_checked(category_id, True)

    query = select(
        FCategories.category_name, FCategories.category_id)
    
    response = await session_.execute(query)
    result = response.all()

    return {"subcategories": result}



async def window4_get_data(session_: AsyncSession, dialog_manager: DialogManager, **kwargs):
        
    query = select(
        Municipalities.municipality_name, Municipalities.municipality_id)
    response = await session_.execute(query)
    result = response.all()
    user_id = dialog_manager.event.from_user.id
    
    chek_query = select(MunicSubscriptions.map_id).where(MunicSubscriptions.user_id == user_id)
    check_response = await session_.execute(chek_query)
    users_subscriptions = check_response.all()
    map_ids = [i[0] for i in users_subscriptions]
    query = select(Municipalities.municipality_id).where(Municipalities.map_id.in_(map_ids))
    response = await session_.execute(query)
    municipality_ids = response.all()
    municipality_ids = [i[0] for i in municipality_ids]

    multiselect = dialog_manager.find("munsub")
    if dialog_manager.event.data.split("\x1d")[1] == 'noall':
        query = select(Municipalities.municipality_id)
        response = await session_.execute(query)
        municipality_ids = response.all()
        municipality_ids = [i[0] for i in municipality_ids]
        for municipality_id in municipality_ids:
            if multiselect.is_checked(municipality_id):
                await multiselect.set_checked(municipality_id, False)
                
    if dialog_manager.event.data.split("\x1d")[1] == 'all':
        for municipality_id in municipality_ids:
            if not multiselect.is_checked(municipality_id):
                await multiselect.set_checked(municipality_id, True)
    
    return {"municsubscritions": result}



async def delete_sub(session_: AsyncSession, user_id, category_id):
    user_id = int(user_id)
    category_id = int(category_id)
    query = (delete(FCategoriesSubscriptions).where(
        and_(
            FCategoriesSubscriptions.user_id == user_id, FCategoriesSubscriptions.category_id == category_id
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
    insert_query = (insert(FCategoriesSubscriptions).values(user_id=user_id, category_id=category_id, date_subscribed = dt.now()))
    try:
        await session_.execute(insert_query)
        await session_.commit()
    except Exception as e:
        logging.error(e)
        
        
        
        
async def delete_munsub(session_: AsyncSession, user_id, municipality_id):
    user_id = int(user_id)
    check_query = select(Municipalities.map_id).where(Municipalities.municipality_id == municipality_id)
    response = await session_.execute(check_query)
    map_id = response.fetchone()[0]
    query = (delete(MunicSubscriptions).where(
        and_(
            MunicSubscriptions.user_id == user_id, MunicSubscriptions.map_id == map_id
        )
    ))
    try:
        await session_.execute(query)
        await session_.commit()
    except Exception as e:
        logging.error(e)        
        
        
        
async def add_munsub(session_: Optional[AsyncSession], user_id, municipality_id):
    user_id = int(user_id)
    check_query = select(Municipalities.map_id).where(Municipalities.municipality_id == municipality_id)
    response = await session_.execute(check_query)
    map_id = response.fetchone()[0]
    
    query = select(MunicSubscriptions.map_id).where(and_(MunicSubscriptions.user_id == user_id, (MunicSubscriptions.map_id ==map_id)))
    result = await session_.execute(query)
    result = result.all()
    if not result:
        insert_query = (insert(MunicSubscriptions).values(user_id=user_id, map_id=map_id, date_subscribed = dt.now())).on_conflict_do_nothing()

        try:
            await session_.execute(insert_query)
            await session_.commit()
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
    
    if clicked_button == '4':
        await dialog_manager.switch_to(MySG.window4)
        return
    
    if clicked_button == '3':
        flood_districts = dialog_manager.start_data['flood_districts']
        response = await split_message(flood_districts)
        for msg_part in response:
            await callback.message.answer(text=msg_part)
    
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
    
    
    
    
async def button4_clicked(
    callback: CallbackQuery, session_: AsyncSession, dialog_manager: DialogManager, data_: Optional[Any]=None):
    from database.engine import session_maker
    from bot import bot
    user_id = callback.from_user.id
    multiselect = dialog_manager.find("munsub")
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    
    
    allmunic_query = select(
        Municipalities.map_id, Municipalities.municipality_id
    ).order_by(Municipalities.municipality_name)
    async with session_maker() as session_:
        result = await session_.execute(allmunic_query)
    response = result.all()
    map_ids = [item[0] for item in response]
    
    
    query = select(MunicSubscriptions.map_id, MunicSubscriptions.user_id).where(MunicSubscriptions.user_id == user_id)
    async with session_maker() as session_:
        result = await session_.execute(query)
    user_subs = result.all()
    user_subs = [item[0] for item in user_subs]
    
    query = select(Municipalities.municipality_id).where(Municipalities.map_id.in_(user_subs))
    async with session_maker() as session_:
        result = await session_.execute(query)
    response = result.all()
    
    if callback.data == 'all':
        to_subscribe = list(set(map_ids) - set(user_subs))
        for map_id in to_subscribe:
            async with session_maker() as session_:
                query = (insert(MunicSubscriptions)
                        .values(user_id=user_id, map_id=map_id, date_subscribed = dt.now())).on_conflict_do_nothing()
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
    msg_parts = await split_message(response)
    for msg_part in msg_parts:
        await callback.message.answer(text=msg_part)
        


# sd_qfh_result - H  
# ap_epp_result -    AS
# ap_efz_result -    AX
# ap_epp_wta_people - AT
# ap_efz_wta_people - AY


# 
async def check_news_ago(callback: CallbackQuery, session: AsyncSession, dialog_manager: DialogManager):
    async with session_maker() as session_:
        query = select(DFloodAggoAndChs.municipality, DFloodAggoAndChs.date_incident, DFloodAggoAndChs.operating_mode,DFloodAggoAndChs.type_flood, DFloodAggoAndChs.settlement,
                       DFloodAggoAndChs.omd_wlwb_cwl, DFloodAggoAndChs.omd_wlwb_cl, DFloodAggoAndChs.sd_qfh_result, DFloodAggoAndChs.sd_qft_result, DFloodAggoAndChs.sd_qft_estate_territory, DFloodAggoAndChs.ap_qvfz_result,
                       DFloodAggoAndChs.ap_qvfz_children, DFloodAggoAndChs.ap_epp_result, DFloodAggoAndChs.ap_efz_result, DFloodAggoAndChs.ap_epp_wta_people, DFloodAggoAndChs.ap_efz_wta_people)
        
        response = await session_.execute(query)
        result = response.all()
        
        df = pd.DataFrame(result)
        df['date_incident'] = df['date_incident'].apply(lambda x: x.strftime('%d.%m.%Y') if pd.notnull(x) else x)
        df['danger_icon'] = df.apply(lambda row: '🟢' if row['operating_mode'] == 'Повседневная деятельность' else '🔴', axis=1)
        
        response = ''
        for i in df.iterrows():
            
            response += f"{i[1]['danger_icon']} {i[1]['municipality']}\n"
            response += f"{i[1]['date_incident']}. {i[1]['type_flood']}.\n"
            response += f"н/п {i[1]['settlement']}\n"
            evacuated_people = i[1]['ap_epp_result'] + i[1]['ap_efz_result']
            temp_holded = i[1]['ap_efz_wta_people'] + i[1]['ap_epp_wta_people']
            difference = i[1]['omd_wlwb_cwl'] - i[1]['omd_wlwb_cl']
            
            if difference > 0:
                response += f"Текущий уровень воды {i[1]['omd_wlwb_cwl']} см (критический {i[1]['omd_wlwb_cl']} см + {difference} см)\n"
            if difference < 0:
                response += f"Текущий уровень воды {i[1]['omd_wlwb_cwl']} см (критический {i[1]['omd_wlwb_cl']} см - {abs(difference)} см)\n"
            if difference == 0:
                response += f"Текущий уровень воды {i[1]['omd_wlwb_cwl']} см (критический {i[1]['omd_wlwb_cl']} см)\n"

            home_form = await choose_plural(i[1]['sd_qfh_result'], ["дом", "дома", "домов"])
            home_form_1 = await choose_plural(i[1]['sd_qfh_result'], ['Затоплен', 'Затоплены', 'Затоплено'])
            
            affected_form = await choose_plural(i[1]['ap_qvfz_result'], ['человек', 'человека', 'человек'])
            teritory_form = await choose_plural(i[1]['sd_qfh_result'], ['территория', 'территории', 'территорий'])
            evacuated_people_form = await choose_plural(evacuated_people, ['человек', 'человека', 'человек'])
            temp_holded_form = await choose_plural(temp_holded, ['человек', 'человека', 'человек'])
            
            affected_form_1 = await choose_plural(i[1]['ap_qvfz_children'], ['Пострадал','Пострадали','Пострадало'])
            evacuated_people_form_1 = await choose_plural(evacuated_people, ['Эвакуирован','Эвакуированы','Эвакуировано'])
            temp_holded_1 = await choose_plural(temp_holded, ['Размещен','Размещены','Размещено'])
            
            
            
            response += f"{home_form_1} всего {i[1]['sd_qfh_result']}  {home_form}"
            if i[1]['sd_qfh_result'] > 0:
                response += f", всего {i[1]['sd_qfh_result']} {teritory_form}\n"
            else :
                response += "\n"
                
            response += f"{affected_form_1} {i[1]['ap_qvfz_result']} {affected_form}, из них {i[1]['ap_qvfz_children']} детей\n"
            response += f"{evacuated_people_form_1} {evacuated_people} {evacuated_people_form}\n"
            response += f"{temp_holded_1} в пунктах временного содержания {temp_holded} {temp_holded_form}\n\n"
            
        
        msg_parts = await split_message(response)
        for msg_part in msg_parts:
            await callback.message.answer(text=msg_part)
        
                
                
                

multi2 = Multiselect(
    Format("✅ {item[0]}"),
    Format("☑️{item[0]}"),
    id="sub",
    item_id_getter=operator.itemgetter(1),
    items="subcategories",
    on_click=button2_clicked,
)



multi4 = Multiselect(
    Format("✅ {item[0]}"),
    Format("☑️{item[0]}"),
    id="munsub",
    item_id_getter=operator.itemgetter(1),
    items="municsubscritions",
    on_click=button4_clicked
)



dialog = Dialog(
    Window(
        Format("Добро пожаловать"),
        Button(Const("Выбрать категорию"), id="1", on_click=button1_clicked),
        Button(Const("Выбрать муниципальные образования"), id="4", on_click=button1_clicked),
        Button(Const("🆘Помощь"), id="2", on_click=button1_clicked),
        Button(Const("🗞️Получить новости"), id="3", on_click=check_news),
        Button(Const("Получить новости по подтоплениям ГО и ЧС"), id="5", on_click=check_news_ago),
        state=MySG.window1,
        getter=window1_get_data),
    
    
    Window(
        Format("Выберите подкатегории для оформления подписки"),
        Group(multi2, width=1),
        Back(text=Const("Главное меню")),
        Button(Const("🆘Помощь"), id="2", on_click=button1_clicked),
        state=MySG.window2,
        getter=window2_get_data, 
    ),
    Window(
        Format("Если нужна помощь то не звоните"),
        Button(Const("К выбору категорий"), id="1", on_click=button1_clicked),
        Button(Const("Главное меню"), id="3", on_click=button3_clicked),
        state=MySG.window3,
    ),
    Window(
        Format("Муниципальные образования для выбора"),
        Group(Button(Const("✅подписаться на все"), id="all", on_click=button4_clicked),Button(Const("❌отписаться от всего"), id="noall", on_click=button4_clicked), width=2),
        Group(multi4, width=1),
        Button(Const("⏪Назад"), id="3", on_click=button3_clicked),
        Button(Const("🆘Помощь"), id="2", on_click=button1_clicked),
        state=MySG.window4,
        getter=window4_get_data,
        markup_factory=ReplyKeyboardFactory(selective=True, resize_keyboard=True, input_field_placeholder = Const(text= 'Выберите муниципальное образование')),
    ),
    
)