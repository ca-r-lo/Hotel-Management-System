from .database import get_conn, DB_DRIVER
from datetime import datetime

# Helper to adapt parameter placeholder depending on DB driver
def _paramstyle():
    return "%s" if DB_DRIVER == 'mariadb' else "?"

def _exec(conn, sql, params=None):
    cur = conn.cursor()
    # Debugging: print SQL and params when running to aid troubleshooting
    try:
        if params:
            # ensure params is a tuple/list for DB API
            cur.execute(sql, params)
        else:
            cur.execute(sql)
    except Exception:
        try:
            # best-effort debug output
            print("[SQL DEBUG] Failed SQL:\n", sql)
            print("[SQL DEBUG] Params:\n", params)
        except Exception:
            pass
        raise
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
                    sender_id INT NOT NULL,
                    recipient_id INT NOT NULL,
                    category VARCHAR(64) DEFAULT 'General',
                    title VARCHAR(255),
                    body TEXT,
                    is_read BOOLEAN DEFAULT FALSE,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (sender_id) REFERENCES users(id),
                    FOREIGN KEY (recipient_id) REFERENCES users(id)
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
                    sender_id INTEGER NOT NULL,
                    recipient_id INTEGER NOT NULL,
                    category TEXT DEFAULT 'General',
                    title TEXT,
                    body TEXT,
                    is_read INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (sender_id) REFERENCES users(id),
                    FOREIGN KEY (recipient_id) REFERENCES users(id)
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
            cur.execute("SELECT id, name, sku, unit, unit_cost, stock_qty, min_stock, category, created_at FROM items ORDER BY name")
            rows = cur.fetchall()
            result = []
            for r in rows:
                try:
                    result.append(dict(r))
                except Exception:
                    result.append({
                        'id': r[0], 
                        'name': r[1], 
                        'sku': r[2], 
                        'unit': r[3], 
                        'unit_cost': r[4], 
                        'stock_qty': r[5], 
                        'min_stock': r[6], 
                        'category': r[7], 
                        'created_at': r[8]
                    })
            return result
        finally:
            conn.close()

    @staticmethod
    def get_item(iid: int):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, name, sku, unit, unit_cost, stock_qty, min_stock, category FROM items WHERE id = {}".format(_paramstyle()), (iid,))
            row = cur.fetchone()
            if not row:
                return None
            try:
                return dict(row)
            except Exception:
                return {
                    'id': row[0], 
                    'name': row[1], 
                    'sku': row[2], 
                    'unit': row[3], 
                    'unit_cost': row[4], 
                    'stock_qty': row[5], 
                    'min_stock': row[6], 
                    'category': row[7]
                }
        finally:
            conn.close()

    @staticmethod
    def adjust_stock(item_id: int, delta: int):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("UPDATE items SET stock_qty = COALESCE(stock_qty,0) + {} WHERE id = {}".format(_paramstyle(), _paramstyle()), (delta, item_id))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()
    
    @staticmethod
    def add_item(name: str, category: str, unit: str, stock_qty: int, min_stock: int):
        """Add a new inventory item."""
        conn = get_conn()
        try:
            param = _paramstyle()
            sql = f"INSERT INTO items (name, category, unit, stock_qty, min_stock, created_at) VALUES ({param},{param},{param},{param},{param},{param})"
            _exec(conn, sql, (name, category, unit, stock_qty, min_stock, datetime.now()))
            conn.commit()
            return True
        except Exception as e:
            try:
                conn.rollback()
            except Exception:
                pass
            print(f"[ADD_ITEM ERROR] {repr(e)}")
            return False
        finally:
            conn.close()
    
    @staticmethod
    def update_item(item_id: int, name: str, category: str, unit: str, stock_qty: int, min_stock: int):
        """Update an existing inventory item."""
        conn = get_conn()
        try:
            param = _paramstyle()
            sql = f"UPDATE items SET name = {param}, category = {param}, unit = {param}, stock_qty = {param}, min_stock = {param} WHERE id = {param}"
            _exec(conn, sql, (name, category, unit, stock_qty, min_stock, item_id))
            conn.commit()
            return True
        except Exception as e:
            try:
                conn.rollback()
            except Exception:
                pass
            print(f"[UPDATE_ITEM ERROR] {repr(e)}")
            return False
        finally:
            conn.close()


