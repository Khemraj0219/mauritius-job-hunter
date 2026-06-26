from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# Import jobs from shared (best practice)
try:
    from shared.jobs import JOBS
except ImportError:
    JOBS = []  # fallback if import fails

app = FastAPI(title="Mauritius Job Hunter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],                    # Change to your exact Streamlit URL later for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Mauritius Job Hunter API is running", "owner": "Khemraj Dhunput"}

@app.get("/jobs/matches")
def get_job_matches():
    return {
        "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_matches": len(JOBS),
        "jobs": JOBS
    }

@app.post("/jobs/request-approval/{job_id}")
def request_approval(job_id: str):
    return {
        "message": f"Approval request received for {job_id}",
        "next_step": "You will receive an email asking for final confirmation"
    }
