import logging
import bcrypt
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from .repository.ticket_priority import TicketRepository

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
repo = TicketRepository()

@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json(force=True)
        
        if not data:
            return jsonify({"error": "Request body is required"}), 422
        
        username = data.get("username", "").strip().lower()
        password = data.get("password", "")
        
        # Validate username and password
        if not username:
            return jsonify({"error": "username is required and cannot be empty"}), 422
        if not password:
            return jsonify({"error": "password is required and cannot be empty"}), 422
        if len(username) < 3:
            return jsonify({"error": "username must be at least 3 characters long"}), 422
        if len(password) < 6:
            return jsonify({"error": "password must be at least 6 characters long"}), 422
        
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        repo.create_user(username, password_hash)
        logger.debug("Create user: %s", username)
        return jsonify({"msg": "user created"}), 201
    except Exception as e:
        logger.exception("Register error")
        # Check if it's a duplicate user error
        if "UNIQUE" in str(e) or "duplicate" in str(e).lower():
            return jsonify({"error": "username already exists"}), 409
        return jsonify({"error": str(e)}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json(force=True)
        
        if not data:
            return jsonify({"error": "Request body is required"}), 422
        
        username = data.get("username", "").strip().lower()
        password = data.get("password", "")

        if not username or not password:
            return jsonify({"error": "username and password are required"}), 422

        user = repo.get_user(username)
        if not isinstance(user, dict) or not user:
            logger.error("Expected dict from repo.get_user, got: %s", type(user))
            return jsonify({"error": "Invalid credentials"}), 401

        stored_hash = user.get("password_hash")
        if not stored_hash:
            return jsonify({"error": "Invalid credentials"}), 401

        if not bcrypt.checkpw(password.encode(), stored_hash.encode()):
            return jsonify({"error": "Invalid credentials"}), 401

        token = create_access_token(identity=str(user.get("id")))
        return jsonify({"access_token": token}), 200

    except Exception as e:
        logger.exception("Login error")
        return jsonify({"error": str(e)}), 500