import stripe
from fastapi import APIRouter, HTTPException

stripe.api_key = "sk_test_51S0PU7AyQzk81ZkIaFYzuT2UtnY4WnjZ1vfRotTP24swQO0t7BwaecM8Ofeb0msIONwO2umjKTkJiG2hNDk8aNSd00swKNebXV"

router = APIRouter()

@router.post("/create-checkout-session")
async def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "Premium Plan",
                    },
                    "unit_amount": 3000,
                },
                "quantity": 1,
            }],
            mode="subscription",
            success_url="https://yourdomain.com/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://yourdomain.com/cancel",
        )
        return {"id": session.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
