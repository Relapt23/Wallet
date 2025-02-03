from uuid import uuid4
import pytest
from app.api.models.models import Base
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.main import app
from app.api.v1.endpoints.wallet import get_session


@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", connect_args={"check_same_thread": False})
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
async def run_before_and_after_tests(test_engine):
    async_session = async_sessionmaker(bind=test_engine, expire_on_commit=False, autocommit=False, autoflush=False)

    async def get_session_override():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_session] = get_session_override
    yield


@pytest.fixture
async def client(run_before_and_after_tests):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_deposit_to_new_wallet(client):
    test_uuid = uuid4()
    response = await client.post(
        f"/api/v1/wallets/{test_uuid}/operation",
        json={"operationType": "DEPOSIT", "amount": 1000},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["wallet_uuid"] == str(test_uuid)
    assert data["balance"] == 1000


@pytest.mark.asyncio
async def test_withdraw_to_new_wallet(client):
    test_uuid = uuid4()
    await client.post(
        f"/api/v1/wallets/{test_uuid}/operation",
        json={"operationType": "DEPOSIT", "amount": 1000},
    )

    response = await client.post(
        f"/api/v1/wallets/{test_uuid}/operation",
        json={"operationType": "WITHDRAW", "amount": 500},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["wallet_uuid"] == str(test_uuid)
    assert data["balance"] == 500


@pytest.mark.asyncio
async def test_get_balance(client):
    test_uuid = uuid4()

    deposit_response = await client.post(
        f"/api/v1/wallets/{test_uuid}/operation",
        json={"operationType": "DEPOSIT", "amount": 2000},
    )
    assert deposit_response.status_code == 200

    response = await client.get(f"/api/v1/wallets/{test_uuid}")
    assert response.status_code == 200
    data = response.json()
    assert data["wallet_uuid"] == str(test_uuid)
    assert data["balance"] == 2000


@pytest.mark.asyncio
async def test_insufficient_funds(client):
    test_uuid = uuid4()
    await client.post(
        f"/api/v1/wallets/{test_uuid}/operation",
        json={"operationType": "DEPOSIT", "amount": 1500},
    )

    response = await client.post(
        f"/api/v1/wallets/{test_uuid}/operation",
        json={"operationType": "WITHDRAW", "amount": 2000},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Insufficient funds"


@pytest.mark.asyncio
async def test_wallet_not_found(client):
    test_uuid = uuid4()
    response = await client.get(f"/api/v1/wallets/{test_uuid}")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Wallet not found"
