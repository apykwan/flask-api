// Remove alert message after 4 seconds
const alert = document.querySelector('[role="alert"]');
if (alert) {
  setTimeout(() => {
    alert.classList.add("fade");
    document.querySelector('[role="container"]').removeChild(alert);
  }, 3500);
}

// const dash_updateForm = document.querySelector('[role="dash-update"]');
// const form_body = document.querySelector('[role="dash-update-body"]');
// dash_updateForm.addEventListener('click', function() {
//   form_body.classList.toggle("opacity-0");
// });

const search_btn = document.querySelector('#search_btn');
const search_input = document.querySelector('#search_input');

search_btn.addEventListener('click', () => {
  console.log(search_input)
  console.log(search_input.value);
  if (!search_input.value) return alert('Please enter what you want to search!!!');
});