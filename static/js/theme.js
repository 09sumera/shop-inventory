
// Apply saved theme
(function () {
    const theme = localStorage.getItem("theme");
    if (theme === "dark") {
        document.body.classList.add("dark");
    }
})();

// Toggle dark mode
function toggleDarkMode() {
    document.body.classList.toggle("dark");

    if (document.body.classList.contains("dark")) {
        localStorage.setItem("theme", "dark");
    } else {
        localStorage.setItem("theme", "light");
    }
}

// Active sidebar link
document.addEventListener("DOMContentLoaded", () => {
    const page = window.location.pathname.split("/").pop();

    document.querySelectorAll(".sidebar a").forEach(link => {
        if (link.getAttribute("href") === page) {
            link.classList.add("active");
        }
    });
});
