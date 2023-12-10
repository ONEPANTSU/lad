from src.models import Price
from src.repositories.sqlalchemy_repository import SQLAlchemyRepository


class PriceRepository(SQLAlchemyRepository):
    model_table = Price
    model = model_table()
    __association_id_name = "price_id"