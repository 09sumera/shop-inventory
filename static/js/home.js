fetch("http://127.0.0.1:5000/stats")
    .then(res => res.json())
    .then(data => {
        document.getElementById("kpiProducts").innerText = data.totalProducts;
        document.getElementById("kpiQuantity").innerText = data.totalQuantity;
        document.getElementById("kpiLow").innerText = data.lowStock;
        document.getElementById("kpiValue").innerText = data.inventoryValue;
    })
    .catch(() => {
        console.log("Failed to load KPI data");
    });
