from flask import Flask, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import os

from routes.inventory import inventory_bp
from routes.auth import auth_bp

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# 🔐 Secret key for session
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")

# Session config (safe for Render deployment)
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = True

CORS(app, supports_credentials=True)

bcrypt = Bcrypt(app)

# ---------------- MONGODB (Atlas for Production) ----------------
MONGO_URI = os.environ.get("MONGO_URI")

if MONGO_URI:
    # Production (Render / Atlas)
    client = MongoClient(MONGO_URI)
else:
    # Local Development
    client = MongoClient("mongodb://localhost:27017/")

db = client["inventory_db"]

products = db["products"]
users = db["users"]

# Share collections with blueprints
app.config["PRODUCTS_COLLECTION"] = products
app.config["USERS_COLLECTION"] = users
app.config["BCRYPT"] = bcrypt

# Register blueprints
app.register_blueprint(inventory_bp)
app.register_blueprint(auth_bp)

# ---------------- AUTH PROTECTION HELPER ----------------

def login_required():
    return "user" in session

# ---------------- FRONTEND ROUTES ----------------

@app.route("/")
def login_page():
    if "user" in session:
        return redirect(url_for("home_page"))
    return render_template("login.html")


@app.route("/register-page")
def register_page():
    if "user" in session:
        return redirect(url_for("home_page"))
    return render_template("register.html")


@app.route("/home")
def home_page():
    if not login_required():
        return redirect(url_for("login_page"))
    return render_template("index.html")


@app.route("/products-page")
def products_page():
    if not login_required():
        return redirect(url_for("login_page"))
    return render_template("products.html")


@app.route("/add-product-page")
def add_product_page():
    if not login_required():
        return redirect(url_for("login_page"))
    return render_template("add-product.html")


@app.route("/sell-page")
def sell_page():
    if not login_required():
        return redirect(url_for("login_page"))
    return render_template("sell.html")


@app.route("/restock-page")
def restock_page():
    if not login_required():
        return redirect(url_for("login_page"))
    return render_template("restock.html")


@app.route("/dashboard-page")
def dashboard_page():
    if not login_required():
        return redirect(url_for("login_page"))
    return render_template("dashboard.html")


# ---------------- HEALTH CHECK ----------------

@app.route("/api-status")
def api_status():
    return jsonify({"status": "Backend running with Login System"})


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run()