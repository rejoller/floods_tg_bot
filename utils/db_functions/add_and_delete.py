from typing import Optional
import logging
from datetime import datetime as dt

from sqlalchemy import and_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert


from database.models import FCategoriesSubscriptions, Municipalities, MunicSubscriptions


async def delete_sub(session_: AsyncSession, user_id, category_id):
    user_id = int(user_id)
    category_id = int(category_id)
    query = delete(FCategoriesSubscriptions).where(
        and_(
            FCategoriesSubscriptions.user_id == user_id,
            FCategoriesSubscriptions.category_id == category_id,
        )
    )
    try:
        await session_.execute(query)
        await session_.commit()
    except Exception as e:
        logging.error(e)


async def add_sub(session_: Optional[AsyncSession], user_id, category_id):
    user_id = int(user_id)
    category_id = int(category_id)
    insert_query = insert(FCategoriesSubscriptions).values(
        user_id=user_id, category_id=category_id, date_subscribed=dt.now()
    )
    try:
        await session_.execute(insert_query)
        await session_.commit()
    except Exception as e:
        logging.error(e)


async def delete_munsub(session_: AsyncSession, user_id, municipality_id):
    query = delete(MunicSubscriptions).where(
        and_(
            MunicSubscriptions.user_id == user_id,
            MunicSubscriptions.municipality_id == municipality_id,
        )
    )
    try:
        await session_.execute(query)
        await session_.commit()
    except Exception as e:
        logging.error(e)


async def add_munsub(session_: Optional[AsyncSession], user_id, municipality_id):
    query = select(MunicSubscriptions.municipality_id).where(
        and_(
            MunicSubscriptions.user_id == user_id,
            (MunicSubscriptions.municipality_id == municipality_id),
        )
    )
    result = await session_.execute(query)
    result = result.all()
    if not result:
        insert_query = (
            insert(MunicSubscriptions).values(
                user_id=user_id, municipality_id=municipality_id, date_subscribed=dt.now()
            )
        ).on_conflict_do_nothing()

        try:
            await session_.execute(insert_query)
            await session_.commit()
        except Exception as e:
            logging.error(e)
