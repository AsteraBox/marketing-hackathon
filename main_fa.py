from fastapi import FastAPI, Query, Header, Depends, HTTPException
from typing import Optional
from fastapi.security import HTTPBearer


app = FastAPI()
security = HTTPBearer()

data = {
    1: {'user_id': 1, 'communication_text': 'Text for user 1', 'confidence': 0.85}, 
    2: {'user_id': 2, 'communication_text': 'Text for user 2', 'confidence': 0.92}, 
}

@app.get("/api/v1/data")
async def read_item(
    base_auth: str = Depends(security),
    user_id: str = Query(None),
    user_data: str = Query(None),
    product_data: str = Query(None),
    channel_data: str = Query(None),
):
    #TODO
    pass

    print(base_auth) 
    print(user_id, user_data, product_data, channel_data)

    if int(user_id) not in data and int(user_id) != 0:
        raise HTTPException(status_code=404, detail="Item not found")
    elif int(user_id) == 0: 
        return data
    else:
        return data.get(int(user_id))

'''uvicorn main_fa:app --host 127.0.0.1 --port 3000 --reload'''