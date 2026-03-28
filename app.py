"""
Smart Daily Productivity & Habit Tracker
A premium productivity app for college students preparing for placements.
Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import os
import random
from datetime import datetime, date, timedelta

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ProductivityOS",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS & THEME
# ─────────────────────────────────────────────────────────────────────────────
DATA_FILE = "productivity_data.json"

CATEGORY_COLORS = {
    "DSA":           {"bg": "#1a3a5c", "accent": "#4fc3f7", "text": "#4fc3f7",  "tag": "#0d47a1"},
    "AI/ML":         {"bg": "#2d1b5e", "accent": "#ce93d8", "text": "#ce93d8",  "tag": "#6a1b9a"},
    "Interview Prep":{"bg": "#3e2000", "accent": "#ffb74d", "text": "#ffb74d",  "tag": "#e65100"},
    "Study":         {"bg": "#1b3a1f", "accent": "#81c784", "text": "#81c784",  "tag": "#2e7d32"},
    "Break":         {"bg": "#1a1a2e", "accent": "#90a4ae", "text": "#90a4ae",  "tag": "#455a64"},
    "Fun":           {"bg": "#3a2800", "accent": "#ffd54f", "text": "#ffd54f",  "tag": "#f57f17"},
    "Class/Lab":     {"bg": "#1a2a3a", "accent": "#80cbc4", "text": "#80cbc4",  "tag": "#00695c"},
}

MOTIVATIONAL_QUOTES = [
    "The expert in anything was once a beginner. Keep grinding! 💪",
    "DSA today, dream offer tomorrow. Stay consistent! 🎯",
    "Every line of code brings you closer to your goal. 🚀",
    "Placement season separates the consistent from the wisher. Be consistent. 🔥",
    "Your future self is watching. Make them proud today. ✨",
    "One more problem solved = one step closer to that dream company. 💡",
    "Discipline is choosing between what you want now and what you want most. 🧠",
    "The grind never lies. Results come to those who show up daily. 🌟",
    "Today's preparation = tomorrow's performance. Let's go! ⚡",
    "You don't rise to your goals, you fall to your systems. Build yours. 🏗️",
]

HABITS = [
    {"id": "dsa",       "label": "DSA Practice",         "icon": "💻", "category": "DSA",            "target_min": 90},
    {"id": "aiml",      "label": "AI/ML Learning",        "icon": "🤖", "category": "AI/ML",          "target_min": 60},
    {"id": "interview", "label": "Interview Preparation", "icon": "🎤", "category": "Interview Prep", "target_min": 60},
    {"id": "study",     "label": "Class Study",           "icon": "📚", "category": "Study",          "target_min": 45},
    {"id": "assignment","label": "Assignment Work",       "icon": "📝", "category": "Study",          "target_min": 30},
]

# Full week schedule (base - non-lab days)
BASE_SCHEDULE = [
    {"time": "08:00–09:00", "task": "Morning DSA (Warm-up)",              "category": "DSA",            "duration": 60},
    {"time": "09:00–10:30", "task": "Deep Work: DSA Problems",            "category": "DSA",            "duration": 90},
    {"time": "10:30–11:00", "task": "Break + Breakfast",                  "category": "Break",          "duration": 30},
    {"time": "11:00–12:30", "task": "AI/ML Study / Project Work",         "category": "AI/ML",          "duration": 90},
    {"time": "12:30–13:30", "task": "Lunch Break",                        "category": "Break",          "duration": 60},
    {"time": "13:30–15:00", "task": "College Study / Assignments",        "category": "Study",          "duration": 90},
    {"time": "15:00–16:30", "task": "Interview Prep (Core CS + HR)",      "category": "Interview Prep", "duration": 90},
    {"time": "16:30–17:00", "task": "Power Nap / Refresh",                "category": "Break",          "duration": 30},
    {"time": "17:00–18:00", "task": "Revision + Note Making",             "category": "Study",          "duration": 60},
    {"time": "18:00–20:00", "task": "Advanced DSA / CP",                  "category": "DSA",            "duration": 120},
    {"time": "20:00–21:00", "task": "Dinner + Casual Reading",            "category": "Break",          "duration": 60},
    {"time": "21:00–22:30", "task": "AI/ML Deep Dive / Research",         "category": "AI/ML",          "duration": 90},
    {"time": "22:30–23:30", "task": "Mock Interviews / Aptitude",         "category": "Interview Prep", "duration": 60},
    {"time": "23:30–01:00", "task": "🎮 Minecraft / Chill (if deserved)", "category": "Fun",            "duration": 90},
]

# Lab day overrides
LAB_SCHEDULES = {
    "Monday": [
        # 8:00-9:40 → Lab slot (removed from base, replaced with class)
        {"time": "08:00–09:40", "task": "🔬 Lab Session (College)",           "category": "Class/Lab",      "duration": 100},
        {"time": "09:40–11:00", "task": "Deep Work: DSA Problems",            "category": "DSA",            "duration": 80},
        {"time": "11:00–11:30", "task": "Break + Snack",                      "category": "Break",          "duration": 30},
        {"time": "11:30–13:00", "task": "AI/ML Study / Project Work",         "category": "AI/ML",          "duration": 90},
        {"time": "13:00–14:00", "task": "Lunch Break",                        "category": "Break",          "duration": 60},
        {"time": "14:00–15:30", "task": "College Study / Assignments",        "category": "Study",          "duration": 90},
        {"time": "15:30–17:00", "task": "Interview Prep (Core CS + HR)",      "category": "Interview Prep", "duration": 90},
        {"time": "17:00–17:30", "task": "Power Nap / Refresh",                "category": "Break",          "duration": 30},
        {"time": "17:30–18:00", "task": "Revision + Note Making",             "category": "Study",          "duration": 30},
        {"time": "18:00–20:00", "task": "Advanced DSA / CP",                  "category": "DSA",            "duration": 120},
        {"time": "20:00–21:00", "task": "Dinner + Casual Reading",            "category": "Break",          "duration": 60},
        {"time": "21:00–22:30", "task": "AI/ML Deep Dive / Research",         "category": "AI/ML",          "duration": 90},
        {"time": "22:30–23:30", "task": "Mock Interviews / Aptitude",         "category": "Interview Prep", "duration": 60},
        {"time": "23:30–01:00", "task": "🎮 Minecraft / Chill (if deserved)", "category": "Fun",            "duration": 90},
    ],
    "Thursday": [
        # 8:00-11:30 → Long lab block
        {"time": "08:00–11:30", "task": "🔬 Extended Lab Session (College)",  "category": "Class/Lab",      "duration": 210},
        {"time": "11:30–12:00", "task": "Break + Lunch Prep",                 "category": "Break",          "duration": 30},
        {"time": "12:00–13:30", "task": "AI/ML Study / Project Work",         "category": "AI/ML",          "duration": 90},
        {"time": "13:30–14:30", "task": "Lunch Break",                        "category": "Break",          "duration": 60},
        {"time": "14:30–16:00", "task": "College Study / Assignments",        "category": "Study",          "duration": 90},
        {"time": "16:00–17:30", "task": "Interview Prep (Core CS + HR)",      "category": "Interview Prep", "duration": 90},
        {"time": "17:30–18:00", "task": "Revision + Note Making",             "category": "Study",          "duration": 30},
        {"time": "18:00–20:00", "task": "Advanced DSA / CP",                  "category": "DSA",            "duration": 120},
        {"time": "20:00–21:00", "task": "Dinner + Casual Reading",            "category": "Break",          "duration": 60},
        {"time": "21:00–22:30", "task": "AI/ML Deep Dive / Research",         "category": "AI/ML",          "duration": 90},
        {"time": "22:30–23:30", "task": "Mock Interviews / Aptitude",         "category": "Interview Prep", "duration": 60},
        {"time": "23:30–01:00", "task": "🎮 Minecraft / Chill (if deserved)", "category": "Fun",            "duration": 90},
    ],
    "Friday": [
        {"time": "08:00–09:50", "task": "Morning DSA (Warm-up) + Deep Work",  "category": "DSA",            "duration": 110},
        # 9:50-11:30 → Lab slot
        {"time": "09:50–11:30", "task": "🔬 Lab Session (College)",           "category": "Class/Lab",      "duration": 100},
        {"time": "11:30–12:30", "task": "AI/ML Study / Project Work",         "category": "AI/ML",          "duration": 60},
        {"time": "12:30–13:30", "task": "Lunch Break",                        "category": "Break",          "duration": 60},
        {"time": "13:30–15:00", "task": "College Study / Assignments",        "category": "Study",          "duration": 90},
        {"time": "15:00–16:30", "task": "Interview Prep (Core CS + HR)",      "category": "Interview Prep", "duration": 90},
        {"time": "16:30–17:00", "task": "Power Nap / Refresh",                "category": "Break",          "duration": 30},
        {"time": "17:00–18:00", "task": "Revision + Note Making",             "category": "Study",          "duration": 60},
        {"time": "18:00–20:00", "task": "Advanced DSA / CP",                  "category": "DSA",            "duration": 120},
        {"time": "20:00–21:00", "task": "Dinner + Casual Reading",            "category": "Break",          "duration": 60},
        {"time": "21:00–22:30", "task": "AI/ML Deep Dive / Research",         "category": "AI/ML",          "duration": 90},
        {"time": "22:30–23:30", "task": "Mock Interviews / Aptitude",         "category": "Interview Prep", "duration": 60},
        {"time": "23:30–01:00", "task": "🎮 Minecraft / Chill (if deserved)", "category": "Fun",            "duration": 90},
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# DATA PERSISTENCE
# ─────────────────────────────────────────────────────────────────────────────
def load_data() -> dict:
    """Load persisted data from JSON file."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"days": {}, "streaks": {h["id"]: 0 for h in HABITS}, "settings": {"theme": "dark"}}

