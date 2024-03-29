import json
import re
from typing import Annotated

import psycopg2
import pydantic
import requests
from fastapi import Depends, FastAPI, HTTPException, Path, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from promtsgenerator import promtsgenerator
from pyd_models import Client
from settings_db import settings_DB

app = FastAPI()

security = HTTPBasic()


# список всех продуктов
PRODUCTS = {
    "ПК": "Классический потребительский кредит",
    "TOPUP": "Рефинансирование внутреннего ПК в Газпромбанке",
    "REFIN": "Рефинансирование внешнего ПК в другом банке",
    "CC": "Кредитная карта",
    "AUTO": "Классический автокредит",
    "AUTO_SCR": "Кредит под залог авто",
    "MORTG": "Ипотека (обычная, льготная, ИТ, дальневосточная и тд)",
    "MORTG_REFIN": "Рефинансирование ипотеки",
    "MORTG_SCR": "Кредит под залог недвижимости",
    "DEPOSIT": "Депозит",
    "SAVE_ACC": "Накопительный счет",
    "DC": "Дебетовая карта (МИР, UNION PAY, и тд)",
    "PREMIUM": "Премиальная карта",
    "INVEST": "Брокерский и инвестиционный счет (акции, облигации, ПИФ, валюта)",
    "ISG": "Инвестиционное страхование жизни",
    "NSG": "Накопительное страхование жизни",
    "INS_LIFE": "Страхование жизни",
    "INS_PROPERTY": "Страхование жизни",
    "TRUST": "Доверительное управление",
    "OMS": "Обезличенный металлический счет",
    "IZP": "Индивидуальный зарплатный проект",
    "CURR_EXC": "Обмен валюты",
}

# список всех каналов
CHANNELS = {
    "SMS": "СМС",
    "PUSH": "Пуш в мобильном банке",
    "EMAIL": "Емэйл",
    "MOB_BANNER": "Текст для баннера в мобильном приложении",
    "OFFICE_BANNER": "Текст для баннера для менеджера в доп офисе",
    "MOBILE_CHAT": "Предложение в чате мобильном банке",
    "KND": "Продажный текст для курьера на дом",
}


def connect_db(settings_DB):
    con = psycopg2.connect(
        database=settings_DB.database,
        user=settings_DB.admin,
        password=settings_DB.password,
        host=settings_DB.host,
        port=settings_DB.port,
    )
    return con


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
        print(
            f"ID: {info_text[0]}, JSON Input: {info_text[1]}, Text: {info_text[2]}, Result: {info_text[3]}"
        )
        record_object = {
            "id": info_text[0],
            "json_input": info_text[1],
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
        print(
            f"ID: {info_text[0]}, JSON Input: {info_text[1]}, Text: {info_text[2]}, Result: {info_text[3]}"
        )
        record_object = {
            "id": info_text[0],
            "json_input": info_text[1],
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
async def get_all_text(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)], page: int = 0
):
    con = connect_db(settings_DB)
    cur = con.cursor()
    cur.execute(
        "SELECT * FROM admin WHERE username = %s AND password = %s",
        (credentials.username, credentials.password),
    )
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
    credentials: Annotated[HTTPBasicCredentials, Depends(security)], id: int
):
    con = connect_db(settings_DB)
    cur = con.cursor()
    cur.execute(
        "SELECT * FROM admin WHERE username = %s AND password = %s",
        (credentials.username, credentials.password),
    )
    admin_user = cur.fetchone()

    if admin_user:
        cur.execute("SELECT * FROM info_text WHERE id = %s", (id,))
        existing_text = cur.fetchone()
        if existing_text:
            cur.execute(f"UPDATE info_text SET result = NOT result WHERE id = {id}")
            con.commit()
            cur.close()
            con.close()
            return HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f"Information about the validity of the text has been changed",
            )
        else:
            cur.close()
            con.close()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Text with id {id} not found",
            )
    else:
        cur.close()
        con.close()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.post("/api/v1/data")
async def read_item(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    client: Client,
):
    con = connect_db(settings_DB)
    cur = con.cursor()
    cur.execute(
        "SELECT * FROM admin WHERE username = %s AND password = %s",
        (credentials.username, credentials.password),
    )
    admin_user = cur.fetchone()

    if admin_user:
        print(client)
        # валидация
        if client.product_data not in PRODUCTS:
            raise HTTPException(status_code=400, detail="Unknown product name")
        if client.channel_data not in CHANNELS:
            raise HTTPException(status_code=400, detail="Unknown channel name")
        # используем поля в client (напр., client.gender) для доступа к информации о клиенте, продукте и канале
        # TODO:
        example_promt = promtsgenerator.generate_personalized_promt(
            client.product_data, client.channel_data, dict(client)
        )

        query = {
            "text": example_promt,
            "top_k": 30,
            "top_p": 0.9,
            "temperature": 0.2,
            "repeat_penalty": 1.1,
        }
        response = requests.post("http://model:8000/generate", json=query)

        if response.status_code == 200:
            response_data = response.json()
        else:
            print(f"Ошибка при запросе модели: {response.status_code}")
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при запросе модели: {response.status_code}",
            )

        # TODO:

        user_data_dict = {
            "user_data": client.user_data.model_dump(),
            "product_data": client.product_data,
            "channel_data": client.channel_data,
        }

        cur.execute(
            "INSERT INTO info_text (json_input, text, result) VALUES (%s, %s, %s)",
            (json.dumps(dict(user_data_dict)), response_data["text"], False),
        )

        con.commit()
        cur.close()
        con.close()

        return {"advertisement": response_data["text"]}
    else:
        cur.close()
        con.close()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
