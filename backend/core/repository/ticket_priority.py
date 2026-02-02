import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool

try:
    db_pool = MySQLConnectionPool(
        pool_name="ticket_pool", pool_size=5, pool_reset_session=True,
        host="127.0.0.1", user="root", password="Vineel@2001",
        database="ticket_priority_system", port=3306, autocommit=False
    )
except Exception as e:
    raise Exception(f"Pool creation failed: {e}")

class TicketRepository:
    def _get_connection(self):
        return db_pool.get_connection()

    def _execute(self, query, params=None, fetch=False):
        conn = self._get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            if fetch == 'one':
                return cursor.fetchone()
            elif fetch == 'all':
                return cursor.fetchall()
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()
    
    def get_all(self):
        return self._execute("SELECT * FROM tickets ORDER BY created_at DESC", fetch='all')
    
    def get_paginated(self, limit, offset):
        return self._execute("SELECT * FROM tickets ORDER BY created_at DESC LIMIT %s OFFSET %s", 
                           (limit, offset), fetch='all')
    
    def get_count(self):
        result = self._execute("SELECT COUNT(*) AS total FROM tickets", fetch='one')
        return result["total"] if result else 0
    
    def save(self, ticket):
        query = "INSERT INTO tickets (issue_type, impact, customer_type, created_at, priority_score, priority_level) VALUES(%s,%s,%s,%s,%s,%s)"
        self._execute(query, (ticket.issue_type, ticket.impact, ticket.customer_type, 
                            ticket.created_at, ticket.priority_score, ticket.priority_level))
    
    def create_user(self, username, password_hash):
        self._execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
    
    def get_user(self, username):
        return self._execute("SELECT id, username, password_hash FROM users WHERE username = %s", (username,), fetch='one')
