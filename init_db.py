import asyncio
from app.db.models import Base
from app.db.database import engine

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init())
    print("✅ Database (orders + users) created.")