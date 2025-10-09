from datetime import datetime
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Query, Depends

from app.auth_dependencies import get_current_user_id
from app.enum.analytics import AnalyticsEnum
from app.schemas.analytics import AnalyticsGetOverview, AnalyticsGetExpensesByCategory, AnalyticsGetIncomesByCategory, \
    AnalyticsGetBalanceTrend, AnalyticsPeriodsComparison

router = APIRouter(prefix="analytics", tags=["analytics"])


@router.get("/overview")
async def get_overview(data: AnalyticsGetOverview, user_id: int = Depends(get_current_user_id)):
    pass


@router.get("/expenses-by-category")
async def get_expenses_by_category(data: AnalyticsGetExpensesByCategory, user_id: int = Depends(get_current_user_id)):
    pass


@router.get("/income-by-category")
async def get_incomes_by_category(data: AnalyticsGetIncomesByCategory, user_id: int = Depends(get_current_user_id)):
    pass


@router.get("/balance_trend")
async def get_balance_trend(data: AnalyticsGetBalanceTrend, user_id: int = Depends(get_current_user_id)):
    pass


@router.get("/compare-periods")
async def get_periods_comparison(data: AnalyticsPeriodsComparison, user_id: int = Depends(get_current_user_id)):
    pass