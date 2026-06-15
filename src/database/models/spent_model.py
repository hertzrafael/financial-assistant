from database.base import Base

from sqlalchemy import String, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime


class SpentModel(Base):

    __tablename__ = 'spent'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(80))
    shop_name: Mapped[str] = mapped_column(String(60))
    cost: Mapped[float] = mapped_column(Numeric(10, 2))
    category: Mapped[str] = mapped_column(String(60))
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"SpentModel(id={self.id}, user_id='{self.user_id}', shop_name='{self.shop_name}', cost={self.cost}, category='{self.category}', date='{self.date}')"
