from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import bcrypt
import logging
from .repository.ticket_priority import TicketRepository

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

auth_bp = Blueprint("auth", __name__,url_prefix="/auth")
repo = TicketRepository()

@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json(force=True)
        username = data.get("username", "").strip().lower()
        password = data.get("password", "")
        if not username or not password:
            return jsonify({"error": "Username and password are required"}),400
        password_hash= bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
        repo.create_user(username, password_hash)
        logger.debug("Create user: %s",username)
        return jsonify({"msg": "user created"}), 201
    except Exception as e:
        logger.exception(f"Register error")
        return jsonify({"error": str(e)}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json(force=True)
        username = data.get("username", "").strip().lower()
        password = data.get("password","")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}),400
        
        user=repo.get_user(username)        
        logger.debug("Fetched user for login: %s",user)
        if not isinstance(user, dict):
            logger.error("Expected dict from repo.get_user, got: %s", type(user))
            return jsonify({"error": "Invalid credentials"}), 401
        
        stored_hash = user.get("password_hash") if isinstance(user, dict) else None
        if not stored_hash:
            logger.debug("Password hash missing in DB record: %s", username)
            return jsonify({"error": "Invalid credentials"}), 401

        check = bcrypt.checkpw(password.encode(), stored_hash.encode())
        if not check:
            logger.debug("Password check for '%s': %s", username, check)
            return jsonify({"error": "Invalid credentials"}), 401

        token = create_access_token(identity=str(user.get("id")))
        return jsonify({"access_identity": token}), 200

    except Exception as e:
        logger.exception("Login error")
        return jsonify({"error": str(e)}), 500