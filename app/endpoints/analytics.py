from datetime import datetime

from fastapi import APIRouter
from fastapi.params import Depends

from app.dependencies.auth import get_current_user_id, get_current_user_utc_offset
from app.repositories.analytics import get_overview_data, get_top_by_category_data, get_balance_trend_data
from app.schemas.analytics import AnalyticsOverviewRequest, AnalyticsExpensesByCategoryRequest, AnalyticsIncomesByCategoryRequest, \
    AnalyticsBalanceTrendRequest, AnalyticsPeriodsComparison

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.post("/overview")#, response_model=AnalyticsOverviewResponse)
async def get_overview(data: AnalyticsOverviewRequest, user_id: int = Depends(get_current_user_id)):
    return await get_overview_data(data=data, user_id=user_id)


@router.post("/expenses-by-category")
async def get_expenses_by_category(data: AnalyticsExpensesByCategoryRequest, user_id: int = Depends(get_current_user_id)):
    return await get_top_by_category_data(data=data, user_id=user_id, transactions_type="expense")


@router.post("/income-by-category")
async def get_incomes_by_category(data: AnalyticsIncomesByCategoryRequest, user_id: int = Depends(get_current_user_id)):
    return await get_top_by_category_data(data=data, user_id=user_id, transactions_type="income")


@router.post("/balance_trend")
async def get_balance_trend(
        data: AnalyticsBalanceTrendRequest,
        user_id: int = Depends(get_current_user_id),
        user_utc_offset: int = Depends(get_current_user_utc_offset)
):
    time_start = datetime.utcnow()
    balance_trend = await get_balance_trend_data(data=data, user_id=user_id, user_utc_offset=user_utc_offset)
    end = datetime.utcnow()
    print(end-time_start)
    return balance_trend


@router.post("/compare-periods")
async def get_periods_comparison(data: AnalyticsPeriodsComparison, user_id: int = Depends(get_current_user_id)):
    pass