import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import os
from datetime import datetime, timedelta
import random

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NeuroTrack AI",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# STYLING (Premium Modern SaaS Look)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global Theme & Background */
    .stApp {
        background-color: #09090b;
        background-image: 
            radial-gradient(circle at 15% 50%, rgba(120, 119, 198, 0.1), transparent 25%),
            radial-gradient(circle at 85% 30%, rgba(58, 163, 163, 0.1), transparent 25%);
        color: #ededed;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide top header and default padding */
    header {visibility: hidden;}
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1400px;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(24, 24, 27, 0.65);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin-bottom: 24px;
        overflow: hidden;
        position: relative;
    }
    .glass-card:hover {
        transform: translateY(-6px);
        border: 1px solid rgba(46, 204, 113, 0.4);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6), 0 0 20px rgba(46, 204, 113, 0.15);
    }

    /* Animated Gradient Text */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -0.05em;
        margin-bottom: 0.2rem;
        background: linear-gradient(to right, #4facfe 0%, #00f2fe 50%, #4facfe 100%);
        background-size: 200% auto;
        color: #000;
        background-clip: text;
        text-fill-color: transparent;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
    }
    @keyframes shine {
        to {
            background-position: 200% center;
        }
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: #a1a1aa;
        font-weight: 400;
        margin-bottom: 2rem;
        letter-spacing: 0.02em;
    }

    /* Status Text */
    .status-badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        background: rgba(46, 204, 113, 0.1);
        color: #2ecc71;
        border: 1px solid rgba(46, 204, 113, 0.3);
        box-shadow: 0 0 15px rgba(46, 204, 113, 0.2);
    }

    /* Custom Checkbox as Toggle Cards */
    div[data-testid="stCheckbox"] {
        background: rgba(39, 39, 42, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 16px 20px;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        cursor: pointer;
    }
    div[data-testid="stCheckbox"]:hover {
        background: rgba(39, 39, 42, 0.8);
        transform: scale(1.02);
        border-color: rgba(255, 255, 255, 0.15);
    }
    /* When Checked - using :has for modern browsers */
    div[data-testid="stCheckbox"]:has(input:checked) {
        background: linear-gradient(135deg, rgba(46, 204, 113, 0.15) 0%, rgba(24, 24, 27, 0.8) 100%);
        border-color: #2ecc71;
        box-shadow: inset 0 0 20px rgba(46, 204, 113, 0.05), 0 0 15px rgba(46, 204, 113, 0.2);
    }
    
    .stCheckbox label {
        color: #ededed !important;
        font-weight: 500;
        font-size: 1.1rem;
        cursor: pointer;
    }
    
    .stCheckbox [data-testid="stCheckboxMark"] {
        border-color: rgba(255,255,255,0.3) !important;
        background-color: transparent !important;
    }
    .stCheckbox input:checked + div[data-testid="stCheckboxMark"] {
        background-color: #2ecc71 !important;
        border-color: #2ecc71 !important;
        box-shadow: 0 0 10px #2ecc71;
    }

    /* Metric Styling Overrides */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #ffffff 0%, #a1a1aa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    [data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        font-weight: 500 !important;
        color: #a1a1aa;
    }

    /* Smart Insight Panel Text */
    .insight-text {
        font-size: 1.1rem;
        font-weight: 500;
        color: #e4e4e7;
        background: linear-gradient(90deg, transparent, rgba(168, 85, 247, 0.1), transparent);
        padding: 12px;
        border-left: 4px solid #a855f7;
        border-radius: 4px;
        margin-top: 10px;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #09090b; 
    }
    ::-webkit-scrollbar-thumb {
        background: #27272a; 
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #3f3f46; 
    }

    /* Loading animation logic could go here */
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS & DATA MANAGEMENT
# ─────────────────────────────────────────────────────────────────────────────
DATA_FILE = "productivity_data.json"
WEEKLY_SCHEDULE = {
    "Monday": [
        "10:00 – 11:30 → AI/ML Learning",
        "11:30 – 12:15 → Interview Preparation",
        "12:15 – 1:00 → Class Study",
        "6:00 – 7:00 → Class Study",
        "7:00 – 8:00 → Assignment",
        "8:00 – 8:30 → Dinner",
        "8:30 – 9:30 → DSA",
        "9:30 – 10:30 → AI/ML Practice",
        "10:30 – 11:00 → Minecraft",
        "11:00 – 12:00 → Interview Preparation",
        "12:00 – 1:00 → Relax"
    ],
    "Tuesday": [
        "8:00 – 10:00 → DSA",
        "10:00 – 11:30 → AI/ML",
        "11:30 – 12:15 → Interview Preparation",
        "12:15 – 1:00 → Class Study",
        "6:00 – 7:00 → Class Study",
        "7:00 – 8:00 → Assignment",
        "8:00 – 8:30 → Dinner",
        "8:30 – 9:30 → AI/ML",
        "9:30 – 10:30 → DSA Revision",
        "10:30 – 11:30 → Relax"
    ],
    "Wednesday": [
        "8:00 – 9:30 → DSA",
        "9:30 – 11:00 → AI/ML",
        "6:00 – 7:00 → Class Study",
        "7:00 – 8:00 → Assignment",
        "8:00 – 8:30 → Dinner",
        "8:30 – 9:30 → Interview Preparation",
        "9:30 – 10:30 → AI/ML Project",
        "10:30 – 11:30 → Minecraft / Relax",
        "11:30 – 1:00 → Revision"
    ],
    "Thursday": [
        "11:30 – 1:00 → AI/ML / Light Work",
        "6:00 – 7:00 → Class Study",
        "7:00 – 8:00 → Assignment",
        "8:00 – 8:30 → Dinner",
        "8:30 – 9:15 → AI News / Revision",
        "9:15 – 10:00 → DSA (Easy)"
    ],
    "Friday": [
        "8:00 – 9:30 → DSA",
        "11:30 – 1:00 → AI/ML",
        "6:00 – 7:00 → Class Study",
        "7:00 – 8:00 → Assignment",
        "8:00 – 8:30 → Dinner",
        "8:30 – 9:30 → AI/ML",
        "9:30 – 10:30 → Interview Preparation",
        "10:30 – 11:30 → Relax"
    ],
    "Saturday": [
        "8:00 – 10:30 → DSA",
        "10:30 – 1:00 → AI/ML Project",
        "6:00 – 7:00 → Interview Preparation",
        "7:00 – 8:00 → GitHub / Portfolio",
        "8:00 – 8:30 → Dinner",
        "8:30 – 10:00 → AI/ML Build",
        "10:00 – 11:00 → Minecraft"
    ],
    "Sunday": [
        "8:00 – 10:00 → DSA Revision",
        "10:00 – 12:00 → AI/ML Recap",
        "6:00 – 7:00 → Weekly Planning",
        "7:00 – 8:00 → Light Coding",
        "8:00 – 8:30 → Dinner",
        "8:30 – 10:00 → Relax"
    ]
}

