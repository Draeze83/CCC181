// Served at /static/js/main.js and linked from templates/base.html.
console.log("Qonnect starter app loaded");

// Same rules and messages as join() in app.py, so the browser and Flask agree.
// [...text].length counts characters the way Python's len() does.
const JOIN_RULES = {
  name(field) {
    const name = field.value.trim();
    if (!name) return "Enter your name.";
    const length = [...name].length;
    if (length > 100) return `Your name must be 100 characters or fewer (you entered ${length}).`;
    return "";
  },
  student_id(field) {
    const studentId = field.value.trim();
    if (!studentId) return "Enter your student ID, for example 2024-0013.";
    if (studentId.length > 9) {
      return `Your student ID must be 9 characters or fewer, including the dash (you entered ${studentId.length}).`;
    }
    if (/^[0-9]{4}-?[0-9]{4}$/.test(studentId)) return "";
    return "Enter your 8-digit student ID, for example 2024-0013.";
  },
  email(field) {
    const email = field.value.trim();
    if (!email) return "Enter your school email.";
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return "Enter a valid email address, for example ana@school.edu.";
    if ([...email].length > 120) return "Your email must be 120 characters or fewer.";
    return "";
  },
  service_id(field) {
    return field.value ? "" : "Choose a service.";
  },
  has_documents(field) {
    return field.checked ? "" : "Confirm you have the required documents before joining.";
  },
};

function showError(field, message) {
  field.classList.toggle("is-invalid", Boolean(message));
  field.setAttribute("aria-invalid", message ? "true" : "false");
  document.getElementById(`${field.id}-error`).textContent = message;
}

const joinForm = document.getElementById("join-form");
if (joinForm) {
  joinForm.addEventListener("submit", (event) => {
    let firstError = null;
    for (const [id, rule] of Object.entries(JOIN_RULES)) {
      const field = document.getElementById(id);
      const message = rule(field);
      showError(field, message);
      if (message && !firstError) firstError = field;
    }
    if (firstError) {
      event.preventDefault();
      firstError.focus();
      return;
    }
    const button = joinForm.querySelector("button[type=submit]");
    button.disabled = true;
    button.textContent = "Getting your ticket…";
  });

  // Once a field shows an error, update the message as the user fixes it
  for (const [id, rule] of Object.entries(JOIN_RULES)) {
    const field = document.getElementById(id);
    const recheck = () => {
      if (field.classList.contains("is-invalid")) showError(field, rule(field));
    };
    field.addEventListener("input", recheck);
    field.addEventListener("change", recheck);
  }
}

const firstInvalid = document.querySelector(".is-invalid");
if (firstInvalid) firstInvalid.focus();

// Ask before any form marked data-confirm, such as a hard delete.
document.querySelectorAll("form[data-confirm]").forEach((form) => {
  form.addEventListener("submit", (event) => {
    if (!confirm(form.dataset.confirm)) event.preventDefault();
  });
});