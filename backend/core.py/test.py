
from ticket import Ticket

from priority_engine import PriorityEngine

from repository.ticket_priority import TicketRepository


engine=PriorityEngine()
repo=TicketRepository()


ticket=Ticket(
    issue_type="critical",
    customer_type="enterprise",
    impact=120,

)

engine.calculate_priority(ticket)

repo.save(ticket)

print(ticket)
print("ticket saved to DB")