def get_day_habits(date_obj):
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.strptime(date_obj, "%Y-%m-%d").date()
        except Exception:
            return []
    day_name = date_obj.strftime("%A")
    return WEEKLY_SCHEDULE.get(day_name, [])

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                # Ensure structure
                if "history" not in data:
                    data = {"history": data.get("days", {}), "settings": data.get("settings", {})}
                return data
        except Exception:
            return {"history": {}}
    return {"history": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

if "data" not in st.session_state:
    st.session_state.data = load_data()

# Helper Functions
def get_productivity_score(completed_habits_count, date_obj):
    day_habits = get_day_habits(date_obj)
    return (completed_habits_count / len(day_habits)) * 100 if day_habits else 0

def get_lab_adjustment(selected_date):
    day_name = selected_date.strftime("%A")
    if day_name == "Monday":
        return ["08:00–09:40 (Lab Session)"]
    elif day_name == "Thursday":
        return ["08:00–11:30 (Lab Session)"]
    elif day_name == "Friday":
        return ["09:50–11:30 (Lab Session)"]
    return []

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<h2 style='text-align:center; font-weight: 800; letter-spacing: -1px; background: -webkit-linear-gradient(#fff, #999); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>NeuroTrack OS</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    page = st.radio("Navigation", ["🏠 Dashboard", "📅 Daily Tracker", "📊 Analytics"], label_visibility="collapsed")
    
    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    today = datetime.now().date()
    st.markdown(f"<p style='color:#a1a1aa; font-weight: 500;'>Today: <span style='color:#fff;'>{today.strftime('%d %b, %Y')}</span></p>", unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    if st.button("Reset Everything", use_container_width=True):
        st.session_state.data = {"history": {}}
        save_data(st.session_state.data)
        st.rerun()

# Date string for today
today_str = str(today)
if today_str not in st.session_state.data["history"]:
    today_habits = get_day_habits(today)
    st.session_state.data["history"][today_str] = {"habits": {h: False for h in today_habits}, "score": 0}

today_data = st.session_state.data["history"][today_str]
today_score = today_data["score"]

# Calculate Streak
streak = 0
curr_date = today
while str(curr_date) in st.session_state.data["history"] and st.session_state.data["history"][str(curr_date)]["score"] > 0:
    streak += 1
    curr_date -= timedelta(days=1)

status_text = "Excellent" if today_score >= 80 else "Good" if today_score >= 50 else "Focus Needed"
status_color = "#2ecc71" if today_score >= 80 else "#f39c12" if today_score >= 50 else "#e74c3c"

# ─────────────────────────────────────────────────────────────────────────────
# HERO SECTION (Always visible top)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align: center; margin-bottom: 2rem;">
    <div class="hero-title">NeuroTrack AI</div>
    <div class="hero-subtitle">Your Intelligent Productivity System</div>
    <div>
        <span class="status-badge" style="color: {status_color}; border-color: {status_color}55; background: {status_color}1a; box-shadow: 0 0 15px {status_color}33;">
            ● {status_text}
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
if page == "🏠 Dashboard":
    # --- Top Metrics Row ---
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.metric("Today's Score", f"{today_score:.0f}%")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.metric("Current Streak", f"{streak} Days", "🔥")
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        completed = sum([1 for d in st.session_state.data["history"].values() if d["score"] == 100])
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.metric("Perfect Days", f"{completed} Days", "💎")
        st.markdown("</div>", unsafe_allow_html=True)
    with c4:
        all_scores = [d["score"] for d in st.session_state.data["history"].values()]
        avg_score = sum(all_scores)/len(all_scores) if all_scores else 0
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.metric("Avg Performance", f"{avg_score:.1f}%")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Github Style Heatmap & Smart Insights ---
    colA, colB = st.columns([2.5, 1])
    
    with colA:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0; color:#fff;'>Activity Heatmap</h3>", unsafe_allow_html=True)
        
        # Prepare Data for Heatmap
        year_ago = today - timedelta(days=364)
        dates = [year_ago + timedelta(days=i) for i in range(365)]
        
        heat_data = []
        hover_text = []
        for d in dates:
            d_str = str(d)
            if d_str in st.session_state.data["history"]:
                score = st.session_state.data["history"][d_str]["score"]
            else:
                score = 0
            heat_data.append(score)
            hover_text.append(f"Date: {d_str}<br>Prod: {score:.0f}%")
            
        weeks = [heat_data[i:i + 7] for i in range(0, 364, 7)]
        hover_weeks = [hover_text[i:i + 7] for i in range(0, 364, 7)]
        
        if len(weeks) == 52:
            fig = go.Figure(data=go.Heatmap(
                z=list(zip(*weeks)),
                text=list(zip(*hover_weeks)),
                hoverinfo="text",
                colorscale=[
                    [0.0, '#161b22'],
                    [0.25, '#0e4429'],
                    [0.5, '#006d32'],
                    [0.75, '#26a641'],
                    [1.0, '#39d353']
                ],
                showscale=False,
                xgap=4,
                ygap=4
            ))
            
            fig.update_layout(
                height=220,
                margin=dict(l=20, r=20, t=10, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, autorange='reversed', ticktext=['S','M','T','W','T','F','S'], tickvals=[0,1,2,3,4,5,6], tickfont=dict(color='#8b949e'))
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.warning("Insufficient data shape for heatmap.")
        st.markdown("</div>", unsafe_allow_html=True)

    with colB:
        st.markdown("<div class='glass-card' style='height: 100%;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0; color:#fff;'>🧠 AI Insight</h3>", unsafe_allow_html=True)
        
        if today_score == 100:
            msg = "You're on fire! 🔥 An absolute productivity machine today."
        elif today_score >= 60:
            msg = "Solid progress! 🚀 Push a bit more to achieve perfection today."
        elif today_score > 0:
            msg = "You've started, which is the hardest part. Keep the momentum going! ⚡"
        else:
            msg = "A fresh day! Let's conquer those tasks. Remember: small consistent steps. 🌌"
            
        st.markdown(f"<div class='insight-text'>{msg}</div>", unsafe_allow_html=True)
        
        labs = get_lab_adjustment(today)
        if labs:
            st.markdown(f"""
            <div style='margin-top: 20px; padding: 10px; background: rgba(231, 76, 60, 0.1); border-left: 3px solid #e74c3c; border-radius: 4px; font-size: 0.9rem; color: #e74c3c;'>
                <b>🕒 Lab Day Active:</b><br>{labs[0]}
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: DAILY TRACKER
# ─────────────────────────────────────────────────────────────────────────────
elif page == "📅 Daily Tracker":
    
    st.markdown("<div style='text-align: center; margin-bottom: 2rem;'><h2 style='color:#fff;'>Mission Control</h2></div>", unsafe_allow_html=True)
    
    col_date, col_view = st.columns([1, 2])
    with col_date:
        selected_date = st.date_input("Select Date", today)
        date_str = str(selected_date)
        if date_str not in st.session_state.data["history"]:
            day_habits = get_day_habits(selected_date)
            st.session_state.data["history"][date_str] = {"habits": {h: False for h in day_habits}, "score": 0}
            
    day_data = st.session_state.data["history"][date_str]
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0; color:#fff;'>Daily Protocol</h3>", unsafe_allow_html=True)
        
        # We need a form or immediate update to update score dynamically
        new_habits = {}
        current_day_habits = get_day_habits(selected_date)
        for h in current_day_habits:
            new_habits[h] = st.checkbox(f"   {h}", value=day_data["habits"].get(h, False), key=f"chk_{date_str}_{h}")
            
        # Check if changed
        if any(new_habits.get(h, False) != day_data["habits"].get(h, False) for h in current_day_habits):
            day_data["habits"].update(new_habits)
            completed_count = sum(1 for h in current_day_habits if day_data["habits"].get(h, False))
            day_data["score"] = get_productivity_score(completed_count, selected_date)
            st.session_state.data["history"][date_str] = day_data
            save_data(st.session_state.data)
            st.rerun()
            
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        score = day_data["score"]
        
        st.markdown("<div class='glass-card' style='text-align: center; padding: 40px 20px;'>", unsafe_allow_html=True)
        
        # Circular completion Ring using Plotly Indicator
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score,
            number = {'suffix': "%", 'font': {'size': 50, 'color': '#fff'}},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [None, 100], 'visible': False},
                'bar': {'color': "#2ecc71"},
                'bgcolor': "rgba(255,255,255,0.05)",
                'borderwidth': 0,
                'shape': "angular",
            }
        ))
        fig.update_layout(height=250, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', font={'family': "Inter"})
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Reward System Validation
        if score == 100:
            st.snow() # Using snow + balloon combo for effect
            st.balloons()
            st.markdown("""
                <div class='glass-card' style='background: linear-gradient(45deg, rgba(39, 174, 96, 0.4), rgba(41, 128, 185, 0.4)); border-color: #2ecc71; text-align: center; animation: popIn 0.5s ease-out;'>
                    <h2 style='color: white; margin-top: 0;'>🎉 Protocol Completed!</h2>
                    <p style='color: #eee; font-size: 1.2rem; margin-bottom: 0;'><b>🎮 Minecraft Time Unlocked!</b> Enjoy your reward.</p>
                </div>
                <style>
                    @keyframes popIn { 0% { transform: scale(0.9); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
                </style>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: ANALYTICS
# ─────────────────────────────────────────────────────────────────────────────
elif page == "📊 Analytics":
    
    st.markdown("<h2 style='color:#fff; text-align:center;'>Detailed Analytics</h2><br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3>Weekly Performance</h3>", unsafe_allow_html=True)
        last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
        week_data = []
        for d in last_7_days:
            ds = str(d)
            week_data.append(st.session_state.data["history"].get(ds, {"score": 0})["score"])
            
        fig_week = px.area(
            x=[d.strftime('%a') for d in last_7_days], 
            y=week_data,
            line_shape='spline'
        )
        fig_week.update_traces(
            line_color='#00f2fe', 
            fillcolor='rgba(0, 242, 254, 0.2)',
            mode='lines+markers',
            marker=dict(size=8, color='#4facfe', line=dict(width=2, color='#fff'))
        )
        fig_week.update_layout(
            hovermode="x unified",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, title=""),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title="Score %", range=[0, 105]),
            font=dict(color='#a1a1aa')
        )
        st.plotly_chart(fig_week, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3>Monthly Overview</h3>", unsafe_allow_html=True)
        current_month_days = [d for d in st.session_state.data["history"] if d.startswith(today.strftime('%Y-%m'))]
        
        if current_month_days:
            month_scores = [st.session_state.data["history"][d]["score"] for d in current_month_days]
            avg_month = sum(month_scores) / len(month_scores)
            
            c_m1, c_m2 = st.columns([1, 1.2])
            with c_m1:
                fig_pie = go.Figure(go.Pie(
                    values=[avg_month, 100-avg_month],
                    hole=.75,
                    marker_colors=['#a855f7', 'rgba(255,255,255,0.05)'],
                    textinfo='none',
                    hoverinfo='skip'
                ))
                fig_pie.update_layout(
                    showlegend=False,
                    height=250,
                    margin=dict(l=0, r=0, t=0, b=0),
                    paper_bgcolor='rgba(0,0,0,0)',
                    annotations=[dict(text=f'{avg_month:.0f}%', x=0.5, y=0.5, font_size=30, font_color="#fff", showarrow=False)]
                )
                st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
            
            with c_m2:
                total_habits = 0
                total_possible = 0
                for k in current_month_days:
                    try:
                        k_date = datetime.strptime(k, "%Y-%m-%d").date()
                        k_habits = get_day_habits(k_date)
                        total_possible += len(k_habits)
                        total_habits += sum(1 for h in k_habits if st.session_state.data['history'][k]['habits'].get(h, False))
                    except Exception:
                        pass
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"**Average Score:** {avg_month:.1f}%")
                st.markdown(f"**Tasks Finished:** {total_habits} / {total_possible}")
                st.progress(total_habits/total_possible if total_possible > 0 else 0)
                
        else:
            st.info("No data collected for this month yet.")
        st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("<div style='text-align: center; margin-top: 50px; color: rgba(255,255,255,0.3); font-size: 0.8rem;'>NeuroTrack AI • Powered by Streamlit • 2026</div>", unsafe_allow_html=True)
