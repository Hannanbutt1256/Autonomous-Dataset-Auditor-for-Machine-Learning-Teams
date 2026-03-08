import os
from fastapi import FastAPI, HTTPException
from api.models import AuditRequest, AuditResponse
from agents.crew import AuditorCrew
import json
import re
import ast
import codecs


app = FastAPI(
    title="Autonomous Dataset Auditor API",
    description="API for triggering multi-agent dataset audits",
    version="0.1.0",
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/audit", response_model=AuditResponse)
def trigger_audit(request: AuditRequest):
    try:
        # Initialize and kickoff the crew
        crew = AuditorCrew(dataset_url=request.dataset_url)
        result = crew.run()
        
        # CrewAI's pydantic output preserves all model properties
        # output_model = result.pydantic
        # 
        # # If the LLM failed to cast to Pydantic, fallback safely
        # if not output_model:
        #     return AuditResponse(
        #         status="failed",
        #         dataset_url=request.dataset_url,
        #         human_report=result.raw
        #     )
        #
        # return AuditResponse(
        #     status="completed",
        #     dataset_url=request.dataset_url,
        #     summary=output_model.summary,
        #     schema_analysis=output_model.schema_analysis,
        #     bias_analysis=output_model.bias_analysis,
        #     leakage_analysis=output_model.leakage_analysis,
        #     recommendations=output_model.recommendations,
        #     human_report=output_model.human_report
        # )


        raw_text = result.raw
        
        # Strategy 1: Strip ```json ... ``` markdown code block if present
        json_match = re.search(r'```json\s*(.*?)\s*```', raw_text, re.DOTALL)
        if json_match:
            raw_text = json_match.group(1).strip()

        # Strategy 2: Extract the outermost JSON object from the raw text
        # This handles cases where the LLM adds extra text before/after the JSON
        obj_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if obj_match:
            raw_text = obj_match.group(0).strip()

        data = None
        
        # Strategy 3: Try standard json.loads first
        try:
            data = json.loads(raw_text)
        except json.JSONDecodeError:
            pass

        # Strategy 4: Fix double-escaped sequences (\\n -> \n) then retry
        if data is None:
            try:
                # The LLM often double-escapes newlines in code blocks: \\n instead of \n
                fixed_text = raw_text.encode('utf-8').decode('unicode_escape')
                data = json.loads(fixed_text)
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass

        # Strategy 5: Try ast.literal_eval as a last resort
        if data is None:
            try:
                data = ast.literal_eval(raw_text)
            except (ValueError, SyntaxError):
                pass

        # If all strategies fail, return a failure response with the raw text as human_report
        if data is None:
            print("All parsing strategies failed. Raw output:", raw_text)
            return AuditResponse(
                status="failed",
                dataset_url=request.dataset_url,
                human_report=f"Failed to parse LLM JSON output. Raw result: {raw_text}"
            )

        # Make sure pipeline_code is safely casted to a string to satisfy Pydantic
        # Sometimes the LLM ignores instructions and outputs a nested dictionary
        pipeline_code_content = data.get("pipeline_code")
        if isinstance(pipeline_code_content, dict):
            # Extract just the nested value if it gave us {"python_code": "..."}
            pipeline_code_content = list(pipeline_code_content.values())[0] if pipeline_code_content else ""
        
        # Make sure human_report is safely casted to a string
        human_report_content = data.get("human_report")
        if isinstance(human_report_content, dict):
            # Try to format the dict nicely into a markdown block instead of crashing
            human_report_content = json.dumps(human_report_content, indent=2)

        return AuditResponse(
            status="completed",
            dataset_url=request.dataset_url,
            summary=data.get("summary"),
            schema_analysis=data.get("schema_analysis"),
            bias_analysis=data.get("bias_analysis"),
            leakage_analysis=data.get("leakage_analysis"),
            recommendations=data.get("recommendations"),
            data_quality_analysis=data.get("data_quality_analysis"),
            feature_readiness_analysis=data.get("feature_readiness_analysis"),
            preprocessing_plan=data.get("preprocessing_plan"),
            model_compatibility_analysis=data.get("model_compatibility_analysis"),
            pipeline_code=str(pipeline_code_content) if pipeline_code_content else None,
            human_report=str(human_report_content) if human_report_content else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
