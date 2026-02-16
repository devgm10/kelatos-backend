import logging
from fastapi import FastAPI, HTTPException
from app.schemas.models import LeadSchema
from app.services.google_sheets import get_sheet, email_exists
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
from app.services.google_sheets import get_sheet
from datetime import datetime
from app.services.ai_service import classify_and_summarize, assign_priority
from app.services.email_service import send_email

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


@app.post("/webhook/lead")
async def receive_lead(lead: LeadSchema):
    return {
        "status": "received",
        "data": lead
    }


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")

    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "message": "Datos inválidados o campos obligatorios faltantes",
            "details": exc.errors()
        }
    )


@app.get("/test-sheet")
def test_sheet():
    sheet = get_sheet()
    sheet.append_row(["TEST", "Desde FastAPI"])
    return {"message": "Fila agregada"}


@app.post("/leads")
def create_lead(lead: LeadSchema):

    if email_exists(lead.email):
        raise HTTPException(status_code=400, detail="Email already exists")

    ai_result = classify_and_summarize(lead.message)

    category = ai_result["category"]
    summary = ai_result["summary"]
    priority = assign_priority(category)

    sheet = get_sheet()
    sheet.append_row([
        datetime.now().isoformat(),
        lead.name,
        lead.email,
        category,
        priority,
        summary
    ])

    send_email(lead.email, category, summary)

    return {"message": "Lead created successfully"}