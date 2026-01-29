from flask import Flask , request , jsonify
from priority_engine import PriorityEngine
from ticket import Ticket
from repository.ticket_priority import TicketRepository

app=Flask(__name__)

engine=PriorityEngine()
repo=TicketRepository()

@app.route("/tickets",methods=["GET"])
def get_tickets():

    tickets=repo.get_all()

    return jsonify(tickets),200


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
    


