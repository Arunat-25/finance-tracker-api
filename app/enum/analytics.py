from enum import Enum


class AnalyticsEnum(str, Enum):
    TODAY = "today"
    FOR_3_DAYS = "for-3-days"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


class BalanceGranularityEnum(str, Enum):
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
