from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models.annotated_types import created_at, int_pk, updated_at


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int_pk]
    name: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    cities: Mapped[list["City"] | None] = relationship(secondary="product_city")
    categories: Mapped[list["Category"] | None] = relationship(
        secondary="product_category"
    )
    characteristics: Mapped[list["Characteristic"] | None] = relationship(
        secondary="product_characteristic"
    )
    prices: Mapped[list["Price"] | None] = relationship(back_populates="product")

    def get_info(self):
        attrs_dict = super().get_dict()
        attrs_dict["cities"] = [city.name for city in self.cities]
        attrs_dict["categories"] = [category.name for category in self.categories]
        attrs_dict["characteristics"] = {
            characteristic.name: characteristic.value
            for characteristic in self.characteristics
        }
        attrs_dict["prices"] = [price.get_info() for price in self.prices]
        return attrs_dict


class ProductCity(Base):
    __tablename__ = "product_city"

    id: Mapped[int_pk]
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))


class City(Base):
    __tablename__ = "city"

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(unique=True)
    products: Mapped[list["Product"]] = relationship(
        secondary="product_city", back_populates="cities"
    )


class ProductCategory(Base):
    __tablename__ = "product_category"

    id: Mapped[int_pk]
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(unique=True)
    products: Mapped[list["Product"]] = relationship(
        secondary="product_category", back_populates="categories"
    )


class ProductCharacteristic(Base):
    __tablename__ = "product_characteristic"

    id: Mapped[int_pk]
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    characteristic_id: Mapped[int] = mapped_column(ForeignKey("characteristic.id"))


class Characteristic(Base):
    __tablename__ = "characteristic"

    id: Mapped[int_pk]
    name: Mapped[str]
    value: Mapped[str]


class PriceType(Base):
    __tablename__ = "price_type"

    id: Mapped[int_pk]
    name: Mapped[str]


class Price(Base):
    __tablename__ = "price"

    id: Mapped[int_pk]
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    price: Mapped[float]
    price_type_id: Mapped[int] = mapped_column(ForeignKey("price_type.id"))
    link: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    price_type: Mapped["PriceType"] = relationship(lazy="subquery")
    product: Mapped["Product"] = relationship(back_populates="prices")

    def get_info(self):
        attrs_dict = super().get_info()
        attrs_dict["price_type"] = self.price_type.name
        return attrs_dict
