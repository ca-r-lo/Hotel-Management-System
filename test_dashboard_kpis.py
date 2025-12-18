"""
Test script to verify dashboard KPI calculations and display sample data
"""

from models.purchase import DashboardModel
from models.database import get_conn

def test_dashboard_kpis():
    """Test all dashboard KPI calculations."""
    print("=" * 60)
    print("DASHBOARD KPI TEST")
    print("=" * 60)
    
    # Get all KPIs
    kpis = DashboardModel.get_all_kpis()
    
    print(f"\n📊 DASHBOARD STATISTICS:")
    print(f"   Inventory Value: ₱ {kpis['inventory_value']:,.2f}")
    print(f"   Wastages: {kpis['wastages']}")
    print(f"   Inventory Items: {kpis['inventory_items']}")
    print(f"   Low Stocks: {kpis['low_stocks']}")
    
    # Show individual items
    print(f"\n📦 INVENTORY ITEMS BREAKDOWN:")
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT name, stock_qty, min_stock, unit_cost, (stock_qty * unit_cost) as value
            FROM items 
            ORDER BY value DESC 
            LIMIT 10
        """)
        rows = cur.fetchall()
        
        if rows:
            print(f"   {'Item':<30} {'Stock':<10} {'Min':<10} {'Unit Cost':<12} {'Total Value':<15}")
            print(f"   {'-'*80}")
            for row in rows:
                try:
                    name = row['name'] if 'name' in row.keys() else row[0]
                    stock = row['stock_qty'] if 'stock_qty' in row.keys() else row[1]
                    min_stock = row['min_stock'] if 'min_stock' in row.keys() else row[2]
                    unit_cost = row['unit_cost'] if 'unit_cost' in row.keys() else row[3]
                    value = row['value'] if 'value' in row.keys() else row[4]
                except:
                    name, stock, min_stock, unit_cost, value = row[0], row[1], row[2], row[3], row[4]
                
                low_stock_indicator = " ⚠️" if stock <= min_stock else ""
                print(f"   {name[:28]:<30} {stock:<10} {min_stock:<10} ₱{unit_cost:<11.2f} ₱{value:<14.2f}{low_stock_indicator}")
        else:
            print("   No items found in inventory")
            
    finally:
        conn.close()
    
    # Show damages
    print(f"\n🗑️  RECENT DAMAGES:")
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT quantity, reason, created_at
            FROM damages 
            ORDER BY created_at DESC 
            LIMIT 5
        """)
        rows = cur.fetchall()
        
        if rows:
            for row in rows:
                try:
                    qty = row['quantity'] if 'quantity' in row.keys() else row[0]
                    reason = row['reason'] if 'reason' in row.keys() else row[1]
                    created_at = row['created_at'] if 'created_at' in row.keys() else row[2]
                except:
                    qty, reason, created_at = row[0], row[1], row[2]
                print(f"   - Qty: {qty}, Reason: {reason[:50]}, Date: {created_at}")
        else:
            print("   No damage reports found")
            
    finally:
        conn.close()
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    test_dashboard_kpis()
