from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import bcrypt
import logging
from .repository.ticket_priority import TicketRepository

logger = logging.getLogger(__name__)
auth_bp = Blueprint("auth", __name__)
repo = TicketRepository()

@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.json
        username = data.get("username", "").lower()
        password_hash = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode()
        repo.create_user(username, password_hash)
        logger.info(f"User {username} created successfully")
        return jsonify({"msg": "user created"}), 201
    except Exception as e:
        logger.error(f"Register error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        username = data.get("username", "").lower()
        user = repo.get_user(username)
        
        if not user or not bcrypt.checkpw(data["password"].encode(), user["password_hash"].encode()):
            logger.warning(f"Login failed for user: {username}")
            return jsonify({"msg": "invalid username or password"}), 401
        
        token = create_access_token(identity=str(user["id"]))
        logger.info(f"Login successful for user: {username}")
        return jsonify(access_identity=token), 200
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({"error": str(e)}), 500