from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from backend.database import Base
from datetime import datetime, timedelta

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

    click_count = Column(Integer, default=0)
    last_accessed_at = Column(DateTime, nullable=True)