def save_data(data: dict) -> None:
    """Persist data to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_today_key() -> str:
    return date.today().isoformat()

def get_day_data(data: dict, day_key: str) -> dict:
    """Get or initialise data for a given day."""
    if day_key not in data["days"]:
        data["days"][day_key] = {
            "habits":      {h["id"]: False for h in HABITS},
            "task_status": {},
            "notes":       "",
            "score":       0,
        }
    return data["days"][day_key]

def compute_score(day_data: dict) -> int:
    """Compute daily productivity score (0–100)."""
    habits = day_data.get("habits", {})
    completed = sum(1 for v in habits.values() if v)
    total = len(HABITS)
    return int((completed / total) * 100) if total else 0

def compute_streaks(data: dict) -> dict:
    """Recompute streaks for each habit based on history."""
    streaks = {h["id"]: 0 for h in HABITS}
    today = date.today()
    for habit in HABITS:
        hid = habit["id"]
        streak = 0
        check_date = today
        while True:
            key = check_date.isoformat()
            if key in data["days"] and data["days"][key]["habits"].get(hid, False):
                streak += 1
                check_date -= timedelta(days=1)
            else:
                break
        streaks[hid] = streak
    return streaks

def get_last_n_days(data: dict, n: int = 7) -> list:
    """Return list of (date_str, score) for last n days."""
    result = []
    today = date.today()
    for i in range(n - 1, -1, -1):
        d = today - timedelta(days=i)
        key = d.isoformat()
        score = 0
        if key in data["days"]:
            score = compute_score(data["days"][key])
        result.append({"date": d.strftime("%b %d"), "score": score, "key": key})
    return result

# ─────────────────────────────────────────────────────────────────────────────
# SCHEDULE HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def get_today_schedule() -> list:
    day_name = datetime.now().strftime("%A")
    return LAB_SCHEDULES.get(day_name, BASE_SCHEDULE)

def is_task_completed(day_data: dict, task_id: str) -> bool:
    return day_data.get("task_status", {}).get(task_id, False)

def get_current_time_slot(schedule: list) -> int:
    """Return index of current time slot, -1 if none."""
    now = datetime.now()
    now_minutes = now.hour * 60 + now.minute
    for i, slot in enumerate(schedule):
        try:
            start_str = slot["time"].split("–")[0]
            h, m = map(int, start_str.split(":"))
            start_min = h * 60 + m
            end_str = slot["time"].split("–")[1]
            he, me = map(int, end_str.split(":"))
            end_min = he * 60 + me
            # handle overnight (e.g. 23:30–01:00)
            if end_min < start_min:
                end_min += 24 * 60
            if start_min <= now_minutes < end_min:
                return i
        except Exception:
            pass
    return -1

# ─────────────────────────────────────────────────────────────────────────────
# CSS INJECTION
# ─────────────────────────────────────────────────────────────────────────────
def inject_css(theme: str = "dark") -> None:
    if theme == "dark":
        bg_main      = "#0a0e1a"
        bg_secondary = "#0f1526"
        bg_card      = "rgba(255,255,255,0.04)"
        bg_card2     = "rgba(255,255,255,0.07)"
        text_primary = "#e8eaf6"
        text_muted   = "#7986cb"
        border_color = "rgba(255,255,255,0.08)"
        sidebar_bg   = "#060912"
        accent       = "#6c63ff"
        accent2      = "#4fc3f7"
    else:
        bg_main      = "#f0f4ff"
        bg_secondary = "#e8edf8"
        bg_card      = "rgba(255,255,255,0.85)"
        bg_card2     = "rgba(255,255,255,0.95)"
        text_primary = "#1a1d2e"
        text_muted   = "#5c6bc0"
        border_color = "rgba(0,0,0,0.08)"
        sidebar_bg   = "#e0e8ff"
        accent       = "#6c63ff"
        accent2      = "#0288d1"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── GLOBAL RESET ─────────────────────────────────────── */
    html, body, [class*="css"] {{
        font-family: 'Space Grotesk', sans-serif !important;
    }}
    .stApp {{
        background: {bg_main} !important;
        background-image:
            radial-gradient(ellipse 80% 50% at 20% 0%, rgba(108,99,255,0.12) 0%, transparent 60%),
            radial-gradient(ellipse 60% 40% at 80% 100%, rgba(79,195,247,0.08) 0%, transparent 60%) !important;
        color: {text_primary} !important;
    }}

    /* ── SIDEBAR ──────────────────────────────────────────── */
    section[data-testid="stSidebar"] {{
        background: {sidebar_bg} !important;
        border-right: 1px solid {border_color} !important;
    }}
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stRadio label {{
        color: {text_primary} !important;
    }}

    /* ── MAIN CONTENT ─────────────────────────────────────── */
    .main .block-container {{
        padding: 2rem 2.5rem 3rem 2.5rem !important;
        max-width: 1300px !important;
    }}

    /* ── HEADINGS ─────────────────────────────────────────── */
    h1, h2, h3, h4 {{
        color: {text_primary} !important;
        letter-spacing: -0.02em;
    }}

    /* ── GLASS CARD ───────────────────────────────────────── */
    .glass-card {{
        background: {bg_card};
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid {border_color};
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.25s ease;
        box-shadow: 0 4px 24px rgba(0,0,0,0.15);
    }}
    .glass-card:hover {{
        background: {bg_card2};
        box-shadow: 0 8px 40px rgba(108,99,255,0.18);
        border-color: rgba(108,99,255,0.3);
        transform: translateY(-2px);
    }}

    /* ── TIMELINE ITEM ────────────────────────────────────── */
    .timeline-item {{
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        padding: 0.9rem 1.2rem;
        border-radius: 12px;
        margin-bottom: 0.5rem;
        border-left: 3px solid transparent;
        transition: all 0.2s ease;
        cursor: default;
    }}
    .timeline-item:hover {{
        transform: translateX(4px);
    }}
    .timeline-time {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        font-weight: 500;
        min-width: 110px;
        opacity: 0.7;
        padding-top: 2px;
    }}
    .timeline-task {{
        flex: 1;
        font-size: 0.88rem;
        font-weight: 500;
        line-height: 1.4;
    }}
    .timeline-badge {{
        font-size: 0.68rem;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        white-space: nowrap;
    }}
    .current-slot {{
        animation: pulse-glow 2s infinite;
    }}
    @keyframes pulse-glow {{
        0%, 100% {{ box-shadow: 0 0 0 0 rgba(108,99,255,0); }}
        50%        {{ box-shadow: 0 0 12px 3px rgba(108,99,255,0.35); }}
    }}

    /* ── HABIT CARD ───────────────────────────────────────── */
    .habit-card {{
        background: {bg_card};
        border: 1px solid {border_color};
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 0.6rem;
        transition: all 0.2s ease;
    }}
    .habit-card.completed {{
        border-color: rgba(129,199,132,0.5);
        background: rgba(129,199,132,0.06);
    }}
    .habit-card:hover {{
        border-color: rgba(108,99,255,0.4);
        box-shadow: 0 4px 20px rgba(108,99,255,0.1);
    }}
    .habit-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }}
    .habit-title {{
        font-weight: 600;
        font-size: 0.9rem;
        color: {text_primary};
    }}
    .streak-badge {{
        font-size: 0.78rem;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 20px;
        background: linear-gradient(135deg, #ff6b35, #f7c59f);
        color: #1a0a00;
    }}

    /* ── PROGRESS BAR ─────────────────────────────────────── */
    .progress-wrap {{
        background: rgba(255,255,255,0.08);
        border-radius: 99px;
        height: 6px;
        overflow: hidden;
        margin-top: 6px;
    }}
    .progress-fill {{
        height: 100%;
        border-radius: 99px;
        transition: width 0.6s ease;
    }}

    /* ── METRIC CARD ──────────────────────────────────────── */
    .metric-card {{
        background: {bg_card};
        border: 1px solid {border_color};
        border-radius: 16px;
        padding: 1.4rem;
        text-align: center;
        transition: all 0.25s ease;
    }}
    .metric-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(108,99,255,0.2);
    }}
    .metric-value {{
        font-size: 2.2rem;
        font-weight: 700;
        line-height: 1;
        margin-bottom: 0.4rem;
        background: linear-gradient(135deg, {accent}, {accent2});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    .metric-label {{
        font-size: 0.78rem;
        color: {text_muted};
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.07em;
    }}

    /* ── INSIGHT CARD ─────────────────────────────────────── */
    .insight-card {{
        padding: 1rem 1.3rem;
        border-radius: 12px;
        margin-bottom: 0.6rem;
        font-size: 0.88rem;
        line-height: 1.5;
        font-weight: 500;
        border-left: 3px solid;
    }}
    .insight-success {{
        background: rgba(129,199,132,0.1);
        border-color: #81c784;
        color: #81c784;
    }}
    .insight-warning {{
        background: rgba(255,183,77,0.1);
        border-color: #ffb74d;
        color: #ffb74d;
    }}
    .insight-info {{
        background: rgba(79,195,247,0.1);
        border-color: #4fc3f7;
        color: #4fc3f7;
    }}

    /* ── SCORE RING ───────────────────────────────────────── */
    .score-ring-wrap {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 1rem;
    }}
    .score-number {{
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6c63ff, #4fc3f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
    }}

    /* ── REWARD CARD ──────────────────────────────────────── */
    .reward-card {{
        background: linear-gradient(135deg, rgba(255,213,79,0.15), rgba(255,111,0,0.15));
        border: 1px solid rgba(255,213,79,0.4);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        animation: reward-glow 2s ease-in-out infinite alternate;
    }}
    @keyframes reward-glow {{
        from {{ box-shadow: 0 0 15px rgba(255,213,79,0.2); }}
        to   {{ box-shadow: 0 0 35px rgba(255,213,79,0.5); }}
    }}

    /* ── QUOTE CARD ───────────────────────────────────────── */
    .quote-card {{
        background: linear-gradient(135deg, rgba(108,99,255,0.1), rgba(79,195,247,0.1));
        border: 1px solid rgba(108,99,255,0.2);
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        font-size: 0.9rem;
        font-style: italic;
        color: {text_muted};
        line-height: 1.6;
        margin-bottom: 1.2rem;
    }}

    /* ── SECTION HEADER ───────────────────────────────────── */
    .section-header {{
        display: flex;
        align-items: center;
        gap: 0.7rem;
        margin-bottom: 1.2rem;
        padding-bottom: 0.7rem;
        border-bottom: 1px solid {border_color};
    }}
    .section-title {{
        font-size: 1.1rem;
        font-weight: 700;
        color: {text_primary};
        letter-spacing: -0.01em;
    }}
    .section-icon {{
        font-size: 1.2rem;
    }}

    /* ── LOGO ─────────────────────────────────────────────── */
    .app-logo {{
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #6c63ff 0%, #4fc3f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.2rem;
    }}
    .app-tagline {{
        font-size: 0.72rem;
        color: {text_muted};
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-weight: 500;
    }}

    /* ── STREAMLIT OVERRIDES ──────────────────────────────── */
    .stCheckbox label {{
        color: {text_primary} !important;
        font-size: 0.88rem !important;
    }}
    .stTabs [data-baseweb="tab-list"] {{
        background: transparent !important;
        gap: 0.3rem !important;
        border-bottom: 1px solid {border_color} !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        background: transparent !important;
        border: none !important;
        border-radius: 8px 8px 0 0 !important;
        color: {text_muted} !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        padding: 0.5rem 1.2rem !important;
    }}
    .stTabs [aria-selected="true"] {{
        background: rgba(108,99,255,0.15) !important;
        color: {text_primary} !important;
    }}
    div[data-testid="stMarkdownContainer"] p {{
        color: {text_primary} !important;
    }}
    .stSelectbox > label, .stTextArea > label {{
        color: {text_muted} !important;
        font-size: 0.82rem !important;
    }}
    .stButton > button {{
        background: linear-gradient(135deg, #6c63ff, #5a52d5) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        transition: all 0.2s ease !important;
        padding: 0.5rem 1.3rem !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(108,99,255,0.4) !important;
    }}
    /* hide default streamlit header */
    header[data-testid="stHeader"] {{ display: none !important; }}
    .stDeployButton {{ display: none !important; }}
    </style>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# COMPONENTS
# ─────────────────────────────────────────────────────────────────────────────

def render_timeline(schedule: list, day_data: dict, data: dict, today_key: str) -> None:
    """Render the timeline view with completion toggles."""
    current_idx = get_current_time_slot(schedule)

    st.markdown('<div class="section-header"><span class="section-icon">🕐</span><span class="section-title">Today\'s Timeline</span></div>', unsafe_allow_html=True)

    task_status = day_data.setdefault("task_status", {})

    for i, slot in enumerate(schedule):
        cat = slot["category"]
        colors = CATEGORY_COLORS.get(cat, CATEGORY_COLORS["Break"])
        task_id = f"{slot['time']}_{slot['task'][:20]}"
        completed = task_status.get(task_id, False)

        # Determine styling
        if completed:
            bg_alpha = "rgba(129,199,132,0.08)"
            border_color = "#4caf50"
            opacity = "0.7"
            status_icon = "✅"
        elif i == current_idx:
            bg_alpha = f"rgba(108,99,255,0.12)"
            border_color = "#6c63ff"
            opacity = "1"
            status_icon = "▶️"
        else:
            bg_alpha = colors["bg"].replace(")", ", 0.4)").replace("rgb", "rgba") if colors["bg"].startswith("rgb") else colors["bg"] + "cc"
            # simpler approach:
            bg_alpha = f"rgba(255,255,255,0.03)"
            border_color = colors["accent"]
            opacity = "1"
            status_icon = "⏳"

        current_class = "current-slot" if i == current_idx and not completed else ""

        # Checkbox for non-break items
        col_check, col_content = st.columns([0.06, 0.94])
        with col_check:
            if cat not in ["Break"]:
                checked = st.checkbox(
                    label="",
                    value=completed,
                    key=f"task_{today_key}_{task_id}",
                    label_visibility="collapsed"
                )
                if checked != completed:
                    task_status[task_id] = checked
                    save_data(data)
                    st.rerun()

        with col_content:
            completed_style = "text-decoration: line-through; opacity: 0.6;" if completed else ""
            current_border = f"border-left-color: {border_color}; background: {bg_alpha};" if i == current_idx else f"border-left-color: {border_color}; background: rgba(255,255,255,0.025);"

            st.markdown(f"""
            <div class="timeline-item {current_class}" style="{current_border}">
                <span class="timeline-time">{slot['time']}</span>
                <span class="timeline-task" style="{completed_style}">{status_icon} {slot['task']}</span>
                <span class="timeline-badge" style="background: {colors['tag']}22; color: {colors['accent']}; border: 1px solid {colors['accent']}44;">{cat}</span>
            </div>
            """, unsafe_allow_html=True)


def render_habits(day_data: dict, data: dict, today_key: str, streaks: dict) -> None:
    """Render the habit tracker with checkboxes and progress bars."""
    st.markdown('<div class="section-header"><span class="section-icon">✅</span><span class="section-title">Habit Tracker</span></div>', unsafe_allow_html=True)

    habits_data = day_data.setdefault("habits", {h["id"]: False for h in HABITS})
    completed_count = sum(1 for v in habits_data.values() if v)

    # Overall progress
    pct = int((completed_count / len(HABITS)) * 100) if HABITS else 0
    progress_color = "#81c784" if pct == 100 else "#6c63ff" if pct >= 60 else "#ffb74d"

    st.markdown(f"""
    <div class="glass-card" style="margin-bottom: 1.2rem;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.8rem;">
            <span style="font-weight:700; font-size:0.95rem;">Daily Completion</span>
            <span style="font-size:1.5rem; font-weight:800; color:{progress_color};">{pct}%</span>
        </div>
        <div class="progress-wrap">
            <div class="progress-fill" style="width:{pct}%; background: linear-gradient(90deg, #6c63ff, {progress_color});"></div>
        </div>
        <div style="font-size:0.75rem; color:#7986cb; margin-top:0.5rem;">{completed_count}/{len(HABITS)} habits done today</div>
    </div>
    """, unsafe_allow_html=True)

    for habit in HABITS:
        hid = habit["id"]
        is_done = habits_data.get(hid, False)
        streak = streaks.get(hid, 0)
        cat_colors = CATEGORY_COLORS.get(habit["category"], CATEGORY_COLORS["Study"])
        completed_cls = "completed" if is_done else ""

        col_cb, col_info = st.columns([0.1, 0.9])
        with col_cb:
            checked = st.checkbox(
                label="",
                value=is_done,
                key=f"habit_{today_key}_{hid}",
                label_visibility="collapsed"
            )
            if checked != is_done:
                habits_data[hid] = checked
                save_data(data)
                st.rerun()

        with col_info:
            done_style = "text-decoration: line-through; opacity: 0.65;" if is_done else ""
            streak_html = f'<span class="streak-badge">🔥 {streak}d</span>' if streak > 0 else ""

            st.markdown(f"""
            <div class="habit-card {completed_cls}">
                <div class="habit-header">
                    <span class="habit-title" style="{done_style}">{habit['icon']} {habit['label']}</span>
                    {streak_html}
                </div>
                <div style="font-size:0.72rem; color:{cat_colors['accent']}; margin-bottom:4px;">{habit['category']}</div>
                <div class="progress-wrap">
                    <div class="progress-fill" style="width:{'100' if is_done else '0'}%; background: {cat_colors['accent']};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_score_and_reward(day_data: dict) -> None:
    """Show today's score and the Minecraft reward if earned."""
    score = compute_score(day_data)
    all_done = all(day_data.get("habits", {}).values()) if day_data.get("habits") else False

    col1, col2 = st.columns([1, 1])
    with col1:
        color = "#81c784" if score >= 80 else "#6c63ff" if score >= 50 else "#ffb74d"
        st.markdown(f"""
        <div class="metric-card" style="height:140px; display:flex; flex-direction:column; align-items:center; justify-content:center;">
            <div class="metric-value" style="background: linear-gradient(135deg, {color}, #4fc3f7); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem;">{score}%</div>
            <div class="metric-label">Today's Score</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if all_done:
            st.markdown("""
            <div class="reward-card" style="height:140px; display:flex; flex-direction:column; align-items:center; justify-content:center;">
                <div style="font-size:2rem;">🎮</div>
                <div style="font-weight:800; font-size:0.95rem; color:#ffd54f; margin-top:0.4rem;">Minecraft Unlocked!</div>
                <div style="font-size:0.75rem; color:#ffb74d; margin-top:0.3rem;">You earned your gaming time!</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            remaining = sum(1 for v in day_data.get("habits", {}).values() if not v)
            st.markdown(f"""
            <div class="metric-card" style="height:140px; display:flex; flex-direction:column; align-items:center; justify-content:center;">
                <div style="font-size:2rem;">🔒</div>
                <div style="font-weight:700; font-size:0.85rem; color:#ffb74d; margin-top:0.4rem;">Minecraft Locked</div>
                <div style="font-size:0.75rem; color:#7986cb; margin-top:0.3rem;">{remaining} habit{'s' if remaining != 1 else ''} remaining</div>
            </div>
            """, unsafe_allow_html=True)


def render_insights(day_data: dict, streaks: dict) -> None:
    """Generate and display smart insights."""
    st.markdown('<div class="section-header" style="margin-top:1.5rem;"><span class="section-icon">🧠</span><span class="section-title">Smart Insights</span></div>', unsafe_allow_html=True)

    habits_data = day_data.get("habits", {})
    score = compute_score(day_data)

    insights = []

    # Score-based
    if score == 100:
        insights.append(("success", "🏆 Perfect day! You completed everything. You're built different!"))
    elif score >= 80:
        insights.append(("success", f"🔥 Outstanding! {score}% done. You're on a roll — keep the momentum!"))
    elif score >= 60:
        insights.append(("info", f"💪 Good progress at {score}%. A final push will make today count!"))
    elif score >= 40:
        insights.append(("warning", f"⚠️ Only {score}% completed. Your future FAANG self needs you to step up today!"))
    else:
        insights.append(("warning", f"🚨 {score}% done — don't let the day slip. Even 2 more habits changes everything!"))

    # Habit-specific
    for habit in HABITS:
        hid = habit["id"]
        done = habits_data.get(hid, False)
        streak = streaks.get(hid, 0)
        if not done and habit["category"] in ["DSA", "AI/ML"]:
            insights.append(("warning", f"⏰ {habit['label']} is pending — this is your placement currency. Do it now!"))
        if streak >= 7:
            insights.append(("success", f"🔥 {streak}-day streak on {habit['label']}! Compound consistency is your superpower."))
        elif streak >= 3:
            insights.append(("info", f"✨ {streak} days straight on {habit['label']}. Keep building that streak!"))

    # Weak-area suggestions
    dsa_done = habits_data.get("dsa", False)
    aiml_done = habits_data.get("aiml", False)
    interview_done = habits_data.get("interview", False)
    if not dsa_done and not interview_done:
        insights.append(("warning", "📌 Both DSA and Interview Prep are incomplete — these are your core placement pillars!"))
    if not aiml_done:
        insights.append(("info", "🤖 AI/ML learning pending — your project experience is your differentiator in ML roles!"))

    # Cap at 4 insights
    for kind, msg in insights[:4]:
        st.markdown(f'<div class="insight-card insight-{kind}">{msg}</div>', unsafe_allow_html=True)


def render_analytics(data: dict) -> None:
    """Full analytics dashboard."""
    st.markdown("## 📊 Analytics Dashboard")

    history = get_last_n_days(data, 7)
    dates   = [d["date"] for d in history]
    scores  = [d["score"] for d in history]

    # ── Row 1: Metrics ──
    col1, col2, col3, col4 = st.columns(4)
    avg_score = int(sum(scores) / len(scores)) if scores else 0
    perfect_days = sum(1 for s in scores if s == 100)
    best_streak  = max((max(data["streaks"].values(), default=0) if data.get("streaks") else 0), 0)
    total_days   = len([k for k, v in data.get("days", {}).items() if compute_score(v) > 0])

    for col, (val, label, icon) in zip(
        [col1, col2, col3, col4],
        [(f"{avg_score}%", "7-Day Avg", "📈"),
         (f"{perfect_days}", "Perfect Days", "⭐"),
         (f"{best_streak}🔥", "Best Streak", "🏆"),
         (f"{total_days}", "Active Days", "📅")]
    ):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size:1.5rem; margin-bottom:0.3rem;">{icon}</div>
                <div class="metric-value" style="font-size:1.8rem;">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 2: Charts ──
    col_left, col_right = st.columns([3, 2])

    with col_left:
        # Weekly productivity bar chart
        bar_colors = ["#81c784" if s == 100 else "#6c63ff" if s >= 70 else "#ffb74d" if s >= 40 else "#ef5350" for s in scores]
        fig_bar = go.Figure(go.Bar(
            x=dates, y=scores,
            marker_color=bar_colors,
            text=[f"{s}%" for s in scores],
            textposition="outside",
            textfont=dict(color="rgba(255,255,255,0.8)", size=11),
        ))
        fig_bar.update_layout(
            title=dict(text="Weekly Productivity Score", font=dict(color="rgba(255,255,255,0.9)", size=14)),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="rgba(255,255,255,0.7)", family="Space Grotesk"),
            yaxis=dict(range=[0, 115], gridcolor="rgba(255,255,255,0.05)", ticksuffix="%"),
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            margin=dict(l=10, r=10, t=45, b=10),
            height=280,
            showlegend=False,
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    with col_right:
        # Category time distribution (from today's schedule)
        schedule = get_today_schedule()
        cat_time: dict = {}
        for slot in schedule:
            cat = slot["category"]
            if cat != "Break":
                cat_time[cat] = cat_time.get(cat, 0) + slot.get("duration", 0)
        if cat_time:
            cat_colors_pie = [CATEGORY_COLORS.get(c, {"accent": "#6c63ff"})["accent"] for c in cat_time.keys()]
            fig_pie = go.Figure(go.Pie(
                labels=list(cat_time.keys()),
                values=list(cat_time.values()),
                hole=0.5,
                marker=dict(colors=cat_colors_pie, line=dict(color="rgba(0,0,0,0.3)", width=2)),
                textinfo="label+percent",
                textfont=dict(size=10, color="rgba(255,255,255,0.85)"),
            ))
            fig_pie.update_layout(
                title=dict(text="Time by Category (Today)", font=dict(color="rgba(255,255,255,0.9)", size=14)),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="rgba(255,255,255,0.7)", family="Space Grotesk"),
                showlegend=False,
                margin=dict(l=10, r=10, t=45, b=10),
                height=280,
            )
            st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

    # ── Row 3: Habit heatmap ──
    st.markdown('<div class="section-header" style="margin-top: 0.5rem;"><span class="section-icon">🔥</span><span class="section-title">Habit Completion — Last 7 Days</span></div>', unsafe_allow_html=True)

    days_data = get_last_n_days(data, 7)
    habit_labels = [h["label"] for h in HABITS]
    z_matrix = []
    for habit in HABITS:
        row = []
        for day in days_data:
            hval = data.get("days", {}).get(day["key"], {}).get("habits", {}).get(habit["id"], False)
            row.append(1 if hval else 0)
        z_matrix.append(row)

    fig_heat = go.Figure(go.Heatmap(
        z=z_matrix,
        x=dates,
        y=habit_labels,
        colorscale=[[0, "rgba(255,255,255,0.05)"], [1, "#6c63ff"]],
        showscale=False,
        text=[["✅" if v else "❌" for v in row] for row in z_matrix],
        texttemplate="%{text}",
        textfont=dict(size=16),
        hoverongaps=False,
        xgap=3, ygap=3,
    ))
    fig_heat.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="rgba(255,255,255,0.7)", family="Space Grotesk"),
        xaxis=dict(side="top", tickfont=dict(size=11)),
        yaxis=dict(tickfont=dict(size=11)),
        margin=dict(l=10, r=10, t=40, b=10),
        height=230,
    )
    st.plotly_chart(fig_heat, use_container_width=True, config={"displayModeBar": False})


