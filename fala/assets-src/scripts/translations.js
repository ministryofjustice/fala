/**
 * Handles language switcher form submission when clicked.
 */
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("language_switcher_form");

  if (form) {
      form.addEventListener("click", () => form.submit());
  }
});
