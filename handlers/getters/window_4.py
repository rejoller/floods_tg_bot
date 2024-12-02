from aiogram_dialog import DialogManager

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Municipalities, MunicSubscriptions





async def window4_get_data(session_: AsyncSession, dialog_manager: DialogManager, **kwargs):
        
    query = select(
        Municipalities.caption_full, Municipalities.id_r_omsu)
    response = await session_.execute(query)
    result = response.all()
    user_id = dialog_manager.event.from_user.id
    
    chek_query = select(MunicSubscriptions.municipality_id).where(MunicSubscriptions.user_id == user_id)
    check_response = await session_.execute(chek_query)
    users_subscriptions = check_response.all()
    municipality_ids = [i[0] for i in users_subscriptions]
    query = select(Municipalities.id_r_omsu).where(Municipalities.id_r_omsu.in_(municipality_ids))
    response = await session_.execute(query)
    municipality_ids = response.all()
    municipality_ids = [i[0] for i in municipality_ids]

    multiselect = dialog_manager.find("munsub")
    if dialog_manager.event.data.split("\x1d")[1] == 'noall':
        query = select(Municipalities.id_r_omsu)
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