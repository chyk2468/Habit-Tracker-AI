// script.js - Core logic for NeuroTrack AI web app
// ---------------------------------------------------
// Data persistence using localStorage (equivalent to productivity_data.json)
const STORAGE_KEY = "neuroData";
let neuroData = { history: {} };

// Weekly schedule provided by the user
const WEEKLY_SCHEDULE = {
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
};

// ---------------------------------------------------
// Utility Functions
// ---------------------------------------------------
function loadData() {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
        try { neuroData = JSON.parse(stored); } catch (_) { neuroData = { history: {} }; }
    } else {
        neuroData = { history: {} };
    }
}
function saveData() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(neuroData));
}
function getDayHabits(dateObj) {
    const dayName = dateObj.toLocaleDateString('en-US', { weekday: 'long' });
    return WEEKLY_SCHEDULE[dayName] || [];
}
function getTodayStr() { return new Date().toISOString().split('T')[0]; }
function initDayIfMissing(dateStr) {
    if (!neuroData.history[dateStr]) {
        const dateObj = new Date(dateStr);
        const habits = getDayHabits(dateObj);
        neuroData.history[dateStr] = { habits: {}, score: 0 };
        habits.forEach(h => neuroData.history[dateStr].habits[h] = false);
    }
}
function calculateScore(completedCount, total) {
    return total ? Math.round((completedCount / total) * 100) : 0;
}
function calculateStreak() {
    let streak = 0;
    let cur = new Date();
    while (true) {
        const key = cur.toISOString().split('T')[0];
        const day = neuroData.history[key];
        if (day && day.score > 0) {
            streak++;
            cur.setDate(cur.getDate() - 1);
        } else {
            break;
        }
    }
    return streak;
}
function getStatus(score) {
    if (score >= 80) return { text: "Excellent", color: "#2ecc71" };
    if (score >= 50) return { text: "Good", color: "#f39c12" };
    return { text: "Focus Needed", color: "#e74c3c" };
}
function getInsight(score) {
    if (score === 100) return "You're on fire! 🔥 An absolute productivity machine today.";
    if (score >= 60) return "Solid progress! 🚀 Push a bit more to achieve perfection today.";
    if (score > 0) return "You've started, which is the hardest part. Keep the momentum going! ⚡";
    return "A fresh day! Let's conquer those tasks. Remember: small consistent steps. 🌌";
}

// ---------------------------------------------------
// UI Rendering Functions
// ---------------------------------------------------
function renderMetrics() {
    const todayStr = getTodayStr();
    const todayData = neuroData.history[todayStr];
    const todayScore = todayData ? todayData.score : 0;
    const streak = calculateStreak();
    const perfectDays = Object.values(neuroData.history).filter(d => d.score === 100).length;
    const allScores = Object.values(neuroData.history).map(d => d.score);
    const avgScore = allScores.length ? (allScores.reduce((a,b)=>a+b,0)/allScores.length).toFixed(1) : 0;
    const status = getStatus(todayScore);

    document.getElementById('statusBadge').textContent = `● ${status.text}`;
    document.getElementById('statusBadge').style.color = status.color;
    document.getElementById('statusBadge').style.borderColor = `${status.color}55`;
    document.getElementById('statusBadge').style.background = `${status.color}1a`;
    document.getElementById('statusBadge').style.boxShadow = `0 0 15px ${status.color}33`;

    // Metric cards – we inject simple HTML
    document.getElementById('todayScoreCard').innerHTML = `<h4>Today's Score</h4><div class="value">${todayScore}%</div>`;
    document.getElementById('streakCard').innerHTML = `<h4>Current Streak</h4><div class="value">${streak} Days 🔥</div>`;
    document.getElementById('perfectDaysCard').innerHTML = `<h4>Perfect Days</h4><div class="value">${perfectDays} 💎</div>`;
    document.getElementById('avgPerfCard').innerHTML = `<h4>Avg Performance</h4><div class="value">${avgScore}%</div>`;
}

