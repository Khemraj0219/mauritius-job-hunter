import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Mauritius Job Hunter", page_icon="🎯", layout="wide")

st.title("🎯 Mauritius Job Hunter Agent")
st.markdown("**Personal AI Agent for Khemraj Dhunput** — Targeting Lecturer, AI & Computing Roles")

BACKEND_URL = "http://127.0.0.1:8000"

# Sidebar Controls
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("🔄 Refresh Matches", use_container_width=True):
        st.rerun()
    st.caption("Backend: FastAPI running")

# Fetch data from backend
try:
    res = requests.get(f"{BACKEND_URL}/jobs/matches", timeout=5)
    data = res.json()
    jobs = data.get("jobs", [])
except Exception as e:
    st.error("❌ Cannot connect to backend. Make sure FastAPI is running.")
    jobs = []

# Display Jobs
st.header("📋 Job Matches with Deadlines")

if jobs:
    for job in jobs:
        with st.container(border=True):
            col1, col2 = st.columns([3.5, 1.5])
            
            with col1:
                st.subheader(job["title"])
                st.write(f"**Organization:** {job['organization']}")
                st.write(f"⏰ **Deadline:** `{job['deadline']}`")
                st.write(f"**Why it matches you:** {job['why_matches']}")
                st.markdown(f"[🔗 View Official Posting]({job['link']})")
            
            with col2:
                if job["match_level"] == "Strong":
                    st.success(f"🔥 {job['match_level']}\nScore: **{job['match_score']}%**")
                else:
                    st.info(f"⭐ {job['match_level']}\nScore: **{job['match_score']}%**")
                
                if st.button("✅ Request Approval", key=job["job_id"], use_container_width=True):
                    try:
                        approval_res = requests.post(
                            f"{BACKEND_URL}/jobs/request-approval/{job['job_id']}"
                        )
                        st.success(approval_res.json().get("message"))
                    except:
                        st.error("Failed to send approval request")
else:
    st.warning("No matching jobs found at the moment.")

st.divider()
st.caption("Hybrid Architecture: FastAPI Backend + Streamlit Frontend | Ready for Android App later")