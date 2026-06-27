# Workout Tracker

Daily workout video tracker with progress insights.

## Public Web Version

This app can run as a static GitHub Pages site from `index.html`.

- Progress saves in each browser with `localStorage`.
- Optional Google Sheet sync can share progress across devices.
- Videos are not stored in this repo.
- Add public video links in `video-config.js`.
- See `DEPLOY.md` for the GitHub Pages flow.
- See `SYNC.md` for the Google Apps Script sync setup.

## Quick Start

### Option 1: From Spotlight (Recommended) ⭐
1. Press `Cmd + Space` to open Spotlight
2. Type: `Workout Tracker`
3. Press Enter (opens a native app window, no browser)

The app is installed in: `/Users/kaamiaar/Applications/Workout Tracker.app`

### Option 2: From Terminal
```bash
cd /Users/kaamiaar/workout
python3 server.py
```

Then open: http://localhost:8081

## Features

- **Today View**: Auto-suggests next workout in sequence (currently Workout 19)
- **Video Player**: Full-screen capable with seeking support
- **Mark as Done**: Track completions with dates
- **All Workouts**: Browse all 24 workouts filtered by body part
- **Insights**: View streaks, weekly activity, and body part distribution
- **Sync**: Optional Google Sheet-backed progress sync across devices

## Files

- `index.html` - Web app interface
- `video-config.js` - Public video URL config for static hosting
- `server.py` - HTTP server with video streaming (port 8081)
- `workout_app.py` - Native desktop launcher (embedded webview + server lifecycle)
- `workout-db.json` - Your workout completion history
- `start-workout-tracker.sh` - Launcher script for easy Spotlight access

## Design

- Red accent color for workout theme
- Body part colors: Chest (red), Arms (purple), Abs (coral), Legs (green)
- Dark mode enabled by default
- Mobile responsive

## Note

The Spotlight app launches a native window and owns the server lifecycle. Closing the app window terminates the local server automatically.
