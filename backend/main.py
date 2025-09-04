from dotenv import load_dotenv

# .env.localファイルを明示的に読み込む
load_dotenv(dotenv_path='.env.local')

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
import json

from database import SessionLocal, User, Profile, DivinationResult, Favorite
from auth import get_current_user_id
from divination_service import DivinationService

app = FastAPI(title="uranAI Backend", version="1.0.0")

# 占いサービスを初期化
divination_service = DivinationService()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# データベースセッションの依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Welcome to uranAI backend!"}

# ユーザー管理API
@app.post("/users/", response_model=dict)
async def create_user(
    user_data: dict,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """ユーザー情報を作成または更新"""
    try:
        # 既存のユーザーを確認
        existing_user = db.query(User).filter(User.id == current_user_id).first()
        
        if existing_user:
            # 既存ユーザーの更新
            for key, value in user_data.items():
                if hasattr(existing_user, key):
                    setattr(existing_user, key, value)
            existing_user.updated_at = datetime.utcnow()
            db.commit()
            return {"message": "User updated successfully", "user_id": current_user_id}
        else:
            # 新規ユーザーの作成
            new_user = User(
                user_id=current_user_id,
                email=user_data.get("email", ""),
                plan_type=user_data.get("plan_type", "Free"),
                ticket_balance=user_data.get("ticket_balance", 5),
                auth_provider=user_data.get("auth_provider", "email"),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(new_user)
            db.commit()
            return {"message": "User created successfully", "user_id": current_user_id}
            
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/me", response_model=dict)
async def get_current_user(
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """現在のユーザー情報を取得"""
    user = db.query(User).filter(User.user_id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "user_id": user.user_id,
        "email": user.email,
        "plan_type": user.plan_type,
        "ticket_balance": user.ticket_balance,
        "auth_provider": user.auth_provider,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }

# プロフィール管理API
@app.post("/profiles/", response_model=dict)
async def create_profile(
    profile_data: dict,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """プロフィール情報を作成"""
    try:
        print(f"Creating profile with data: {profile_data}")  # デバッグログ
        print(f"Current user ID: {current_user_id}")        # デバッグログ
        
        # ユーザーが存在するかチェックし、存在しない場合は作成
        user = db.query(User).filter(User.user_id == current_user_id).first()
        if not user:
            print(f"User not found, creating new user with ID: {current_user_id}")  # デバッグログ
            new_user = User(
                user_id=current_user_id,
                email="",  # 後で更新可能
                plan_type="Free",
                ticket_balance=5,
                auth_provider="email",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(new_user)
            db.commit()
            print(f"New user created successfully")  # デバッグログ
        
        # デフォルト値の設定
        birth_time = profile_data.get("birth_time") or "12:00"
        birth_location_json = profile_data.get("birth_location_json") or {"place": "東京都中央区"}
        
        new_profile = Profile(
            user_id=current_user_id,
            nickname=profile_data.get("nickname", ""),
            name_hiragana=profile_data.get("name_hiragana"),
            gender=profile_data.get("gender"),
            birth_date=profile_data.get("birth_date"),
            birth_time=birth_time,
            birth_location_json=birth_location_json,
            is_self_flag=profile_data.get("is_self_flag", False),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        print(f"Profile object created: {new_profile}")  # デバッグログ
        
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        
        print(f"Profile saved successfully with ID: {new_profile.profile_id}")  # デバッグログ
        
        return {
            "message": "Profile created successfully",
            "profile_id": new_profile.profile_id,
            "profile": {
                "profile_id": new_profile.profile_id,
                "nickname": new_profile.nickname,
                "name_hiragana": new_profile.name_hiragana,
                "gender": new_profile.gender,
                "birth_date": str(new_profile.birth_date) if new_profile.birth_date else None,
                "birth_time": str(new_profile.birth_time) if new_profile.birth_time else None,
                "birth_location_json": new_profile.birth_location_json,
                "is_self_flag": new_profile.is_self_flag,
                "created_at": new_profile.created_at,
                "updated_at": new_profile.updated_at
            }
        }
        
    except Exception as e:
        db.rollback()
        print(f"Error creating profile: {e}")  # デバッグログ
        print(f"Error type: {type(e)}")       # エラーの型
        import traceback
        print(f"Traceback: {traceback.format_exc()}")  # スタックトレース
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/profiles/", response_model=List[dict])
async def get_profiles(
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """ユーザーのプロフィール一覧を取得"""
    print(f"Getting profiles for user: {current_user_id}")
    profiles = db.query(Profile).filter(Profile.user_id == current_user_id).all()
    print(f"Found {len(profiles)} profiles")
    
    return [
        {
            "profile_id": profile.profile_id,
            "nickname": profile.nickname,
            "name_hiragana": profile.name_hiragana,
            "gender": profile.gender,
            "birth_date": str(profile.birth_date) if profile.birth_date else None,
            "birth_time": str(profile.birth_time) if profile.birth_time else None,
            "birth_location_json": profile.birth_location_json,
            "is_self_flag": profile.is_self_flag,
            "created_at": profile.created_at,
            "updated_at": profile.updated_at
        }
        for profile in profiles
    ]

@app.put("/profiles/{profile_id}", response_model=dict)
async def update_profile(
    profile_id: int,
    profile_data: dict,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """プロフィール情報を更新"""
    profile = db.query(Profile).filter(
        Profile.profile_id == profile_id,
        Profile.user_id == current_user_id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    try:
        for key, value in profile_data.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        profile.updated_at = datetime.utcnow()
        db.commit()
        
        return {"message": "Profile updated successfully", "profile_id": profile_id}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/profiles/{profile_id}")
async def delete_profile(
    profile_id: int,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """プロフィール情報を削除"""
    profile = db.query(Profile).filter(
        Profile.profile_id == profile_id,
        Profile.user_id == current_user_id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    try:
        db.delete(profile)
        db.commit()
        return {"message": "Profile deleted successfully"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# 占い結果管理API
@app.post("/divination-results/", response_model=dict)
async def create_divination_result(
    result_data: dict,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """占い結果を作成"""
    try:
        # 占い結果を生成
        request_data = result_data.get("request_data", {})
        divination_result = divination_service.generate_divination_result(request_data)
        
        # データベースに保存
        new_result = DivinationResult(
            user_id=current_user_id,
            fortune_type=result_data.get("fortune_type"),
            request_data=request_data,
            visual_result=divination_result.get("visual_result", {}),
            ai_text=divination_result.get("ai_analysis", ""),
            created_at=datetime.utcnow()
        )
        db.add(new_result)
        db.commit()
        db.refresh(new_result)
        
        return {
            "message": "Divination result created successfully",
            "result_id": new_result.id,
            "divination_result": divination_result
        }
        
    except Exception as e:
        db.rollback()
        print(f"占い結果作成エラー: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/divination-results/", response_model=List[dict])
async def get_divination_results(
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """ユーザーの占い結果一覧を取得"""
    results = db.query(DivinationResult).filter(
        DivinationResult.user_id == current_user_id
    ).order_by(DivinationResult.created_at.desc()).all()
    
    return [
        {
            "id": result.id,
            "fortune_type": result.fortune_type,
            "request_data": result.request_data,
            "visual_result": result.visual_result,
            "ai_text": result.ai_text,
            "created_at": result.created_at
        }
        for result in results
    ]

@app.get("/divination-results/{result_id}", response_model=dict)
async def get_divination_result(
    result_id: int,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """特定の占い結果を取得"""
    result = db.query(DivinationResult).filter(
        DivinationResult.id == result_id,
        DivinationResult.user_id == current_user_id
    ).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Divination result not found")
    
    return {
        "id": result.id,
        "fortune_type": result.fortune_type,
        "request_data": result.request_data,
        "visual_result": result.visual_result,
        "ai_text": result.ai_text,
        "created_at": result.created_at
    }