class PurchaseModel:
    @staticmethod
    def create_purchase(supplier_id: int, items: list, expected_date: str | None, created_by: str | None = None):
        """items is a list of dicts: {item_id, quantity, unit_price}
        Returns new purchase id on success or None.
        """
        conn = get_conn()
        try:
            cur = conn.cursor()
            param = _paramstyle()
            # insert purchase with created_by
            sql = f"INSERT INTO purchases (supplier_id, expected_date, total_amount, status, created_by, created_at) VALUES ({param}, {param}, {param}, {param}, {param}, {param})"
            total = sum([(float(i.get('quantity',0)) * float(i.get('unit_price',0))) for i in items])
            cur_ins = _exec(conn, sql, (supplier_id, expected_date or None, total, 'pending', created_by, datetime.now()))
            # fetch last id from the cursor that executed the insert
            try:
                purchase_id = cur_ins.lastrowid
            except Exception:
                # fallback for sqlite or drivers without lastrowid on cursor
                try:
                    purchase_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
                except Exception:
                    purchase_id = None

            # insert items
            for it in items:
                _exec(conn, f"INSERT INTO purchase_items (purchase_id, item_id, quantity, unit_price, total) VALUES ({param},{param},{param},{param},{param})",
                      (purchase_id, it.get('item_id'), it.get('quantity'), it.get('unit_price'), float(it.get('quantity',0)) * float(it.get('unit_price',0))))
            conn.commit()
            return purchase_id
        except Exception as e:
            try:
                conn.rollback()
            except Exception:
                pass
            # debug print
            try:
                print("[CREATE_PURCHASE ERROR]", repr(e))
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
            # Join with suppliers and count items
            sql = """
                SELECT 
                    p.id, 
                    p.supplier_id, 
                    p.expected_date, 
                    p.total_amount, 
                    p.status, 
                    p.created_at,
                    p.created_by,
                    s.name as supplier_name,
                    s.contact_name as supplier_contact,
                    COUNT(pi.id) as item_count
                FROM purchases p
                LEFT JOIN suppliers s ON p.supplier_id = s.id
                LEFT JOIN purchase_items pi ON p.id = pi.purchase_id
            """
            if status:
                sql += " WHERE p.status = {} ".format(_paramstyle())
                sql += " GROUP BY p.id, p.supplier_id, p.expected_date, p.total_amount, p.status, p.created_at, p.created_by, s.name, s.contact_name"
                sql += " ORDER BY p.created_at DESC"
                cur.execute(sql, (status,))
            else:
                sql += " GROUP BY p.id, p.supplier_id, p.expected_date, p.total_amount, p.status, p.created_at, p.created_by, s.name, s.contact_name"
                sql += " ORDER BY p.created_at DESC"
                cur.execute(sql)
            rows = cur.fetchall()
            result = []
            for r in rows:
                try:
                    result.append(dict(r))
                except Exception:
                    result.append({
                        'id': r[0], 
                        'supplier_id': r[1], 
                        'expected_date': r[2], 
                        'total_amount': r[3], 
                        'status': r[4], 
                        'created_at': r[5],
                        'created_by': r[6],
                        'supplier_name': r[7],
                        'supplier_contact': r[8],
                        'items_count': r[9]  # Changed from item_count to items_count
                    })
            return result
        finally:
            conn.close()
    
    @staticmethod
    def update_order_status(order_id: int, new_status: str):
        """Update the status of a purchase order."""
        conn = get_conn()
        try:
            param = _paramstyle()
            sql = f"UPDATE purchases SET status = {param} WHERE id = {param}"
            _exec(conn, sql, (new_status, order_id))
            conn.commit()
            return True
        except Exception as e:
            try:
                conn.rollback()
            except Exception:
                pass
            print(f"[UPDATE_ORDER_STATUS ERROR] {repr(e)}")
            return False
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
    def add_damage_report(purchase_id: int, category: str, reason: str, created_by: str | None = None):
        """Add a new damage report."""
        conn = get_conn()
        try:
            param = _paramstyle()
            sql = f"INSERT INTO damages (purchase_id, category, reason, created_by, created_at, item_id, quantity) VALUES ({param},{param},{param},{param},{param},{param},{param})"
            # Using item_id=1 and quantity=1 as placeholder since schema requires them
            _exec(conn, sql, (purchase_id, category, reason, created_by, datetime.now(), 1, 1))
            conn.commit()
            return True
        except Exception as e:
            try:
                conn.rollback()
            except Exception:
                pass
            print(f"[ADD_DAMAGE_REPORT ERROR] {repr(e)}")
            return False
        finally:
            conn.close()

    @staticmethod
    def list_damages():
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, purchase_id, item_id, category, quantity, reason, status, created_by, created_at FROM damages ORDER BY created_at DESC")
            rows = cur.fetchall()
            result = []
            for r in rows:
                try:
                    result.append(dict(r))
                except Exception:
                    result.append({
                        'id': r[0], 
                        'purchase_id': r[1], 
                        'item_id': r[2], 
                        'category': r[3], 
                        'quantity': r[4], 
                        'reason': r[5], 
                        'status': r[6], 
                        'created_by': r[7], 
                        'created_at': r[8]
                    })
            return result
        finally:
            conn.close()


