document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("form").forEach((form) => {
    form.addEventListener("submit", () => form.querySelectorAll("button[type=submit], button:not([type])").forEach((btn) => btn.disabled = true));
  });
});
