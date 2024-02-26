// Remove alert message after 4 seconds
const alert = document.querySelector('[role="alert"]');
if (alert) {
  setTimeout(() => {
    alert.classList.add("fade");
    document.querySelector('[role="container"]').removeChild(alert);
  }, 3500);
}