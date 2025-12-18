import mariadb

class UserModel:
    def __init__(self, db_config):
        self.config = db_config

    def authenticate(self, email, password):
        conn = None
        try:
            conn = mariadb.connect(**self.config)
            cur = conn.cursor()
            
            # Simple query for demonstration. 
            # Note: Use password hashing (like bcrypt) for real applications.
            query = "SELECT full_name, role, department FROM users WHERE email = ? AND password = ?"
            cur.execute(query, (email, password))
            
            user = cur.fetchone()
            return user  # Returns (name, role, department) if found, else None
            
        except mariadb.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def get_all_users(self):
        """Fetch all users from the database."""
        conn = None
        try:
            conn = mariadb.connect(**self.config)
            cur = conn.cursor()
            query = "SELECT id, full_name, email, role FROM users ORDER BY full_name"
            cur.execute(query)
            rows = cur.fetchall()
            users = []
            for row in rows:
                users.append({
                    'id': row[0],
                    'full_name': row[1],
                    'email': row[2],
                    'role': row[3]
                })
            return users
        except mariadb.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def get_user_by_name(self, full_name):
        """Fetch a user by their full name."""
        conn = None
        try:
            conn = mariadb.connect(**self.config)
            cur = conn.cursor()
            query = "SELECT id, full_name, email, role FROM users WHERE full_name = ?"
            cur.execute(query, (full_name,))
            row = cur.fetchone()
            if row:
                return {
                    'id': row[0],
                    'full_name': row[1],
                    'email': row[2],
                    'role': row[3]
                }
            return None
        except mariadb.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn:
                conn.close()
