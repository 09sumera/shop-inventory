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

    const currentPath = window.location.pathname;

    document.querySelectorAll(".sidebar a").forEach(link => {

        const linkPath = link.getAttribute("href");

        if (linkPath && currentPath.includes(linkPath)) {
            link.classList.add("active");
        }

    });

});
function toggleSidebar() {
    const sidebar = document.querySelector(".sidebar");
    sidebar.classList.toggle("show");
}