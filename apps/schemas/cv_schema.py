from pydantic import BaseModel
from typing import List, Dict, Optional, Any



class CVEvaluationResponse(BaseModel):
    score: int
    color: str
    tips: List[str]
    cta: str


class CVFormData(BaseModel):
    """Comming from multi-step form"""
    personal_details: Dict[str, Any]   
    education: List[Dict[str, Any]]    
    employment: List[Dict[str, Any]]   
    languages: List[Dict[str, Any]]    
    skills: List[Dict[str, Any]]       
    activities: List[Dict[str, Any]]



class CVGenerateRequest(BaseModel):
    form_data: CVFormData
    format: str = "pdf"


class CoverLetterRequest(BaseModel):
    reference_cv_id: str
    job_description: Optional[str] = None
    format: str = "pdf"

class CVDashboardItem(BaseModel):
    id: str
    title: Optional[str] = None
    score: Optional[int] = None
    file_url: str
    created_at: str