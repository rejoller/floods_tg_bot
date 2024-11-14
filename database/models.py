from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import ForeignKey, String, BIGINT, TIMESTAMP, DateTime, BOOLEAN, FLOAT, INTEGER

class Base(DeclarativeBase):
    pass




class Users(Base):
    __tablename__ = 'tg_bot_users'
    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(255), nullable=True)
    joined_at: Mapped[DateTime] = mapped_column(TIMESTAMP)
    is_admin: Mapped[bool] = mapped_column(BOOLEAN)
    latitude: Mapped[float] = mapped_column(FLOAT, nullable=True)
    longitude: Mapped[float] = mapped_column(FLOAT, nullable=True)
    phone_number: Mapped[str] = mapped_column(String(255), nullable=True)
    
    
class DFloodKrudor(Base):
    __tablename__ = 'd_flood_krudor'
    id_flood: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    date_event: Mapped[DateTime] = mapped_column(TIMESTAMP, nullable=True)
    district: Mapped[str] = mapped_column(String(255), nullable=True)
    road: Mapped[str] = mapped_column(String(255), nullable=True)
    oper_mode: Mapped[str] = mapped_column(String(255), nullable=True)
    type: Mapped[str] = mapped_column(String(255), nullable=True)
    f_closing_date: Mapped[DateTime] = mapped_column(TIMESTAMP, nullable=True)
    f_opening_date: Mapped[DateTime] = mapped_column(TIMESTAMP, nullable=True)
    f_location: Mapped[str] = mapped_column(String(255), nullable=True)
    f_water_level: Mapped[int] = mapped_column(INTEGER, nullable=True)
    f_road_q: Mapped[int] = mapped_column(BIGINT, nullable=True)
    f_road_l: Mapped[int] = mapped_column(BIGINT, nullable=True)
    f_bridge_q: Mapped[int] = mapped_column(BIGINT, nullable=True)
    f_bridge_d: Mapped[int] = mapped_column(BIGINT, nullable=True)
    f_pipes_q: Mapped[int] = mapped_column(BIGINT, nullable=True)
    f_pipes_d: Mapped[int] = mapped_column(BIGINT, nullable=True)
    f_detour: Mapped[int] = mapped_column(String(255), nullable=True)
    f_note: Mapped[str] = mapped_column(String(255), nullable=True)
    

class Sub_categories(Base):
    __tablename__ ='tg_bot_sub_categories'
    category_id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    category_name: Mapped[str] = mapped_column(String(255))
    

class Subscriptions(Base):
    __tablename__ = 'tg_bot_subscriptions'
    subscription_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('tg_bot_users.user_id'))
    category_id: Mapped[int] = mapped_column(INTEGER, ForeignKey('tg_bot_sub_categories.category_id'))
    date_subscribed: Mapped[DateTime] = mapped_column(TIMESTAMP)
    
    






    
    
    
    
    
    
    
    
    
    
    
    
