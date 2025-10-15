import asyncio
from datetime import timedelta

from sqlalchemy import text

from app.db.session import session_factory
from app.models import TransactionOrm
from app.models import CategoryOrm
from app.schemas.analytics import AnalyticsGetOverview



async def get_overview(data: AnalyticsGetOverview, user_id: int): # создать столбец с фактическим transaction_type
    async with session_factory() as session:
        with open("sql/overview_summary.sql", "r") as sql_file:
            sql_code = sql_file.read()
        summary = await session.execute(text(sql_code), {"user_id": user_id,
                                                         "date_from": data.date_from,
                                                         "date_to": data.date_to + timedelta(days=1),
                                                         "list_account_id": [72, 73, 74, 75]})

        with open("sql/overview_top_categories.sql", "r") as sql_file:
            sql_code = sql_file.read()
        top_categories = await session.execute(text(sql_code), {"user_id": user_id,
                                                                "date_from": data.date_from,
                                                                "date_to": data.date_to + timedelta(days=1),
                                                                "list_account_id": [72, 73, 74, 75]})
        return summary.mappings().first(), top_categories.mappings().all(), {"data_from": data.date_from, "data_to": data.date_to}