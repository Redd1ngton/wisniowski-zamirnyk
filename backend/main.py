from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import zipfile
import io
import json
import httpx

app = FastAPI(title="WIŚNIOWSKI Zamirnyk Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # У продакшені обмежте доменом фронтенду
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@app.post("/send")
async def send_to_telegram(
    data: str = Form(...),
    photos: list[UploadFile] = File(default=[])
):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return {"error": "TELEGRAM_TOKEN або TELEGRAM_CHAT_ID не налаштовані"}

    try:
        payload = json.loads(data)
    except Exception:
        payload = {"raw": data}

    # Створюємо ZIP в пам'яті
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        # JSON з даними
        zf.writestr("zamir.json", json.dumps(payload, ensure_ascii=False, indent=2))
        # Фото
        for i, photo in enumerate(photos):
            content = await photo.read()
            ext = photo.filename.split(".")[-1] if photo.filename else "jpg"
            zf.writestr(f"photo_{i+1}.{ext}", content)

    zip_buffer.seek(0)
    zip_bytes = zip_buffer.getvalue()

    # Відправляємо в Telegram
    async with httpx.AsyncClient() as client:
        files = {
            "document": ("zamir.zip", zip_bytes, "application/zip")
        }
        caption = (
            f"Новий замір WIŚNIOWSKI\n"
            f"Тип: {payload.get('type', '—')}\n"
            f"Менеджер: {payload.get('manager', '—')}\n"
            f"Адреса: {payload.get('client', {}).get('address', '—')}\n"
            f"Фото: {len(photos)} шт."
        )
        resp = await client.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument",
            data={
                "chat_id": TELEGRAM_CHAT_ID,
                "caption": caption
            },
            files=files,
            timeout=60.0
        )

    if resp.status_code == 200:
        return {"status": "ok", "message": "Архів відправлено в Telegram"}
    else:
        return {"status": "error", "detail": resp.text}


@app.get("/")
def root():
    return {"status": "ok", "service": "WIŚNIOWSKI Zamirnyk Backend"}
