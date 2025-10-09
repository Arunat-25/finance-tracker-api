from datetime import datetime

from fastapi.openapi.models import Schema
from pydantic import BaseModel

from app.enum.analytics import BalanceGranularityEnum


class Analytics(BaseModel):
    pass


class AnalyticsGetOverview(Analytics):
    list_account_id: list[int]
    date_from: datetime
    date_to: datetime


class AnalyticsGetExpensesByCategory(AnalyticsGetOverview):
    pass


class AnalyticsGetIncomesByCategory(AnalyticsGetOverview):
    pass


class AnalyticsGetBalanceTrend(AnalyticsGetOverview):
    granularity: BalanceGranularityEnum


class AnalyticsPeriodsComparison(Analytics):
    list_account_id_1: list[int]
    list_account_id_2: list[int]
    date_from_1: datetime
    date_to_1: datetime
    date_from_2: datetime
    date_to_2: datetime