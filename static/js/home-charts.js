fetch("http://127.0.0.1:5000/stats")
    .then(res => res.json())
    .then(data => {
        const labels = data.products.map(p => p.name);
        const qty = data.products.map(p => p.qty);

        // MINI BAR
        new Chart(document.getElementById("miniBar"), {
            type: "bar",
            data: {
                labels,
                datasets: [{
                    data: qty,
                    backgroundColor: "#7c6ee6",
                    barThickness: 25
                }]
            },
            options: {
                plugins: { legend: { display: false } },
                maintainAspectRatio: false
            }
        });

        // MINI PIE
        new Chart(document.getElementById("miniPie"), {
            type: "doughnut",
            data: {
                labels,
                datasets: [{
                    data: qty,
                    backgroundColor: [
                        "#7c6ee6",
                        "#9b8df2",
                        "#c7d2fe",
                        "#ede9fe"
                    ]
                }]
            },
            options: {
                cutout: "65%",
                maintainAspectRatio: false
            }
        });
    });
