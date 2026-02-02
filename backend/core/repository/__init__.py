#This empty file tells Python that the 'repository' folder is a package.
# Without it, Python can't import the database functions from this folder.
# Other files like auth_routes.py and ticket_routes.py use:
# from .repository.ticket_priority import TicketRepository
# and this file makes that import work.