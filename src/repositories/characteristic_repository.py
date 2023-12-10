from src.models import Characteristic
from src.repositories.sqlalchemy_repository import SQLAlchemyRepository


class CharacteristicRepository(SQLAlchemyRepository):
    model_table = Characteristic
    model = model_table()
    __association_id_name = "characteristic_id"