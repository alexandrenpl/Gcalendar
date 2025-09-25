function doPost(e) {
  try {
    // Read request body (assuming it comes in JSON)
    const data = JSON.parse(e.postData.contents);

    // Get calendar (uses your calendarId if not default)
    const cal = CalendarApp.getDefaultCalendar();

    // Create event
    const start = new Date(data.start);  // ISO format: "2025-10-05T10:00:00Z"
    const end = new Date(data.end);
    const event = cal.createEvent(data.title, start, end, {
      description: data.description || "",
      location: data.location || ""
    });

    // Response for caller
    return ContentService.createTextOutput(
      JSON.stringify({ status: "ok", eventId: event.getId() })
    ).setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService.createTextOutput(
      JSON.stringify({ status: "error", message: err.message })
    ).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet() {
  return ContentService.createTextOutput("OK");
}

