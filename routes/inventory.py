from flask import Blueprint, request, jsonify, current_app, session
from models.product import Product

inventory_bp = Blueprint("inventory", __name__)

# ================= HELPER =================
def products_collection():
    return current_app.config["PRODUCTS_COLLECTION"]

# ================= LOGIN CHECK =================
def require_login():
    if "user" not in session:
        return False
    return True


# ---------------- ADD PRODUCT ----------------
@inventory_bp.route("/add", methods=["POST"])
def add_product():
    if not require_login():
        return jsonify({"error": "Unauthorized. Please login."}), 401

    try:
        product = Product(request.json)
        valid, error = product.is_valid()

        if not valid:
            return jsonify({"error": error}), 400

        products = products_collection()

        # 🔹 Check duplicate product name
        existing_name = products.find_one({"name": product.name})
        if existing_name:
            return jsonify({"error": "Product with this name already exists"}), 400

        # 🔹 Existing ID → update quantity
        existing = products.find_one({"id": product.id})

        if existing:
            products.update_one(
                {"id": product.id},
                {"$inc": {"qty": product.qty}}
            )
            return jsonify({"message": "Product quantity updated"})
        else:
            products.insert_one(product.to_dict())
            return jsonify({"message": "Product added"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- GET ALL PRODUCTS ----------------
@inventory_bp.route("/products", methods=["GET"])
def get_products():
    products = list(products_collection().find({}, {"_id": 0}))
    return jsonify(products)


# ---------------- SELL PRODUCT ----------------
@inventory_bp.route("/sell", methods=["POST", "OPTIONS"])
def sell_product():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    if not require_login():
        return jsonify({"error": "Unauthorized. Please login."}), 401

    data = request.json
    products = products_collection()

    product = products.find_one({"id": data.get("id")})

    if not product:
        return jsonify({"error": "Product not found"}), 404

    qty = int(data.get("qty", 0))
    if product["qty"] < qty:
        return jsonify({"error": "Insufficient stock"}), 400

    products.update_one(
        {"id": data.get("id")},
        {"$inc": {"qty": -qty}}
    )

    return jsonify({"message": "Product sold successfully"})


# ---------------- RESTOCK PRODUCT ----------------
@inventory_bp.route("/restock", methods=["POST"])
def restock_product():
    if not require_login():
        return jsonify({"error": "Unauthorized. Please login."}), 401

    data = request.json
    products = products_collection()

    products.update_one(
        {"id": data.get("id")},
        {"$inc": {"qty": int(data.get("qty"))}}
    )

    return jsonify({"message": "Product restocked"})


# ---------------- DELETE PRODUCT ----------------
@inventory_bp.route("/delete/<int:pid>", methods=["DELETE"])
def delete_product(pid):
    if not require_login():
        return jsonify({"error": "Unauthorized. Please login."}), 401

    products_collection().delete_one({"id": pid})
    return jsonify({"message": "Product deleted"})


# ---------------- DASHBOARD STATS ----------------
@inventory_bp.route("/stats", methods=["GET"])
def inventory_stats():
    products = list(products_collection().find({}, {"_id": 0}))

    total_products = len(products)
    total_quantity = 0
    total_value = 0
    low_stock = 0

    for p in products:
        qty = p.get("qty", 0)
        price = p.get("price", 0)

        total_quantity += qty
        total_value += price * qty

        if qty < 5:
            low_stock += 1

    return jsonify({
        "totalProducts": total_products,
        "totalQuantity": total_quantity,
        "lowStock": low_stock,
        "inventoryValue": total_value,
        "products": products
    })