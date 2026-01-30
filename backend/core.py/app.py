from flask import Flask , request , jsonify
from priority_engine import PriorityEngine
from ticket import Ticket
from repository.ticket_priority import TicketRepository
from flask_cors import CORS

app=Flask(__name__)
CORS(app)
engine=PriorityEngine()
repo=TicketRepository()

@app.route("/tickets",methods=["GET"])
def get_tickets():

    page=int(request.args.get("page",1))
    limit=int(request.args.get("limit",10))

    tickets=repo.get_paginated(page,limit)
    total=repo.get_count()

    return jsonify({
        "tickets":tickets,
        "total":total,
        "page":page,
        "limit":limit
    }),200


@app.route("/tickets",methods=["POST"])


def create_ticket():

    data=request.json

    if not data:
        return jsonify({"Error: Invalid missing json body"}),400

    ticket=Ticket(
        issue_type=data["issue_type"],
        impact=data["impact"],
        customer_type=data["customer_type"]
    )
    engine.calculate_priority(ticket)
    repo.save(ticket)

    return jsonify({
        "score":ticket.priority_score,
        "level":ticket.priority_level

    }),201

if __name__=="__main__":
    app.run(debug=False)
    


