// static/js/themeToggle.js

document.addEventListener("DOMContentLoaded", () => {
  const switchEl = document.getElementById("theme-toggle-switch");
  if (!switchEl) return;

  // Get stored theme or default
  const savedTheme = localStorage.getItem("theme") || "auto";
  document.documentElement.setAttribute("data-theme", savedTheme);

  // Set switch state based on theme
  switchEl.checked = savedTheme === "dark";

  switchEl.addEventListener("change", () => {
    const newTheme = switchEl.checked ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
  });
});