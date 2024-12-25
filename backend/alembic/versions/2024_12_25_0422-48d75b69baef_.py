"""empty message

Revision ID: 48d75b69baef
Revises: 42b691cd2194
Create Date: 2024-12-25 04:22:35.909271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '48d75b69baef'
down_revision: Union[str, None] = '42b691cd2194'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bets',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('win_team_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('odds', sa.Numeric(precision=5, scale=2), nullable=False),
    sa.Column('bet_date', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['win_team_id'], ['team.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('current_odds',
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('first_win_odds', sa.Numeric(precision=4, scale=2), nullable=False),
    sa.Column('second_win_odds', sa.Numeric(precision=4, scale=2), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('event_id')
    )
    op.alter_column('events', 'event_end_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    # ### end Alembic commands ###

    op.execute("""
        CREATE OR REPLACE FUNCTION create_current_odds()
        RETURNS TRIGGER AS $$
        DECLARE
            random_first_odds DECIMAL(4,2);
            second_odds DECIMAL(4,2);
            margin DECIMAL(4,2) := 0.1;
        BEGIN
            random_first_odds := ROUND(1 + (random() * 3)::numeric, 2);

            second_odds := ROUND((1 / (1 - margin)) * (1 / random_first_odds), 2);

            INSERT INTO current_odds(event_id, first_win_odds, second_win_odds)
            VALUES (NEW.id, random_first_odds, second_odds);

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;""")
    op.execute("""
        CREATE TRIGGER after_event_insert
        AFTER INSERT ON events
        FOR EACH ROW
        EXECUTE FUNCTION create_current_odds();
        """)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('events', 'event_end_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.drop_table('current_odds')
    op.drop_table('bets')
    # ### end Alembic commands ###
