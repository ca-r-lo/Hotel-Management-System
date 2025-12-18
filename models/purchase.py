from .database import get_conn, DB_DRIVER
from datetime import datetime

# Helper to adapt parameter placeholder depending on DB driver
def _paramstyle():
    return "%s" if DB_DRIVER == 'mariadb' else "?"

def _exec(conn, sql, params=None):
    cur = conn.cursor()
    if params:
        cur.execute(sql, params)
    else:
        cur.execute(sql)
    return cur


def create_tables():
    conn = get_conn()
    try:
        cur = conn.cursor()
        if DB_DRIVER == 'mariadb':
            cur.execute("""
                CREATE TABLE IF NOT EXISTS suppliers (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL,
                    contact_name VARCHAR(255),
                    email VARCHAR(255),
                    phone VARCHAR(64),
                    address TEXT
                ) ENGINE=InnoDB;
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS purchases (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    supplier_id INT,
                    expected_date DATE,
                    total_amount DECIMAL(12,2) DEFAULT 0,
                    status VARCHAR(32) DEFAULT 'pending',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB;
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS purchase_items (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    purchase_id INT,
                    item_name VARCHAR(255),
                    qty INT,
                    price DECIMAL(12,2),
                    total DECIMAL(12,2)
                ) ENGINE=InnoDB;
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL,
                    stock INT DEFAULT 0
                ) ENGINE=InnoDB;
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS damages (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    item_id INT,
                    quantity INT,
                    reason TEXT,
                    created_by VARCHAR(255),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB;
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    title VARCHAR(255),
                    body TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB;
            """)
            conn.commit()
        else:
            # sqlite
            cur.execute("""
                CREATE TABLE IF NOT EXISTS suppliers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    contact_name TEXT,
                    email TEXT,
                    phone TEXT,
                    address TEXT
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS purchases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    supplier_id INTEGER,
                    expected_date TEXT,
                    total_amount REAL DEFAULT 0,
                    status TEXT DEFAULT 'pending',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS purchase_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    purchase_id INTEGER,
                    item_name TEXT,
                    qty INTEGER,
                    price REAL,
                    total REAL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    stock INTEGER DEFAULT 0
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS damages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id INTEGER,
                    quantity INTEGER,
                    reason TEXT,
                    created_by TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    body TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
    finally:
        try:
            conn.close()
        except Exception:
            pass


class SupplierModel:
    @staticmethod
    def add_supplier(data: dict):
        conn = get_conn()
        try:
            sql = "INSERT INTO suppliers (name, contact_name, email, phone, address) VALUES ({})".format(
                ",".join([_paramstyle()]*5)
            )
            cur = _exec(conn, sql, (data.get('name'), data.get('contact_name'), data.get('email'), data.get('phone'), data.get('address')))
            conn.commit()
            return cur.lastrowid if hasattr(cur, 'lastrowid') else cur.lastrowid
        finally:
            conn.close()

    @staticmethod
    def get_supplier(sid: int):
        conn = get_conn()
        try:
            sql = "SELECT id, name, contact_name, email, phone, address FROM suppliers WHERE id = {}".format(_paramstyle())
            cur = _exec(conn, sql, (sid,))
            row = cur.fetchone()
            if not row:
                return None
            try:
                return dict(row)
            except Exception:
                return {
                    'id': row[0], 'name': row[1], 'contact_name': row[2], 'email': row[3], 'phone': row[4], 'address': row[5]
                }
        finally:
            conn.close()

    @staticmethod
    def list_suppliers():
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, name, contact_name, email, phone, address FROM suppliers ORDER BY name")
            rows = cur.fetchall()
            result = []
            for r in rows:
                try:
                    result.append(dict(r))
                except Exception:
                    result.append({ 'id': r[0], 'name': r[1], 'contact_name': r[2], 'email': r[3], 'phone': r[4], 'address': r[5] })
            return result
        finally:
            conn.close()

    @staticmethod
    def update_supplier(sid: int, data: dict):
        conn = get_conn()
        try:
            sql = "UPDATE suppliers SET name = {}, contact_name = {}, email = {}, phone = {}, address = {} WHERE id = {}".format(
                _paramstyle(), _paramstyle(), _paramstyle(), _paramstyle(), _paramstyle(), _paramstyle()
            )
            _exec(conn, sql, (data.get('name'), data.get('contact_name'), data.get('email'), data.get('phone'), data.get('address'), sid))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()

    @staticmethod
    def delete_supplier(sid: int):
        conn = get_conn()
        try:
            _exec(conn, f"DELETE FROM suppliers WHERE id = {_paramstyle()}", (sid,))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()


class ItemModel:
    @staticmethod
    def list_items():
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, name, stock FROM items ORDER BY name")
            rows = cur.fetchall()
            result = []
            for r in rows:
                try:
                    result.append(dict(r))
                except Exception:
                    result.append({'id': r[0], 'name': r[1], 'stock': r[2]})
            return result
        finally:
            conn.close()

    @staticmethod
    def get_item(iid: int):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, name, stock FROM items WHERE id = {}".format(_paramstyle()), (iid,))
            row = cur.fetchone()
            if not row:
                return None
            try:
                return dict(row)
            except Exception:
                return {'id': row[0], 'name': row[1], 'stock': row[2]}
        finally:
            conn.close()

    @staticmethod
    def adjust_stock(item_id: int, delta: int):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("UPDATE items SET stock = COALESCE(stock,0) + %s WHERE id = %s" % (_paramstyle(), _paramstyle()), (delta, item_id))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()


class PurchaseModel:
    @staticmethod
    def create_purchase(supplier_id: int, items: list, expected_date: str | None, created_by: str | None = None):
        """items is a list of dicts: {item_name, qty, price}
        Returns new purchase id on success or None.
        """
        conn = get_conn()
        try:
            cur = conn.cursor()
            param = _paramstyle()
            # insert purchase
            sql = f"INSERT INTO purchases (supplier_id, expected_date, total_amount, status, created_at) VALUES ({param}, {param}, {param}, {param}, {param})"
            total = sum([(float(i.get('qty',0)) * float(i.get('price',0))) for i in items])
            _exec(conn, sql, (supplier_id, expected_date or None, total, 'pending', datetime.now()))
            # fetch last id
            if DB_DRIVER == 'mariadb':
                purchase_id = cur.lastrowid
            else:
                purchase_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]

            # insert items
            for it in items:
                _exec(conn, f"INSERT INTO purchase_items (purchase_id, item_name, qty, price, total) VALUES ({param},{param},{param},{param},{param})",
                      (purchase_id, it.get('item_name'), it.get('qty'), it.get('price'), float(it.get('qty',0)) * float(it.get('price',0))))
            conn.commit()
            return purchase_id
        except Exception as e:
            try:
                conn.rollback()
            except Exception:
                pass
            raise
        finally:
            conn.close()

    @staticmethod
    def list_purchases(status: str | None = None):
        conn = get_conn()
        try:
            cur = conn.cursor()
            if status:
                cur.execute("SELECT id, supplier_id, expected_date, total_amount, status, created_at FROM purchases WHERE status = {} ORDER BY created_at DESC".format(_paramstyle()), (status,))
            else:
                cur.execute("SELECT id, supplier_id, expected_date, total_amount, status, created_at FROM purchases ORDER BY created_at DESC")
            rows = cur.fetchall()
            result = []
            for r in rows:
                try:
                    result.append(dict(r))
                except Exception:
                    result.append({'id': r[0], 'supplier_id': r[1], 'expected_date': r[2], 'total_amount': r[3], 'status': r[4], 'created_at': r[5]})
            return result
        finally:
            conn.close()


class DamageModel:
    @staticmethod
    def log_damage(item_id: int, quantity: int, reason: str, created_by: str | None = None):
        conn = get_conn()
        try:
            param = _paramstyle()
            _exec(conn, f"INSERT INTO damages (item_id, quantity, reason, created_by, created_at) VALUES ({param},{param},{param},{param},{param})",
                  (item_id, quantity, reason, created_by, datetime.now()))
            conn.commit()
            return True
        except Exception:
            try:
                conn.rollback()
            except Exception:
                pass
            return False
        finally:
            conn.close()

    @staticmethod
    def list_damages():
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, item_id, quantity, reason, created_by, created_at FROM damages ORDER BY created_at DESC")
            rows = cur.fetchall()
            result = []
            for r in rows:
                try:
                    result.append(dict(r))
                except Exception:
                    result.append({'id': r[0], 'item_id': r[1], 'quantity': r[2], 'reason': r[3], 'created_by': r[4], 'created_at': r[5]})
            return result
        finally:
            conn.close()


class MessageModel:
    @staticmethod
    def add_message(title: str, body: str):
        conn = get_conn()
        try:
            _exec(conn, f"INSERT INTO messages (title, body, created_at) VALUES ({_paramstyle()},{_paramstyle()},{_paramstyle()})",
                  (title, body, datetime.now()))
            conn.commit()
            return True
        finally:
            conn.close()

    @staticmethod
    def list_messages(limit: int = 50):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, title, body, created_at FROM messages ORDER BY created_at DESC LIMIT {}".format(limit))
            rows = cur.fetchall()
            result = []
            for r in rows:
                try:
                    result.append(dict(r))
                except Exception:
                    result.append({'id': r[0], 'title': r[1], 'body': r[2], 'created_at': r[3]})
            return result
        finally:
            conn.close()
