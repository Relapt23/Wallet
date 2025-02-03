from decimal import Decimal
from pydantic import BaseModel, Field
from typing import Literal
from uuid import UUID


class WalletOperation(BaseModel):
    operationType: Literal["DEPOSIT", "WITHDRAW"]
    amount: Decimal = Field(gt=0)


class WalletResponse(BaseModel):
    wallet_uuid: UUID
    balance: Decimal
