# NeuroTrack Habit Tracker

A React app organised around a dashboard, daily tracker, analytics, and settings. The repository uses the `neurotrack-app/` directory for the frontend.

**Stack:** React, Vite, JavaScript, Tailwind CSS, Framer Motion

![NeuroTrack workflow](docs/readme-architecture.svg)

## App flow

1. Initialise the current day's data when the app loads.
2. Record daily habit activity in the tracker.
3. Review progress through the analytics view.
4. Navigate between dashboard, tracker, analytics, and settings.

## Run locally

```bash
git clone https://github.com/chyk2468/Habit-Tracker-AI.git
cd Habit-Tracker-AI/neurotrack-app
npm install
npm run dev
```

Open the local URL printed by Vite.

## Source layout

- `src/App.jsx`: app shell and view selection
- `src/hooks/useNeuroData`: daily data logic
- `src/pages/`: dashboard, tracker, analytics, and settings
- `src/components/layout/`: navigation/sidebar
- `src/`: UI styling and reusable components

Use the current UI and source files as the reference for available tracking options.
