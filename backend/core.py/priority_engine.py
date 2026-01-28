from datetime import datetime

class PriorityEngine():

    ISSUE_WEIGHTS={
        "critical":5,
        "major":3,
        "minor":1
    }

    CUSTOMER_TYPE_WEIGHTS={
        "free":1,
        "paid":3,
        "enterprise":5
    }


    def time_weight(self,created_at):

        hours_passed=(datetime.now()-created_at).total_seconds()/3600

        if hours_passed < 1:
            return 0
        
        elif hours_passed < 6:

            return 1
        
        elif hours_passed <24:

            return 3
        
        else:
            return 5
    

    def calculate_priority(self,ticket):

        issue_weight=self.ISSUE_WEIGHTS.get(ticket.issue_type,0)
        customer_weight=self.CUSTOMER_TYPE_WEIGHTS.get(ticket.customer_type,0)
        time_creation=self.time_weight(ticket.created_at)

        if ticket.impact <=10:
            impact_weight=1
        
        elif ticket.impact <=100:

            impact_weight=3
        
        else:
            impact_weight=5
        
        score = (issue_weight ) + (customer_weight ) + (time_creation) + (impact_weight )

        ticket.priority_score=score

        ticket.priority_level=self.map_score_to_priority(score)

        return ticket
    


    def map_score_to_priority(self,score):

        if score >=16:

            return "P0"

        elif score >=11:
            return "P1"
        
        elif score >=6:
            return "P2"

        else:
            return "P3"