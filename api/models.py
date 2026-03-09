from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class AuditRequest(BaseModel):
    dataset_url: str
    target_column: Optional[str] = None
    job_id: Optional[str] = None

class DatasetSummary(BaseModel):
    dataset_name: Optional[str] = None
    rows: Optional[int] = None
    total_rows: Optional[int] = None # Added for frontend compatibility
    columns: Optional[int] = None
    total_columns: Optional[int] = None # Added for frontend compatibility
    target_variable: Optional[str] = None # Added for frontend compatibility
    domain: Optional[str] = None
    ml_readiness: Optional[str] = None
    bias_risk: Optional[str] = None
    leakage_risk: Optional[str] = None
    data_quality_risk: Optional[str] = None
    feature_readiness_risk: Optional[str] = None
    preprocessing_plan_risk: Optional[str] = None
    model_compatibility_risk: Optional[str] = None
    pipeline_code_risk: Optional[str] = None  

class AuditResponse(BaseModel):
    status: str
    dataset_url: str
    job_id: Optional[str] = None
    summary: Optional[DatasetSummary] = None
    schema_analysis: Optional[Dict[str, Any]] = None
    bias_analysis: Optional[Dict[str, Any]] = None
    leakage_analysis: Optional[Dict[str, Any]] = None
    recommendations: Optional[List[str]] = None
    data_quality_analysis: Optional[Dict[str, Any]] = None
    feature_readiness_analysis: Optional[Dict[str, Any]] = None
    preprocessing_plan: Optional[Dict[str, Any]] = None
    model_compatibility_analysis: Optional[Dict[str, Any]] = None
    pipeline_code: Optional[str] = None
    human_report: Optional[str] = None

    class Config:
        extra = "allow" # Allow extra fields from LLM to pass through