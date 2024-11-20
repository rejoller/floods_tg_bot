import operator

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.kbd import Back, Group, Multiselect, Button
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory

from sqlalchemy.ext.asyncio import AsyncSession

from handlers import (button1_clicked, button2_clicked, button3_clicked, check_news,
                    check_news_ago, button4_clicked, window1_get_data, window2_get_data, window4_get_data)


from . import MySG




router = Router()

@router.message(CommandStart(), F.chat.type == "private")
async def handle_subscribe(message: Message, session_: AsyncSession, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.window1, mode=StartMode.RESET_STACK)

        
                        
                

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
        Group(Button(Const("✅подписаться на все"), id="all", on_click=button4_clicked),Button(Const("❌отписаться от всего"),
                                                                                              id="noall", on_click=button4_clicked), width=2),
        Group(multi4, width=1),
        Button(Const("⏪Назад"), id="3", on_click=button3_clicked),
        Button(Const("🆘Помощь"), id="2", on_click=button1_clicked),
        state=MySG.window4,
        getter=window4_get_data,
        markup_factory=ReplyKeyboardFactory(selective=True, resize_keyboard=True, input_field_placeholder = Const(text= 'Выберите муниципальное образование')),
    ),
    
)