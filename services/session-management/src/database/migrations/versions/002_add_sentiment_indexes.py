"""Add sentiment analysis indexes and optimizations

Revision ID: 002
Revises: 001
Create Date: 2024-01-02 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add composite indexes for better query performance
    op.create_index(
        'idx_sentiment_scores_session_timestamp', 
        'sentiment_scores', 
        ['session_id', 'timestamp']
    )
    
    op.create_index(
        'idx_sentiment_scores_overall_sentiment', 
        'sentiment_scores', 
        ['overall_sentiment']
    )
    
    op.create_index(
        'idx_sessions_user_start_time', 
        'sessions', 
        ['user_id', 'start_time']
    )
    
    # Add GIN index for JSONB columns for better search performance
    op.create_index(
        'idx_sentiment_emotions_gin', 
        'sentiment_scores', 
        ['emotions'], 
        postgresql_using='gin'
    )
    
    op.create_index(
        'idx_sessions_metadata_gin', 
        'sessions', 
        ['metadata'], 
        postgresql_using='gin'
    )
    
    # Add partial index for active sessions only
    op.create_index(
        'idx_sessions_active_last_activity', 
        'sessions', 
        ['last_activity'], 
        postgresql_where="status = 'active'"
    )


def downgrade() -> None:
    op.drop_index('idx_sessions_active_last_activity')
    op.drop_index('idx_sessions_metadata_gin')
    op.drop_index('idx_sentiment_emotions_gin')
    op.drop_index('idx_sessions_user_start_time')
    op.drop_index('idx_sentiment_scores_overall_sentiment')
    op.drop_index('idx_sentiment_scores_session_timestamp')
