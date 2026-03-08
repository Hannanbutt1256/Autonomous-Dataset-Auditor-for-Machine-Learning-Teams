from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class AuditRequest(BaseModel):
    dataset_url: str
    target_column: Optional[str] = None

class DatasetSummary(BaseModel):
    dataset_name: Optional[str]
    rows: Optional[int]
    columns: Optional[int]
    domain: Optional[str]
    ml_readiness: Optional[str]
    bias_risk: Optional[str]
    leakage_risk: Optional[str]
    data_quality_risk: Optional[str]
    feature_readiness_risk: Optional[str]
    preprocessing_plan_risk: Optional[str]
    model_compatibility_risk: Optional[str]
    pipeline_code_risk: Optional[str]  

class AuditResponse(BaseModel):
    status: str
    dataset_url: str
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