def render_settings(data: dict) -> None:
    """Settings panel."""
    st.markdown("## ⚙️ Settings & Preferences")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🎨 Appearance")
        theme = data.get("settings", {}).get("theme", "dark")
        new_theme = st.radio("Theme", ["dark", "light"], index=0 if theme == "dark" else 1, key="theme_radio")
        if new_theme != theme:
            data.setdefault("settings", {})["theme"] = new_theme
            save_data(data)
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📝 Today's Notes")
        today_key = get_today_key()
        day_data  = get_day_data(data, today_key)
        note = st.text_area("Jot something down…", value=day_data.get("notes", ""), height=120, key="notes_ta", label_visibility="collapsed")
        if note != day_data.get("notes", ""):
            day_data["notes"] = note
            save_data(data)
        st.markdown("</div>", unsafe_allow_html=True)

    # Reset today
    st.markdown("---")
    st.markdown("### 🔄 Data Management")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        if st.button("🗑️ Reset Today's Progress", use_container_width=True):
            today_key = get_today_key()
            if today_key in data["days"]:
                data["days"][today_key] = {
                    "habits": {h["id"]: False for h in HABITS},
                    "task_status": {},
                    "notes": "",
                    "score": 0,
                }
                save_data(data)
                st.success("Today's progress has been reset.")
                st.rerun()
    with col_r2:
        if st.button("📤 Export Data (JSON)", use_container_width=True):
            st.download_button(
                label="💾 Download productivity_data.json",
                data=json.dumps(data, indent=2),
                file_name="productivity_data.json",
                mime="application/json",
            )


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
def render_sidebar(data: dict, today_key: str, streaks: dict, day_data: dict) -> str:
    with st.sidebar:
        st.markdown("""
        <div style="padding: 0.5rem 0 1.5rem 0;">
            <div class="app-logo">ProductivityOS</div>
            <div class="app-tagline">Placement Prep · Daily Tracker</div>
        </div>
        """, unsafe_allow_html=True)

        # Navigation
        page = st.radio(
            "Navigation",
            ["📅 Daily Planner", "📊 Analytics", "⚙️ Settings"],
            label_visibility="collapsed",
        )

        st.markdown("---")

        # Today summary
        now = datetime.now()
        day_name = now.strftime("%A")
        date_str = now.strftime("%B %d, %Y")
        score    = compute_score(day_data)
        is_lab   = day_name in ["Monday", "Thursday", "Friday"]

        lab_badge = f'<span style="background:#00695c33; color:#80cbc4; border:1px solid #80cbc433; border-radius:4px; padding:2px 7px; font-size:0.68rem; font-weight:600;">🔬 LAB DAY</span>' if is_lab else ""

        st.markdown(f"""
        <div class="glass-card" style="padding:1rem;">
            <div style="font-size:1.1rem; font-weight:700; margin-bottom:0.2rem;">{day_name} {lab_badge}</div>
            <div style="font-size:0.75rem; color:#7986cb; margin-bottom:0.8rem;">{date_str}</div>
            <div style="font-size:0.8rem; color:#90a4ae; margin-bottom:0.3rem;">Today's Progress</div>
            <div style="font-size:1.6rem; font-weight:800; color:{'#81c784' if score >= 80 else '#6c63ff' if score >= 50 else '#ffb74d'};">{score}%</div>
            <div class="progress-wrap" style="margin-top:0.4rem;">
                <div class="progress-fill" style="width:{score}%; background: linear-gradient(90deg, #6c63ff, #4fc3f7);"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Streak summary
        st.markdown('<div style="font-size:0.75rem; color:#7986cb; margin:0.8rem 0 0.4rem; text-transform:uppercase; letter-spacing:0.08em; font-weight:600;">Active Streaks</div>', unsafe_allow_html=True)
        for habit in HABITS:
            s = streaks.get(habit["id"], 0)
            if s > 0:
                st.markdown(f'<div style="display:flex; justify-content:space-between; font-size:0.8rem; padding:3px 0; color:#e8eaf6;">'
                            f'<span>{habit["icon"]} {habit["label"]}</span>'
                            f'<span style="color:#ff7043; font-weight:700;">🔥 {s}d</span></div>', unsafe_allow_html=True)

        st.markdown("---")

        # Quote
        quote = random.choice(MOTIVATIONAL_QUOTES)
        st.markdown(f'<div class="quote-card">"{quote}"</div>', unsafe_allow_html=True)

        # Time
        st.markdown(f'<div style="font-size:0.7rem; color:#455a64; text-align:center;">Last refreshed: {now.strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

    return page


# ─────────────────────────────────────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────────────────────────────────────
def main() -> None:
    # Load data
    data = load_data()
    theme = data.get("settings", {}).get("theme", "dark")
    inject_css(theme)

    today_key = get_today_key()
    day_data  = get_day_data(data, today_key)
    streaks   = compute_streaks(data)
    schedule  = get_today_schedule()

    # Sidebar
    page = render_sidebar(data, today_key, streaks, day_data)

    # ── DAILY PLANNER PAGE ──────────────────────────────────────────────────
    if "Daily Planner" in page:
        # Header
        day_name = datetime.now().strftime("%A")
        is_lab   = day_name in ["Monday", "Thursday", "Friday"]
        lab_note = ""
        if day_name == "Monday":
            lab_note = "🔬 Lab adjustment: 8:00–9:40 slot replaced with Lab Session"
        elif day_name == "Thursday":
            lab_note = "🔬 Lab adjustment: 8:00–11:30 slot replaced with Extended Lab Session"
        elif day_name == "Friday":
            lab_note = "🔬 Lab adjustment: 9:50–11:30 slot replaced with Lab Session"

        st.markdown(f"""
        <div style="margin-bottom: 1.8rem;">
            <h1 style="font-size:2rem; font-weight:800; letter-spacing:-0.03em; margin-bottom:0.2rem;">
                Daily Planner 📅
            </h1>
            <p style="color:#7986cb; font-size:0.88rem;">
                {datetime.now().strftime("%A, %B %d, %Y")} · {len(schedule)} time blocks scheduled
                {f' · <span style="color:#80cbc4;">{lab_note}</span>' if is_lab else ''}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Score row
        render_score_and_reward(day_data)
        st.markdown("<br>", unsafe_allow_html=True)

        # Two columns: timeline + habits
        col_timeline, col_habits = st.columns([3, 2])
        with col_timeline:
            with st.container():
                render_timeline(schedule, day_data, data, today_key)

        with col_habits:
            render_habits(day_data, data, today_key, streaks)
            render_insights(day_data, streaks)

    # ── ANALYTICS PAGE ──────────────────────────────────────────────────────
    elif "Analytics" in page:
        render_analytics(data)

    # ── SETTINGS PAGE ───────────────────────────────────────────────────────
    elif "Settings" in page:
        render_settings(data)


if __name__ == "__main__":
    main()
