"""empty message

Revision ID: 8938e3bcb0ef
Revises: d3406098bbdc
Create Date: 2024-12-25 05:18:46.384486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8938e3bcb0ef'
down_revision: Union[str, None] = 'd3406098bbdc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE ROLE manager")
    op.execute('GRANT CONNECT ON DATABASE "mamonts-scam" TO manager')
    op.execute("GRANT USAGE ON SCHEMA public TO manager")
    op.execute("GRANT SELECT ON ALL TABLES IN SCHEMA public TO manager")
    op.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO manager")
    op.execute("REVOKE INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public FROM manager")
    op.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE INSERT, UPDATE, DELETE ON TABLES FROM manager")



def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
