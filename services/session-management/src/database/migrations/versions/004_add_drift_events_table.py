"""Add drift events tracking table

Revision ID: 004
Revises: 003
Create Date: 2024-01-04 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create drift_events table
    op.create_table(
        'drift_events',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), 
                  sa.ForeignKey('sessions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), 
                  sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('message_id', postgresql.UUID(as_uuid=True), 
                  sa.ForeignKey('messages.id', ondelete='SET NULL'), nullable=True),
        sa.Column('event_type', sa.String(50), nullable=False),  # 'drift_detected', 'sentiment_spike', etc.
        sa.Column('drift_magnitude', sa.Float, nullable=False),
        sa.Column('drift_direction', sa.String(20), nullable=False),  # 'positive', 'negative', 'neutral'
        sa.Column('confidence', sa.Float, nullable=False),
        sa.Column('detection_method', sa.String(50), nullable=False),
        sa.Column('window_analyzed', sa.Integer, nullable=False),
        sa.Column('baseline_sentiment', sa.Float, nullable=True),
        sa.Column('current_sentiment', sa.Float, nullable=False),
        sa.Column('recommended_action', sa.String(100), nullable=True),
        sa.Column('action_taken', sa.String(100), nullable=True),
        sa.Column('metadata', postgresql.JSONB(), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    
    # Create response_adaptations table
    op.create_table(
        'response_adaptations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('drift_event_id', postgresql.UUID(as_uuid=True), 
                  sa.ForeignKey('drift_events.id', ondelete='CASCADE'), nullable=False),
        sa.Column('session_id', postgresql.UUID(as_uuid=True), 
                  sa.ForeignKey('sessions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('original_response', sa.Text, nullable=True),
        sa.Column('adapted_response', sa.Text, nullable=False),
        sa.Column('adaptation_strategy', sa.String(100), nullable=False),
        sa.Column('adaptation_confidence', sa.Float, nullable=False),
        sa.Column('effectiveness_score', sa.Float, nullable=True),  # Measured later
        sa.Column('metadata', postgresql.JSONB(), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    
    # Create indexes for drift_events
    op.create_index('idx_drift_events_session_id', 'drift_events', ['session_id'])
    op.create_index('idx_drift_events_user_id', 'drift_events', ['user_id'])
    op.create_index('idx_drift_events_timestamp', 'drift_events', ['timestamp'])
    op.create_index('idx_drift_events_type', 'drift_events', ['event_type'])
    op.create_index('idx_drift_events_magnitude', 'drift_events', ['drift_magnitude'])
    op.create_index('idx_drift_events_direction', 'drift_events', ['drift_direction'])
    
    # Composite index for common queries
    op.create_index(
        'idx_drift_events_session_timestamp', 
        'drift_events', 
        ['session_id', 'timestamp']
    )
    
    # Create indexes for response_adaptations
    op.create_index('idx_response_adaptations_drift_event', 'response_adaptations', ['drift_event_id'])
    op.create_index('idx_response_adaptations_session', 'response_adaptations', ['session_id'])
    op.create_index('idx_response_adaptations_strategy', 'response_adaptations', ['adaptation_strategy'])
    op.create_index('idx_response_adaptations_timestamp', 'response_adaptations', ['timestamp'])
    
    # Create session analytics view (materialized view for performance)
    op.execute("""
        CREATE MATERIALIZED VIEW session_analytics AS
        SELECT 
            s.id as session_id,
            s.user_id,
            s.start_time,
            s.end_time,
            s.status,
            COUNT(m.id) as message_count,
            COUNT(CASE WHEN m.role = 'user' THEN 1 END) as user_message_count,
            COUNT(CASE WHEN m.role = 'assistant' THEN 1 END) as assistant_message_count,
            AVG(sent.overall_sentiment) as avg_sentiment,
            MIN(sent.overall_sentiment) as min_sentiment,
            MAX(sent.overall_sentiment) as max_sentiment,
            STDDEV(sent.overall_sentiment) as sentiment_stddev,
            COUNT(de.id) as drift_events_count,
            COUNT(CASE WHEN de.drift_direction = 'negative' THEN 1 END) as negative_drift_count,
            COUNT(CASE WHEN de.drift_direction = 'positive' THEN 1 END) as positive_drift_count,
            MAX(de.drift_magnitude) as max_drift_magnitude
        FROM sessions s
        LEFT JOIN messages m ON s.id = m.session_id
        LEFT JOIN sentiment_scores sent ON m.id = sent.message_id
        LEFT JOIN drift_events de ON s.id = de.session_id
        GROUP BY s.id, s.user_id, s.start_time, s.end_time, s.status;
        
        CREATE UNIQUE INDEX idx_session_analytics_session_id 
        ON session_analytics (session_id);
    """)


def downgrade() -> None:
    # Drop materialized view
    op.execute("DROP MATERIALIZED VIEW IF EXISTS session_analytics")
    
    # Drop tables
    op.drop_table('response_adaptations')
    op.drop_table('drift_events')
