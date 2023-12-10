from src.models import Product, Price
from src.repositories import *


class ProductService:
    product_repository = ProductRepository()
    characteristic_repository = CharacteristicRepository()
    category_repository = CategoryRepository()
    city_repository = CityRepository()
    price_type_repository = PriceTypeRepository()
    price_repository = PriceRepository()

    async def get_all_products_info(self) -> list[Product]:
        return await self.product_repository.get_all_info()

    async def get_products_with_newest_price(self) -> Price:
        return await self.product_repository.get_with_newest_price()
