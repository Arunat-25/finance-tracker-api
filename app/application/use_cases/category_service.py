from app.application.dtos.category_dto import CategoryCreateDTO, CategoryResponseDTO, CategoryDeleteDTO
from app.domain.interfaces.category_interface import CategoryRepositoryInterface
from app.domain.entities.category import Category
from app.domain.enums.category_type import CategoryTypeEnum


class CategoryService:
    def __init__(self, category_repo: CategoryRepositoryInterface):
        self.category_repo = category_repo


    async def get_categories(self, user_id: int) -> list[CategoryResponseDTO]:
        categories_entity = await self.category_repo.get_categories(user_id)
        categories = [self._entity_to_response_dto(category_entity) for category_entity in categories_entity]
        return categories


    async def delete_category_by_id(self, dto: CategoryDeleteDTO):
        category_entity = self._dto_to_entity(dto)
        deleted_category_entity = await self.category_repo.delete_category_by_id(category_entity)
        deleted_category = self._entity_to_response_dto(deleted_category_entity)
        return deleted_category


    async def create_default_categories(self, user_id: int) -> list[CategoryResponseDTO]:
        default_categories = [
            Category(name="Зарплата", category_type=CategoryTypeEnum.INCOME, owner_id=user_id),
            Category(name="Подарок", category_type=CategoryTypeEnum.INCOME, owner_id=user_id),
            Category(name="Инвестиции", category_type=CategoryTypeEnum.INCOME, owner_id=user_id),
            Category(name="Стипендия", category_type=CategoryTypeEnum.INCOME, owner_id=user_id),

            Category(name="Развлечение", category_type=CategoryTypeEnum.EXPENSE, owner_id=user_id),
            Category(name="Продукты", category_type=CategoryTypeEnum.EXPENSE, owner_id=user_id),
            Category(name="Жилье", category_type=CategoryTypeEnum.EXPENSE, owner_id=user_id),
            Category(name="Транспорт", category_type=CategoryTypeEnum.EXPENSE, owner_id=user_id),

            Category(name="Перевод", category_type=CategoryTypeEnum.TRANSFER, owner_id=user_id),
        ]
        created_categories_entity = await self.category_repo.create_categories(
            categories=default_categories,
            user_id=user_id
        )

        created_categories = [self._entity_to_response_dto(category) for category in created_categories_entity]
        return created_categories


    async def create_category(self, dto: CategoryCreateDTO) -> CategoryResponseDTO:
        category_entity = self._dto_to_entity(dto)
        created_category_entity = await self.category_repo.create_category(category=category_entity, user_id=dto.user_id)
        created_category = self._entity_to_response_dto(created_category_entity)
        return created_category


    def _dto_to_entity(self, dto) -> Category:
        entity = Category(owner_id=dto.user_id)
        if hasattr(dto, 'name'): entity.name = dto.name
        if hasattr(dto, 'category_type'): entity.category_type = dto.category_type
        if hasattr(dto, 'category_id'): entity.category_id = dto.category_id
        if hasattr(dto, 'created_at'): entity.created_at = dto.created_at
        if hasattr(dto, 'deleted_at'): entity.deleted_at = dto.deleted_at
        return entity


    def _entity_to_response_dto(self, entity: Category) -> CategoryResponseDTO:
        response_dto = CategoryResponseDTO(
            category_id=entity.category_id,
            name=entity.name,
            category_type=entity.category_type,
            user_id=entity.owner_id,
            created_at=entity.created_at,
            deleted_at=entity.deleted_at
        )
        return response_dto