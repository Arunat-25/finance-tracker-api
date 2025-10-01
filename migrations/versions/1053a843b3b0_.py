from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '1053a843b3b0'
down_revision = 'e7e65bbb6b73'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # БЕЗОПАСНОЕ создание ENUM типа
    op.execute("""
        DO $$ 
        BEGIN 
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'currencyenum') THEN
                CREATE TYPE currencyenum AS ENUM ('RUB', 'USD', 'EUR');
            END IF;
        END $$;
    """)

    # Временное преобразование через TEXT для обхода ошибки
    op.alter_column('accounts', 'currency',
                    type_=sa.Text(),
                    existing_type=sa.VARCHAR(),
                    existing_nullable=True,
                    postgresql_using='currency::text')

    # Финальное преобразование в ENUM
    op.alter_column('accounts', 'currency',
                    type_=postgresql.ENUM('RUB', 'USD', 'EUR', name='currencyenum'),
                    existing_type=sa.Text(),
                    existing_nullable=True,
                    postgresql_using='currency::text::currencyenum')


def downgrade() -> None:
    # Возвращаем обратно в VARCHAR
    op.alter_column('accounts', 'currency',
                    type_=sa.VARCHAR(),
                    existing_type=postgresql.ENUM('RUB', 'USD', 'EUR', name='currencyenum'),
                    existing_nullable=True,
                    postgresql_using='currency::text')

    # Осторожно удаляем ENUM тип (только если больше не используется)
    op.execute("DROP TYPE IF EXISTS currencyenum")