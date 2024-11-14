from aiogram import Router
from aiogram_dialog import setup_dialogs



def setup_routers():
    from handlers import start, dialog_subscribe
    from handlers.dialog_subscribe import dialog
    
    router = Router()

    # router.include_router(start.router)
    router.include_router(dialog_subscribe.router)
    router.include_router(dialog)
    
    setup_dialogs(router)
    
    return router