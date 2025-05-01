from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from .auth import get_current_user
from .db import create_challenge, create_submission, get_submissions_by_student, get_challenge
from .models import ChallengeCreate, SubmissionCreate, PortfolioResponse
from .ai import evaluate_submission
from .payments import check_active_subscription

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def verify_subscription(user):
    # Assuming user payload has 'sub' as user id and 'role'
    user_id = user.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user token")
    # For demo, assume Stripe customer ID is same as user_id
    has_subscription = check_active_subscription(user_id)
    if not has_subscription:
        raise HTTPException(status_code=403, detail="Subscription required")
    return user

@app.post("/post-challenge")
async def post_challenge(challenge: ChallengeCreate, user=Depends(get_current_user)):
    if user.get("role") != "company":
        raise HTTPException(status_code=403, detail="Only companies can post challenges")
    await verify_subscription(user)
    data = {
        "title": challenge.title,
        "description": challenge.description,
        "posted_by": user.get("sub"),
    }
    created = create_challenge(data)
    return {"message": "Challenge posted", "challenge": created}

@app.post("/submit-challenge")
async def submit_challenge(submission: SubmissionCreate, user=Depends(get_current_user)):
    if user.get("role") != "student":
        raise HTTPException(status_code=403, detail="Only students can submit solutions")
    await verify_subscription(user)
    challenge = get_challenge(submission.challenge_id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    # Evaluate submission
    evaluation = evaluate_submission(submission.code, challenge["description"])
    data = {
        "code": submission.code,
        "student_id": user.get("sub"),
        "challenge_id": submission.challenge_id,
        "feedback": evaluation.get("feedback"),
        "score": evaluation.get("score"),
    }
    created = create_submission(data)
    return {"message": "Submission received", "submission": created, "evaluation": evaluation}

@app.get("/portfolio/{student_id}", response_model=PortfolioResponse)
async def get_portfolio(student_id: str):
    submissions = get_submissions_by_student(student_id)
    return {"submissions": submissions}
