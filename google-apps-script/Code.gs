const SYNC_KEY = "CHANGE_THIS_TO_A_LONG_RANDOM_SECRET";
const SHEET_NAME = "Workout Sync";
const DATA_CELL = "A2";

const EMPTY_DATA = {
  completions: [],
  settings: {
    darkMode: false,
    lastCompleted: 0,
    updatedAt: 0,
  },
};

function doGet(e) {
  const callback = String(e.parameter.callback || "");
  const action = String(e.parameter.action || "load");
  const key = String(e.parameter.key || "");

  const result =
    key === SYNC_KEY
      ? handleAction(action, null)
      : { ok: false, error: "Invalid sync key" };

  return jsonp(callback, result);
}

function doPost(e) {
  let payload = {};
  try {
    payload = JSON.parse(e.postData.contents || "{}");
  } catch (error) {
    return json({ ok: false, error: "Invalid JSON" });
  }

  if (String(payload.key || "") !== SYNC_KEY) {
    return json({ ok: false, error: "Invalid sync key" });
  }

  return json(handleAction(String(payload.action || ""), payload.data));
}

function handleAction(action, data) {
  if (action === "load") {
    return { ok: true, data: loadData() };
  }

  if (action === "save") {
    if (!isValidData(data)) {
      return { ok: false, error: "Invalid workout data" };
    }
    saveData(data);
    return { ok: true };
  }

  return { ok: false, error: "Unknown action" };
}

function loadData() {
  const sheet = getDataSheet();
  const raw = String(sheet.getRange(DATA_CELL).getValue() || "");
  if (!raw) return EMPTY_DATA;

  try {
    const parsed = JSON.parse(raw);
    return isValidData(parsed) ? parsed : EMPTY_DATA;
  } catch (error) {
    return EMPTY_DATA;
  }
}

function saveData(data) {
  const sheet = getDataSheet();
  sheet.getRange("A1").setValue("workout-db-json");
  sheet.getRange(DATA_CELL).setValue(JSON.stringify(data));
  sheet.getRange("B1").setValue("updated-at");
  sheet.getRange("B2").setValue(new Date());
}

function getDataSheet() {
  const properties = PropertiesService.getScriptProperties();
  let spreadsheetId = properties.getProperty("SPREADSHEET_ID");
  let spreadsheet;

  if (spreadsheetId) {
    spreadsheet = SpreadsheetApp.openById(spreadsheetId);
  } else {
    spreadsheet = SpreadsheetApp.create("Workout Tracker Sync");
    properties.setProperty("SPREADSHEET_ID", spreadsheet.getId());
  }

  let sheet = spreadsheet.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = spreadsheet.insertSheet(SHEET_NAME);
    sheet.hideSheet();
  }
  return sheet;
}

function isValidData(value) {
  return Boolean(
    value &&
      Array.isArray(value.completions) &&
      value.settings &&
      typeof value.settings.darkMode === "boolean"
  );
}

function json(payload) {
  return ContentService.createTextOutput(JSON.stringify(payload)).setMimeType(
    ContentService.MimeType.JSON
  );
}

function jsonp(callback, payload) {
  const safeCallback = /^[A-Za-z_$][\w$]*$/.test(callback)
    ? callback
    : "callback";
  return ContentService.createTextOutput(
    `${safeCallback}(${JSON.stringify(payload)});`
  ).setMimeType(ContentService.MimeType.JAVASCRIPT);
}
