import mysql.connector

class TicketRepository():

    def __init__(self):
        self.conn=mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Vineel@2001",
            database="ticket_priority_system",
            port="3306"


        )
        self.cursor=self.conn.cursor(dictionary=True)
    
    def save(self,ticket):
        query="""

        INSERT INTO TICKETS

        (issue_type , impact , customer_type , created_at , priority_score , priority_level)
        VALUES(%s,%s,%s,%s,%s,%s)
        
    """
        
        values=(

            ticket.issue_type,
            ticket.impact,
            ticket.customer_type,
            ticket.created_at,
            ticket.priority_score,
            ticket.priority_level

        )

        self.cursor.execute(query,values)
        self.conn.commit()
