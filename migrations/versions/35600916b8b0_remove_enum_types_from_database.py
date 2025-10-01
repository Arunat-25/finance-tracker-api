from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '35600916b8b0'
down_revision = 'baf0866d680e'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 1. Меняем тип category_type с ENUM на VARCHAR
    op.alter_column('categories', 'category_type',
               existing_type=sa.Enum('income', 'expense', name='category_enum'),
               type_=sa.VARCHAR(),
               nullable=False,
               postgresql_using='category_type::text')
    
    # 2. Меняем тип currency с ENUM на VARCHAR  
    op.alter_column('accounts', 'currency',
               existing_type=sa.Enum('RUB', 'USD', 'EUR', 'KZT', name='currency_enum'),
               type_=sa.VARCHAR(),
               nullable=True,
               postgresql_using='currency::text')
    
    # 3. Удаляем ENUM типы из БД
    op.execute("DROP TYPE IF EXISTS category_enum")
    op.execute("DROP TYPE IF EXISTS currency_enum")
    
    # 4. Добавляем CheckConstraint для валидации category_type
    op.create_check_constraint(
        'chk_category_type',
        'categories',
        "category_type IN ('income', 'expense')"
    )

def downgrade() -> None:
    # 1. Удаляем CheckConstraint
    op.drop_constraint('chk_category_type', 'categories', type_='check')
    
    # 2. Восстанавливаем ENUM типы
    op.execute("CREATE TYPE category_enum AS ENUM ('income', 'expense')")
    op.execute("CREATE TYPE currency_enum AS ENUM ('RUB', 'USD', 'EUR', 'KZT')")
    
    # 3. Возвращаем типы колонок на ENUM
    op.alter_column('categories', 'category_type',
               existing_type=sa.VARCHAR(),
               type_=sa.Enum('income', 'expense', name='category_enum'),
               nullable=False,
               postgresql_using='category_type::category_enum')
    
    op.alter_column('accounts', 'currency',
               existing_type=sa.VARCHAR(),
               type_=sa.Enum('RUB', 'USD', 'EUR', 'KZT', name='currency_enum'),
               nullable=True,
               postgresql_using='currency::currency_enum')