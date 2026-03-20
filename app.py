import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="AI Sales Copilot", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main-header { font-size: 3rem; color: #FF4B4B; text-align: center; }
    .hot-lead { background: linear-gradient(90deg, #ff6b6b, #ff8e8e); 
                padding: 1rem; border-radius: 10px; color: white; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🚀 AI Sales Copilot for Startups</h1>', 
            unsafe_allow_html=True)

# Lead Scorer Class
class LeadScorer:
    def predict_score(self, lead_data):
        score = 0
        if lead_data.get('email_opens', 0) > 3: score += 20
        if lead_data.get('email_clicks', 0) > 1: score += 15
        if lead_data.get('meetings', 0) > 0: score += 30
        if lead_data.get('website_visits', 0) > 5: score += 10
        if lead_data.get('days_since_contact', 999) < 7: score += 10
        return max(0, min(100, score))

# Load sample data
@st.cache_data
def load_sample_data():
    return pd.DataFrame({
        'name': ['John Smith', 'Sarah Chen', 'Priya Patel', 'Mike Johnson', 'Lisa Wong'],
        'company': ['TechCorp', 'GrowthLabs', 'AIDynamics', 'StartupHub', 'DataFlow'],
        'email_opens': [5, 8, 12, 2, 4],
        'meetings': [1, 2, 3, 0, 1],
        'score': [75, 92, 88, 45, 62],
        'industry': ['SaaS', 'AI/ML', 'AI/ML', 'E-commerce', 'Data']
    })

df = load_sample_data()

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["📊 Dashboard", "🎯 Lead Scoring", "ℹ️ About"])

if page == "📊 Dashboard":
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Leads", len(df))
    col2.metric("Hot Leads", len(df[df['score'] > 70]))
    col3.metric("Avg Score", f"{df['score'].mean():.1f}")
    col4.metric("Industries", df['industry'].nunique())
    
    # Leads table
    st.subheader("📋 All Leads")
    st.dataframe(df, use_container_width=True)
    
    # Hot leads
    st.subheader("🔥 Hot Leads")
    hot_leads = df[df['score'] > 70]
    for _, row in hot_leads.iterrows():
        st.markdown(f"""
        <div class="hot-lead">
            <h3>{row['name']} - {row['company']}</h3>
            <p>Score: {row['score']}/100 | Industry: {row['industry']}</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "🎯 Lead Scoring":
    st.header("🎯 Lead Score Calculator")
    
    col1, col2 = st.columns(2)
    with col1:
        email_opens = st.slider("Email Opens", 0, 20, 5)
        email_clicks = st.slider("Email Clicks", 0, 10, 2)
    with col2:
        meetings = st.slider("Meetings", 0, 5, 0)
        visits = st.slider("Website Visits", 0, 50, 10)
    
    days = st.slider("Days Since Contact", 0, 90, 7)
    
    if st.button("Calculate Score"):
        test_lead = {
            'email_opens': email_opens,
            'email_clicks': email_clicks,
            'meetings': meetings,
            'website_visits': visits,
            'days_since_contact': days
        }
        scorer = LeadScorer()
        score = scorer.predict_score(test_lead)
        
        if score >= 70:
            st.success(f"🔥 HOT LEAD! Score: {score}/100")
        elif score >= 40:
            st.info(f"👍 Warm Lead - Score: {score}/100")
        else:
            st.warning(f"🧊 Cold Lead - Score: {score}/100")

else:  # About page
    st.header("ℹ️ About")
    st.markdown("""
    **AI Sales Copilot** helps startups:
    - 🔍 Identify hot leads
    - 📊 Track engagement metrics
    - 🎯 Score leads automatically
    - 📈 Optimize sales process
    
    ### How to use:
    1. Add your leads data
    2. Check dashboard for hot leads
    3. Use score calculator for new leads
    4. Export insights to CSV
    
    ### Tech Stack:
    - Streamlit for dashboard
    - Pandas for data analysis
    - Python for ML scoring
    """)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ for startups")
