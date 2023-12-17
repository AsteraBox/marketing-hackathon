
# Запуск

Переменные окружения для локального запуска:
```powershell
$Env:username_db = "postgres"
$Env:password = "adminpass"
$Env:host = "127.0.0.1"
$Env:port = 5432
$Env:database = "model_result"
```

Из командной строки:
```powershell
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
