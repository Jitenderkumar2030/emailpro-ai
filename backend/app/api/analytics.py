from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.core.auth import get_current_user
from app.services.analytics_service import generate_pdf_report, generate_excel_report
from app.services.ab_testing_service import create_ab_test, get_ab_test_results
from pydantic import BaseModel
from typing import Optional
import io

router = APIRouter()

class ABTestRequest(BaseModel):
    campaign_id: int
    variant_a_subject: str
    variant_b_subject: str
    split_percentage: int = 50

@router.get("/report/pdf")
def download_pdf_report(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pdf_buffer = generate_pdf_report(current_user.id, start_date, end_date, db)
    
    return Response(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=analytics_report.pdf"}
    )

@router.get("/report/excel")
def download_excel_report(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    excel_buffer = generate_excel_report(current_user.id, start_date, end_date, db)
    
    return Response(
        content=excel_buffer.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=analytics_report.xlsx"}
    )

@router.post("/ab-test")
def create_ab_test_endpoint(
    payload: ABTestRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    test_id = create_ab_test(
        payload.campaign_id,
        payload.variant_a_subject,
        payload.variant_b_subject,
        payload.split_percentage,
        current_user.id,
        db
    )
    return {"message": "A/B test created", "test_id": test_id}

@router.get("/ab-test/{test_id}/results")
def get_ab_test_results_endpoint(
    test_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    results = get_ab_test_results(test_id, db)
    return results
