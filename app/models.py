from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


class Category(Base):
    __tablename__ = "categories"          
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    tasks = relationship("Task", back_populates="category")



class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    status = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    category = relationship("Category", back_populates="tasks")