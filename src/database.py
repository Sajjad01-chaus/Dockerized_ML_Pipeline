from sqlalchemy import create_engine, Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pandas as pd
from src.config import config

Base = declarative_base()

class GeneratedData(Base):
    __tablename__ = "generated_data"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    category = Column(String)
    tags = Column(JSON)
    content = Column(Text)
    industry = Column(String)
    founded_year = Column(Integer)
    location = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

def save_to_db(data_list):
    session = SessionLocal()
    session.query(GeneratedData).delete()

    # ✅ Filter out any unexpected fields (e.g., "headquarters")
    allowed_keys = {col.name for col in GeneratedData.__table__.columns}

    for item in data_list:
        filtered_item = {k: v for k, v in item.items() if k in allowed_keys}
        entry = GeneratedData(**filtered_item)
        session.add(entry)

    session.commit()
    session.close()

    pd.DataFrame(data_list).to_csv(config.CSV_FILE_PATH, index=False)

def get_all_data():
    session = SessionLocal()
    records = session.query(GeneratedData).all()
    result = [r.__dict__ for r in records]
    for r in result:
        r.pop("_sa_instance_state", None)
    session.close()
    return result

def get_by_category(category):
    session = SessionLocal()
    records = session.query(GeneratedData).filter(GeneratedData.category == category).all()
    result = [r.__dict__ for r in records]
    for r in result:
        r.pop("_sa_instance_state", None)
    session.close()
    return result

def clear_data():
    session = SessionLocal()
    session.query(GeneratedData).delete()
    session.commit()
    session.close()
