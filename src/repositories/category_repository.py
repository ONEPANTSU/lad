from src.models import Category
from src.repositories.sqlalchemy_repository import SQLAlchemyRepository


class CategoryRepository(SQLAlchemyRepository):
    model_table = Category
    model = model_table()
    __association_id_name = "category_id"