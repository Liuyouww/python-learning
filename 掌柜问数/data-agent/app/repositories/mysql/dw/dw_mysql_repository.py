from sqlalchemy import text

from sqlalchemy.ext.asyncio import AsyncSession


class DWMySQLRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_column_types(self, table_name) -> dict[str:str]:
        sql = f'show columns from {table_name}'
        result = await self.session.execute(text(sql))
        result_dict = result.mappings().fetchall()  # [{Field:order_id,Type:varchar(30),Null:No,},{}]
        return {row['Field']: row['Type'] for row in result_dict}  # {order_id:varchar(30)}

    async def get_column_values(self, table_name, column_name, limit=10) -> list[str]:
        sql = f'select distinct {column_name} from {table_name} limit {limit}'
        result = await self.session.execute(text(sql))
        return [row[0] for row in result.fetchall()]

    async def get_db_info(self):
        sql = 'select version()'
        result = await self.session.execute(text(sql))
        version = result.scalar()  # 只有一个值的时候使用scalar(),只有一列或一排输出为列表的，使用scalars

        dialect = self.session.bind.dialect.name
        return {'version': version, 'dialect': dialect}

    async def validate(self,sql:str):
        sql = f"explain {sql}"
        await self.session.execute(text(sql))

    async def run(self, sql:str) -> list[dict]:
        result = await self.session.execute(text(sql))
        return [dict(row) for row in result.mappings().fetchall()]