import requests
from bs4 import BeautifulSoup
import streamlit as st
from datetime import datetime

@st.cache_data(ttl=3600)  # Refresh every hour
def get_psc_vacancies():
    jobs = []
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; MauritiusJobHunter/1.0)"}
        url = "https://psc.govmu.org/"
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Target current vacancies section (adjust selector if needed)
        for item in soup.find_all(['a', 'div'], string=lambda text: text and any(kw in text.lower() for kw in ['manager', 'programme', 'analyst', 'lecturer', 'officer'])):
            # Extract title, link, deadline — improve this part
            title = item.get_text(strip=True)
            link = item.get('href')
            if link and 'psc.govmu.org' not in link:
                link = "https://psc.govmu.org" + link if link.startswith('/') else link
            
            jobs.append({
                "job_id": f"PSC-{datetime.now().strftime('%Y%m%d')}",
                "title": title,
                "organization": "Public Service Commission",
                "deadline": "Check PSC site (e.g. 7-9 July 2026)",
                "match_score": 85,  # You can add AI matching later
                "match_level": "Strong",
                "why_matches": "Relevant to your AI/Computing background & SEN experience.",
                "link": link or "https://psc.govmu.org/",
                "source": "PSC Mauritius"
            })
    except Exception as e:
        st.error(f"Scraping failed: {e}")
        # Fallback to some jobs
        jobs = [{"title": "Scraping failed - visit PSC directly", "link": "https://psc.govmu.org/"}]
    
    return jobs
