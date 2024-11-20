from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from sqlalchemy.ext.asyncio import AsyncSession

from utils import add_sub, delete_sub
from typing import Optional





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