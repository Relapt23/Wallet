import uuid
from datetime import datetime
from sqlalchemy import DateTime, func, Numeric
from decimal import Decimal
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Wallet(Base):
    __tablename__ = "wallet"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    wallet_uuid: Mapped[str] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0.00, nullable=False)
    date_created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