function renderHeatmap() {
    const today = new Date();
    // Calculate start date (1 year ago, aligned to Sunday)
    const startDate = new Date();
    startDate.setDate(today.getDate() - 364);
    while (startDate.getDay() !== 0) {
        startDate.setDate(startDate.getDate() - 1);
    }
    
    const weeks = [];
    const monthLabels = [];
    let currentMonth = -1;
    let curDate = new Date(startDate);
    
    for (let w = 0; w < 53; w++) {
        const week = [];
        let weekMonth = -1;
        for (let d = 0; d < 7; d++) {
            if (curDate > today) {
                week.push(null);
            } else {
                const key = curDate.toISOString().split('T')[0];
                const dayData = neuroData.history[key];
                const score = dayData ? dayData.score : 0;
                let level = 0;
                if (score > 0) level = 1;
                if (score >= 40) level = 2;
                if (score >= 70) level = 3;
                if (score >= 90) level = 4;
                week.push({ date: key, score: score, level: level });
            }
            if (d === 0) weekMonth = curDate.getMonth();
            curDate.setDate(curDate.getDate() + 1);
        }
        weeks.push(week);
        
        if (weekMonth !== currentMonth) {
            monthLabels.push({ text: new Date(2000, weekMonth, 1).toLocaleString('en-US', { month: 'short' }), weekIndex: w });
            currentMonth = weekMonth;
        }
    }
    
    let html = `<div class="github-heatmap">`;
    // Months row
    html += `<div class="heatmap-months">`;
    let monthGridHtml = '';
    for(let w=0; w<53; w++) {
        const month = monthLabels.find(m => m.weekIndex === w);
        if (month) {
            monthGridHtml += `<div style="grid-column: span 1; white-space: nowrap;">${month.text}</div>`;
        } else {
            monthGridHtml += `<div></div>`;
        }
    }
    html += monthGridHtml + `</div>`;
    
    // Body (days + grid)
    html += `<div class="heatmap-body">`;
    html += `<div class="heatmap-days">`;
    const dayNames = ['','Mon','','Wed','','Fri',''];
    for(let i=0; i<7; i++) {
        html += `<div>${dayNames[i]}</div>`;
    }
    html += `</div>`;
    
    html += `<div class="heatmap-grid">`;
    for (let w = 0; w < 53; w++) {
        for (let d = 0; d < 7; d++) {
            const cell = weeks[w][d];
            if (cell) {
                let cellScore = cell.score;
                html += `<div class="heatmap-cell" data-level="${cell.level}" title="${cell.date}: ${cellScore}% Productivity"></div>`;
            } else {
                html += `<div style="width:12px; height:12px;"></div>`;
            }
        }
    }
    html += `</div></div>`; // End body & grid
    
    // Footer
    html += `<div class="heatmap-footer" style="justify-content: flex-end;">
        <div class="heatmap-legend">
            <span style="color: #8b949e; margin-right: 4px;">Less</span>
            <div class="heatmap-cell" data-level="0"></div>
            <div class="heatmap-cell" data-level="1"></div>
            <div class="heatmap-cell" data-level="2"></div>
            <div class="heatmap-cell" data-level="3"></div>
            <div class="heatmap-cell" data-level="4"></div>
            <span style="color: #8b949e; margin-left: 4px;">More</span>
        </div>
    </div>`;
    html += `</div>`;
    
    document.getElementById('heatmap').innerHTML = html;
    
    // Automatically scroll to the present date (right side)
    const heatmapEl = document.querySelector('.github-heatmap');
    if (heatmapEl) {
        heatmapEl.scrollLeft = heatmapEl.scrollWidth;
    }
}

function renderInsight() {
    const todayScore = neuroData.history[getTodayStr()]?.score || 0;
    const insight = getInsight(todayScore);
    document.getElementById('insightText').innerHTML = insight;
}

function renderDashboard() {
    renderMetrics();
    renderHeatmap();
    renderInsight();
}

