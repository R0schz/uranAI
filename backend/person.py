from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import database
from .auth import get_current_user
from pydantic import BaseModel
import datetime

class PersonCreate(BaseModel):
    nickname: str
    name: str | None = None
    birthDate: str | None = None
    birthTime: str | None = None
    birthPlace: str | None = None

router = APIRouter(
    prefix="/person",
    tags=["person"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_person(person_data: PersonCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    
    # ▼▼▼ usersテーブルにユーザーが存在するか確認・作成する処理を追加 ▼▼▼
    db_user = db.query(database.User).filter(database.User.id == current_user.id).first()
    if not db_user:
        db_user = database.User(
            id=current_user.id,
            email=current_user.email,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    # 日付と時刻の変換処理（変更なし）
    birth_date_obj = None
    if person_data.birthDate:
        try:
            birth_date_obj = datetime.date.fromisoformat(person_data.birthDate)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format for birthDate. Use YYYY-MM-DD.")

    birth_time_obj = None
    if person_data.birthTime:
        try:
            birth_time_obj = datetime.time.fromisoformat(person_data.birthTime)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid time format for birthTime. Use HH:MM or HH:MM:SS.")

    # Personオブジェクトの作成（user_idに認証ユーザーのIDをセット）
    new_person = database.Person(
        nickname=person_data.nickname,
        name_kana=person_data.name,
        birth_date=birth_date_obj,
        birth_time=birth_time_obj,
        birth_place=person_data.birthPlace,
        user_id=db_user.id, # 確実に存在するユーザーのIDをセット
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow()
    )
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    
    return {"id": new_person.id}