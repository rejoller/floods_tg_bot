from aiogram import Router
from aiogram_dialog import setup_dialogs

from .getters.window_1 import window1_get_data
from .getters.window_2 import window2_get_data
from .getters.window_4 import window4_get_data

from .on_click.button_1 import button1_clicked
from .on_click.button_2 import button2_clicked
from .on_click.button_3 import button3_clicked
from .on_click.button_4 import button4_clicked

from .on_click.check_news import check_news
from .on_click.check_news_ago import check_news_ago

from aiogram.filters.state import State, StatesGroup


class MySG(StatesGroup):
    window1 = State()
    window2 = State()
    window3 = State()
    window4 = State()

def setup_routers():
    from handlers import dialog_subscribe
    from handlers.dialog_subscribe import dialog
    
    router = Router()

    router.include_router(dialog_subscribe.router)
    router.include_router(dialog)
    
    setup_dialogs(router)
    
    return router