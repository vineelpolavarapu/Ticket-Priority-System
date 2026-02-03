import os
import logging
import sqlite3
from .db import get_connection, is_sqlite

logger = logging.getLogger(__name__)

class TicketRepository:
    def _get_connection(self):
        return get_connection()

    def _execute(self, query, params=None, fetch=False):
        conn = self._get_connection()
        cursor = None
        try:
            # adapt placeholder style between sqlite (?) and MySQL (%s)
            if not is_sqlite():
                query = query.replace('?', '%s')

            if is_sqlite():
                cursor = conn.cursor()
            else:
                cursor = conn.cursor(dictionary=True)

            cursor.execute(query, params or ())

            if fetch == 'one':
                row = cursor.fetchone()
                if row is None:
                    return None
                return dict(row) if is_sqlite() else row

            if fetch == 'all':
                rows = cursor.fetchall()
                if is_sqlite():
                    return [dict(r) for r in rows]
                return rows

            conn.commit()
        except Exception:
            conn.rollback()
            logger.exception("DB execution error")
            raise
        finally:
            try:
                if cursor:
                    cursor.close()
            except Exception:
                pass
            try:
                conn.close()
            except Exception:
                pass

    def get_all(self):
        return self._execute("SELECT * FROM tickets ORDER BY created_at DESC", fetch='all')

    def get_paginated(self, limit, offset):
        return self._execute("SELECT * FROM tickets ORDER BY created_at DESC LIMIT ? OFFSET ?", 
                             (limit, offset), fetch='all')

    def get_count(self):
        result = self._execute("SELECT COUNT(*) AS total FROM tickets", fetch='one')
        return result["total"] if result else 0

    def save(self, ticket):
        query = "INSERT INTO tickets (issue_type, impact, customer_type, created_at, priority_score, priority_level) VALUES(?,?,?,?,?,?)"
        params = (ticket.issue_type, ticket.impact, ticket.customer_type, ticket.created_at.isoformat() if hasattr(ticket.created_at, "isoformat") else ticket.created_at, ticket.priority_score, ticket.priority_level)
        self._execute(query, params)

    def create_user(self, username, password_hash):
        self._execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))

    def get_user(self, username):
        query = "SELECT * FROM users WHERE username=?" if is_sqlite() else "SELECT * FROM users WHERE username=%s"
        return self._execute(query, (username,), fetch='one')