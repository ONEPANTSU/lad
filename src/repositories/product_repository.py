from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from src.database import session_factory
from src.models import *
from src.models.product_models import (
    ProductCategory,
    ProductCharacteristic,
    ProductCity,
)
from src.repositories.sqlalchemy_repository import SQLAlchemyRepository


class ProductRepository(SQLAlchemyRepository):
    model_table = Product
    model = model_table()
    _association_id_name = "product_id"

    async def get_all_info(self):
        query = select(self.model_table).options(
            selectinload(self.model_table.cities),
            selectinload(self.model_table.categories),
            selectinload(self.model_table.characteristics),
            selectinload(self.model_table.prices),
        )
        async with session_factory() as session:
            result = await session.execute(query)
        return result.unique().scalars().all()

    async def get_with_newest_price(self):
        async with session_factory() as session:
            latest_price_subq = (
                select(Price.product_id, func.max(Price.updated_at).label("max_date"))
                .group_by(Price.product_id)
                .subquery()
            )

            result = await session.execute(
                select(self.model_table.id, self.model_table.name, Price.price, PriceType.name)
                .join(latest_price_subq, self.model_table.id == latest_price_subq.c.product_id)
                .join(Price, self.model_table.id == Price.product_id)
                .filter(latest_price_subq.c.max_date == Price.updated_at)
                .join(PriceType, Price.price_type_id == PriceType.id)
            )
            return result.all()

    async def add_city(self, product_id: int, city_id: int) -> None | IntegrityError:
        try:
            await self._add_association(
                model_id=product_id,
                association_table=ProductCity,
                association_name="city_id",
                association_id=city_id,
            )
        except IntegrityError as error:
            return error

    async def add_category(
        self, product_id: int, category_id: int
    ) -> None | IntegrityError:
        try:
            await self._add_association(
                model_id=product_id,
                association_table=ProductCategory,
                association_name="category_id",
                association_id=category_id,
            )
        except IntegrityError as error:
            return error

    async def add_characteristic(
        self, product_id: int, characteristic_id: int
    ) -> None | IntegrityError:
        try:
            await self._add_association(
                model_id=product_id,
                association_table=ProductCharacteristic,
                association_name="characteristic_id",
                association_id=characteristic_id,
            )
        except IntegrityError as error:
            return error
