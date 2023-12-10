import asyncio

from db_filling_example import fill_tables_example
from src.database import init_database
from src.service.product_service import ProductService


def main():
    init_database()
    service = ProductService()
    asyncio.run(fill_tables_example())
    result = asyncio.run(service.get_products_with_newest_price())
    print("Перечень всех товаров с их новейшей ценой:\n", result)
    result = asyncio.run(service.get_all_products_info())
    print("\nПолная информация о товарах:\n", result)


if __name__ == "__main__":
    main()
