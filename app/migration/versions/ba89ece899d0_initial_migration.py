"""Initial migration

Revision ID: ba89ece899d0
Revises: 
Create Date: 2024-11-07 12:22:00.261456

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba89ece899d0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('news',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('article', sa.String(), nullable=True),
        sa.Column('img_url', sa.String(), nullable=True),
        sa.Column('link', sa.String(), nullable=True),
        sa.Column('body_text', sa.String(), nullable=True),
        sa.Column('news_date', sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('link')
    )
    op.create_index(op.f('ix_news_article'), 'news', ['article'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_news_article'), table_name='news')
    op.drop_table('news')
    # ### end Alembic commands ###
