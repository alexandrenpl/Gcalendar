function doPost(e) {
  try {
    // Ler o corpo do pedido (assumindo que vem em JSON)
    const data = JSON.parse(e.postData.contents);

    // Obter o calendário (usa o teu calendarId se não for o predefinido)
    const cal = CalendarApp.getDefaultCalendar();

    // Criar evento
    const start = new Date(data.start);  // formato ISO: "2025-10-05T10:00:00Z"
    const end = new Date(data.end);
    const event = cal.createEvent(data.title, start, end, {
      description: data.description || "",
      location: data.location || ""
    });

    // Resposta para quem chamou
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

