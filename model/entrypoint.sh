#!/bin/bash
if [ -f /app/weights/model-q4_K.gguf ]; then
  echo "Weigths file exists, starting app..."
else
  echo "Weigts file does not exist, downloading..."
  wget -P /app/weights/ https://huggingface.co/IlyaGusev/saiga_mistral_7b_gguf/resolve/main/model-q4_K.gguf
  echo "Download complete, starting app..."
fi
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
