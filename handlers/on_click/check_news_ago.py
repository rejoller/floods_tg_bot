from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import pandas as pd
from utils import split_message, choose_plural

from database.engine import session_maker
from database.models import DFloodAggoAndChs, Municipalities, MunicSubscriptions
from icecream import ic


async def check_news_ago(
    callback: CallbackQuery, session: AsyncSession, dialog_manager: DialogManager
):
    async with session_maker() as session_:
        user_id = callback.from_user.id
        query = select(
            DFloodAggoAndChs.municipality,
            DFloodAggoAndChs.date_incident,
            DFloodAggoAndChs.operating_mode,
            DFloodAggoAndChs.type_flood,
            DFloodAggoAndChs.settlement,
            DFloodAggoAndChs.omd_wlwb_cwl,
            DFloodAggoAndChs.omd_wlwb_cl,
            DFloodAggoAndChs.sd_qfh_result,
            DFloodAggoAndChs.sd_qft_result,
            DFloodAggoAndChs.sd_qft_estate_territory,
            DFloodAggoAndChs.ap_qvfz_result,
            DFloodAggoAndChs.ap_qvfz_children,
            DFloodAggoAndChs.ap_epp_result,
            DFloodAggoAndChs.ap_efz_result,
            DFloodAggoAndChs.ap_epp_wta_people,
            DFloodAggoAndChs.ap_efz_wta_people,
        )

        response = await session_.execute(query)
        result = response.all()

        query_users_subs = (
            select(Municipalities.caption_full)
            .join(
                MunicSubscriptions,
                Municipalities.map_id == MunicSubscriptions.municipality_id,
            )
            .where(MunicSubscriptions.user_id == user_id)
        )
        response = await session_.execute(query_users_subs)
        response = response.all()
        users_subs = [i[0] for i in response]

        df = pd.DataFrame(result)

        df = df.query("municipality in @users_subs")
        ic(df.empty)
        if df.empty:
            await callback.answer("Для вас сейчас нет новостей😳", show_alert=True)
            return

        df["date_incident"] = df["date_incident"].apply(
            lambda x: x.strftime("%d.%m.%Y") if pd.notnull(x) else x
        )
        df["danger_icon"] = df.apply(
            lambda row: "🟢"
            if row["operating_mode"] == "Повседневная деятельность"
            else "🔴",
            axis=1,
        )

        response = ""
        for i in df.iterrows():
            response += f"{i[1]['danger_icon']} {i[1]['municipality']}\n"
            response += f"{i[1]['date_incident']}. {i[1]['type_flood']}.\n"
            response += f"н/п {i[1]['settlement']}\n"
            evacuated_people = i[1]["ap_epp_result"] + i[1]["ap_efz_result"]
            temp_holded = i[1]["ap_efz_wta_people"] + i[1]["ap_epp_wta_people"]
            difference = i[1]["omd_wlwb_cwl"] - i[1]["omd_wlwb_cl"]

            if difference > 0:
                response += f"Текущий уровень воды {i[1]['omd_wlwb_cwl']} см (критический {i[1]['omd_wlwb_cl']} см + {difference} см)\n"
            if difference < 0:
                response += f"Текущий уровень воды {i[1]['omd_wlwb_cwl']} см (критический {i[1]['omd_wlwb_cl']} см - {abs(difference)} см)\n"
            if difference == 0:
                response += f"Текущий уровень воды {i[1]['omd_wlwb_cwl']} см (критический {i[1]['omd_wlwb_cl']} см)\n"

            home_form = await choose_plural(
                i[1]["sd_qfh_result"], ["дом", "дома", "домов"]
            )
            home_form_1 = await choose_plural(
                i[1]["sd_qfh_result"], ["Затоплен", "Затоплены", "Затоплено"]
            )

            affected_form = await choose_plural(
                i[1]["ap_qvfz_result"], ["человек", "человека", "человек"]
            )
            teritory_form = await choose_plural(
                i[1]["sd_qfh_result"], ["территория", "территории", "территорий"]
            )
            evacuated_people_form = await choose_plural(
                evacuated_people, ["человек", "человека", "человек"]
            )
            temp_holded_form = await choose_plural(
                temp_holded, ["человек", "человека", "человек"]
            )

            affected_form_1 = await choose_plural(
                i[1]["ap_qvfz_children"], ["Пострадал", "Пострадали", "Пострадало"]
            )
            evacuated_people_form_1 = await choose_plural(
                evacuated_people, ["Эвакуирован", "Эвакуированы", "Эвакуировано"]
            )
            temp_holded_1 = await choose_plural(
                temp_holded, ["Размещен", "Размещены", "Размещено"]
            )

            response += f"{home_form_1} всего {i[1]['sd_qfh_result']}  {home_form}"
            if i[1]["sd_qfh_result"] > 0:
                response += f", всего {i[1]['sd_qfh_result']} {teritory_form}\n"
            else:
                response += "\n"

            response += f"{affected_form_1} {i[1]['ap_qvfz_result']} {affected_form}, из них {i[1]['ap_qvfz_children']} детей\n"
            response += f"{evacuated_people_form_1} {evacuated_people} {evacuated_people_form}\n"
            response += f"{temp_holded_1} в пунктах временного содержания {temp_holded} {temp_holded_form}\n\n"

        msg_parts = await split_message(response)
        for msg_part in msg_parts:
            await callback.message.answer(text=msg_part)
