import os
import mysql.connector
import logging
from mysql.connector.pooling import MySQLConnectionPool
logger = logging.getLogger(__name__)
try:
    db_pool = MySQLConnectionPool(
        pool_name="ticket_pool", pool_size=5, pool_reset_session=True,
        host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"), port=int(os.getenv("DB_PORT", 3306)), autocommit=False
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
        """Get user by username"""
        try:
            conn = db_pool.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, username, password_hash FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            return user
        except Exception as e:
            logger.error(f"Error getting user: {str(e)}")
            return None