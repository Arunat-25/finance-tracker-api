from enum import Enum


class BalanceGranularityEnum(str, Enum):
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
