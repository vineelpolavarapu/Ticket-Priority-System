from datetime import datetime

class PriorityEngine:
    ISSUE_WEIGHTS = {"critical": 5, "major": 3, "minor": 1}
    CUSTOMER_WEIGHTS = {"free": 1, "paid": 3, "enterprise": 5}
    
    def time_weight(self, created_at):
        hours = (datetime.now() - created_at).total_seconds() / 3600
        return 0 if hours < 1 else (1 if hours < 6 else (3 if hours < 24 else 5))
    
    def impact_weight(self, impact):
        return 1 if impact <= 10 else (3 if impact <= 100 else 5)
    
    def calculate_priority(self, ticket):
        issue_weight = self.ISSUE_WEIGHTS.get(ticket.issue_type, 0)
        customer_weight = self.CUSTOMER_WEIGHTS.get(ticket.customer_type, 0)
        time_weight = self.time_weight(ticket.created_at)
        impact_weight=self.impact_weight(ticket.impact)

        score = issue_weight + customer_weight + time_weight + impact_weight
        ticket.priority_score = score
        ticket.priority_level = self.map_score_to_priority(score)
        
        return ticket
    
    def map_score_to_priority(self, score):
        return "P0" if score >= 16 else ("P1" if score >= 11 else ("P2" if score >= 6 else "P3"))