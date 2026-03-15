"""Initial migration - create all tables

Revision ID: 001_initial
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum type for organization types
    org_type_enum = sa.Enum('school', 'kindergarten', 'additional_education', name='organizationtype')
    org_type_enum.create(op.get_bind())
    
    # Organizations table
    op.create_table(
        'organizations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('inn', sa.String(length=12), nullable=False),
        sa.Column('name', sa.String(length=500), nullable=True),
        sa.Column('type', org_type_enum, nullable=False, default='school'),
        sa.Column('region', sa.String(length=200), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_organizations_id'), 'organizations', ['id'], unique=False)
    op.create_index(op.f('ix_organizations_inn'), 'organizations', ['inn'], unique=True)
    
    # Heads table
    op.create_table(
        'heads',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_name', sa.String(length=300), nullable=True),
        sa.Column('organization_id', sa.Integer(), nullable=True),
        sa.Column('last_test_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_results', sa.JSON(), nullable=True),
        sa.Column('is_candidate', sa.Boolean(), nullable=True),
        sa.Column('candidate_login', sa.String(length=100), nullable=True),
        sa.Column('candidate_password', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_heads_id'), 'heads', ['id'], unique=False)
    
    # Test sessions table
    op.create_table(
        'test_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('head_id', sa.Integer(), nullable=False),
        sa.Column('organization_id', sa.Integer(), nullable=True),
        sa.Column('test_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('answers', sa.JSON(), nullable=False),
        sa.Column('scores', sa.JSON(), nullable=True),
        sa.Column('case_answers', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['head_id'], ['heads.id'], ),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_test_sessions_id'), 'test_sessions', ['id'], unique=False)
    
    # Admin users table
    op.create_table(
        'admin_users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=False),
        sa.Column('hashed_password', sa.String(length=200), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_admin_users_id'), 'admin_users', ['id'], unique=False)
    op.create_index(op.f('ix_admin_users_username'), 'admin_users', ['username'], unique=True)
    
    # Prompt templates table
    op.create_table(
        'prompt_templates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=False),
        sa.Column('organization_type', sa.String(length=50), nullable=True),
        sa.Column('template_text', sa.Text(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_prompt_templates_id'), 'prompt_templates', ['id'], unique=False)
    
    # Model settings table
    op.create_table(
        'model_settings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('model_name', sa.String(length=100), nullable=False),
        sa.Column('parameters', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_model_settings_id'), 'model_settings', ['id'], unique=False)
    
    # Embedding models table
    op.create_table(
        'embedding_models',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('model_name', sa.String(length=200), nullable=False),
        sa.Column('model_type', sa.String(length=50), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_embedding_models_id'), 'embedding_models', ['id'], unique=False)
    
    # Similarity thresholds table
    op.create_table(
        'similarity_thresholds',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('threshold', sa.Float(), nullable=True),
        sa.Column('description', sa.String(length=300), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_similarity_thresholds_id'), 'similarity_thresholds', ['id'], unique=False)
    
    # Normative documents table
    op.create_table(
        'normative_documents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('organization_type', sa.String(length=50), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('file_path', sa.String(length=300), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_normative_documents_id'), 'normative_documents', ['id'], unique=False)
    
    # Generated questions table
    op.create_table(
        'generated_questions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=False),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('answer_variants', sa.JSON(), nullable=True),
        sa.Column('correct_answer', sa.String(length=500), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('organization_type', sa.String(length=50), nullable=True),
        sa.Column('generated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_generated_questions_id'), 'generated_questions', ['id'], unique=False)
    
    # Case templates table
    op.create_table(
        'case_templates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('organization_type', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=300), nullable=True),
        sa.Column('template_text', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_case_templates_id'), 'case_templates', ['id'], unique=False)
    
    # Generated cases table
    op.create_table(
        'generated_cases',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('organization_type', sa.String(length=50), nullable=False),
        sa.Column('case_text', sa.Text(), nullable=False),
        sa.Column('ai_answer', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('generated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_generated_cases_id'), 'generated_cases', ['id'], unique=False)
    
    # Cluster results table
    op.create_table(
        'cluster_results',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cluster_name', sa.String(length=200), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('heads_data', sa.JSON(), nullable=True),
        sa.Column('avg_scores', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cluster_results_id'), 'cluster_results', ['id'], unique=False)
    
    # Testing schedules table
    op.create_table(
        'testing_schedules',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('organization_inn', sa.String(length=12), nullable=True),
        sa.Column('candidate_name', sa.String(length=300), nullable=True),
        sa.Column('test_date', sa.Date(), nullable=False),
        sa.Column('test_time', sa.Time(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_testing_schedules_id'), 'testing_schedules', ['id'], unique=False)
    
    # Association table for case templates and documents
    op.create_table(
        'case_template_documents',
        sa.Column('case_template_id', sa.Integer(), nullable=True),
        sa.Column('document_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['case_template_id'], ['case_templates.id'], ),
        sa.ForeignKeyConstraint(['document_id'], ['normative_documents.id'], )
    )


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('case_template_documents')
    op.drop_table('testing_schedules')
    op.drop_table('cluster_results')
    op.drop_table('generated_cases')
    op.drop_table('case_templates')
    op.drop_table('generated_questions')
    op.drop_table('normative_documents')
    op.drop_table('similarity_thresholds')
    op.drop_table('embedding_models')
    op.drop_table('model_settings')
    op.drop_table('prompt_templates')
    op.drop_table('admin_users')
    op.drop_table('test_sessions')
    op.drop_table('heads')
    op.drop_table('organizations')
    
    # Drop enum type
    op.execute('DROP TYPE IF EXISTS organizationtype')
