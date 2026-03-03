function animateValue(id, start, end, duration) {
    const element = document.getElementById(id);
    let startTimestamp = null;

    function step(timestamp) {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        element.innerText = Math.floor(progress * (end - start) + start);

        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    }

    window.requestAnimationFrame(step);
}

fetch("http://127.0.0.1:5000/stats")
    .then(res => res.json())
    .then(data => {
        animateValue("totalProducts", 0, data.totalProducts, 800);
        animateValue("totalQuantity", 0, data.totalQuantity, 900);
        animateValue("lowStock", 0, data.lowStock, 800);
        animateValue("inventoryValue", 0, data.inventoryValue, 1000);
    });
// INVENTORY HEALTH STATUS
fetch("http://127.0.0.1:5000/stats")
    .then(res => res.json())
    .then(data => {
        const lowStock = data.lowStock;

        const statusBox = document.getElementById("healthStatus");
        const text = document.getElementById("healthText");
        const icon = document.getElementById("healthIcon");

        if (lowStock === 0) {
            statusBox.className = "health-status healthy";
            text.innerText = "Healthy";
            icon.style.color = "#16a34a";
        }
        else if (lowStock <= 3) {
            statusBox.className = "health-status warning";
            text.innerText = "Attention Needed";
            icon.style.color = "#ca8a04";
        }
        else {
            statusBox.className = "health-status critical";
            text.innerText = "Critical";
            icon.style.color = "#dc2626";
        }
    });
