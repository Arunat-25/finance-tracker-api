import asyncio
from datetime import timedelta

from sqlalchemy import text

from app.db.session import session_factory
from app.models import TransactionOrm
from app.models import CategoryOrm
from app.schemas.analytics import AnalyticsGetOverview, AnalyticsOverviewSummaryResponse, \
    AnalyticsOverviewTopCategories, CategorySummary, AnalyticsOverviewPeriodResponse, AnalyticsOverviewResponse


async def get_overview_data(data: AnalyticsGetOverview, user_id: int):
    async with session_factory() as session:
        params = {
            "user_id": user_id,
            "date_from": data.date_from,
            "date_to": data.date_to + timedelta(days=1),
            "list_account_id": data.list_account_id
        }

        with open("sql/overview_summary.sql", "r") as sql_file:
            sql_code = sql_file.read()
        result_summary = await session.execute(text(sql_code), params)
        dict_summary = result_summary.mappings().first() or {}

        with open("sql/overview_top_categories.sql", "r") as sql_file:
            sql_code = sql_file.read()
        result_top_categories = await session.execute(text(sql_code), params)
        dict_top_categories = result_top_categories.mappings().all() or [{},{}]

        summary = AnalyticsOverviewSummaryResponse(
            total_income=dict_summary.get("total_income", 0),
            total_expense=dict_summary.get("total_expense", 0),
            net_balance=dict_summary.get("net_balance", 0),
            transaction_income_count=dict_summary.get("transaction_income_count", 0),
            transaction_expense_count=dict_summary.get("transaction_expense_count", 0),
            transfer_income_count=dict_summary.get("transfer_income_count", 0),
            transfer_expense_count=dict_summary.get("transfer_expense_count", 0),
            transaction_count=dict_summary.get("transaction_count", 0)
        )

        top_categories = AnalyticsOverviewTopCategories(
            income = CategorySummary(
                title=dict_top_categories[1].get("title", ""),
                total=dict_top_categories[1].get("total", 0),
                percentage=round(dict_top_categories[1].get("total", 0)*100/summary.total_income, 2)
            ),
            expense = CategorySummary(
                title=dict_top_categories[0].get("title", ""),
                total=dict_top_categories[0].get("total", 0),
                percentage=round(dict_top_categories[0].get("total", 0)*100/summary.total_expense, 2)
            )
        )
        period = AnalyticsOverviewPeriodResponse(
            date_from=data.date_from,
            date_to=data.date_to
        )
        response = AnalyticsOverviewResponse(summary=summary, top_categories=top_categories, period=period)
        return response