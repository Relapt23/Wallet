from app.api.models.models import Wallet
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, HTTPException
from uuid import UUID
from decimal import Decimal


async def deposit(wallet_uuid: UUID, amount: Decimal, session: AsyncSession) -> Decimal:
    response = await session.execute(select(Wallet).where(Wallet.wallet_uuid == wallet_uuid).with_for_update())
    wallet = response.scalar_one_or_none()
    if not wallet:
        wallet = Wallet(wallet_uuid=wallet_uuid, balance=amount)
        session.add(wallet)
        await session.commit()
        await session.refresh(wallet)
        return wallet.balance
    else:
        wallet.balance += amount
        session.add(wallet)
        await session.commit()
        await session.refresh(wallet)
        return wallet.balance


async def withdraw(wallet_uuid: UUID, amount: Decimal, session: AsyncSession) -> Decimal:
    response = await session.execute(select(Wallet).where(Wallet.wallet_uuid == wallet_uuid).with_for_update())
    wallet = response.scalar_one_or_none()
    if not wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")

    if wallet.balance < amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds")

    wallet.balance -= amount
    session.add(wallet)

    await session.commit()
    await session.refresh(wallet)
    return wallet.balance


async def get_balance(wallet_uuid: UUID, session: AsyncSession):
    response = await session.execute(select(Wallet).where(Wallet.wallet_uuid == wallet_uuid))
    wallet = response.scalar_one_or_none()
    if not wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")

    return wallet.balance
