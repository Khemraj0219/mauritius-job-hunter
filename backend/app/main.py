from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI(title="Mauritius Job Hunter API")

app.add_middleware(
    app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mauritius-job-hunter.streamlit.app"], # Your specific app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
)

SAMPLE_JOBS = [
    {
        "job_id": "PSC-2026-7791",
        "title": "Programme Manager, ITSU",
        "organization": "Ministry of Information Technology",
        "deadline": "09 July 2026",
        "match_score": 87,
        "match_level": "Strong",
        "why_matches": "Good match for your MSc Computing + IT background",
        "link": "https://psc.govmu.org/psc/?p=7791",
        "source": "PSC"
    },
    {
        "job_id": "POLY-2026-AI01",
        "title": "Part-Time Lecturer – AI & Computer Science",
        "organization": "Polytechnics Mauritius",
        "deadline": "Rolling",
        "match_score": 92,
        "match_level": "Strong",
        "why_matches": "Excellent fit! Your MSc AI/ML + research publications are perfect",
        "link": "https://www.poly.ac.mu/",
        "source": "Polytechnics Mauritius"
    }
]

@app.get("/")
def root():
    return {"message": "Mauritius Job Hunter API is running", "owner": "Khemraj Dhunput"}

@app.get("/jobs/matches")
def get_job_matches():
    return {
        "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_matches": len(SAMPLE_JOBS),
        "jobs": SAMPLE_JOBS
    }

@app.post("/jobs/request-approval/{job_id}")
def request_approval(job_id: str):
    return {
        "message": f"Approval request received for {job_id}",
        "next_step": "You will receive an email asking for final confirmation"
    }
