from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '929f6fa41b90'
down_revision = 'debb5f6c9797'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 1. Создаем ENUM тип если не существует
    op.execute("""
        DO $$ 
        BEGIN 
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'currency_enum') THEN
                CREATE TYPE currency_enum AS ENUM (
                    'RUB', 'INR', 'IRR', 'BRL', 'UZC', 'TRY', 'BYN', 'KZT', 
                    'UAH', 'USD', 'EUR', 'JPY', 'GBP', 'CNY'
                );
            END IF;
        END $$;
    """)
    
    # 2. Безопасное изменение типа через временную колонку
    op.add_column('accounts', sa.Column('currency_new', postgresql.ENUM(
        'RUB', 'INR', 'IRR', 'BRL', 'UZC', 'TRY', 'BYN', 'KZT', 
        'UAH', 'USD', 'EUR', 'JPY', 'GBP', 'CNY', name='currency_enum'
    )))
    
    # 3. Копируем данные
    op.execute("UPDATE accounts SET currency_new = currency::text::currency_enum")
    
    # 4. Удаляем старую колонку
    op.drop_column('accounts', 'currency')
    
    # 5. Переименовываем новую колонку
    op.alter_column('accounts', 'currency_new', new_column_name='currency')
    
    # 6. Создаем таблицу categories (если нужно)
    # ... остальной код создания таблиц и индексов

def downgrade() -> None:
    # Обратная миграция
    op.alter_column('accounts', 'currency', type_=sa.VARCHAR())
    op.execute("DROP TYPE IF EXISTS currency_enum")
    
    # Удаляем таблицу categories если создавали
    op.drop_table('categories')