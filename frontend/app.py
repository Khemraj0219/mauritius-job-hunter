import streamlit as st
import requests

st.set_page_config(
    page_title="Mauritius Job Hunter | Khemraj Dhunput",
    page_icon="🎯",
    layout="wide"
)

# Header
st.title("🎯 Mauritius Job Hunter Agent")
st.markdown("**Personal AI Assistant for Khemraj Dhunput** — Targeting Lecturer, AI & Computing Roles in Mauritius")

# Profile Summary
with st.expander("👤 Your Profile Summary", expanded=False):
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


# Change this to your new cloud URL
BACKEND_URL = "https://your-deployed-backend-url.com"

# Fetch jobs from backend
try:
    response = requests.get(f"{BACKEND_URL}/jobs/matches", timeout=5)
    data = response.json()
    jobs = data.get("jobs", [])
except:
    st.error("❌ Cannot connect to backend. Please make sure FastAPI is running.")
    jobs = []

# Quick Stats
col1, col2, col3 = st.columns(3)
col1.metric("Total Matches", len(jobs) if jobs else 0)
col2.metric("Strong Matches", len([j for j in jobs if j["match_level"] == "Strong"]) if jobs else 0)
col3.metric("Last Updated", data.get("scan_time", "N/A") if 'data' in locals() else "N/A")

st.header("📋 Recommended Job Matches")

if jobs:
    for job in jobs:
        with st.container(border=True):
            col1, col2 = st.columns([3.2, 1.3])
            
            with col1:
                st.subheader(job["title"])
                st.write(f"**{job['organization']}**")
                st.write(f"⏰ **Deadline:** `{job['deadline']}`")
                st.write(f"**Why it matches you:** {job['why_matches']}")
                st.markdown(f"[🔗 View Job Posting]({job['link']})")
            
            with col2:
                if job["match_level"] == "Strong":
                    st.success(f"🔥 {job['match_level']}\n**Score: {job['match_score']}%**")
                else:
                    st.info(f"⭐ {job['match_level']}\n**Score: {job['match_score']}%**")
                
                if st.button("✅ Request Approval", key=job["job_id"], use_container_width=True):
                    try:
                        res = requests.post(f"{BACKEND_URL}/jobs/request-approval/{job['job_id']}")
                        st.success(res.json().get("message"))
                    except:
                        st.error("Failed to send request. Try again.")
else:
    st.warning("No matching jobs found at the moment.")

st.divider()

# Footer
st.caption("Hybrid System: FastAPI Backend + Streamlit Frontend | Ready for future Agentic upgrades & Android app")
