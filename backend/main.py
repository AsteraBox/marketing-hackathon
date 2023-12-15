from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic
import pydantic
import psycopg2
from settings_db import *
from typing import Annotated
import json

app = FastAPI()
security = HTTPBasic()

'''
не настроен settings!!!!
'''
DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{database}"

class User(pydantic.BaseModel):
    user_id: int
    user_data: str
    product_data: str
    channel_data: str


class UserCredentials(pydantic.BaseModel):
    username: str
    password: str


def all_record():
    con = psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host=host,
        port=port
    )

    cur = con.cursor()
    info_texts = get_info_texts_psycopg2(cur)
    cur.close()
    con.close()

    response_json = {}
    for info_text in info_texts:
        print(f"ID: {info_text[0]}, JSON Input: {info_text[1]}, Text: {info_text[2]}, Result: {info_text[3]}")
        response_json[info_text[0]] = info_text[2]

    return response_json

def get_info_texts_psycopg2(cursor):
    cursor.execute("SELECT * FROM info_text")
    info_texts = cursor.fetchall()
    return info_texts


@app.get("/texts")
async def get_all_text():
    return all_record()


@app.put("/texts/{id}")
async def change_result(id):
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
async def read_item(credentials : Annotated[HTTPBasicCredentials, 
                                            Depends(security)], user: User = Depends(), 
):    
    user_data_dict = {
        "user_id": user.user_id,
        "user_data": user.user_data,
        "product_data": user.product_data,
        "channel_data": user.channel_data,
    }
    
    con = psycopg2.connect(
    database=database,
    user=username,
    password=password,
    host=host,
    port=port
    )

    cur = con.cursor()
    cur.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (credentials.username, credentials.password))
    admin_user = cur.fetchone()

    if admin_user:
        user_data_dict = {
            "user_id": user.user_id,
            "user_data": user.user_data,
            "product_data": user.product_data,
            "channel_data": user.channel_data,
        }

        # TODO: 
        text = "Example text"
        # TODO:
        cur.execute("INSERT INTO info_text (json_input, text, result) VALUES (%s, %s, %s)",
        (json.dumps(user_data_dict), text, False),
    )

        con.commit()
        cur.close()
        con.close()
    else:
        cur.close()
        con.close()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

'''uvicorn main:app --host 127.0.0.1 --port 8000 --reload'''
