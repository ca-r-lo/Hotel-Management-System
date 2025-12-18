"""Request model for stock requests."""

from models.database import get_conn, _paramstyle
from datetime import datetime


class RequestModel:
    """Model for managing stock requests."""
    
    @staticmethod
    def create_table():
        """Create requests table if it doesn't exist."""
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id INT AUTO_INCREMENT PRIMARY KEY,
                department VARCHAR(50) NOT NULL,
                requested_by VARCHAR(100) NOT NULL,
                item_name VARCHAR(255) NOT NULL,
                quantity INT NOT NULL,
                unit VARCHAR(50),
                reason TEXT,
                status VARCHAR(20) DEFAULT 'Pending',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                notes TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def create_request(department, requested_by, item_name, quantity, unit, reason=None):
        """Create a new stock request."""
        conn = get_conn()
        cur = conn.cursor()
        
        try:
            cur.execute(f"""
                INSERT INTO requests (department, requested_by, item_name, quantity, unit, reason)
                VALUES ({_paramstyle()}, {_paramstyle()}, {_paramstyle()}, {_paramstyle()}, {_paramstyle()}, {_paramstyle()})
            """, (department, requested_by, item_name, quantity, unit, reason))
            
            conn.commit()
            request_id = cur.lastrowid
            conn.close()
            return request_id
        except Exception as e:
            conn.close()
            raise e
    
    @staticmethod
    def get_requests_by_department(department, include_archived=False):
        """Get all requests for a specific department."""
        conn = get_conn()
        cur = conn.cursor()
        
        if include_archived:
            query = f"""
                SELECT id, department, requested_by, item_name, quantity, unit, reason, status, created_at, updated_at, notes
                FROM requests
                WHERE department = {_paramstyle()}
                ORDER BY created_at DESC
            """
        else:
            query = f"""
                SELECT id, department, requested_by, item_name, quantity, unit, reason, status, created_at, updated_at, notes
                FROM requests
                WHERE department = {_paramstyle()} AND status != 'Archived'
                ORDER BY created_at DESC
            """
        
        cur.execute(query, (department,))
        rows = cur.fetchall()
        
        requests = []
        for row in rows:
            requests.append({
                'id': row[0],
                'department': row[1],
                'requested_by': row[2],
                'item_name': row[3],
                'quantity': row[4],
                'unit': row[5],
                'reason': row[6],
                'status': row[7],
                'created_at': row[8],
                'updated_at': row[9],
                'notes': row[10]
            })
        
        conn.close()
        return requests
    
    @staticmethod
    def get_all_requests(include_archived=False):
        """Get all requests (for Purchase Admin)."""
        conn = get_conn()
        cur = conn.cursor()
        
        if include_archived:
            query = """
                SELECT id, department, requested_by, item_name, quantity, unit, reason, status, created_at, updated_at, notes
                FROM requests
                ORDER BY created_at DESC
            """
        else:
            query = """
                SELECT id, department, requested_by, item_name, quantity, unit, reason, status, created_at, updated_at, notes
                FROM requests
                WHERE status != 'Archived'
                ORDER BY created_at DESC
            """
        
        cur.execute(query)
        rows = cur.fetchall()
        
        requests = []
        for row in rows:
            requests.append({
                'id': row[0],
                'department': row[1],
                'requested_by': row[2],
                'item_name': row[3],
                'quantity': row[4],
                'unit': row[5],
                'reason': row[6],
                'status': row[7],
                'created_at': row[8],
                'updated_at': row[9],
                'notes': row[10]
            })
        
        conn.close()
        return requests
    
    @staticmethod
    def update_status(request_id, status, notes=None):
        """Update request status."""
        conn = get_conn()
        cur = conn.cursor()
        
        try:
            if notes:
                cur.execute(f"""
                    UPDATE requests
                    SET status = {_paramstyle()}, notes = {_paramstyle()}
                    WHERE id = {_paramstyle()}
                """, (status, notes, request_id))
            else:
                cur.execute(f"""
                    UPDATE requests
                    SET status = {_paramstyle()}
                    WHERE id = {_paramstyle()}
                """, (status, request_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            raise e
    
    @staticmethod
    def delete_request(request_id):
        """Delete a request."""
        conn = get_conn()
        cur = conn.cursor()
        
        try:
            cur.execute(f"DELETE FROM requests WHERE id = {_paramstyle()}", (request_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            raise e
