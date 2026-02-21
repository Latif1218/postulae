# apps/routers/cv.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from typing import Dict, Any
from sqlalchemy.orm import Session

# সঠিক পাথ — apps/ai/app/ থেকে
from apps.ai.app.cv_grader import (
    grade_cv,
    analyze_cv_metadata,
    format_client_output,
    GradingResult
)
from apps.ai.app.generator import generate_cv_from_data, CVGenerationResult
from apps.ai.app.llm_client import extract_text_from_pdf_bytes

# বাকি ইম্পোর্টগুলো তোমার আগের মতো
from apps.authentication.users_oauth import get_current_user
from apps.database import get_db
from apps.models.users_model import User
from apps.models.cv_model import CV, CVForm, CoverLetter
from apps.schemas.cv_schema import CVEvaluationResponse, CVGenerateRequest, CoverLetterRequest, CVFormData
from apps.utils.file_storage import save_uploaded_file, save_bytes_file, get_file_url

import os


router = APIRouter(
    prefix="/cv",
    tags=["CV"])


@router.post("/evaluate", response_model=CVEvaluationResponse)
async def evaluate_cv(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    if user type is free then if he uplode PDF he genarate only scode and tips .
    work only essential plan
    """

    if current_user.plan != "essential":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This feature is only available for Essential plan users."
        )
    
    file_path = save_uploaded_file(file, "cv", str(current_user.id))

    with open(file_path, "rb") as f:
        pdf_bytes = f.read()

    try:
        raw_text = extract_text_from_pdf_bytes(pdf_bytes)
        metadata = analyze_cv_metadata(raw_text, page_count=1)
        cv_data: Dict[str, Any] = {"raw_text": raw_text}

        result: GradingResult = grade_cv(cv_data, metadata)
        formatted = format_client_output(result)


        db_cv = CV(
            user_id = current_user.id,
            file_path = file_path,
            score = result.score,
            tips = result.tips
        )
        db.add(db_cv)
        db.commit()
        db.refresh(db_cv)

        return CVEvaluationResponse(**formatted)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the CV: {str(e)}"
        )