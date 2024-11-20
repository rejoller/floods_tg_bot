from aiogram_dialog import DialogManager

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from database.models import FCategoriesSubscriptions, FCategories



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