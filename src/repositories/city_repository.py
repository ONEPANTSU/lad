from src.models import City
from src.repositories.sqlalchemy_repository import SQLAlchemyRepository


class CityRepository(SQLAlchemyRepository):
    model_table = City
    model = model_table()
    __association_id_name = "city_id"