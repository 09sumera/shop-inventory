function addProduct() {
    fetch("http://127.0.0.1:5000/add", {
        method: "POST",
        credentials: "include",   // 🔥 IMPORTANT
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            id: 1,
            name: "Soap",
            price: 30,
            qty: 10
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        loadProducts();
    });
}


function loadProducts() {
    fetch("http://127.0.0.1:5000/products")
        .then(res => res.json())
        .then(data => {
            const table = document.getElementById("productTable");
            table.innerHTML = "";

            data.forEach(p => {
                table.innerHTML += `
                <tr>
                    <td>${p.id}</td>
                    <td>${p.name}</td>
                    <td>${p.price}</td>
                    <td>${p.qty}</td>
                    <td>
                        <button onclick="sellProduct(${p.id})">Sell</button>
                        <button onclick="restockProduct(${p.id})">Restock</button>
                        <button onclick="deleteProduct(${p.id})">Delete</button>
                    </td>
                </tr>`;
            });
        });
}


function sellProduct(id) {
    fetch("http://127.0.0.1:5000/sell", {
        method: "POST",
        credentials: "include",   // 🔥 IMPORTANT
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: id, qty: 1 })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        loadProducts();
    });
}


function restockProduct(id) {
    fetch("http://127.0.0.1:5000/restock", {
        method: "POST",
        credentials: "include",   // 🔥 IMPORTANT
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: id, qty: 5 })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        loadProducts();
    });
}


function deleteProduct(id) {
    fetch(`http://127.0.0.1:5000/delete/${id}`, {
        method: "DELETE",
        credentials: "include"   // 🔥 IMPORTANT
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        loadProducts();
    });
}