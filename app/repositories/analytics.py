from datetime import timedelta, datetime
from decimal import Decimal
from typing import Literal

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.account import get_accounts
from app.currency import get_rates
from app.infrastructure.db.session import session_factory
from app.schemas.analytics import AnalyticsOverviewRequest, AnalyticsOverviewSummaryResponse, \
    AnalyticsOverviewTopCategoriesResponse, CategorySummary, AnalyticsOverviewPeriodResponse, \
    AnalyticsOverviewResponse,     AnalyticsExpensesByCategoryRequest, AnalyticsExpensesByCategoryResponse, \
    AnalyticsIncomesByCategoryRequest, AnalyticsBalanceTrendRequest
from app.infrastructure.sql.get_sql_code_from_file import get_sql_code


async def get_overview_data(data: AnalyticsOverviewRequest, user_id: int):
    async with session_factory() as session:
        params = {
            "user_id": user_id,
            "date_from": data.date_from,
            "date_to": data.date_to + timedelta(days=1),
            "list_account_id": data.list_account_id
        }

        rates = await get_rates(base_currency=data.currency.value)

        sql_code_summary = await get_sql_code("app/infrastructure/sql/overview_summary.sql")
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

        sql_code_top_categories = await get_sql_code("app/infrastructure/sql/overview_top_categories.sql")
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

        sql_code = await get_sql_code("app/infrastructure/sql/expenses_or_incomes_by_category.sql")
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


