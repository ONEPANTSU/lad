from src.models import PriceType
from src.repositories.sqlalchemy_repository import SQLAlchemyRepository


class PriceTypeRepository(SQLAlchemyRepository):
    model_table = PriceType
    model = model_table()
    __association_id_name = "price_type_id"