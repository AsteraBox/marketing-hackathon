from llama_cpp import Llama
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional

class Query(BaseModel):
    text: str
    top_k: Optional[int] = 30
    top_p: Optional[float] = 0.9
    temperature: Optional[float] = 0.2
    repeat_penalty: Optional[float] = 1.1

class Response(BaseModel):
    text: str

app = FastAPI()

# Создаем экземпляр языковой модели Llama
model = Llama(
    model_path="weights/model-q4_K.gguf", # Укажите путь к вашей модели
    n_ctx=2000,
    n_parts=1,
)

# Создаем константы для токенов
SYSTEM_PROMPT = "Ты — опытный автор рекламных текстов для продуктов ГАЗПРОМБАНК. Ты должен будешь придумывать краткие и лаконичные рекламные тексты согласно предоставленной информации. Стиль и структура текста должны соответствовать типу текста, который указан в промте."
SYSTEM_TOKEN = 1587
USER_TOKEN = 2188
BOT_TOKEN = 12435
LINEBREAK_TOKEN = 13

ROLE_TOKENS = {
    "user": USER_TOKEN,
    "bot": BOT_TOKEN,
    "system": SYSTEM_TOKEN
}

def get_message_tokens(model, role, content):
    message_tokens = model.tokenize(content.encode("utf-8"))
    message_tokens.insert(1, ROLE_TOKENS[role])
    message_tokens.insert(2, LINEBREAK_TOKEN)
    message_tokens.append(model.token_eos())
    return message_tokens

def get_system_tokens(model):
    system_message = {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
    return get_message_tokens(model, **system_message)

system_tokens = get_system_tokens(model)
tokens = system_tokens
model.eval(tokens)

def generate_text(query):
    query_message = query.text
    message_tokens = get_message_tokens(model=model, role="user", content=query_message)
    role_tokens = [model.token_bos(), BOT_TOKEN, LINEBREAK_TOKEN]
    tokens = system_tokens + message_tokens + role_tokens

    generator = model.generate(
        tokens,
        top_k=query.top_k,
        top_p=query.top_p,
        temp=query.temperature,
        repeat_penalty=query.repeat_penalty
    )

    res_text = ""
    for token in generator:
        token_str = model.detokenize([token]).decode("utf-8", errors="ignore")
        tokens.append(token)
        if token == model.token_eos():
            break
        res_text += token_str
    # Возвращаем текст
    return res_text

@app.post("/generate", response_model=Response)
def generate(request: Request, query: Query):
    if not query.text:
        return Response(text="Пожалуйста, введите запрос для генерации рекламного текста.")
    text = generate_text(query)
    return Response(text=text)
