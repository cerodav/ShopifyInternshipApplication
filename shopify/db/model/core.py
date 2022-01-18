from datetime import datetime
from sqlalchemy import Column, String, Integer, Date, PrimaryKeyConstraint, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Enum as SQLAlchemyEnumType
from shopify.db.model.enumType import InventoryType

Base = declarative_base()

class Inventory(Base):
    __tablename__ = 'inventory'
    __table_args__ = (
        PrimaryKeyConstraint('inventoryId'),
    )
    inventoryId = Column(Integer)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    type = Column(SQLAlchemyEnumType(InventoryType), nullable=False)
    description = Column(String)
    supplier = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    createdTime = Column(Date, default=datetime.now())
    modifiedTime = Column(Date, default=datetime.now())