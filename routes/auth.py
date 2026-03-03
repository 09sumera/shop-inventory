from flask import Blueprint, request, jsonify, current_app, session

auth_bp = Blueprint("auth", __name__)

def users_collection():
    return current_app.config["USERS_COLLECTION"]

def bcrypt():
    return current_app.config["BCRYPT"]


# -------- REGISTER --------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username & password required"}), 400

    users = users_collection()

    if users.find_one({"username": username}):
        return jsonify({"error": "User already exists"}), 400

    hashed_pw = bcrypt().generate_password_hash(password).decode("utf-8")

    users.insert_one({
        "username": username,
        "password": hashed_pw
    })

    return jsonify({"message": "User registered successfully"})


# -------- LOGIN --------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = users_collection().find_one({"username": username})

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not bcrypt().check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid password"}), 401

    session["user"] = username
    return jsonify({"message": "Login successful"})


# -------- LOGOUT --------
@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"message": "Logged out"})


# -------- LOGIN CHECK --------
@auth_bp.route("/login-check", methods=["GET"])
def login_check():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({"message": "Logged in", "user": session["user"]})