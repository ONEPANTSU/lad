from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError

from src.database import Base, session_factory


class SQLAlchemyRepository:
    model_table: type = Base
    model: model_table = model_table()
    _association_id_name: str = "model_id"

    async def add(self, model: model_table) -> int | IntegrityError:
        try:
            async with session_factory() as session:
                model_id = await session.execute(
                    insert(self.model_table)
                    .values(**self.get_filled_fields(model))
                    .returning(self.model_table.id)
                )
                await session.commit()
            return model_id.scalar()
        except IntegrityError as error:
            return error

    async def find_by_id(self, model_id: int) -> model_table | Exception:
        try:
            async with session_factory() as session:
                models = await session.execute(
                    select(self.model_table).filter(self.model_table.id == model_id)
                )
            row = models.first()
            if row is not None:
                return row[0]
            else:
                return None
        except Exception as error:
            return error

    async def find_all(self) -> list[model_table] | None | Exception:
        try:
            async with session_factory() as session:
                models = await session.execute(select(self.model_table))
            rows = models.all()
            if len(rows) > 0:
                return [row[0] for row in rows]
            else:
                return None
        except Exception as error:
            return error

    async def find_by_filter(self, **kwargs) -> list[model_table] | None | Exception:
        try:
            async with session_factory() as session:
                models = await session.execute(
                    select(self.model_table).filter_by(**kwargs)
                )
            rows = models.all()
            if len(rows) > 0:
                return [row[0] for row in rows]
            else:
                return None
        except Exception as error:
            return error

    async def edit(self, model: model_table) -> None | IntegrityError:
        try:
            async with session_factory() as session:
                await session.execute(
                    update(self.model_table)
                    .values(**self.get_filled_fields(model))
                    .where(self.model_table.id == model.id)
                    .returning(self.model_table.id)
                )
                await session.commit()
        except IntegrityError as error:
            return error

    async def remove(self, model_id: int) -> None | IntegrityError:
        try:
            async with session_factory() as session:
                await session.execute(
                    delete(self.model_table).where(self.model_table.id == model_id)
                )
                await session.commit()
        except IntegrityError as error:
            return error

    async def remove_all(self) -> None | IntegrityError:
        try:
            async with session_factory() as session:
                await session.execute(delete(self.model_table))
                await session.commit()
        except IntegrityError as error:
            return error

    async def _add_association(
        self,
        model_id: int,
        association_table: Base,
        association_name: str,
        association_id: int,
        fields: dict = None,
    ) -> None | IntegrityError:
        try:
            async with session_factory() as session:
                values = {
                    self._association_id_name: model_id,
                    association_name: association_id,
                }
                if fields:
                    values.update(fields)
                await session.execute(insert(association_table).values(**values))
                await session.commit()
        except IntegrityError as error:
            return error

    @staticmethod
    def get_filled_fields(model: model_table) -> dict:
        return {
            column: value
            for column, value in model.get_dict().items()
            if value is not None
        }
