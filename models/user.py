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
            query = "SELECT full_name, role FROM users WHERE email = ? AND password = ?"
            # cur.execute(query, (email, password))

            cur.execute(query, ("admin@stash.com", "admin123"))
            
            user = cur.fetchone()
            return user  # Returns (name, role) if found, else None
            
        except mariadb.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn:
                conn.close()