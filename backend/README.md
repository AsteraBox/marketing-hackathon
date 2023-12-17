
# Запуск

Переменные окружения для локального запуска в Windows:
```powershell
$Env:username_db = "postgres"
$Env:password = "adminpass"
$Env:host = "127.0.0.1"
$Env:port = 5432
$Env:database = "model_result"
```

Переменные окружения для локального запуска в Linux:
```bash
export username_db="postgres"
export password="adminpass"
export host="127.0.0.1"
export port=5432
export database="model_result"
```

Из командной строки:
```powershell
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
