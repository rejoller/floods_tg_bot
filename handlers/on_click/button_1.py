from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from sqlalchemy.ext.asyncio import AsyncSession

from utils.text.msg_splitter import split_message





async def button1_clicked(
        callback: CallbackQuery,
        session_: AsyncSession,
        dialog_manager: DialogManager
    ):
    from .. import MySG
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