"""Initial migration.

Revision ID: 819cbf6e030b
Revises:
Create Date: 2023-01-13 16:53:05.484024

"""

import sqlalchemy as sa
from alembic import op

revision = "819cbf6e030b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "accounts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("iban", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("country", sa.String(length=255), nullable=False),
        sa.Column("balance", sa.DECIMAL(precision=20, scale=2), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("iban"),
    )
    op.create_index(op.f("ix_accounts_id"), "accounts", ["id"], unique=False)
    op.create_table(
        "transactions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("amount", sa.DECIMAL(precision=20, scale=2), nullable=False),
        sa.Column("source_account_iban", sa.String(length=255), nullable=False),
        sa.Column("target_account_iban", sa.String(length=255), nullable=False),
        sa.Column("target_bic", sa.String(), nullable=False),
        sa.Column("reference", sa.String(), nullable=False),
        sa.Column("recipient_name", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["source_account_iban"],
            ["accounts.iban"],
        ),
        sa.ForeignKeyConstraint(
            ["target_account_iban"],
            ["accounts.iban"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_transactions_id"), "transactions", ["id"], unique=False)
    op.create_index(
        op.f("ix_transactions_source_account_iban"),
        "transactions",
        ["source_account_iban"],
        unique=False,
    )
    op.create_index(
        op.f("ix_transactions_target_account_iban"),
        "transactions",
        ["target_account_iban"],
        unique=False,
    )
    op.create_table(
        "transfer_logs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("transaction_id", sa.Uuid(), nullable=True),
        sa.Column(
            "transfer_status",
            sa.Enum("SUCCESS", "FAILED", name="transferstatus"),
            nullable=False,
        ),
        sa.Column(
            "transfer_fail_reason",
            sa.Enum(
                "INSUFFICIENT_FUNDS",
                "INVALID_ACCOUNT",
                "UNKNOWN",
                name="transferfailreason",
            ),
            nullable=True,
        ),
        sa.Column("transfer_request", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["transaction_id"],
            ["transactions.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_transfer_logs_id"), "transfer_logs", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_transfer_logs_id"), table_name="transfer_logs")
    op.drop_table("transfer_logs")
    op.drop_index(
        op.f("ix_transactions_target_account_iban"), table_name="transactions"
    )
    op.drop_index(
        op.f("ix_transactions_source_account_iban"), table_name="transactions"
    )
    op.drop_index(op.f("ix_transactions_id"), table_name="transactions")
    op.drop_table("transactions")
    op.drop_index(op.f("ix_accounts_id"), table_name="accounts")
    op.drop_table("accounts")
