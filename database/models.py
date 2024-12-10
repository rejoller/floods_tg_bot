from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import ForeignKey, String, BIGINT, TIMESTAMP, DateTime, BOOLEAN, FLOAT, INTEGER

class Base(DeclarativeBase):
    pass





    
    
class DFloodKrudor(Base):
    __table_args__ = {'schema': 'flood'}
    __tablename__ = 'd_flood_krudor'
    id_flood: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    date_event: Mapped[DateTime] = mapped_column(TIMESTAMP, nullable=True)
    municipality: Mapped[str] = mapped_column(String(255), nullable=True)
    road: Mapped[str] = mapped_column(String(255), nullable=True)
    oper_mode: Mapped[str] = mapped_column(String(255), nullable=True)
    type_flood: Mapped[str] = mapped_column(String(255), nullable=True)
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
    date_create: Mapped[DateTime] = mapped_column(TIMESTAMP)
    
    
    

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
    __tablename__ ='r_tg_bot_f_category'
    category_id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    caption: Mapped[str] = mapped_column(String(255))
    
    
class Municipalities(Base):
    __table_args__ = {'schema': 'shared'}
    __tablename__ = 'r_omsu'
    num: Mapped[int] = mapped_column(INTEGER, nullable=True)
    map_id: Mapped[str] = mapped_column(String(50), nullable=True)
    user_id: Mapped[str] = mapped_column(String(50), nullable=True)
    caption_full: Mapped[str] = mapped_column(String(50), nullable=True)
    caption_short: Mapped[str] = mapped_column(String(50), nullable=True)
    region_group: Mapped[str] = mapped_column(String(50), nullable=True)
    omsu_type: Mapped[str] = mapped_column(String(50), nullable=True)
    onf: Mapped[str] = mapped_column(String(50), nullable=True)
    onf_short: Mapped[str] = mapped_column(String(50), nullable=True)
    caption_ano_dialog: Mapped[str] = mapped_column(String(50), nullable=True)
    admin_caption: Mapped[str] = mapped_column(String(255), nullable=True)
    admin_caption_short: Mapped[str] = mapped_column(String(50), nullable=True)
    admin_region: Mapped[str] = mapped_column(String(255), nullable=True)
    head_post: Mapped[str] = mapped_column(String(255), nullable=True)
    head_fio: Mapped[str] = mapped_column(String(255), nullable=True)
    omsu: Mapped[str] = mapped_column(String(255), nullable=True)
    id_r_omsu: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    date_ins: Mapped[DateTime] = mapped_column(TIMESTAMP)
    date_upd: Mapped[DateTime] = mapped_column(TIMESTAMP)



    
    
class FCategoriesSubscriptions(Base):
    __table_args__ = {'schema': 'flood'}
    __tablename__ = 'd_tg_bot_f_category_subscription'
    subscription_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('flood.d_tg_bot_users.user_id'))
    category_id: Mapped[int] = mapped_column(INTEGER, ForeignKey('flood.r_tg_bot_f_category.category_id'))
    date_subscribed: Mapped[DateTime] = mapped_column(TIMESTAMP)    
    
    
    
    
    
class MunicSubscriptions(Base):
    __table_args__ = {'schema': 'flood'}
    __tablename__ = 'd_tg_bot_f_municip_subscription'
    subscription_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('flood.d_tg_bot_user.user_id'))
    municipality_id: Mapped[int] = mapped_column(INTEGER, ForeignKey('shared.r_omsu.id_r_omsu'))
    date_subscribed: Mapped[DateTime] = mapped_column(TIMESTAMP)
    
    
    
    
    
    
class Users(Base):
    __table_args__ = {'schema': 'flood'}
    __tablename__ = 'd_tg_bot_user'
    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(255), nullable=True)
    joined_at: Mapped[DateTime] = mapped_column(TIMESTAMP)
    is_admin: Mapped[bool] = mapped_column(BOOLEAN)
    latitude: Mapped[float] = mapped_column(FLOAT, nullable=True)
    longitude: Mapped[float] = mapped_column(FLOAT, nullable=True)
    phone_number: Mapped[str] = mapped_column(String(255), nullable=True)






    
    
    
    
    
    
    
    
    
    
    
    
