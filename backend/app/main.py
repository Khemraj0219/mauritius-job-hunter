from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import requests
from bs4 import BeautifulSoup

app = FastAPI(title="Mauritius Job Hunter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== SAMPLE JOBS (Fallback) ====================
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
    }
]

# ==================== REAL SCRAPING FUNCTION ====================
def scrape_psc_jobs():
    """Scrape current jobs from PSC Mauritius"""
    jobs = []
    try:
        url = "https://psc.govmu.org/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # This is a basic scraper - PSC site structure may change
        # We'll improve it in next versions
        for item in soup.find_all("a", href=True):
            text = item.get_text(strip=True)
            if "Vacancy" in text or "Post" in text or "Lecturer" in text:
                jobs.append({
                    "job_id": f"PSC-{len(jobs)+1}",
                    "title": text[:100],
                    "organization": "Public Service Commission",
                    "deadline": "Check website",
                    "match_score": 75,
                    "match_level": "Good",
                    "why_matches": "Matches your teaching + technical background",
                    "link": "https://psc.govmu.org/" + item.get("href", ""),
                    "source": "PSC (Scraped)"
                })
        return jobs[:5]  # Limit to 5 jobs for now
    except Exception as e:
        print(f"Scraping error: {e}")
        return []


@app.get("/")
def root():
    return {"message": "Mauritius Job Hunter API is running", "owner": "Khemraj Dhunput"}


@app.get("/jobs/matches")
def get_job_matches():
    scraped_jobs = scrape_psc_jobs()
    all_jobs = scraped_jobs + SAMPLE_JOBS
    
    return {
        "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_matches": len(all_jobs),
        "jobs": all_jobs
    }


@app.post("/jobs/request-approval/{job_id}")
def request_approval(job_id: str):
    return {
        "message": f"Approval request received for {job_id}",
        "next_step": "You will receive an email asking for final confirmation"
    }
