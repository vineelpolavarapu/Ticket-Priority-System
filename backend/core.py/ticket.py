from datetime import datetime

class Ticket():
    def __init__(self,issue_type,impact,customer_type,created_at=None):

        self.issue_type=issue_type

        self.impact=impact

        self.customer_type=customer_type

        self.created_at=created_at or datetime.now()


        self.priority_score=None

        self.priority_level=None


    def __str__(self):
        return f"priority : {self.priority_level}"
