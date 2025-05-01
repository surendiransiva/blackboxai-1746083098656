import stripe
from fastapi import HTTPException
from .config import settings

stripe.api_key = settings.STRIPE_API_KEY

def check_active_subscription(customer_id: str) -> bool:
    try:
        subscriptions = stripe.Subscription.list(customer=customer_id, status='active', limit=1)
        return len(subscriptions.data) > 0
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")
