from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
import logging
from .priority_engine import PriorityEngine
from .ticket import Ticket
from .repository.ticket_priority import TicketRepository

logger = logging.getLogger(__name__)
ticket_bp = Blueprint("ticket", __name__)
engine = PriorityEngine()
repo = TicketRepository()

@ticket_bp.route("/test-jwt", methods=["GET"])
def test_jwt():
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        return jsonify({"status": "JWT valid", "user_id": user_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@ticket_bp.route("/tickets", methods=["GET"])
def get_tickets():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        offset = (page - 1) * limit
        tickets = repo.get_paginated(limit, offset)
        for ticket in tickets:
            if 'created_at' in ticket and hasattr(ticket['created_at'], 'isoformat'):
                ticket['created_at'] = ticket['created_at'].isoformat()
        return jsonify({"tickets": tickets, "total": repo.get_count(), "page": page, "limit": limit}), 200
    except Exception as e:
        logger.error(f"GET tickets error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@ticket_bp.route("/health", methods=["GET"])
def health_check():
    return {"status": "ok"},200

@ticket_bp.route("/tickets", methods=["POST"])
@jwt_required()
def create_ticket():
    try:
        data = request.get_json(force=True) if request.data else None
        if not data:
            return jsonify({"error": "Missing JSON body"}), 400

        required = ["issue_type", "impact", "customer_type"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing field {field}"}), 400

        if not isinstance(data["impact"], int) or not (1 <= data["impact"] <= 999):
            return jsonify({"error": "Impact must be int between 1-999"}), 400

        ticket = Ticket(**data)
        engine.calculate_priority(ticket)
        repo.save(ticket)
        logger.info(f"Ticket created with priority {ticket.priority_level}")
        return jsonify({"score": ticket.priority_score, "level": ticket.priority_level}), 201
    except Exception as e:
        logger.error(f"Create ticket error: {str(e)}")
        return jsonify({"error": str(e)}), 500