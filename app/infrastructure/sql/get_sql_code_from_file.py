import aiofiles
from sqlalchemy import text


async def get_sql_code(filepath: str) -> str:
    async with aiofiles.open(filepath) as sql_file:
        sql_code = await sql_file.read()
    return sql_code