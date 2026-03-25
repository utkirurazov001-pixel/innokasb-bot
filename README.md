# INNO KASB MARKAZI Telegram Bot (Production-ready MVP)

INNO KASB MARKAZI uchun lead yig'uvchi, kurs/voucher/aloqa bo'limlari va AI yordamchi chatga ega Telegram bot.

## Imkoniyatlar
- `/start`, `/kurslar`, `/voucher`, `/aloqa`, `/yordam`
- FSM asosidagi `/royxat` forma
- Google Sheets'ga lead yozish (retry bilan)
- Menejer chat ID'ga formatlangan yangi lid yuborish
- OpenAI orqali markaz mavzusida cheklangan AI chat
- Env orqali konfiguratsiya (filiallar, kurslar, vaqtlar, model)

## 1) O'rnatish
```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2) `.env` tayyorlash
```bash
cp .env.example .env
```

Majburiy envlar:
- `BOT_TOKEN`
- `OPENAI_API_KEY`
- `GOOGLE_SHEET_NAME`
- `GOOGLE_CREDS_JSON`

Qo'shimcha envlar:
- `MANAGER_CHAT_ID`
- `OPENAI_MODEL` (default: `gpt-4.1-mini`)
- `OPENAI_MAX_TOKENS` (default: `220`)
- `OPENAI_TEMPERATURE` (default: `0.4`)
- `COURSE_OPTIONS_JSON` (ixtiyoriy JSON list)
- `TIME_OPTIONS_JSON` (ixtiyoriy JSON list)
- `REG_BRANCH_OPTIONS_JSON` (ixtiyoriy JSON list)
- `CONTACTS_JSON` (ixtiyoriy JSON list)

## 3) Google Service Account ulash
1. Google Cloud'da Service Account yarating.
2. Google Sheets API ni yoqing.
3. JSON credential yuklab oling.
4. Google Sheet'ni service account email bilan Editor qilib share qiling.
5. JSON'ni `GOOGLE_CREDS_JSON` ga bitta qatorda joylang yoki JSON fayl yo'lini kiriting.

## 4) Ishga tushirish
```bash
python bot.py
```

## 5) Production tavsiyalar
- Long polling o'rniga webhook + HTTPS ishlatish.
- `systemd` yoki `supervisor` bilan process management.
- Markaziy log monitoring (Sentry / ELK / Grafana Loki).
- Redis FSM storage va task queue (kelajakdagi yuqori yuklama uchun).

## Arxitektura
- `handlers/` — command va FSM oqimi
- `utils/text.py` — matnlar markazlashuvi
- `keyboards.py` — keyboardlar
- `sheets.py` — Google Sheets integratsiya
- `ai_helper.py` — OpenAI integratsiya
- `config.py` — env va validatsiya

## Eslatma
Bot javoblari savdo oqimiga yo'naltirilgan: foydalanuvchi imkon qadar `/royxat` orqali lead qoldirishga undaladi.
