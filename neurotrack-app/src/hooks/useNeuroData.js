import { useState, useEffect } from 'react';

const STORAGE_KEY = 'neuroData';

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

export function getTodayStr() {
    return new Date().toISOString().split('T')[0];
}

function calculateScore(habits) {
    const total = Object.keys(habits).length;
    if (total === 0) return 0;
    const completed = Object.values(habits).filter(Boolean).length;
    return Math.round((completed / total) * 100);
}

export function useNeuroData() {
    const [data, setData] = useState(() => {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
            try { return JSON.parse(stored); } catch (e) { console.error("Failed to parse local storage", e); }
        }
        return { history: {} };
    });

    useEffect(() => {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    }, [data]);

    const initDayIfMissing = (dateStr) => {
        if (!data.history[dateStr]) {
            const dateObj = new Date(dateStr);
            const dayName = dateObj.toLocaleDateString('en-US', { weekday: 'long' });
            const habitsList = WEEKLY_SCHEDULE[dayName] || [];
            
            const newHabits = {};
            habitsList.forEach(h => newHabits[h] = false);

            setData(prev => ({
                history: {
                    ...prev.history,
                    [dateStr]: { habits: newHabits, score: 0 }
                }
            }));
        }
    };

    const toggleHabit = (dateStr, habit) => {
        setData(prev => {
            const dayData = prev.history[dateStr];
            if (!dayData) return prev;

            const newHabits = { ...dayData.habits, [habit]: !dayData.habits[habit] };
            const newScore = calculateScore(newHabits);

            return {
                history: {
                    ...prev.history,
                    [dateStr]: { habits: newHabits, score: newScore }
                }
            };
        });
    };

    const getStreak = () => {
        let streak = 0;
        let cur = new Date();
        while (true) {
            const key = cur.toISOString().split('T')[0];
            const day = data.history[key];
            if (day && day.score > 0) {
                streak++;
                cur.setDate(cur.getDate() - 1);
            } else {
                break;
            }
        }
        return streak;
    };

    const getPerfectDays = () => {
        return Object.values(data.history).filter(d => d.score === 100).length;
    };

    const getAverageScore = () => {
        const scores = Object.values(data.history).map(d => d.score);
        if (scores.length === 0) return 0;
        return (scores.reduce((a, b) => a + b, 0) / scores.length).toFixed(1);
    };

    const getStatus = (score) => {
        if (score >= 80) return { text: "Peak Performance", color: "text-accent border-accent/30 bg-accent/10 shadow-[0_0_15px_rgba(16,185,129,0.3)]" };
        if (score >= 50) return { text: "Good Progress", color: "text-amber-400 border-amber-400/30 bg-amber-400/10 shadow-[0_0_15px_rgba(251,191,36,0.2)]" };
        return { text: "Focus Required", color: "text-rose-400 border-rose-400/30 bg-rose-400/10 shadow-[0_0_15px_rgba(251,113,133,0.2)]" };
    };

    const getWeeklyData = () => {
        const today = new Date();
        const dates = [];
        for (let i = 6; i >= 0; i--) {
            const d = new Date(today);
            d.setDate(today.getDate() - i);
            const key = d.toISOString().split('T')[0];
            dates.push({
                name: d.toLocaleDateString('en-US', { weekday: 'short' }),
                score: data.history[key]?.score || 0
            });
        }
        return dates;
    };

    return { 
        data, 
        initDayIfMissing, 
        toggleHabit, 
        getStreak, 
        getPerfectDays, 
        getAverageScore,
        getStatus,
        getWeeklyData
    };
}
