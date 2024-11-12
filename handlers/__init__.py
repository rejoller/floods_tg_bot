from aiogram import Router



def setup_routers():
    from handlers import start
    
    router = Router()
    router.include_router(start.router)
    
    return router