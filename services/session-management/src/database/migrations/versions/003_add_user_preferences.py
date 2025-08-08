"""Add user preferences and settings

Revision ID: 003
Revises: 002
Create Date: 2024-01-03 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create user_preferences table
    op.create_table(
        'user_preferences',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), 
                  sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('preference_key', sa.String(100), nullable=False),
        sa.Column('preference_value', postgresql.JSONB(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    
    # Add unique constraint on user_id + preference_key
    op.create_unique_constraint(
        'uq_user_preferences_user_key', 
        'user_preferences', 
        ['user_id', 'preference_key']
    )
    
    # Add new columns to users table
    op.add_column('users', sa.Column('timezone', sa.String(50), nullable=True, default='UTC'))
    op.add_column('users', sa.Column('language', sa.String(10), nullable=True, default='en'))
    op.add_column('users', sa.Column('sentiment_baseline', sa.Float, nullable=True))
    op.add_column('users', sa.Column('interaction_count', sa.Integer, nullable=False, default=0))
    
    # Add new columns to sessions table
    op.add_column('sessions', sa.Column('sentiment_summary', postgresql.JSONB(), nullable=True))
    op.add_column('sessions', sa.Column('drift_events_count', sa.Integer, nullable=False, default=0))
    op.add_column('sessions', sa.Column('avg_sentiment', sa.Float, nullable=True))
    op.add_column('sessions', sa.Column('min_sentiment', sa.Float, nullable=True))
    op.add_column('sessions', sa.Column('max_sentiment', sa.Float, nullable=True))
    
    # Create indexes
    op.create_index('idx_user_preferences_user_id', 'user_preferences', ['user_id'])
    op.create_index('idx_users_sentiment_baseline', 'users', ['sentiment_baseline'])


def downgrade() -> None:
    # Remove columns from sessions table
    op.drop_column('sessions', 'max_sentiment')
    op.drop_column('sessions', 'min_sentiment')
    op.drop_column('sessions', 'avg_sentiment')
    op.drop_column('sessions', 'drift_events_count')
    op.drop_column('sessions', 'sentiment_summary')
    
    # Remove columns from users table
    op.drop_column('users', 'interaction_count')
    op.drop_column('users', 'sentiment_baseline')
    op.drop_column('users', 'language')
    op.drop_column('users', 'timezone')
    
    # Drop user_preferences table
    op.drop_table('user_preferences')
