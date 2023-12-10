from src.models import Category, Characteristic, City, Price, PriceType, Product
from src.repositories import (
    CategoryRepository,
    CharacteristicRepository,
    CityRepository,
    PriceRepository,
    PriceTypeRepository,
    ProductRepository,
)


async def fill_tables_example() -> None:
    product_repository = ProductRepository()
    category_repository = CategoryRepository()
    city_repository = CityRepository()
    price_type_repository = PriceTypeRepository()
    price_repository = PriceRepository()
    cities = [
        await city_repository.add(City(name="Санкт-Петербург")),
        await city_repository.add(City(name="Самара")),
    ]
    category_id = await category_repository.add(Category(name="Книги"))
    price_types = [
        await price_type_repository.add(PriceType(name="Оптовая")),
        await price_type_repository.add(PriceType(name="Розничная")),
    ]
    characteristic_id = await CharacteristicRepository().add(
        Characteristic(name="Автор", value="Говард Филлипс Лавкрафт")
    )
    product_id = await product_repository.add(Product(name=f"Зов Ктулху"))
    await product_repository.add_city(product_id, cities[0])
    await product_repository.add_city(product_id, cities[1])
    await product_repository.add_category(product_id, category_id)
    await product_repository.add_characteristic(product_id, characteristic_id)
    await price_repository.add(
        Price(
            product_id=product_id,
            price=899.99,
            price_type_id=price_types[0],
            link="https://www.lad.ru/product/9785",
        )
    )
    await price_repository.add(
        Price(
            product_id=product_id,
            price=399.99,
            price_type_id=price_types[1],
            link="https://www.lad.ru/product/9785",
        )
    )

    product_id = await product_repository.add(Product(name=f"Стихи"))
    await product_repository.add_city(product_id, cities[1])
    await product_repository.add_category(product_id, category_id)
    await product_repository.add_characteristic(product_id, characteristic_id)

    await price_repository.add(
        Price(
            product_id=product_id,
            price=299.99,
            price_type_id=price_types[1],
            link="https://www.lad.ru/product/9787",
        )
    )
    await price_repository.add(
        Price(
            product_id=product_id,
            price=799.99,
            price_type_id=price_types[0],
            link="https://www.lad.ru/product/9787",
        )
    )
