fetch("http://127.0.0.1:5000/stats")
    .then(res => res.json())
    .then(data => {
        console.log("Dashboard data:", data);

        const products = data.products;
        if (!products || products.length === 0) {
            alert("No products to show");
            return;
        }

        const labels = products.map(p => p.name);
        const quantities = products.map(p => p.qty);

        /* ===== BAR CHART ===== */
        new Chart(document.getElementById("barChart"), {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                    label: "Product Quantity",
                    data: quantities,
                    backgroundColor: "#7c6ee6",   // SAME COLOR
                    barThickness: 45,             // ✔ balanced thickness
                    maxBarThickness: 55,
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });

        /* ===== PIE CHART ===== */
        new Chart(document.getElementById("pieChart"), {
            type: "pie",
            data: {
                labels: labels,
                datasets: [{
                    data: quantities,
                    backgroundColor: [
                        "#7c6ee6",
                        "#9b8df2",
                        "#c7d2fe",
                        "#e0e7ff",
                        "#ede9fe"
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    })
    .catch(err => {
        console.error("Chart error:", err);
        alert("Error loading dashboard");
    });
