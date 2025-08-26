from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import SessionLocal, DivinationResult
from .auth import get_current_user
from kerykeion import AstrologicalSubject
from numerology import Pythagorean
from .gemini import generate_narrative

router = APIRouter()

@router.post("/")
async def divine(fortune_type: str, request_data: dict, db: Session = Depends(SessionLocal), current_user: dict = Depends(get_current_user)):
    if fortune_type == "numerology":
        numbers = Pythagorean.calculate_numbers(request_data)
        visual_result = {"numbers": numbers}
    elif fortune_type == "horoscope":
        kr = AstrologicalSubject(request_data["birth_date"], request_data["birth_time"], request_data["birth_place"])
        chart = kr.get_chart()
        visual_result = {"chart": chart}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid fortune type")

    prompt = f"Based on the following results, generate a detailed narrative: {visual_result}"
    ai_text = generate_narrative(prompt)

    divination_result = DivinationResult(
        user_id=current_user.id,
        fortune_type=fortune_type,
        request_data=request_data,
        visual_result=visual_result,
        ai_text=ai_text
    )
    db.add(divination_result)
    db.commit()
    db.refresh(divination_result)

    return {"visual_result": visual_result, "ai_text": ai_text}
