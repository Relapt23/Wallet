from pydantic import BaseModel, conint
from typing import Literal
from uuid import UUID


class WalletOperation(BaseModel):
    operationType: Literal["DEPOSIT", "WITHDRAW"]
    amount: conint(gt=0)

class WalletResponse(BaseModel):
    wallet_uuid: UUID
    balance: int
