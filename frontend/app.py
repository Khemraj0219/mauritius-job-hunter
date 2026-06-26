import streamlit as st
import requests
import sys
from pathlib import Path

# Add shared folder to path (for local testing)
sys.path.append(str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="Mauritius Job Hunter | Khemraj Dhunput",
    page_icon="🎯",
    layout="wide"
)

# Header
st.title("🎯 Mauritius Job Hunter Agent")
st.markdown("**Personal AI Assistant for Khemraj Dhunput** — Targeting Lecturer, AI & Computing Roles in Mauritius")

# Profile Summary
with st.expander("👤 Your Profile Summary", expanded=True):
    st.markdown("""
    - **MSc Artificial Intelligence with Machine Learning** (Distinction, 2025)
    - **MSc Computing** (2014)
    - Research Publications: ✅ (First Author)
    - Teaching Experience: 12+ years
    """)

st.divider()

# Sidebar
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("🔄 Refresh Job Matches", use_container_width=True):
        st.rerun()
    st.caption("Backend Status: Connected")

# Backend URL - Change after deployment
BACKEND_URL = st.secrets.get("BACKEND_URL", "http://127.0.0.1:8000")

# Fetch jobs from backend
try:
    response = requests.get(f"{BACKEND_URL}/jobs/matches", timeout=8)
    response.raise_for_status()
    data = response.json()
    jobs = data.get("jobs", [])
except Exception as e:
    st.error(f"❌ Cannot connect to backend. Error: {e}")
    jobs = []

# Quick Stats
col1, col2, col3 = st.columns(3)
col1.metric("Total Matches", len(jobs) if jobs else 0)
col2.metric("Strong Matches", len([j for j in jobs if j.get("match_level") == "Strong"]) if jobs else 0)
col3.metric("Last Updated", data.get("scan_time", "N/A") if 'data' in locals() else "N/A")

st.header("📋 Recommended Job Matches")

if jobs:
    for job in jobs:
        with st.container(border=True):
            col1, col2 = st.columns([3.2, 1.3])
           
            with col1:
                st.subheader(job["title"])
                st.write(f"**{job['organization']}**")
                st.write(f"⏰ **Deadline:** `{job.get('deadline', 'N/A')}`")
                st.write(f"**Why it matches you:** {job.get('why_matches', '')}")
                st.markdown(f"[🔗 View Job Posting]({job.get('link', '#')})")
           
            with col2:
                level = job.get("match_level", "Good")
                score = job.get("match_score", 80)
                if level == "Strong":
                    st.success(f"🔥 {level}\n**Score: {score}%**")
                else:
                    st.info(f"⭐ {level}\n**Score: {score}%**")
               
                if st.button("✅ Request Approval", key=job.get("job_id", "btn"), use_container_width=True):
                    try:
                        res = requests.post(f"{BACKEND_URL}/jobs/request-approval/{job['job_id']}")
                        st.success(res.json().get("message", "Request sent!"))
                    except:
                        st.error("Failed to send request. Backend may be offline.")
else:
    st.warning("No matching jobs found at the moment.")

st.divider()
st.caption("Hybrid System: FastAPI Backend + Streamlit Frontend | Ready for future Agentic upgrades & Android app")
