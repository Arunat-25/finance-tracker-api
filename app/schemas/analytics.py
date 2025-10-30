from datetime import datetime, timezone
from decimal import Decimal

from fastapi.openapi.models import Schema
from pydantic import BaseModel, computed_field, field_validator, model_validator

from app.enum.analytics import BalanceGranularityEnum
from app.enum.currency import CurrencyEnum


class Analytics(BaseModel):
    pass


class AnalyticsOverviewRequest(Analytics):
    list_account_id: list[int]
    currency: CurrencyEnum
    date_from: datetime
    date_to: datetime

    @field_validator('date_to')
    def check_date_to(cls, value):
        if value > datetime.now(timezone.utc):
            raise ValueError('date_to cannot be greater than now')


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
    currency: CurrencyEnum


class AnalyticsExpensesByCategoryRequest(AnalyticsOverviewRequest):
    pass


class AnalyticsExpensesByCategoryResponse(Analytics):
    period: AnalyticsOverviewPeriodResponse
    categories: list[CategorySummary]
    currency: CurrencyEnum


class AnalyticsIncomesByCategoryRequest(AnalyticsOverviewRequest):
    pass


class AnalyticsIncomesByCategoryResponse(Analytics):
    period: AnalyticsOverviewPeriodResponse
    categories: list[CategorySummary]


class AnalyticsBalanceTrendRequest(AnalyticsOverviewRequest):
    @model_validator(mode='after')
    def check_period(self):
        period = self.date_to - self.date_from
        if period < timedelta(hours=1):
            raise ValueError("Период не может быть меньше 1 часа")
        if period > timedelta(days=31):
            raise ValueError("Период не может превышать 31 день")
        return self


class AnalyticsPeriodsComparison(Analytics):
    list_account_id_1: list[int]
    list_account_id_2: list[int]
    date_from_1: datetime
    date_to_1: datetime
    date_from_2: datetime
    date_to_2: datetime
