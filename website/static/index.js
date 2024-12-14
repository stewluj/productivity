// delete our notes
function deleteNote(noteId) {
    //make post request to deltenote endpoint
  fetch("/delete-note", {
      method: "POST",
      headers: { "Content-Type": "application/json" }, // Ensure proper headers
      body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
      window.location.href = "/"; //redirect user
  });
}
//delte calendar events
function deleteEvent(eventId) {
    //ask user for confiramtion first
  if (confirm("Are you sure you want to delete this event?")) {
    //make post request to the /delete-event endpoint
      fetch("/delete-event", {
          method: "POST",
          headers: { "Content-Type": "application/json" }, // Ensure proper headers
          body: JSON.stringify({ eventId: eventId }),  // Send eventId as JSON
      }).then((response) => {
          if (response.ok) {
              window.location.href = "/calendar";  // Reload the page
          } else {
            //if response does not work send error message
              response.json().then((data) => alert(data.error || "Failed to delete event."));
          }
      });
  }
}
//delete an activity
function deleteActivity(activityId) {
    //make post request to delete-activity endpoint
    fetch("/delete-activity", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ activityId: activityId }), //convert into JSON object
    }).then((_res) => {
        //redirect
        window.location.href = "/activities";
    });
}
