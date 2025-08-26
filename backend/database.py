from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

# データベースURLを環境変数から取得（デフォルト値はローカル開発用）
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/uranai"
)

# Renderのデータベース接続文字列を修正（必要な場合）
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# モデルの定義
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP)
    plan = Column(String, default="free")
    tickets = Column(Integer, default=5)
    stripe_customer_id = Column(String, nullable=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    people = relationship("Person", back_populates="owner")
    divination_results = relationship("DivinationResult", back_populates="owner")

class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    nickname = Column(String)
    name_kana = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    birth_date = Column(Date, nullable=True)
    birth_time = Column(Time, nullable=True)
    birth_place = Column(String, nullable=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    owner = relationship("User", back_populates="people")

class DivinationResult(Base):
    __tablename__ = "divination_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    fortune_type = Column(String)
    request_data = Column(JSON)
    visual_result = Column(JSON)
    ai_text = Column(Text)
    created_at = Column(TIMESTAMP)

    owner = relationship("User", back_populates="divination_results")

Base.metadata.create_all(bind=engine)
