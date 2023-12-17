import re

import pydantic
import psycopg2
import json
from settings_db import settings_DB
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status, Path
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from fastapi import HTTPException

from model.promtsgenerator import promtsgenerator

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
        port=settings_DB.port
    )
    return con


class Client(pydantic.BaseModel):
    gender: int = None
    age: float = None
    reg_region_nm: str = None
    cnt_tr_all_3m: int = None
    cnt_tr_top_up_3m: int = None
    cnt_tr_cash_3m: int = None
    cnt_tr_buy_3m: int = None
    cnt_tr_mobile_3m: int = None
    cnt_tr_oil_3m: int = None
    cnt_tr_on_card_3m: int = None
    cnt_tr_service_3m: int = None
    cnt_zp_12m: int = None
    sum_zp_12m: float = None
    limit_exchange_count: int = None
    max_outstanding_amount_6m: float = None
    avg_outstanding_amount_3m: float = None
    cnt_dep_act: int = None
    sum_dep_now: float = None
    avg_dep_avg_balance_1month: float = None
    max_dep_avg_balance_3month: float = None
    app_vehicle_ind: int = None
    app_position_type_nm: str = None
    visit_purposes: str = None
    qnt_months_from_last_visit: int = None
    super_clust: str
    product: str
    channel: str


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
async def get_all_text(credentials: Annotated[HTTPBasicCredentials,
Depends(security)], page: int = 0):
    con = connect_db(settings_DB)
    cur = con.cursor()
    cur.execute("SELECT * FROM admin WHERE username = %s AND password = %s",
                (credentials.username, credentials.password))
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
        credentials: Annotated[HTTPBasicCredentials,
        Depends(security)],
        id: int
):
    con = connect_db(settings_DB)
    cur = con.cursor()
    cur.execute("SELECT * FROM admin WHERE username = %s AND password = %s",
                (credentials.username, credentials.password))
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
                                            Depends(security)], client: Client, 
):    
    def replace_phone_number_in_ad_text(self, text):
        pattern = r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
        bank_phone_number = '8 800 100 07 01'
        text = re.sub(pattern, bank_phone_number, text)
        text = re.sub('\[номер\]', bank_phone_number, text)
        return re.sub(pattern, bank_phone_number, text)

    con = connect_db(settings_DB)
    cur = con.cursor()
    cur.execute("SELECT * FROM admin WHERE username = %s AND password = %s",
                (credentials.username, credentials.password))
    admin_user = cur.fetchone()

    if admin_user:
        print(client)
        # валидация
        if client.product not in PRODUCTS:
            raise HTTPException(status_code=400, detail="Unknown product name")
        if client.channel not in CHANNELS:
            raise HTTPException(status_code=400, detail="Unknown channel name")
        # используем поля в client (напр., client.gender) для доступа к информации о клиенте, продукте и канале
        # TODO: 
        promt = promtsgenerator.generate_personalized_promt(client.product, "", client.channel, dict(client))
        text = "Example text"
        # TODO:
        cur.execute("INSERT INTO info_text (json_input, text, result) VALUES (%s, %s, %s)",
        (json.dumps(dict(client)), text, False),
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
