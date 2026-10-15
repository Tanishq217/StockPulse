"""create initial inventory schema

Revision ID: 001_initial_inventory_schema
Revises:
Create Date: 2026-10-15 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "001_initial_inventory_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        "inventory_items",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("sku", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("min_threshold", sa.Integer(), nullable=False, server_default="10"),
        sa.Column("unit_price", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("supplier", sa.String(length=150), nullable=True),
        sa.Column("location", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(op.f("ix_inventory_items_id"), "inventory_items", ["id"], unique=False)
    op.create_index(op.f("ix_inventory_items_sku"), "inventory_items", ["sku"], unique=True)
    op.create_index(op.f("ix_inventory_items_name"), "inventory_items", ["name"], unique=False)
    op.create_index(op.f("ix_inventory_items_category"), "inventory_items", ["category"], unique=False)

def downgrade() -> None:
    op.drop_index(op.f("ix_inventory_items_category"), table_name="inventory_items")
    op.drop_index(op.f("ix_inventory_items_name"), table_name="inventory_items")
    op.drop_index(op.f("ix_inventory_items_sku"), table_name="inventory_items")
    op.drop_index(op.f("ix_inventory_items_id"), table_name="inventory_items")
    op.drop_table("inventory_items")
