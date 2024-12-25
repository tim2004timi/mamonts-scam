"""empty message

Revision ID: 9bc184a1344a
Revises: 48d75b69baef
Create Date: 2024-12-25 04:35:36.297476

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9bc184a1344a'
down_revision: Union[str, None] = '48d75b69baef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE OR REPLACE FUNCTION create_current_odds()
    RETURNS TRIGGER AS $$
    DECLARE
        random_first_odds DECIMAL(4,2);
        second_odds DECIMAL(4,2);
        margin DECIMAL(4,2) := 0.1;
    BEGIN
        random_first_odds := ROUND(1 + (random() * 3)::numeric, 2);
        
        second_odds := ROUND((1 + margin) * (2 - (1 / random_first_odds)), 2);
        IF second_odds < 1.0 THEN
            second_odds := 1.01; 
        END IF;
    
        INSERT INTO current_odds(event_id, first_win_odds, second_win_odds)
        VALUES (NEW.id, random_first_odds, second_odds);
    
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;""")

    op.execute("""
    CREATE OR REPLACE TRIGGER after_event_insert
    AFTER INSERT ON events
    FOR EACH ROW
    EXECUTE FUNCTION create_current_odds();
    """)


def downgrade() -> None:
    op.execute("DROP FUNCTION create_current_odds")
    op.execute("DROP TRIGGER after_event_insert")
