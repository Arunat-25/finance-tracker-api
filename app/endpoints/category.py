from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from app.application.dtos.category_dto import CategoryCreateDTO
from app.application.services.category_service import CategoryService
from app.dependencies.auth import get_current_user_id
from app.dependencies.category_dependencies import get_category_service
from app.repositories.category import create_category, remove_category
from app.endpoints.exceptions import CategoryAlreadyExists, CategoryNotFound
from app.schemas.category import CategoryCreate, CategoryDelete
from dtos.category_dto import CategoryDeleteDTO

router = APIRouter(prefix="/category", tags=["category"])

@router.get("/create-system-categories")
async def create_system_categories(
        user_id: int = Depends(get_current_user_id),
        category_service: CategoryService = Depends(get_category_service)
):
    created_system_categories = await category_service.create_default_categories(user_id=user_id)
    return created_system_categories


@router.post("/create-personal-category")
async def create_personal_category(
        data: CategoryCreate,
        user_id: int = Depends(get_current_user_id),
        category_service: CategoryService = Depends(get_category_service)
):
    try:
        data_dto = CategoryCreateDTO(name=data.title, category_type=data.category_type, user_id=user_id)
        created_category = await category_service.create_category(dto=data_dto)
        return created_category
    except CategoryAlreadyExists as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete-category")
async def delete_category(
        data: CategoryDelete,
        user_id: int = Depends(get_current_user_id),
        category_service: CategoryService = Depends(get_category_service)
):
    try:
        category_dto = CategoryDeleteDTO(category_id=data.category_id, user_id=user_id)
        deleted_category = await category_service.delete_category_by_id(category_dto)
        return deleted_category
    except CategoryNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))