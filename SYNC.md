# Google Sheet Sync

GitHub Pages cannot write to a local JSON file, so this app can sync progress
through a Google Apps Script attached to a Google Sheet.

## Setup

1. Create a Google Sheet named `Workout Tracker Sync`.
2. Open `Extensions > Apps Script`.
3. Replace the default script with `google-apps-script/Code.gs`.
4. Change `SYNC_KEY` to a long random secret.
5. Deploy with `Deploy > New deployment > Web app`.
6. Set `Execute as` to `Me`.
7. Set `Who has access` to `Anyone`.
8. Copy the Web app URL.

In the workout app, click the cloud button and enter:

- the Web app URL
- the same sync key

The URL and key are stored only in that browser's localStorage. They are not
committed to the public repo.

## Notes

- The Google Sheet stores one JSON blob in a hidden `Workout Sync` sheet.
- `GET` requests use JSONP so the static app can read the data from GitHub
  Pages.
- `POST` requests use `no-cors`, so saves are fire-and-forget from the browser.
  Use the Sync button to pull and confirm current data.
