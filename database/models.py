from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import ForeignKey, String, BIGINT, TIMESTAMP, DateTime, BOOLEAN, FLOAT, INTEGER

class Base(DeclarativeBase):
    pass




class Users(Base):
    __table_args__ = {'schema': 'flood'}
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
    __table_args__ = {'schema': 'flood'}
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
    
    
    

class DFloodAggoAndChs(Base):
    __table_args__ = {'schema': 'flood'}
    __tablename__ = 'd_flood_aggoandchs'

    id_d_flood_aggoandchs: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    date_create: Mapped[DateTime] = mapped_column(TIMESTAMP)
    date_incident: Mapped[DateTime] = mapped_column(TIMESTAMP)
    municipality: Mapped[str] = mapped_column(String(225), nullable=True)
    settlement: Mapped[str] = mapped_column(String(225), nullable=True)
    operating_mode: Mapped[str] = mapped_column(String(225), nullable=True)
    period_year: Mapped[str] = mapped_column(String(225), nullable=True)
    type_flood: Mapped[str] = mapped_column(String(225), nullable=True)
    sd_object_gardening: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_qfh_result: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_qfh_apartment: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_qfh_residential: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_qfh_gardening: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_qft_result: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_qft_house_territory: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_qft_estate_territory: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_qfszno_result: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_qfszno_hi_result: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_qfszno_hi_noctidial: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_qfszno_ei_result: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_qfszno_ei_noctidial: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_qfszno_acsi: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_qfhif_result: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_qfhif_chf: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_qfhif_eptpp: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_qfhif_ehf: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_qfoe_result: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_qfoe_tlep: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_qfoe_ts: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_qfojkh_result: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_qfojkh_ws: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_qfojkh_wd: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_qfojkh_hs: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_qfojkh_gs: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_sfosh_result: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_sfosh_aal: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_psd: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_asd: Mapped[int] = mapped_column(INTEGER, nullable=True)
    sd_cp: Mapped[int] = mapped_column(INTEGER, nullable=True)
    ap_qvfz_result: Mapped[int] = mapped_column(INTEGER, nullable=True)
    ap_qvfz_children: Mapped[int] = mapped_column(INTEGER, nullable=True)
    ap_qvfz_disabled: Mapped[int] = mapped_column(INTEGER, nullable=True)
    ap_qvfz_lcd: Mapped[int] = mapped_column(INTEGER, nullable=True)
    ap_qvfz_lep: Mapped[int] = mapped_column(INTEGER, nullable=True)
    ap_qvfz_shh: Mapped[int] = mapped_column(INTEGER, nullable=True)
    ap_qvfz_died: Mapped[int] = mapped_column(INTEGER, nullable=True)
    ap_epp_result: Mapped[int] = mapped_column(INTEGER, nullable=True)
    ap_epp_wta_people: Mapped[int] = mapped_column(INTEGER, nullable=True)
    ap_epp_wta_children: Mapped[int] = mapped_column(INTEGER, nullable=True)
    ap_epp_wr_people: Mapped[int] = mapped_column(INTEGER, nullable=True)
    ap_epp_wr_children: Mapped[int] = mapped_column(INTEGER, nullable=True)
    ap_efz_result: Mapped[int] = mapped_column(INTEGER, nullable=True)
    ap_efz_wta_people: Mapped[int] = mapped_column(INTEGER, nullable=True)
    ap_efz_wta_children: Mapped[int] = mapped_column(INTEGER, nullable=True)
    ap_efz_wr_people: Mapped[int] = mapped_column(INTEGER, nullable=True)
    ap_efz_wr_children: Mapped[int] = mapped_column(INTEGER, nullable=True)
    iap_112: Mapped[int] = mapped_column(INTEGER, nullable=True)
    iap_sms: Mapped[int] = mapped_column(INTEGER, nullable=True)
    iap_ps: Mapped[int] = mapped_column(INTEGER, nullable=True)
    iap_pws: Mapped[int] = mapped_column(INTEGER, nullable=True)
    omd_wlwb_cwl: Mapped[int] = mapped_column(INTEGER, nullable=True)
    omd_wlwb_cl: Mapped[int] = mapped_column(INTEGER, nullable=True)
    omd_wlwb_th: Mapped[str] = mapped_column(String(225), nullable=True)
    omd_og_tn: Mapped[int] = mapped_column(INTEGER, nullable=True)
    pcom_cm_type: Mapped[str] = mapped_column(String(225), nullable=True)
    pcom_cm_lldo: Mapped[int] = mapped_column(INTEGER, nullable=True)
    pcom_cm_tpu: Mapped[str] = mapped_column(String(225), nullable=True)
    pcom_cm_qmu: Mapped[int] = mapped_column(INTEGER, nullable=True)
    pcom_fsm: Mapped[int] = mapped_column(INTEGER, nullable=True)
    fmier_f_no: Mapped[str] = mapped_column(String(225), nullable=True)
    fmier_f_ao: Mapped[str] = mapped_column(String(225), nullable=True)
    fmier_f_person: Mapped[int] = mapped_column(INTEGER, nullable=True)
    fmier_f_ue: Mapped[int] = mapped_column(INTEGER, nullable=True)
    fmier_f_a: Mapped[int] = mapped_column(INTEGER, nullable=True)
    fmier_r_person: Mapped[int] = mapped_column(INTEGER, nullable=True)
    fmier_r_ue: Mapped[int] = mapped_column(INTEGER, nullable=True)
    fmier_r_a: Mapped[int] = mapped_column(INTEGER, nullable=True)
    fmier_m_person: Mapped[int] = mapped_column(INTEGER, nullable=True)
    fmier_m_ue: Mapped[int] = mapped_column(INTEGER, nullable=True)
    fmier_m_a: Mapped[int] = mapped_column(INTEGER, nullable=True)
    fmier_sco_person: Mapped[int] = mapped_column(INTEGER, nullable=True)
    fmier_sco_ue: Mapped[int] = mapped_column(INTEGER, nullable=True)
    fmier_sco_a: Mapped[int] = mapped_column(INTEGER, nullable=True)




    

class FCategories(Base):
    __table_args__ = {'schema': 'flood'}
    __tablename__ ='tg_bot_f_categories'
    category_id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    category_name: Mapped[str] = mapped_column(String(255))
    

class FCategoriesSubscriptions(Base):
    __table_args__ = {'schema': 'flood'}
    __tablename__ = 'tg_bot_f_categories_subscriptions'
    subscription_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('tg_bot_users.user_id'))
    category_id: Mapped[int] = mapped_column(INTEGER, ForeignKey('tg_bot_f_categories.category_id'))
    date_subscribed: Mapped[DateTime] = mapped_column(TIMESTAMP)
    
    
    
class Municipalities(Base):
    __table_args__ = {'schema': 'flood'}
    __tablename__ = 'municipalities'
    municipality_id: Mapped[int] = mapped_column(INTEGER, autoincrement=True)
    map_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    municipality_name: Mapped[str] = mapped_column(String(225))
    
    
    
class MunicSubscriptions(Base):
    __table_args__ = {'schema': 'flood'}
    __tablename__ = 'tg_bot_municip_subscriptions'
    subscription_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('tg_bot_users.user_id'))
    map_id: Mapped[str] = mapped_column(String(10), ForeignKey('municipalities.map_id'))
    date_subscribed: Mapped[DateTime] = mapped_column(TIMESTAMP)
    






    
    
    
    
    
    
    
    
    
    
    
    
