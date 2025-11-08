from fastapi import APIRouter, Depends, HTTPException

from app.auth_dependencies import get_current_user_id
from app.repositories.transaction import create_transfer, create_expense, create_income, get_transactions
from app.endpoints.exceptions import NotEnoughMoney, NotFoundAccount, CategoryNotFound
from app.schemas.transaction import TransferCreate, TransactionIncomeCreate, TransactionExpenseCreate, TransactionsGet

router = APIRouter(prefix="/transaction", tags=["transaction"])


@router.post("/create-expense-transaction")
async def create_expense_transaction(data: TransactionExpenseCreate, user_id=Depends(get_current_user_id)):
    try:
        return await create_expense(data=data, user_id=user_id)
    except CategoryNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except NotFoundAccount as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/create-income-transaction")
async def create_income_transaction(data: TransactionIncomeCreate, user_id=Depends(get_current_user_id)):
    try:
        return await create_income(user_id=user_id, data=data)
    except CategoryNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except NotFoundAccount as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/make-transfer")
async def make_transfer(data: TransferCreate, user_id=Depends(get_current_user_id)):
    try:
        return await create_transfer(user_id=user_id, data=data)
    except CategoryNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except NotEnoughMoney as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NotFoundAccount as e:
        raise HTTPException(status_code=404, detail=str(e))



@router.post("/transactions-list")
async def get_transactions_for_period(data: TransactionsGet, user_id=Depends(get_current_user_id)):
    return await get_transactions(data=data, user_id=user_id)