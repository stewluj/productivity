function deleteNote(noteId) {
  fetch("/delete-note", {
      method: "POST",
      headers: { "Content-Type": "application/json" }, // Ensure proper headers
      body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
      window.location.href = "/";
  });
}

function deleteEvent(eventId) {
  if (confirm("Are you sure you want to delete this event?")) {
      fetch("/delete-event", {
          method: "POST",
          headers: { "Content-Type": "application/json" }, // Ensure proper headers
          body: JSON.stringify({ eventId: eventId }),  // Send eventId as JSON
      }).then((response) => {
          if (response.ok) {
              window.location.href = "/calendar";  // Reload the page
          } else {
              response.json().then((data) => alert(data.error || "Failed to delete event."));
          }
      });
  }
}
