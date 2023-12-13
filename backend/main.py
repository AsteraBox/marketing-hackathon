from fastapi import FastAPI, Query, Header, Depends
from fastapi.security import HTTPBearer
import pydantic
import psycopg2
from sqlalchemy import create_engine, Column, Integer, Text, JSON, Boolean
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from settings_db import *


app = FastAPI()
security = HTTPBearer()
Base = declarative_base()

DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{database}"

class User(pydantic.BaseModel):
    base_auth: str
    user_id: int
    user_data: str
    product_data: str
    channel_data: str

class InfoText(Base):
    __tablename__ = 'info_text'

    id = Column(Integer, primary_key=True, index=True)
    json_input = Column(JSON)
    text = Column(Text)
    result = Column(Boolean)


def get_info_texts(db: Session):
    return db.query(InfoText).all()

def all_record():
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    info_texts = get_info_texts(db)
    db.close()
    d = {}
    for info_text in info_texts:
        print(f"ID: {info_text.id}, JSON Input: {info_text.json_input}, Text: {info_text.text}, Result: {info_text.result}")
        d[info_text.id]  = info_text.text

    return d
   
@app.get("/texts")
def get_all_text():
    return all_record()

@app.put("/texts/{id}")
def change_result(id):
    con = psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host=host,
        port=port
    )

    cur = con.cursor()
    cur.execute(f"UPDATE info_text set result = True where id = {id}")
    con.commit()
    con.close()


@app.post("/api/v1/data")
async def read_item(user: User = Depends()):    
    user_data_dict = {
        "user_id": user.user_id,
        "user_data": user.user_data,
        "product_data": user.product_data,
        "channel_data": user.channel_data,
    }
    
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    #TODO
    text = "Example text"
    result = False
    #TODO

    new_data = InfoText(json_input=user_data_dict, text="Example text", result=result)
    db.add(new_data)
    db.commit()
    db.close()
    
    all_record()


'''uvicorn main:app --host 127.0.0.1 --port 8000 --reload'''