class MessageModel:
    @staticmethod
    def add_message(sender_id: int, recipient_id: int, category: str, title: str, body: str):
        conn = get_conn()
        try:
            _exec(conn, f"INSERT INTO messages (sender_id, recipient_id, category, title, body, created_at) VALUES ({_paramstyle()},{_paramstyle()},{_paramstyle()},{_paramstyle()},{_paramstyle()},{_paramstyle()})",
                  (sender_id, recipient_id, category, title, body, datetime.now()))
            conn.commit()
            return True
        finally:
            conn.close()

    @staticmethod
    def list_messages(user_id: int, limit: int = 50):
        """List messages for a specific user (both sent and received)."""
        conn = get_conn()
        try:
            cur = conn.cursor()
            # Get messages where user is either sender or recipient
            cur.execute("""
                SELECT m.id, m.sender_id, m.recipient_id, m.category, m.title, m.body, m.is_read, m.created_at,
                       sender.full_name as sender_name, sender.role as sender_role,
                       recipient.full_name as recipient_name, recipient.role as recipient_role
                FROM messages m
                LEFT JOIN users sender ON m.sender_id = sender.id
                LEFT JOIN users recipient ON m.recipient_id = recipient.id
                WHERE m.recipient_id = {} OR m.sender_id = {}
                ORDER BY m.created_at DESC LIMIT {}
            """.format(_paramstyle(), _paramstyle(), limit), (user_id, user_id))
            rows = cur.fetchall()
            result = []
            for r in rows:
                try:
                    result.append(dict(r))
                except Exception:
                    result.append({
                        'id': r[0],
                        'sender_id': r[1],
                        'recipient_id': r[2],
                        'category': r[3],
                        'title': r[4],
                        'body': r[5],
                        'is_read': r[6],
                        'created_at': r[7],
                        'sender_name': r[8],
                        'sender_role': r[9],
                        'recipient_name': r[10],
                        'recipient_role': r[11]
                    })
            return result
        finally:
            conn.close()
    
    @staticmethod
    def mark_as_read(message_id: int):
        """Mark a message as read."""
        conn = get_conn()
        try:
            _exec(conn, f"UPDATE messages SET is_read = 1 WHERE id = {_paramstyle()}", (message_id,))
            conn.commit()
            return True
        finally:
            conn.close()
    
    @staticmethod
    def delete_message(message_id: int):
        """Delete a message."""
        conn = get_conn()
        try:
            _exec(conn, f"DELETE FROM messages WHERE id = {_paramstyle()}", (message_id,))
            conn.commit()
            return True
        finally:
            conn.close()


class DashboardModel:
    """Model for fetching dashboard statistics and KPIs."""
    
    @staticmethod
    def get_inventory_value():
        """Calculate total inventory value (sum of unit_cost * stock_qty for all items)."""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT SUM(unit_cost * stock_qty) as total_value FROM items")
            row = cur.fetchone()
            if row:
                try:
                    total = row['total_value'] if row['total_value'] is not None else 0
                except (TypeError, KeyError):
                    total = row[0] if row[0] is not None else 0
                return float(total)
            return 0.0
        except Exception as e:
            print(f"[DASHBOARD] Error calculating inventory value: {e}")
            return 0.0
        finally:
            conn.close()
    
    @staticmethod
    def get_total_wastages():
        """Get total number of damaged/wasted items."""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT SUM(quantity) as total_wastages FROM damages")
            row = cur.fetchone()
            if row:
                try:
                    total = row['total_wastages'] if row['total_wastages'] is not None else 0
                except (TypeError, KeyError):
                    total = row[0] if row[0] is not None else 0
                return int(total)
            return 0
        except Exception as e:
            print(f"[DASHBOARD] Error calculating wastages: {e}")
            return 0
        finally:
            conn.close()
    
    @staticmethod
    def get_inventory_items_count():
        """Get total count of distinct inventory items."""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) as item_count FROM items")
            row = cur.fetchone()
            if row:
                try:
                    count = row['item_count']
                except (TypeError, KeyError):
                    count = row[0]
                return int(count)
            return 0
        except Exception as e:
            print(f"[DASHBOARD] Error counting inventory items: {e}")
            return 0
        finally:
            conn.close()
    
    @staticmethod
    def get_low_stock_count():
        """Get count of items with stock below minimum threshold."""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) as low_stock_count FROM items WHERE stock_qty <= min_stock")
            row = cur.fetchone()
            if row:
                try:
                    count = row['low_stock_count']
                except (TypeError, KeyError):
                    count = row[0]
                return int(count)
            return 0
        except Exception as e:
            print(f"[DASHBOARD] Error counting low stock items: {e}")
            return 0
        finally:
            conn.close()
    
    @staticmethod
    def get_all_kpis():
        """Get all dashboard KPIs in one call."""
        return {
            'inventory_value': DashboardModel.get_inventory_value(),
            'wastages': DashboardModel.get_total_wastages(),
            'inventory_items': DashboardModel.get_inventory_items_count(),
            'low_stocks': DashboardModel.get_low_stock_count()
        }
