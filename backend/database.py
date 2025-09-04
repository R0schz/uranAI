from sqlalchemy import (
    create_engine, 
    Column, 
    Integer, 
    String, 
    ForeignKey, 
    TIMESTAMP,
    Date,
    Time,
    JSON,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from dotenv import load_dotenv

# .env.localファイルを読み込む（backendディレクトリから実行するため、相対パスに変更）
load_dotenv(dotenv_path='.env.local')

# SupabaseのPostgreSQL接続URL
DATABASE_URL = os.getenv(
    "DATABASE_URL"
)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ▼▼▼ モデルの定義を修正 ▼▼▼
class User(Base):
    __tablename__ = "users"
    # SupabaseのUUIDを保存するため、idをString型に変更
    user_id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=True)  # ソーシャルログインの場合はnull
    auth_provider = Column(String, default="email")  # email, google, x等
    plan_type = Column(String, default="Free")  # Free, Premium
    ticket_balance = Column(Integer, default=5)
    stripe_customer_id = Column(String, nullable=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    profiles = relationship("Profile", back_populates="owner")
    divination_results = relationship("DivinationResult", back_populates="owner")
    favorites = relationship("Favorite", back_populates="owner")

class Profile(Base):
    __tablename__ = "profiles"

    profile_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    nickname = Column(String)
    name_hiragana = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    birth_date = Column(Date, nullable=True)
    birth_time = Column(Time, nullable=True)
    birth_location_json = Column(JSON, nullable=True)  # 出生地の詳細情報をJSONで保存
    is_self_flag = Column(String, default="false")  # 自分自身のプロフィールかどうか
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    owner = relationship("User", back_populates="profiles")

class DivinationResult(Base):
    __tablename__ = "divination_results"

    id = Column(Integer, primary_key=True, index=True)
    # user_idもString型に変更
    user_id = Column(String, ForeignKey("users.user_id"))
    fortune_type = Column(String)
    request_data = Column(JSON)
    visual_result = Column(JSON)
    ai_text = Column(Text)
    created_at = Column(TIMESTAMP)

    owner = relationship("User", back_populates="divination_results")

class Favorite(Base):
    __tablename__ = "favorites"

    favorite_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    divination_result_json = Column(JSON)  # お気に入り登録した占い結果のJSON
    created_at = Column(TIMESTAMP)

    owner = relationship("User", back_populates="favorites")

# テーブル作成を有効化（順序を指定）
# Base.metadata.create_all(bind=engine)