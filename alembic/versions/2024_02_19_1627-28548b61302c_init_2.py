"""init 2

Revision ID: 28548b61302c
Revises: ffd63e3c2ef4
Create Date: 2024-02-19 16:27:21.295309

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "28548b61302c"
down_revision: Union[str, None] = "ffd63e3c2ef4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "products",
        sa.Column(
            "type",
            sa.Enum(
                "PRODUCT",
                "SERVICE",
                "OPERATION",
                "MATERIAL",
                "EQUIPMENT",
                name="producttypes",
            ),
            nullable=False,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("products", "type")
    # ### end Alembic commands ###
