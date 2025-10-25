from datetime import datetime
from decimal import Decimal

from fastapi.openapi.models import Schema
from pydantic import BaseModel, computed_field

from app.enum.analytics import BalanceGranularityEnum
from app.enum.currency import CurrencyEnum


class Analytics(BaseModel):
    pass


class AnalyticsOverviewRequest(Analytics):
    list_account_id: list[int]
    date_from: datetime
    date_to: datetime


class AnalyticsOverviewPeriodResponse(Analytics):
    date_from: datetime
    date_to: datetime


class AnalyticsOverviewSummaryResponse(Analytics):
    total_income: Decimal
    total_expense: Decimal
    net_balance: Decimal
    transaction_income_count: int
    transaction_expense_count: int
    transfer_income_count: int
    transfer_expense_count: int
    transaction_count: int


class CategorySummary(Analytics):
    title: str
    total: Decimal
    percentage: float


class AnalyticsOverviewTopCategoriesResponse(Analytics):
    income: CategorySummary
    expense: CategorySummary


class AnalyticsOverviewResponse(Analytics):
    period: AnalyticsOverviewPeriodResponse
    summary: AnalyticsOverviewSummaryResponse
    top_categories: AnalyticsOverviewTopCategoriesResponse


class AnalyticsExpensesByCategoryRequest(AnalyticsOverviewRequest):
    currency: CurrencyEnum # потом перенести в AnalyticsOverviewRequest


class AnalyticsExpensesByCategoryResponse(Analytics):
    period: AnalyticsOverviewPeriodResponse
    categories: list[CategorySummary]


class AnalyticsIncomesByCategoryRequest(AnalyticsOverviewRequest):
    currency: CurrencyEnum # потом перенести в AnalyticsOverviewRequest

class AnalyticsIncomesByCategoryResponse(Analytics):
    period: AnalyticsOverviewPeriodResponse
    categories: list[CategorySummary]


class AnalyticsBalanceTrendRequest(AnalyticsOverviewRequest):
    granularity: BalanceGranularityEnum


class AnalyticsPeriodsComparison(Analytics):
    list_account_id_1: list[int]
    list_account_id_2: list[int]
    date_from_1: datetime
    date_to_1: datetime
    date_from_2: datetime
    date_to_2: datetime
