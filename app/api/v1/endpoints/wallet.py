from fastapi import APIRouter, Depends
from app.api.models.schemas import WalletOperation, WalletResponse, UUID
from app.services.wallet_services import deposit, withdraw, get_balance
from app.core.db import sess
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()

async def get_session():
    async with sess() as session:
        yield session


@router.post("/wallets/{wallet_uuid}/operation", response_model=WalletResponse)
async def change_balance(wallet_uuid: UUID, operation: WalletOperation, session: AsyncSession = Depends(get_session)):
        if operation.operationType == "DEPOSIT":
            new_balance = await deposit(wallet_uuid, operation.amount, session)
        else:
            new_balance = await withdraw(wallet_uuid, operation.amount, session)

        return WalletResponse(wallet_uuid=wallet_uuid, balance=new_balance)

@router.get("/wallets/{wallet_uuid}", response_model=WalletResponse)
async def wallet_balance(wallet_uuid: UUID, session: AsyncSession = Depends(get_session)):
    balance = await get_balance(wallet_uuid, session)

    return WalletResponse(wallet_uuid=wallet_uuid, balance=balance)
