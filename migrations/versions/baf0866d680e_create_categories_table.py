from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'baf0866d680e'
down_revision = '929f6fa41b90'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Создаем таблицу categories (ENUM уже существует)
    op.create_table('categories',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('category_type', sa.Enum('income', 'expense', name='category_enum'), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"),
                              nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )

    # Создаем индексы
    op.create_index(op.f('ix_categories_title'), 'categories', ['title'], unique=False)
    op.create_index(op.f('ix_categories_user_id'), 'categories', ['user_id'], unique=False)
    op.create_index(op.f('ix_categories_category_type'), 'categories', ['category_type'], unique=False)

    # Уникальный констрейнт - один пользователь не может иметь дубликаты категорий
    op.create_unique_constraint('uq_user_category_title', 'categories', ['user_id', 'title'])

def downgrade() -> None:
    # Удаляем таблицу и индексы
    op.drop_table('categories')
    
    # Удаляем ENUM тип
    op.execute("DROP TYPE IF EXISTS category_enum")