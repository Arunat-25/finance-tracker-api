from datetime import datetime
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Query, Depends

from app.auth_dependencies import get_current_user_id
from app.crud.analytics import get_overview
from app.enum.analytics import AnalyticsEnum
from app.schemas.analytics import AnalyticsGetOverview, AnalyticsGetExpensesByCategory, AnalyticsGetIncomesByCategory, \
    AnalyticsGetBalanceTrend, AnalyticsPeriodsComparison, AnalyticsOverviewResponse

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.post("/overview")#, response_model=AnalyticsOverviewResponse)
async def get_analytics_overview(data: AnalyticsGetOverview, user_id: int = Depends(get_current_user_id)):
    time_start = datetime.now()
    a = await get_overview(data=data, user_id=user_id)
    time_end = datetime.now()
    print(time_end - time_start)
    return a


@router.post("/expenses-by-category")
async def get_analytics_expenses_by_category(data: AnalyticsGetExpensesByCategory, user_id: int = Depends(get_current_user_id)):
    pass


@router.post("/income-by-category")
async def get_analytics_incomes_by_category(data: AnalyticsGetIncomesByCategory, user_id: int = Depends(get_current_user_id)):
    pass


@router.post("/balance_trend")
async def get_analytics_balance_trend(data: AnalyticsGetBalanceTrend, user_id: int = Depends(get_current_user_id)):
    pass


@router.post("/compare-periods")
async def get_analytics_periods_comparison(data: AnalyticsPeriodsComparison, user_id: int = Depends(get_current_user_id)):
    pass