async def get_balance_trend_data(data: AnalyticsBalanceTrendRequest, user_id: int, user_utc_offset: int = 0):
    async with (session_factory() as session):
        adjusted_date_to = adjust_date_to(data.date_to)
        params = {
            "user_id": user_id,
            "list_account_id": data.list_account_id,
            "date_from": data.date_from, #timedelta(hours=user_utc_offset),
            "date_to": adjusted_date_to # - timedelta(hours=user_utc_offset),
        }
        sql_code = await get_sql_code("app/infrastructure/sql/balance_trend.sql")
        res = await session.execute(text(sql_code), params)
        transactions_RawMapping = res.mappings().all()
        transactions = [dict(transaction) for transaction in transactions_RawMapping]

        rates = await get_rates(base_currency=data.currency.value)
        transactions = await convert_transactions_currency(
            transactions=transactions,
            columns_to_convert=["balance_before", "balance_after"],
            rates=rates,
            currency_key="currency"
        )

        period = adjusted_date_to - data.date_from
        if period <= timedelta(days=1):
            granularity = 'hour'
            count_interval = int(period.total_seconds()//60//60)
            intervals = get_list_with_intervals(data.date_from, data.date_to, granularity)
            interval_order_and_interval = {}
            for interval_order in range(count_interval):
                interval_order_and_interval[interval_order] = intervals.index(interval_order)
        else:
            granularity = 'day'
            count_interval = int(period.total_seconds()//60//60//24)
            intervals = get_list_with_intervals(data.date_from, data.date_to, granularity)
            interval_order_and_interval = {}
            for interval_order in range(count_interval):
                interval_order_and_interval[interval_order] = intervals[interval_order]

        if not transactions:
            params_to_get_balance_trend_for_accounts_which_not_in_period = params.copy()
            params_to_get_balance_trend_for_accounts_which_not_in_period["date_to"] = datetime.utcnow()
            balance_trend = await get_balance_trend_for_accounts_which_not_in_period(
                session=session,
                params=params_to_get_balance_trend_for_accounts_which_not_in_period,
                rates=rates,
                count_interval=count_interval
            )
            return balance_trend

        balance_trend = await get_balance_trend_for_period(
            session=session,
            data=data,
            transactions=transactions,
            user_id=user_id,
            rates=rates,
            user_utc_offset=user_utc_offset,
            granularity=granularity,
            count_interval=count_interval,
            interval_order_and_interval=interval_order_and_interval
        )
        return balance_trend


async def get_balance_trend_for_period(
        session:AsyncSession,
        data: AnalyticsBalanceTrendRequest,
        transactions: list,
        user_id: int,
        rates: dict,
        user_utc_offset: int,
        granularity: str,
        count_interval: int,
        interval_order_and_interval: dict
):
    balance_trend = {}
    for interval_order in range(count_interval):
        # interval это порядок интервала времени для которого находится баланс
        # например введено date_to = '2024-09-11 13:00:00' date_from = '2024-09-11 17:00:00'
        # тогда interval_order = 0 будет соответствовать интервалу времени 13ч(13ч00мин00сек - 13ч59мин59сек)
        for tran in transactions:  # удалять те по которым прошел
            end_of_interval = get_end_of_interval(
                date_from=data.date_from,
                granularity=granularity,
                interval_order=interval_order
            )
            if tran["date"] <= end_of_interval:
                tran_account_id = tran["account_id"]
                if tran_account_id in balance_trend:
                    balance_trend[tran_account_id][interval_order] = tran["balance_after"]
                else:
                    balance_trend[tran_account_id] = {interval_order: tran["balance_after"]}
            else:
                break

            count_accounts_with_found_balance = len(balance_trend)
            is_last_iteration = interval_order == count_interval-1 and tran is transactions[-1]
            if is_last_iteration and count_accounts_with_found_balance < len(data.list_account_id):
                accounts_with_found_balance = balance_trend.keys()
                accounts_with_not_found_balance = list(
                    filter(
                        lambda x: x not in accounts_with_found_balance,
                        data.list_account_id
                    )
                )
                params = {
                    "user_id": user_id,
                    "list_account_id": accounts_with_not_found_balance,
                    "date_from": data.date_to.replace(tzinfo=None),
                    "date_to": datetime.utcnow(),
                }
                balance_trend_not_in_period = await get_balance_trend_for_accounts_which_not_in_period(
                    session=session,
                    params=params,
                    rates=rates,
                    count_interval=count_interval
                )

                balance_trend = {**balance_trend, **balance_trend_not_in_period}
                return balance_trend
    return balance_trend


async def get_balance_trend_for_accounts_which_not_in_period(
        session: AsyncSession,
        params: dict,
        rates: dict,
        count_interval: int
):
    sql_code = await get_sql_code("app/infrastructure/sql/get_first_transaction_from_from_date.sql")
    res = await session.execute(text(sql_code), params)
    transactions_RawMapping = res.mappings().all()
    transactions = [dict(transaction) for transaction in transactions_RawMapping]

    transactions = await convert_transactions_currency(
        transactions=transactions,
        currency_key="currency",
        columns_to_convert=["balance_before"],
        rates=rates
    )

    accounts_without_transactions = [*params["list_account_id"]]
    balance_trend = {}
    for tran in transactions:
        balance_trend[tran["account_id"]] = {}
        accounts_without_transactions.remove(tran["account_id"])
        for interval_order in range(count_interval):
            balance_trend[tran["account_id"]][interval_order] = tran["balance_before"]

    if accounts_without_transactions:
        orm_accounts = await get_accounts(
            session=session,
            account_ids=accounts_without_transactions,
            user_id=params["user_id"]
        )
        for orm_account in orm_accounts:
            balance_trend[orm_account.id] = {}
            for interval_order in range(count_interval):
                rate = Decimal(rates[orm_account.currency])
                balance_trend[orm_account.id][interval_order] = round(orm_account.balance / rate, 2)
    return balance_trend


async def convert_transactions_currency(
        transactions: list[dict],
        columns_to_convert: list[str],
        rates: dict,
        currency_key: str
) -> list:
    for tran in transactions:
        rate = Decimal(rates[tran[currency_key]])
        for column_to_convert in columns_to_convert:
            tran[column_to_convert] = round(tran[column_to_convert] / rate, 2)
    return transactions


def adjust_date_to(date_to) -> datetime:
    if date_to.microsecond > 0:
        delta = timedelta(microseconds=1)
    elif date_to.second > 0:
        delta = timedelta(seconds=1)
    elif date_to.minute > 0:
        delta = timedelta(minutes=1)
    elif date_to.hour > 0:
        delta = timedelta(hours=1)
    else:
        delta = timedelta(days=1)
    return date_to + delta


def get_list_with_intervals(date_from: datetime, date_to: datetime, granularity: str) -> list[int]:
    list_with_intervals = []
    if granularity == "hour":
        if date_to.hour > date_from.hour:
            list_with_intervals = [hour for hour in range(date_from.hour, date_to.hour + 1)]
        elif date_to.hour <= date_from.hour:
            list_with_intervals_first_part = [hour for hour in range(date_from.hour, 24)]
            list_with_intervals_second_part = [hour for hour in range(0, date_to.hour+1)]
            list_with_intervals = [*list_with_intervals_first_part, *list_with_intervals_second_part]
    elif granularity == "day":
        if date_to.month == date_from.month:
            list_with_intervals = [day for day in range(date_from.day, date_to.day + 1)]
        else:
            is_leap_year = True if (date_from.year % 4 == 0 and date_from.year % 100 != 0) or \
                                   (date_from.year % 400 == 0) else False
            month_and_count_days = {1: 31, 2: 28 if not is_leap_year else 29, 3: 31, 4: 30, 5: 31, 6: 30,
                                    7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
            last_day_of_month_of_date_from = month_and_count_days[date_from.month]
            list_with_intervals_first_part = [day for day in range(date_from.day, last_day_of_month_of_date_from+1)]
            list_with_intervals_second_part = [day for day in range(1, date_to.day+1)]
            list_with_intervals = [*list_with_intervals_first_part, *list_with_intervals_second_part]
    return list_with_intervals


def get_end_of_interval(date_from: datetime, granularity: str, interval_order: int) -> datetime:
    if granularity == "day":
        end_of_interval = date_from + timedelta(
            days=interval_order, hours=23, minutes=59, seconds=59, microseconds=5999
        )
    else:  # если "hour"
        end_of_interval = date_from + timedelta(
            hours=interval_order, minutes=59, seconds=59, microseconds=5999
        )
    return end_of_interval


async def do_db_request_and_get_transactions(session: AsyncSession, sql_code: str, params: dict) -> list[dict]:
    res = await session.execute(text(sql_code), params)
    transactions_RawMapping = res.mappings().all()
    transactions = [dict(transaction) for transaction in transactions_RawMapping]
    return transactions


async def add_to_balance_trend():
    pass