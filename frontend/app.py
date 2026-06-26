import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="Mauritius Job Hunter | Khemraj Dhunput",
    page_icon="🎯",
    layout="wide"
)

# --- CONFIGURATION ---
# Use st.secrets for the URL (set in your cloud deployment platform)
# Default to localhost for local development
BACKEND_URL = st.secrets.get("BACKEND_URL", "http://127.0.0.1:8000")

# --- PERFORMANCE: CACHED DATA FETCHING ---
@st.cache_data(ttl=300) # Cache data for 5 minutes to improve speed
def fetch_jobs_from_api(url):
    """Fetches job data from the FastAPI backend."""
    response = requests.get(f"{url}/jobs/matches", timeout=15)
    response.raise_for_status()
    return response.json()

# --- HEADER & PROFILE ---
st.title("🎯 Mauritius Job Hunter Agent")
st.markdown("**Personal AI Assistant for Khemraj Dhunput** — Targeting Lecturer, AI & Computing Roles in Mauritius")

with st.expander("👤 Your Profile Summary", expanded=True):
    st.markdown("""
    - **MSc Artificial Intelligence with Machine Learning** (Distinction, 2025)
    - **MSc Computing** (2014)
    - Research Publications: ✅ (First Author)
    - Teaching Experience: 12+ years
    """)

st.divider()

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("🔄 Refresh Job Matches", use_container_width=True):
        st.cache_data.clear() # Clears the cache to force a re-fetch
        st.rerun()
    st.caption(f"Backend: {BACKEND_URL}")

# --- DATA FETCHING ---
try:
    data = fetch_jobs_from_api(BACKEND_URL)
    jobs = data.get("jobs", [])
except Exception as e:
    st.error(f"❌ Cannot connect to backend. It might be 'waking up'. Error: {e}")
    jobs = []
    data = {}

# --- QUICK STATS ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Matches", len(jobs) if jobs else 0)
col2.metric("Strong Matches", len([j for j in jobs if j.get("match_level") == "Strong"]) if jobs else 0)
col3.metric("Last Updated", data.get("scan_time", "N/A"))

# --- JOB DISPLAY ---
st.header("📋 Recommended Job Matches")

if jobs:
    for job in jobs:
        with st.container(border=True):
            col1, col2 = st.columns([3.2, 1.3])
            
            with col1:
                st.subheader(job.get("title", "No Title"))
                st.write(f"**{job.get('organization', 'Unknown')}**")
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
                
                if st.button("✅ Request Approval", key=f"btn_{job.get('job_id', 'unknown')}", use_container_width=True):
                    try:
                        res = requests.post(f"{BACKEND_URL}/jobs/request-approval/{job['job_id']}")
                        st.success(res.json().get("message", "Request sent!"))
                    except Exception as e:
                        st.error("Failed to send request.")
else:
    st.warning("No matching jobs found at the moment.")

st.divider()
st.caption("Hybrid System: FastAPI Backend + Streamlit Frontend")
