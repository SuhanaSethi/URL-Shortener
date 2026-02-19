from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from .database import engine, SessionLocal
from .models import Base, URL
from .utils import encode_base62
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Request model
class ShortenRequest(BaseModel):
    long_url: str
    expiry_days: int | None = 7


# ----------------------------
# Create Short URL
# ----------------------------
@app.post("/api/v1/shorten")
def create_short_url(request: ShortenRequest, db: Session = Depends(get_db)):

    expiry_days = request.expiry_days or 7

    # Step 1: Create DB entry without short_code
    url = URL(
        long_url=request.long_url,
        expires_at=datetime.utcnow() + timedelta(days=expiry_days),
        click_count=0,
        last_accessed_at=None
    )

    db.add(url)
    db.commit()
    db.refresh(url)

    # Step 2: Generate short_code using ID
    short_code = encode_base62(url.id)
    url.short_code = short_code

    db.commit()

    return {
        "short_url": f"http://127.0.0.1:8000/{short_code}"
    }


# ----------------------------
# Redirect Endpoint
# ----------------------------
@app.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)):

    url = db.query(URL).filter(URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    # Expiry check
    if url.expires_at and datetime.utcnow() > url.expires_at:
        raise HTTPException(status_code=410, detail="Short URL expired")

    # Update analytics
    url.click_count += 1
    url.last_accessed_at = datetime.utcnow()
    db.commit()

    return RedirectResponse(url.long_url)


# ----------------------------
# Analytics Endpoint
# ----------------------------
@app.get("/api/v1/analytics/{short_code}")
def get_analytics(short_code: str, db: Session = Depends(get_db)):

    url = db.query(URL).filter(URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    return {
        "long_url": url.long_url,
        "short_code": url.short_code,
        "click_count": url.click_count,
        "created_at": url.created_at,
        "expires_at": url.expires_at,
        "last_accessed_at": url.last_accessed_at
    }
