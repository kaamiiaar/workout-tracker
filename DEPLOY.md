# Publishing to GitHub Pages

This app can be published as a static GitHub Pages site. The Python server is
only needed for the local desktop app.

## What Goes to GitHub

- `index.html`
- `video-config.js`
- `README.md`
- optional local helper files, if you want to keep them backed up

Do not commit the `.mp4` files. They are ignored because the videos are too
large for a normal GitHub Pages repo.

## Video Hosting

Upload the videos to a public video/file host, then paste the public video URLs
into `video-config.js`.

Example:

```js
window.WORKOUT_VIDEO_URLS = {
  1: "https://example.com/path/to/workout-1.mp4",
  2: "https://example.com/path/to/workout-2.mp4",
};
```

The video links are public. A browser cannot play a private video URL without
exposing enough information for visitors to request the video.

## Progress Data

On GitHub Pages, progress is saved in the browser with `localStorage`. That
means your Mac browser and phone browser have separate progress unless a real
backend/database is added later.

The local desktop app still saves to `workout-db.json` through `server.py`.
