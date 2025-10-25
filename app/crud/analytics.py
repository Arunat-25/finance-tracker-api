import asyncio, aiofiles

from datetime import timedelta
from decimal import Decimal

from sqlalchemy import text

import app.enum.currency
from app.currency import get_rates
from app.db.session import session_factory
from app.models import TransactionOrm
from app.models import CategoryOrm
from app.schemas.analytics import AnalyticsOverviewRequest, AnalyticsOverviewSummaryResponse, \
    AnalyticsOverviewTopCategoriesResponse, CategorySummary, AnalyticsOverviewPeriodResponse, AnalyticsOverviewResponse, \
    AnalyticsExpensesByCategoryRequest, AnalyticsExpensesByCategoryResponse, AnalyticsIncomesByCategoryRequest
from app.sql.get_sql_code_from_file import get_sql_code


async def get_overview_data(data: AnalyticsOverviewRequest, user_id: int):
    async with session_factory() as session:
        params = {
            "user_id": user_id,
            "date_from": data.date_from,
            "date_to": data.date_to + timedelta(days=1),
            "list_account_id": data.list_account_id
        }

        sql_code_summary = await get_sql_code("sql/overview_summary.sql")
        result_summary = await session.execute(text(sql_code_summary), params)
        dict_summary = result_summary.mappings().first() or {}

        sql_code_top_categories = await get_sql_code("sql/overview_top_categories.sql")
        result_top_categories = await session.execute(text(sql_code_top_categories), params)
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

        top_income_category_total = dict_top_categories[1].get("total", 0)
        top_expense_category_total = dict_top_categories[0].get("total", 0)
        top_categories = AnalyticsOverviewTopCategoriesResponse(
            income = CategorySummary(
                title=dict_top_categories[1].get("title", ""),
                total=dict_top_categories[1].get("total", 0),
                percentage=round(top_income_category_total*100/summary.total_income, 2) if summary.total_income > 0
                else 0
            ),
            expense = CategorySummary(
                title=dict_top_categories[0].get("title", ""),
                total=dict_top_categories[0].get("total", 0),
                percentage=round(top_expense_category_total*100/summary.total_expense, 2) if summary.total_income > 0
                else 0
            )
        )

        period = AnalyticsOverviewPeriodResponse(
            date_from=data.date_from,
            date_to=data.date_to
        )

        response = AnalyticsOverviewResponse(summary=summary, top_categories=top_categories, period=period)
        return response


async def get_top_by_category_data(
        data: AnalyticsExpensesByCategoryRequest | AnalyticsIncomesByCategoryRequest,
        user_id: int,
        transactions_type: str # попробовать енум
):
    async with session_factory() as session:
        params = {
            "user_id": user_id,
            "date_from": data.date_from,
            "date_to": data.date_to + timedelta(days=1),
            "list_account_id": data.list_account_id,
            "transaction_type": transactions_type
        }

        sql_code = await get_sql_code("sql/expenses_or_incomes_by_category.sql")
        res = await session.execute(text(sql_code), params)
        categories_raw = res.mappings().all()

        categories = []
        if categories_raw:
            rates = await get_rates(base_currency=data.currency.value)
            total_sum = 0
            for category_raw in categories_raw:
                category = {}
                account_currency = category_raw["account_currency"]
                category["category_total_sum"] = category_raw["category_total_sum"] / Decimal(rates[account_currency])
                category["title"] = category_raw["title"]

                total_sum += category["category_total_sum"]

                categories.append(category)

            for category_i in range(len(categories)):
                category = CategorySummary(
                    title=categories[category_i]["title"],
                    total=round(categories[category_i]["category_total_sum"], 2),
                    percentage=round(categories[category_i]["category_total_sum"]*100/total_sum, 2)
                )
                categories[category_i] = category

        period = AnalyticsOverviewPeriodResponse(
            date_from=data.date_from,
            date_to=data.date_to
        )
        response = AnalyticsExpensesByCategoryResponse(
            period=period,
            categories=categories,
            currency=data.currency.value
        )
        return response
