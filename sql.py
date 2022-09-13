import asyncio
import asyncpg

from config import host, PG_USER, PG_PASS


async def create_db():
    create_db_command = open("tables.sql", "r").read()

    conn: asyncpg.Connection = await asyncpg.connect(
        user=PG_USER,
        password=PG_PASS,
        host=host
    )

    await conn.execute(create_db_command)
    await conn.close()


async def create_pool():
    return await asyncpg.create_pool(
        user=PG_USER,
        password=PG_PASS,
        host=host
    )

if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(create_db())
    except Exception as e:
        print(e)
