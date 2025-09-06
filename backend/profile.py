from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import database
from .auth import get_current_user
from pydantic import BaseModel
import datetime
from typing import List

class PersonCreate(BaseModel):
    nickname: str
    name: str | None = None
    birthDate: str | None = None
    birthTime: str | None = None
    birthPlace: str | None = None

# APIからのレスポンスの型を定義
class ProfileResponse(BaseModel):
    profile_id: int
    user_id: str
    nickname: str
    name_hiragana: str | None
    gender: str | None
    birth_date: datetime.date | None
    birth_time: datetime.time | None
    birth_location_json: dict | None
    is_self_flag: bool

    class Config:
        orm_mode = True

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
        
@router.get("s/{user_id}", response_model=List[ProfileResponse])
def get_persons_by_user(user_id: str, db: Session = Depends(get_db)):
    """
    指定されたuser_idに紐づく全てのプロフィール情報を取得する
    """
    profiles = db.query(database.Profile).filter(database.Profile.user_id == user_id).all()
    if not profiles:
        return []
    
    # is_self_flagをbool型に変換
    for profile in profiles:
        profile.is_self_flag = str(profile.is_self_flag).lower() == 'true'
        
    return profiles

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_person(person_data: PersonCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    
    # ユーザーテーブルの確認処理
    db_user = db.query(database.User).filter(database.User.user_id == current_user['id']).first()
    if not db_user:
        db_user = database.User(
            user_id=current_user['id'],
            email=current_user.get('email'),
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

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

    # Profileオブジェクトの作成
    new_profile = database.Profile(
        nickname=person_data.nickname,
        name_hiragana=person_data.name,
        birth_date=birth_date_obj,
        birth_time=birth_time_obj,
        # birth_location_jsonの処理を追加する必要があるかもしれません
        user_id=db_user.user_id,
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow()
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    
    return {"profile_id": new_profile.profile_id}