// Served at /static/js/main.js and linked from templates/base.html.
console.log("Qonnect starter app loaded");

const joinForm = document.getElementById("join-form");
if (joinForm) {
  joinForm.addEventListener("submit", () => {
    const button = joinForm.querySelector("button[type=submit]");
    button.disabled = true;
    button.textContent = "Getting your ticket…";
  });
}

const firstInvalid = document.querySelector(".is-invalid");
if (firstInvalid) firstInvalid.focus();

// Ask before any form marked data-confirm, such as a hard delete.
document.querySelectorAll("form[data-confirm]").forEach((form) => {
  form.addEventListener("submit", (event) => {
    if (!confirm(form.dataset.confirm)) event.preventDefault();
  });
});