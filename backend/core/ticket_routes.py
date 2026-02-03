import os
import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from .priority_engine import PriorityEngine
from .ticket import Ticket
from .repository.ticket_priority import TicketRepository
from datetime import datetime

logger = logging.getLogger(__name__)
ticket_bp = Blueprint("ticket", __name__)
engine = PriorityEngine()
repo = TicketRepository()

@ticket_bp.route("/test-jwt", methods=["GET"])
def test_jwt():
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        return jsonify({"ok": True, "user_id": user_id}), 200
    except Exception as e:
        return jsonify({"error": "invalid token"}), 401

@ticket_bp.route("/tickets", methods=["GET"])
def get_tickets():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        offset = (page - 1) * limit
        tickets = repo.get_paginated(limit, offset)
        total = repo.get_count()
        return jsonify({
            "tickets": tickets or [],
            "page": page,
            "limit": limit,
            "total": total
        }), 200
    except Exception as e:
        logger.error(f"GET tickets error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@ticket_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200

@ticket_bp.route("/tickets", methods=["POST"])
@jwt_required()
def create_ticket():
    try:
        data = request.get_json(force=True)
        
        # Validate required fields
        if not data:
            return jsonify({"error": "Request body is required"}), 422
        
        issue_type = data.get("issue_type")
        customer_type = data.get("customer_type")
        impact = data.get("impact")
        
        # Validate issue_type
        valid_issue_types = ["critical", "major", "minor"]
        if not issue_type or not isinstance(issue_type, str):
            return jsonify({"error": f"issue_type is required and must be a string"}), 422
        if issue_type not in valid_issue_types:
            return jsonify({"error": f"issue_type must be one of: {', '.join(valid_issue_types)}"}), 422
        
        # Validate customer_type
        valid_customer_types = ["enterprise", "paid", "free"]
        if not customer_type or not isinstance(customer_type, str):
            return jsonify({"error": f"customer_type is required and must be a string"}), 422
        if customer_type not in valid_customer_types:
            return jsonify({"error": f"customer_type must be one of: {', '.join(valid_customer_types)}"}), 422
        
        # Validate impact
        if impact is None or impact == "":
            return jsonify({"error": "impact is required"}), 422
        try:
            impact = int(impact)
            if impact < 1 or impact > 999:
                return jsonify({"error": "impact must be between 1 and 999"}), 422
        except (ValueError, TypeError):
            return jsonify({"error": "impact must be a valid integer"}), 422
        
        created_at = datetime.now()
        ticket = Ticket(issue_type, impact, customer_type, created_at)
        engine.calculate_priority(ticket)
        repo.save(ticket)
        return jsonify({
            "id": None,
            "issue_type": ticket.issue_type,
            "impact": ticket.impact,
            "customer_type": ticket.customer_type,
            "created_at": ticket.created_at.isoformat(),
            "priority_score": ticket.priority_score,
            "priority_level": ticket.priority_level
        }), 201
    except Exception as e:
        logger.exception("Create ticket error")
        return jsonify({"error": str(e)}), 500