function renderTracker(dateStr) {
    const dayData = neuroData.history[dateStr];
    const tasksDiv = document.getElementById('taskList');
    tasksDiv.innerHTML = '';
    const habits = Object.keys(dayData.habits);
    habits.forEach(h => {
        const card = document.createElement('div');
        card.className = 'toggle-card' + (dayData.habits[h] ? ' checked' : '');
        card.dataset.task = h;
        card.innerHTML = `<span>${h}</span>`;
        card.addEventListener('click', () => {
            dayData.habits[h] = !dayData.habits[h];
            card.classList.toggle('checked');
            // Recalculate score
            const completed = Object.values(dayData.habits).filter(v=>v).length;
            dayData.score = calculateScore(completed, habits.length);
            saveData();
            renderGauge(dayData.score);
            if (dayData.score === 100) triggerReward();
        });
        tasksDiv.appendChild(card);
    });
    renderGauge(dayData.score);
}

function renderGauge(score) {
    const data = [{
        type: 'indicator',
        mode: 'gauge+number',
        value: score,
        number: {suffix:'%', font:{size:50, color:'#fff'}},
        gauge: {
            axis: {range:[0,100], visible:false},
            bar: {color:'#2ecc71'},
            bgcolor:'rgba(255,255,255,0.05)',
            borderwidth:0,
            shape:'angular'
        }
    }];
    const layout = {height:250, margin:{l:10,r:10,t:10,b:10}, paper_bgcolor:'rgba(0,0,0,0)'};
    Plotly.newPlot('gauge', data, layout, {displayModeBar:false, responsive:true});
}

function renderWeeklyChart() {
    const today = new Date();
    const dates = [];
    const scores = [];
    for (let i = 6; i >= 0; i--) {
        const d = new Date();
        d.setDate(today.getDate() - i);
        const key = d.toISOString().split('T')[0];
        dates.push(d.toLocaleDateString('en-US', {weekday:'short'}));
        scores.push(neuroData.history[key]?.score || 0);
    }
    const trace = {
        x: dates,
        y: scores,
        type: 'scatter',
        mode: 'lines+markers',
        line: {shape:'spline', color:'#00f2fe'},
        fill: 'tozeroy',
        fillcolor: 'rgba(0,242,254,0.2)',
        marker: {size:8, color:'#4facfe', line:{width:2, color:'#fff'}}
    };
    const layout = {
        height:300,
        margin:{l:30,r:30,t:30,b:30},
        paper_bgcolor:'rgba(0,0,0,0)',
        plot_bgcolor:'rgba(0,0,0,0)',
        xaxis:{showgrid:false},
        yaxis:{showgrid:true, gridcolor:'rgba(255,255,255,0.05)', range:[0,105]},
        font:{color:'#a1a1aa'}
    };
    Plotly.newPlot('weeklyChart', [trace], layout, {displayModeBar:false, responsive:true});
}

