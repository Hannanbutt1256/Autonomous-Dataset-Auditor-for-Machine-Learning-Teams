import os
from fastapi import FastAPI, HTTPException, BackgroundTasks
from api.models import AuditRequest, AuditResponse
from agents.crew import AuditorCrew
import json
import re
import ast
import codecs
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client

app = FastAPI(
    title="Autonomous Dataset Auditor API",
    description="API for triggering multi-agent dataset audits",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase Initialization
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") # Use Service Role Key for backend writes

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Failed to initialize Supabase: {e}")

@app.get("/health")
def health_check():
    return {"status": "ok"}

def run_audit_in_background(request: AuditRequest):
    try:
        # Initialize and kickoff the crew
        crew = AuditorCrew(dataset_url=request.dataset_url)
        result = crew.run()
        
        raw_text = result.raw
        
        def repair_json(text):
            """
            Attempts to repair a truncated JSON string by adding missing closing braces/brackets.
            """
            text = text.strip()
            stack = []
            in_string = False
            escape = False
            
            for i, char in enumerate(text):
                if char == '"' and not escape:
                    in_string = not in_string
                if in_string:
                    if char == '\\':
                        escape = not escape
                    else:
                        escape = False
                    continue
                
                if char == '{':
                    stack.append('}')
                elif char == '[':
                    stack.append(']')
                elif char in ('}', ']') and stack:
                    if stack[-1] == char:
                        stack.pop()
            
            # Close any remaining open constructs
            return text + "".join(reversed(stack))

        # Strategy 1: Strip ```json ... ``` markdown code block if present
        json_match = re.search(r'```json\s*(.*?)\s*```', raw_text, re.DOTALL)
        if json_match:
            raw_text = json_match.group(1).strip()

        # Strategy 2: Extract the outermost JSON object from the raw text
        obj_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if obj_match:
            raw_text = obj_match.group(0).strip()

        data = None
        
        # Strategy 3: Try standard json.loads first
        try:
            data = json.loads(raw_text)
        except json.JSONDecodeError:
            pass

        # Strategy 4: Try to REPAIR then load
        if data is None:
            try:
                repaired_text = repair_json(raw_text)
                data = json.loads(repaired_text)
            except json.JSONDecodeError:
                pass

        # Strategy 5: Fix double-escaped sequences (\\n -> \n) then retry
        if data is None:
            try:
                fixed_text = raw_text.encode('utf-8').decode('unicode_escape')
                data = json.loads(fixed_text)
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass
        
        # Strategy 6: Try to fix truncated and escaped
        if data is None:
            try:
                fixed_text = raw_text.encode('utf-8').decode('unicode_escape')
                repaired_text = repair_json(fixed_text)
                data = json.loads(repaired_text)
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass

        # Strategy 7: Try ast.literal_eval as a last resort
        if data is None:
            try:
                data = ast.literal_eval(raw_text)
            except (ValueError, SyntaxError):
                pass

        # If all strategies fail, we'll store the raw text as a failure state in Supabase
        if data is None:
            print(f"FAILED TO PARSE JSON for Job {request.job_id}. RAW OUTPUT START: {raw_text[:500]}...")
            if request.job_id and supabase:
                supabase.table("jobs").update({
                    "status": "failed",
                    "error_message": f"Failed to parse LLM JSON output. Raw result: {raw_text[:1000]}",
                    "updated_at": "now()"
                }).eq("id", request.job_id).execute()
            return

        # Make sure pipeline_code is safely casted to a string to satisfy Pydantic
        pipeline_code_content = data.get("pipeline_code")
        if isinstance(pipeline_code_content, dict):
            pipeline_code_content = list(pipeline_code_content.values())[0] if pipeline_code_content else ""
        
        # Make sure human_report is safely casted to a string
        human_report_content = data.get("human_report")
        if isinstance(human_report_content, dict):
            human_report_content = json.dumps(human_report_content, indent=2)

        # Update Supabase with the final successful result
        if request.job_id and supabase:
            try:
                supabase.table("jobs").update({
                    "status": "completed",
                    "result": data,
                    "updated_at": "now()"
                }).eq("id", request.job_id).execute()
                print(f"Job {request.job_id} successfully updated in Supabase.")
            except Exception as e:
                print(f"Failed to update Supabase job {request.job_id}: {e}")

    except Exception as e:
        print(f"CRITICAL ERROR in Background Task for Job {request.job_id}: {e}")
        # If job_id is provided, update Supabase with the failure
        if request.job_id and supabase:
            try:
                supabase.table("jobs").update({
                    "status": "failed",
                    "error_message": str(e),
                    "updated_at": "now()"
                }).eq("id", request.job_id).execute()
            except Exception as se:
                print(f"Failed to update Supabase failure for job {request.job_id}: {se}")

@app.post("/api/audit", response_model=AuditResponse)
async def trigger_audit(request: AuditRequest, background_tasks: BackgroundTasks):
    # Initiate the audit in the background and return immediately to prevent timeouts
    background_tasks.add_task(run_audit_in_background, request)
    
    return AuditResponse(
        status="processing",
        dataset_url=request.dataset_url,
        job_id=request.job_id
    )
