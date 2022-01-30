import asyncio
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    select,
    DateTime,
    ForeignKey,
    inspect,
)
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import datetime

metadata = MetaData()

user_table = Table(
    "cs_user",
    metadata,
    Column("user_id", Integer(), primary_key=True),
    Column("user_name", String(10), nullable=False, unique=True),
    Column("created_timestamp", DateTime, server_default=func.now()),
)

tweet_table = Table(
    "cs_tweet",
    metadata,
    Column(
        "tweet_id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sqlalchemy.text("uuid_generate_v4()"),
    ),
    Column("tweet", String(140), nullable=False),
    Column("created_timestamp", DateTime, server_default=func.now()),
    Column("user_id", Integer(), ForeignKey("cs_user.user_id"), nullable=False),
)


async def async_main():
    engine = create_async_engine(
        "postgresql+asyncpg://testuser:admin@127.0.0.1:54320/postgres",
        echo=True,
        future=True,
    )
    async with engine.connect() as connection:
        async with connection.begin():
            await connection.run_sync(metadata.drop_all)
            await connection.run_sync(metadata.create_all)

    await engine.dispose()

asyncio.run(async_main())
