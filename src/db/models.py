from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from src.db.database import Base


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key = True)
    user_name: Mapped[str] = mapped_column(String(20), nullable = False)
    email: Mapped[str] = mapped_column(String(30), unique=True, nullable = False)
    password: Mapped[str] = mapped_column(String(20), nullable = False)
    start_date: Mapped[int] = mapped_column(Integer, nullable = False)
    status: Mapped[bool] = mapped_column(Boolean, default = True)