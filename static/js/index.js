// Remove alert message after 4 seconds
const alert = document.querySelector('[role="alert"]');
if (alert) {
  setTimeout(() => {
    alert.classList.add("fade");
    document.querySelector('[role="container"]').removeChild(alert);
  }, 3500);
}

const dash_updateForm = document.querySelector('[role="dash-update"]');
const form_body = document.querySelector('[role="dash-update-body"]');
dash_updateForm.addEventListener('click', function() {
  form_body.classList.toggle("opacity-0");
});