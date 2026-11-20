"""add paid motorcycle slot purchases

Revision ID: f1a7c8d9e2b4
Revises: 3bd312529c96
Create Date: 2026-11-20
"""
from alembic import op
import sqlalchemy as sa


revision = "f1a7c8d9e2b4"
down_revision = "3bd312529c96"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "users",
        sa.Column("extra_motorcycle_slots", sa.Integer(), nullable=False, server_default="0"),
    )
    # Preserve each existing user's current garage size.
    op.execute(sa.text(
        "UPDATE users SET extra_motorcycle_slots = "
        "(SELECT CASE WHEN COUNT(*) > 1 THEN COUNT(*) - 1 ELSE 0 END "
        "FROM motorcycles WHERE motorcycles.owner_id = users.id)"
    ))
    op.create_table(
        "slot_purchases",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False, server_default="49"),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("paid_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_slot_purchases_user_id", "slot_purchases", ["user_id"])
    op.create_index("ix_slot_purchases_status", "slot_purchases", ["status"])


def downgrade():
    op.drop_index("ix_slot_purchases_status", table_name="slot_purchases")
    op.drop_index("ix_slot_purchases_user_id", table_name="slot_purchases")
    op.drop_table("slot_purchases")
    op.drop_column("users", "extra_motorcycle_slots")
