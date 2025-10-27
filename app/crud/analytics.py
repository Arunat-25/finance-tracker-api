import asyncio, aiofiles

from datetime import timedelta
from decimal import Decimal
from typing import Literal

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

        rates = await get_rates(base_currency=data.currency.value)

        sql_code_summary = await get_sql_code("sql/overview_summary.sql")
        result_summary = await session.execute(text(sql_code_summary), params)
        filtered_transactions = result_summary.mappings().all()

        total_income = Decimal(0.00)
        total_expense = Decimal(0.00)
        total_transfer_income = Decimal(0.00)
        total_transfer_expense = Decimal(0.00)
        transaction_income_count = 0
        transaction_expense_count = 0
        transfer_income_count = 0
        transfer_expense_count = 0
        transaction_count = len(filtered_transactions)
        if transaction_count > 0:
            for transaction in filtered_transactions:
                rate = Decimal(rates[transaction["currency"]])
                converted_amount = round(transaction["amount"]/rate, 2)
                if transaction["transaction_type"] == "income":
                    total_income += converted_amount
                    transaction_income_count += 1
                elif transaction["transaction_type"] == "expense":
                    total_expense += converted_amount
                    transaction_expense_count += 1
                else: # если transfer
                    if transaction["to_account_id"] is None: # если income transfer
                        transfer_income_count += 1
                        total_transfer_income += converted_amount
                    else: # если expense transfer
                        transfer_expense_count += 1
                        total_transfer_expense += converted_amount

        summary = AnalyticsOverviewSummaryResponse(
            total_income=total_income,
            total_expense=total_expense,
            net_balance=total_income - total_expense,
            transaction_income_count=transaction_income_count,
            transaction_expense_count=transaction_expense_count,
            transfer_income_count=transfer_income_count,
            transfer_expense_count=transfer_expense_count,
            transaction_count=transaction_count,
        )

        sql_code_top_categories = await get_sql_code("sql/overview_top_categories.sql")
        result_top_categories = await session.execute(text(sql_code_top_categories), params)
        list_RowMapping_categories = result_top_categories.mappings().all()
        list_dict_categories = [dict(category) for category in list_RowMapping_categories]

        for category in list_dict_categories:
            rate = Decimal(rates[category["currency"]])
            category["converted_amount"] = category["amount"] / rate

        aggregated_categories = {}
        for category in list_dict_categories:
            key = (category["title"], category["category_type"])
            if key in aggregated_categories:
                aggregated_categories[key]["converted_amount"] += category["converted_amount"]
            else:
                aggregated_categories[key] = {
                    "title": category["title"],
                    "category_type": category["category_type"],
                    "converted_amount": category["converted_amount"]
                }

        top_income_category = {"converted_amount": Decimal(0), "title": ""}
        top_expense_category = {"converted_amount": Decimal(0), "title": ""}

        for category in aggregated_categories.values():
            if (category["category_type"] == "income"
                    and category["converted_amount"] > top_income_category["converted_amount"]):
                top_income_category = category
            elif (category["category_type"] == "expense"
                  and category["converted_amount"] > top_expense_category["converted_amount"]):
                top_expense_category = category

        top_categories = AnalyticsOverviewTopCategoriesResponse(
            income = CategorySummary(
                title=top_income_category["title"],
                total=round(top_income_category["converted_amount"], 2),
                percentage=round(top_income_category["converted_amount"]*100/summary.total_income, 2)
                if summary.total_income > 0 else 0
            ),
            expense = CategorySummary(
                title=top_expense_category["title"],
                total=round(top_expense_category["converted_amount"], 2),
                percentage=round(top_expense_category["converted_amount"]*100/summary.total_expense, 2)
                if summary.total_income > 0 else 0
            )
        )

        period = AnalyticsOverviewPeriodResponse(
            date_from=data.date_from,
            date_to=data.date_to
        )

        response = AnalyticsOverviewResponse(
            summary=summary,
            top_categories=top_categories,
            period=period,
            currency=data.currency.value
        )
        return response


async def get_top_by_category_data(
        data: AnalyticsExpensesByCategoryRequest | AnalyticsIncomesByCategoryRequest,
        user_id: int,
        transactions_type: Literal["income", "expense"]
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
