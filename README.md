# Google Calendar GUI - Send Events

Desktop application for Windows that allows sending events to Google Calendar through a Google Apps Script Web App.

## Features

- Simple and intuitive graphical interface
- Configuration via `.env` file
- JSON editor with validation and formatting
- Pre-defined templates for events
- Secure HTTP POST sending without authentication
- Technical error logging
- Supports multiple events in a single JSON
- Multi-event payload handling

## Requirements

- Python 3.10 or higher
- Windows 10/11

## Installation and Execution

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the application

```bash
python gcal_gui.py
```

## Creating Executable (.exe)

### 1. Install PyInstaller

```bash
pip install pyinstaller
```

### 2. Create executable

```bash
pyinstaller --onefile --windowed --name GoogleCalendarGUI gcal_gui.py
```

The executable will be created in `dist/GoogleCalendarGUI.exe`.

**Note:** Some antiviruses may detect false positives in executables created with PyInstaller. This is normal and can be safely ignored.

### Quick commands (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --windowed --name GoogleCalendarGUI gcal_gui.py
```

After completion, you'll find `dist/GoogleCalendarGUI.exe`.

## Configuration

### .env File

The application uses a `.env` file to store configurations:

```
WEB_APP_URL=https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec
CALENDAR_ID=primary
```

### How to get credentials

1. **Web App URL**: URL of your Google Apps Script Web App
2. **Calendar ID**: Calendar ID (optional - script always uses default calendar)

## Usage

### 1. Configuration

- Fill in the configuration fields (URL, Calendar ID)
- Click "Save .env" to persist configurations

### 2. JSON Editor

- Use "Insert Test Template" for a basic example
- Load existing JSON files
- Format JSON for better readability
- Validate syntax before sending

Supports:
- Single event (JSON object)
- Multiple events (object with `events` key containing a list)
- Multiple events as top-level list (top-level array)

### 3. Sending

- Click "Send to Web App"
- Response will appear in the response area
- Check HTTP status and response content

## JSON Templates

### Single Event

```json
{
  "title": "Test Event",
  "start": "2025-09-22T09:30:00+01:00",
  "end": "2025-09-22T10:00:00+01:00",
  "description": "Test event created via Web App (Apps Script).",
  "location": "Test Location"
}
```

### Multiple Events

```json
{
  "events": [
    {
      "title": "Productive Block 1",
      "start": "2025-09-22T09:00:00+01:00",
      "end": "2025-09-22T11:00:00+01:00",
      "description": "Decide concrete morning task."
    },
    {
      "title": "Lunch + kitchen cleanup",
      "start": "2025-09-22T13:00:00+01:00",
      "end": "2025-09-22T15:00:00+01:00",
      "description": "Prepare lunch, eat and clean kitchen."
    }
  ]
}
```

### Multiple Events (top-level list)

```json
[
  {
    "title": "Event A",
    "start": "2025-09-23T09:00:00+01:00",
    "end": "2025-09-23T10:00:00+01:00",
    "description": "Event A description"
  },
  {
    "title": "Event B",
    "start": "2025-09-23T11:00:00+01:00",
    "end": "2025-09-23T12:00:00+01:00",
    "location": "Event B location"
  }
]
```

Notes:
- The app sends one POST per event to your Apps Script Web App.
- The response area shows a summary with success/failure per event.
- The script always uses the default calendar (no need for `calendarId`).

## File Structure

```
Gcalendar/
├── gcal_gui.py          # Main application
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── .env                # Configurations (created automatically)
└── gcal_gui.log        # Error log (created automatically)
```

## Troubleshooting

### Connection Error

- Verify the Web App URL is correct
- Confirm the Web App is published and accessible
- Check internet connection

### Web App Connection Error

- **Use the "🔧 Debug" button** to check current configuration
- Confirm the Web App is published as "Anyone"
- Verify the Web App has necessary permissions for Google Calendar
- Test the Web App URL directly in browser
- Check the `gcal_gui.log` file for technical details

### Invalid JSON

- Use the "Format JSON" button to validate syntax
- Check all keys are in quotes
- Confirm commas and braces are correct

### Debug Tools

The application includes several tools to help with troubleshooting:

1. **"🔧 Debug" button** - Shows detailed information about current configuration
2. **Detailed logs** - `gcal_gui.log` file with technical information
3. **Web App Test** - Opens URL directly in browser

## Logs

Technical errors are logged in the `gcal_gui.log` file to facilitate troubleshooting.

## License

This project is provided as-is, without warranties.