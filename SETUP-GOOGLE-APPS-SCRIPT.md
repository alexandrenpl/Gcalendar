# Google Apps Script Web App Configuration

## Identified Problem

The error you're receiving is because **all Google Apps Script Web Apps need a `doGet()` function** as an entry point, even if the application is mainly for processing POST requests.

## Solution

### 1. Create Project in Google Apps Script

1. Go to [script.google.com](https://script.google.com)
2. Click "New project"
3. Delete the default code
4. Paste the code from the `google-apps-script.gs` file
5. Save the project (Ctrl+S)

### 2. Configure Permissions

1. In the menu, go to "Run" → "Run function" → "testScript"
2. You'll be asked to authorize the script
3. Click "Review permissions"
4. Choose your Google account
5. Click "Advanced" → "Go to [project name] (unsafe)"
6. Click "Allow"

### 3. Publish as Web App

1. In the menu, go to "Deploy" → "New deployment"
2. Click the gear icon → "Web app"
3. Configure:
   - **Description**: "Google Calendar Web App"
   - **Execute as**: "Me"
   - **Who has access**: "Anyone"
4. Click "Deploy"
5. **Copy the generated URL** - this is the URL you should use in the Python application

### 4. Test the Web App

#### Test 1: GET Request (should work now)
- Open the Web App URL in browser
- You should see a JSON response with Web App information

#### Test 2: POST Request
- Use the Python application with the copied URL
- Configure a token (can be any string for testing)
- Test with the event template

### 5. Configure in Python Application

1. Open the Python application
2. In the "Web App URL" field, paste the URL copied from Google Apps Script
3. In the "Token" field, you can use any string (e.g., "test-token")
4. Click "Save .env"

## Code Structure

### `doGet()` Function
- **Required** for all Web Apps
- Responds to GET requests (when accessing URL in browser)
- Returns Web App information

### `doPost()` Function
- Processes POST requests from Python application
- Creates events in Google Calendar
- Validates data and returns JSON responses

### Helper Functions
- `testScript()`: Tests if the script is working
- `listCalendars()`: Lists available calendars

## Expected JSON Format

```json
{
  "title": "Event Title",
  "start": "2025-01-15T10:00:00+01:00",
  "end": "2025-01-15T11:00:00+01:00",
  "description": "Event description",
  "location": "Event location (optional)",
  "calendarId": "primary",
  "timeZone": "Europe/Lisbon",
  "reminders": {
    "popupMinutes": 10,
    "emailMinutes": 60
  }
}
```

## Troubleshooting

### Error: "doGet is not defined"
- **Cause**: `doGet()` function doesn't exist
- **Solution**: Add the `doGet()` function to the code

### Error: "Script not authorized"
- **Cause**: Script doesn't have permissions
- **Solution**: Run `testScript()` and authorize permissions

### Error: "Calendar not found"
- **Cause**: Incorrect Calendar ID
- **Solution**: Use "primary" or run `listCalendars()` to see available IDs

### Error: "Access denied"
- **Cause**: Web App is not public
- **Solution**: Configure as "Anyone" in deployment

## Logs and Debug

- Use `console.log()` in Google Apps Script for debugging
- Check logs in Python application (`gcal_gui.log` file)
- Use the "🔧 Debug" function in Python application for detailed information

## Security

- The Web App is configured to accept anyone
- For production, consider implementing proper authentication
- The current token is just for identification, not for real authentication