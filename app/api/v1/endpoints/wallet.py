from fastapi import APIRouter
from app.api.models.schemas import WalletOperation, WalletResponse, UUID
from app.services.wallet_services import deposit, withdraw, get_balance


router = APIRouter()

@router.post("/wallets/{wallet_uuid}/operation", response_model=WalletResponse)
async def change_balance(wallet_uuid: UUID, operation: WalletOperation):
        if operation.operationType == "DEPOSIT":
            new_balance = await deposit(wallet_uuid, operation.amount)
        else:
            new_balance = await withdraw(wallet_uuid, operation.amount)

        return WalletResponse(wallet_uuid=wallet_uuid, balance=new_balance)

@router.get("/wallets/{wallet_uuid}", response_model=WalletResponse)
async def wallet_balance(wallet_uuid: UUID):
    balance = await get_balance(wallet_uuid)

    return WalletResponse(wallet_uuid=wallet_uuid, balance=balance)
