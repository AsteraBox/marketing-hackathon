import pydantic
import psycopg2
import json
from settings_db import settings_DB
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status, Path
from fastapi.security import HTTPBasicCredentials, HTTPBasic


app = FastAPI()

security = HTTPBasic()


def connect_db(settings_DB):
    con = psycopg2.connect(
        database=settings_DB.database,
        user=settings_DB.admin,
        password=settings_DB.password,
        host=settings_DB.host,
        port=settings_DB.port
    )
    return con


class User(pydantic.BaseModel):
    user_id: int
    user_data: str
    product_data: str
    channel_data: str


class UserCredentials(pydantic.BaseModel):
    username: str
    password: str


def page_record(page: int = 1, items_per_page: int = 10):
    con = connect_db(settings_DB)

    cur = con.cursor()
    info_texts = get_info_texts_psycopg2(cur)
    cur.close()
    con.close()
    sorted_info_texts = sorted(info_texts, key=lambda x: x[0])
    start_index = (page - 1) * items_per_page
    end_index = page * items_per_page

    paginated_records = sorted_info_texts[start_index:end_index]

    response_json = {"total": len(info_texts), "records": []}

    for info_text in paginated_records:
        print(f"ID: {info_text[0]}, JSON Input: {info_text[1]}, Text: {info_text[2]}, Result: {info_text[3]}")
        record_object = {
            "id": info_text[0],
            "text": info_text[2],
            "confirmed": info_text[3],
        }
        response_json["records"].append(record_object)

    return response_json


def all_record():
    con = connect_db(settings_DB)
    cur = con.cursor()
    info_texts = get_info_texts_psycopg2(cur)
    cur.close()
    con.close()
    sorted_info_texts = sorted(info_texts, key=lambda x: x[0])
    
    response_json = {"total": len(info_texts), "records": []}

    for info_text in sorted_info_texts:
        print(f"ID: {info_text[0]}, JSON Input: {info_text[1]}, Text: {info_text[2]}, Result: {info_text[3]}")
        record_object = {
            "id": info_text[0],
            "text": info_text[2],
            "confirmed": info_text[3],
        }
        response_json["records"].append(record_object)

    return response_json


def get_info_texts_psycopg2(cursor):
    cursor.execute("SELECT * FROM info_text")
    info_texts = cursor.fetchall()
    return info_texts


@app.get("/texts")
async def get_all_text( credentials : Annotated[HTTPBasicCredentials, 
                                            Depends(security)], page: int = 0):
    con = connect_db(settings_DB)
    cur = con.cursor()
    cur.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (credentials.username, credentials.password))
    admin_user = cur.fetchone()
    cur.close()
    con.close()
    if admin_user:
        if page == 0:
            return all_record()
        return page_record(page=page)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.put("/texts/{id}")
async def change_result(
    credentials : Annotated[HTTPBasicCredentials, 
                                            Depends(security)],
    id: int
):
    con = connect_db(settings_DB)
    cur = con.cursor()
    cur.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (credentials.username, credentials.password))
    admin_user = cur.fetchone()
    if admin_user:
        cur.execute(f"UPDATE info_text SET result = True WHERE id = {id}")
        con.commit()
        con.close()
        cur.close()
    else:
        cur.close()
        con.close()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


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
    
    con = connect_db(settings_DB)
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