function renderMonthlyChart() {
    const today = new Date();
    const monthPrefix = today.toISOString().slice(0,7); // YYYY-MM
    const monthDays = Object.keys(neuroData.history).filter(k=>k.startsWith(monthPrefix));
    if (!monthDays.length) {
        document.getElementById('monthlyChart').innerHTML = '<p>No data for this month yet.</p>';
        document.getElementById('monthlyStats').innerHTML = '';
        return;
    }
    const scores = monthDays.map(k=>neuroData.history[k].score);
    const avg = scores.reduce((a,b)=>a+b,0)/scores.length;
    const pie = {
        values: [avg, 100-avg],
        hole: .75,
        type: 'pie',
        marker: {colors:['#a855f7','rgba(255,255,255,0.05)']},
        textinfo:'none',
        hoverinfo:'skip'
    };
    const layout = {
        height:250,
        margin:{l:0,r:0,t:0,b:0},
        paper_bgcolor:'rgba(0,0,0,0)',
        showlegend:false,
        annotations:[{text:`${avg.toFixed(0)}%`, x:0.5, y:0.5, font:{size:30, color:'#fff'}, showarrow:false}]
    };
    Plotly.newPlot('monthlyChart', [pie], layout, {displayModeBar:false, responsive:true});
    // Stats
    let totalTasks = 0, completedTasks = 0;
    monthDays.forEach(k=>{
        const habits = Object.keys(neuroData.history[k].habits);
        totalTasks += habits.length;
        completedTasks += Object.values(neuroData.history[k].habits).filter(v=>v).length;
    });
    const statsDiv = document.getElementById('monthlyStats');
    statsDiv.innerHTML = `
        <p><strong>Average Score:</strong> ${avg.toFixed(1)}%</p>
        <p><strong>Tasks Finished:</strong> ${completedTasks} / ${totalTasks}</p>
        <div style="background:rgba(255,255,255,0.1); height:8px; border-radius:4px; overflow:hidden;">
            <div style="width:${totalTasks? (completedTasks/totalTasks*100).toFixed(0):0}%; height:100%; background:var(--primary-neon);"></div>
        </div>`;
}

function triggerReward() {
    // Simple modal overlay
    const modal = document.createElement('div');
    modal.style.position = 'fixed';
    modal.style.top = 0; modal.style.left = 0; modal.style.right = 0; modal.style.bottom = 0;
    modal.style.background = 'rgba(0,0,0,0.8)';
    modal.style.display = 'flex';
    modal.style.alignItems = 'center';
    modal.style.justifyContent = 'center';
    modal.style.zIndex = 10000;
    modal.innerHTML = `<div class="glass-card" style="background:linear-gradient(45deg, rgba(39,174,96,0.4), rgba(41,128,185,0.4)); text-align:center; animation:popIn 0.5s ease-out;">
        <h2 style="color:white; margin-top:0;">🎉 Protocol Completed!</h2>
        <p style="color:#eee; font-size:1.2rem; margin-bottom:0;"><b>🎮 Minecraft Time Unlocked!</b> Enjoy your reward.</p>
    </div>`;
    document.body.appendChild(modal);
    // Confetti
    confetti({particleCount:100, spread:70, origin:{y:0.6}});
    setTimeout(()=>{ document.body.removeChild(modal); }, 4000);
}

function initNavigation() {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', e => {
            e.preventDefault();
            const page = link.dataset.page;
            // Update active link
            document.querySelectorAll('.nav-link').forEach(l=>l.classList.remove('active'));
            link.classList.add('active');
            // Show page
            document.querySelectorAll('.page-section').forEach(sec=>sec.classList.remove('active'));
            document.getElementById(page).classList.add('active');
            // Page‑specific actions
            if (page === 'dashboard') renderDashboard();
            else if (page === 'tracker') {
                const todayStr = getTodayStr();
                document.getElementById('datePicker').value = todayStr;
                renderTracker(todayStr);
            } else if (page === 'analytics') {
                renderWeeklyChart();
                renderMonthlyChart();
            }
        });
    });
    // Date picker change
    const datePicker = document.getElementById('datePicker');
    datePicker.addEventListener('change', () => {
        const sel = datePicker.value;
        initDayIfMissing(sel);
        renderTracker(sel);
    });
}

function initTheme() {
    const stored = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', stored);
    const btn = document.getElementById('themeToggle');
    btn.addEventListener('click', () => {
        const cur = document.documentElement.getAttribute('data-theme');
        const next = cur === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
    });
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    overlay.classList.add('hidden');
    setTimeout(()=>{ overlay.style.display='none'; }, 300);
}

// ---------------------------------------------------
// Initialization
// ---------------------------------------------------
function initApp() {
    loadData();
    const todayStr = getTodayStr();
    initDayIfMissing(todayStr);
    initNavigation();
    initTheme();
    // Default page is dashboard
    document.querySelector('.nav-link[data-page="dashboard"]').click();
    hideLoading();
}

window.addEventListener('DOMContentLoaded', initApp);
