import sqlite3
import json
from datetime import datetime
from src.models.database import get_connection

def get_user_plan_periods(user_id: int) -> list[str]:
    """Retrieves all unique months (YYYY-MM) from user's plans."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT DISTINCT strftime('%Y-%m', tanggal) as mon FROM plans WHERE user_id = ? ORDER BY mon DESC", (user_id,))
        return [r['mon'] for r in cursor.fetchall()]
    finally:
        conn.close()


def calculate_plan_total(plan_id: int) -> int:
    """Calculates the total estimated cost for a plan, including locations, items, and transport cost."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Sum of items
        cursor.execute("""
            SELECT SUM(pi.harga_satuan * pi.jumlah) as items_total
            FROM plan_items pi
            JOIN plan_locations pl ON pi.location_id = pl.id
            WHERE pl.plan_id = ?
        """, (plan_id,))
        row = cursor.fetchone()
        items_total = row['items_total'] if row and row['items_total'] is not None else 0
        
        # Transport cost
        cursor.execute("SELECT transport_cost FROM plans WHERE id = ?", (plan_id,))
        plan_row = cursor.fetchone()
        transport_cost = plan_row['transport_cost'] if plan_row and plan_row['transport_cost'] is not None else 0
        
        return items_total + transport_cost
    finally:
        conn.close()

def create_plan(user_id: int, nama_rencana: str, tanggal: str, jumlah_teman: int, 
                budget: int, transportasi: str, transport_cost: int, 
                mood: str = '😐', mood_efek_persen: float = 0.0, status: str = 'draft') -> int:
    """Creates a new plan and returns its ID."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO plans (user_id, nama_rencana, tanggal, jumlah_teman, budget, 
                               transportasi, transport_cost, mood, mood_efek_persen, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, nama_rencana, tanggal, jumlah_teman, budget, 
              transportasi, transport_cost, mood, mood_efek_persen, status))
        plan_id = cursor.lastrowid
        
        # Save initial mood log
        cursor.execute("""
            INSERT INTO mood_logs (plan_id, mood, efek_persen, catatan)
            VALUES (?, ?, ?, ?)
        """, (plan_id, mood, mood_efek_persen, "Initial plan mood"))
        
        conn.commit()
        return plan_id
    finally:
        conn.close()

def update_plan_details(plan_id: int, nama_rencana: str, tanggal: str, jumlah_teman: int, 
                        budget: int, transportasi: str, transport_cost: int) -> bool:
    """Updates the basic details of a plan."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE plans 
            SET nama_rencana = ?, tanggal = ?, jumlah_teman = ?, budget = ?, 
                transportasi = ?, transport_cost = ?
            WHERE id = ?
        """, (nama_rencana, tanggal, jumlah_teman, budget, transportasi, transport_cost, plan_id))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def update_plan_mood(plan_id: int, mood: str, mood_efek_persen: float) -> bool:
    """Updates the mood and saves a new log entry."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE plans SET mood = ?, mood_efek_persen = ? WHERE id = ?", 
                       (mood, mood_efek_persen, plan_id))
        
        # Insert log
        cursor.execute("""
            INSERT INTO mood_logs (plan_id, mood, efek_persen, catatan)
            VALUES (?, ?, ?, ?)
        """, (plan_id, mood, mood_efek_persen, f"Mood updated to {mood}"))
        
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def save_locations_and_items(plan_id: int, data: list[dict]) -> bool:
    """
    Saves locations and their items for a plan.
    It clears existing locations for this plan (cascading to items) and inserts the new ones.
    data format:
    [
        {
            'nama_tempat': 'Cafe A',
            'kategori': 'Kafe',
            'urutan': 0,
            'items': [
                {'nama_item': 'Cappuccino', 'harga_satuan': 30000, 'jumlah': 2},
                ...
            ]
        },
        ...
    ]
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Delete existing plan_locations (this will cascade delete plan_items)
        cursor.execute("DELETE FROM plan_locations WHERE plan_id = ?", (plan_id,))
        
        # Insert new locations and items
        for loc_idx, loc in enumerate(data):
            cursor.execute("""
                INSERT INTO plan_locations (plan_id, nama_tempat, kategori, urutan)
                VALUES (?, ?, ?, ?)
            """, (plan_id, loc['nama_tempat'], loc.get('kategori', 'Lainnya'), loc.get('urutan', loc_idx)))
            
            location_id = cursor.lastrowid
            
            for item in loc.get('items', []):
                cursor.execute("""
                    INSERT INTO plan_items (location_id, nama_item, harga_satuan, jumlah)
                    VALUES (?, ?, ?, ?)
                """, (location_id, item['nama_item'], item['harga_satuan'], item['jumlah']))
                
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print("Error saving locations and items:", e)
        return False
    finally:
        conn.close()

def get_plan_locations_and_items(plan_id: int) -> list[dict]:
    """Retrieves all locations and items for a plan."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM plan_locations WHERE plan_id = ? ORDER BY urutan", (plan_id,))
        locations = [dict(loc) for loc in cursor.fetchall()]
        
        for loc in locations:
            cursor.execute("SELECT * FROM plan_items WHERE location_id = ?", (loc['id'],))
            loc['items'] = [dict(item) for item in cursor.fetchall()]
            
        return locations
    finally:
        conn.close()

def get_plan_details(plan_id: int) -> dict | None:
    """Returns complete details for a plan, including items, total cost, split bills, and mood logs."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM plans WHERE id = ?", (plan_id,))
        plan_row = cursor.fetchone()
        if not plan_row:
            return None
            
        plan_dict = dict(plan_row)
        
        # Get locations and items
        plan_dict['locations'] = get_plan_locations_and_items(plan_id)
        
        # Calculate total cost of items
        items_total = 0
        for loc in plan_dict['locations']:
            loc_subtotal = sum(item['harga_satuan'] * item['jumlah'] for item in loc['items'])
            loc['subtotal'] = loc_subtotal
            items_total += loc_subtotal
            
        plan_dict['items_total'] = items_total
        plan_dict['total_cost'] = items_total + plan_dict['transport_cost']
        
        # Get split bill if exists
        cursor.execute("SELECT * FROM split_bills WHERE plan_id = ?", (plan_id,))
        sb_row = cursor.fetchone()
        plan_dict['split_bill'] = dict(sb_row) if sb_row else None
        
        # Get mood logs
        cursor.execute("SELECT * FROM mood_logs WHERE plan_id = ? ORDER BY created_at DESC", (plan_id,))
        plan_dict['mood_logs'] = [dict(ml) for ml in cursor.fetchall()]
        
        return plan_dict
    finally:
        conn.close()

def save_split_bill(plan_id: int, total_tagihan: int, jumlah_orang: int, per_orang: int) -> bool:
    """Saves or updates split bill for a plan."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO split_bills (plan_id, total_tagihan, jumlah_orang, per_orang)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(plan_id) DO UPDATE SET
                total_tagihan = excluded.total_tagihan,
                jumlah_orang = excluded.jumlah_orang,
                per_orang = excluded.per_orang,
                created_at = CURRENT_TIMESTAMP
        """, (plan_id, total_tagihan, jumlah_orang, per_orang))
        conn.commit()
        return True
    except Exception as e:
        print("Error saving split bill:", e)
        return False
    finally:
        conn.close()

def delete_plan(plan_id: int) -> bool:
    """Deletes a plan (which cascades to locations, items, split bills, mood logs)."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM plans WHERE id = ?", (plan_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def update_plan_status(plan_id: int, status: str) -> bool:
    """Updates plan status (e.g. draft, selesai, dibatalkan)."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE plans SET status = ? WHERE id = ?", (status, plan_id))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def get_user_plans(user_id: int, status: str = None) -> list[dict]:
    """Returns a list of plans for a user, optionally filtered by status."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if status:
            cursor.execute("SELECT * FROM plans WHERE user_id = ? AND status = ? ORDER BY tanggal DESC, id DESC", (user_id, status))
        else:
            cursor.execute("SELECT * FROM plans WHERE user_id = ? ORDER BY tanggal DESC, id DESC", (user_id,))
            
        plans = [dict(row) for row in cursor.fetchall()]
        
        # Add total costs to each plan summary
        for plan in plans:
            plan['total_cost'] = calculate_plan_total(plan['id'])
            
        return plans
    finally:
        conn.close()

def get_monthly_spending(user_id: int, year_month: str) -> int:
    """Returns the total cost of all plans for a user in a specific YYYY-MM period."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id FROM plans 
            WHERE user_id = ? AND strftime('%Y-%m', tanggal) = ?
        """, (user_id, year_month))
        plan_ids = [row['id'] for row in cursor.fetchall()]
        
        total = 0
        for pid in plan_ids:
            total += calculate_plan_total(pid)
            
        return total
    finally:
        conn.close()

def calculate_budget_health_score(user_id: int, target_month: str) -> tuple[int, dict]:
    """
    Calculates the budget health score for a specific month (format 'YYYY-MM').
    Returns (score, breakdown_dict).
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Get user's current balance
        cursor.execute("SELECT saldo FROM users WHERE id = ?", (user_id,))
        user_row = cursor.fetchone()
        saldo = user_row['saldo'] if user_row else 0
        
        # Get all plans in this month
        cursor.execute("""
            SELECT id, budget, tanggal, status FROM plans 
            WHERE user_id = ? AND strftime('%Y-%m', tanggal) = ?
        """, (user_id, target_month))
        plans = [dict(row) for row in cursor.fetchall()]
        
        if not plans:
            # No activity this month means perfect score of 100 or default healthy state
            return 100, {
                "ratio_score": 30,
                "frequency_score": 20,
                "consistency_score": 25,
                "trend_score": 25,
                "total_spending": 0,
                "plan_count": 0,
                "message": "Tidak ada rencana nongkrong bulan ini. Anggaran aman terkendali!"
            }
            
        # Calculate total spending (estimated/actual)
        total_spending = 0
        consistent_plans_count = 0
        for p in plans:
            total_cost = calculate_plan_total(p['id'])
            total_spending += total_cost
            if total_cost <= p['budget']:
                consistent_plans_count += 1
                
        # 1. Spending-to-Balance Ratio Score (Max 30 points)
        # Ratio = Spending / (Saldo + Spending)
        # Healthy if spending <= 15% of total resources
        # 0 points if spending >= 50% of total resources
        denom = saldo + total_spending
        ratio = total_spending / denom if denom > 0 else 0
        ratio_score = int(max(0, min(30, 30 * (1 - (ratio / 0.5)))))
        
        # 2. Frequency Score (Max 20 points)
        # Hanging out too often hurts finances.
        plan_count = len(plans)
        if plan_count <= 2:
            frequency_score = 20
        elif plan_count <= 4:
            frequency_score = 15
        elif plan_count <= 8:
            frequency_score = 10
        else:
            frequency_score = 5
            
        # 3. Consistency Score (Max 25 points)
        # Did user stay within the budget they set for individual plans?
        consistency_score = int(25 * (consistent_plans_count / plan_count))
        
        # 4. Spending Trend vs Previous Month Score (Max 25 points)
        # Parse previous month
        try:
            dt = datetime.strptime(target_month, "%Y-%m")
            if dt.month == 1:
                prev_month = f"{dt.year - 1}-12"
            else:
                prev_month = f"{dt.year}-{dt.month - 1:02d}"
        except Exception:
            prev_month = ""
            
        prev_spending = 0
        if prev_month:
            prev_spending = get_monthly_spending(user_id, prev_month)
            
        if prev_spending == 0:
            trend_score = 20  # Neutral starting score if no previous month data
        elif total_spending < prev_spending:
            # Good! Spending decreased
            trend_score = 25
        elif total_spending == prev_spending:
            trend_score = 20
        else:
            # Spending increased. Score decreases based on how much it increased.
            increase_pct = (total_spending - prev_spending) / prev_spending
            trend_score = int(max(0, min(25, 20 - (20 * increase_pct))))
            
        total_score = ratio_score + frequency_score + consistency_score + trend_score
        
        # Generate supportive recommendations
        if total_score >= 80:
            rec = "Luar biasa! Pengelolaan anggaran nongkrongmu sangat sehat. Pertahankan disiplin keuangan ini! 🌟"
        elif total_score >= 50:
            rec = "Cukup baik, tetapi kamu bisa lebih hemat. Cobalah kurangi frekuensi nongkrong atau cari tempat alternatif yang lebih ramah kantong. 👍"
        else:
            rec = "Waspada! Kebiasaan nongkrongmu mulai mengganggu kesehatan keuangan. Kurangi pengeluaran impulsif dan fokuslah pada menabung dahulu. ⚠️"
            
        breakdown = {
            "ratio_score": ratio_score,
            "frequency_score": frequency_score,
            "consistency_score": consistency_score,
            "trend_score": trend_score,
            "total_spending": total_spending,
            "plan_count": plan_count,
            "message": rec
        }
        
        return total_score, breakdown
    finally:
        conn.close()

def get_saved_budget_health_score(user_id: int, periode: str) -> dict | None:
    """Retrieves saved budget health score for a period."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM budget_health_scores WHERE user_id = ? AND periode = ?", (user_id, periode))
        row = cursor.fetchone()
        if row:
            d = dict(row)
            d['breakdown'] = json.loads(d['breakdown_json']) if d['breakdown_json'] else {}
            return d
        return None
    finally:
        conn.close()

def save_or_update_health_score(user_id: int, periode: str) -> int:
    """Calculates, saves/updates, and returns the budget health score for a period."""
    score, breakdown = calculate_budget_health_score(user_id, periode)
    breakdown_json = json.dumps(breakdown)
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO budget_health_scores (user_id, periode, score, breakdown_json)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, periode) DO UPDATE SET
                score = excluded.score,
                breakdown_json = excluded.breakdown_json,
                created_at = CURRENT_TIMESTAMP
        """, (user_id, periode, score, breakdown_json))
        conn.commit()
        return score
    except Exception as e:
        print("Error saving budget health score:", e)
        # Create UNIQUE index if it doesn't exist
        try:
            cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS uq_user_period ON budget_health_scores(user_id, periode);")
            conn.commit()
            # Retry
            cursor.execute("""
                INSERT INTO budget_health_scores (user_id, periode, score, breakdown_json)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(user_id, periode) DO UPDATE SET
                    score = excluded.score,
                    breakdown_json = excluded.breakdown_json,
                    created_at = CURRENT_TIMESTAMP
            """, (user_id, periode, score, breakdown_json))
            conn.commit()
            return score
        except Exception as ex:
            print("Retry saving budget health score failed:", ex)
            return score
    finally:
        conn.close()

def get_stats_data(user_id: int) -> dict:
    """
    Returns aggregated stats data for charts:
    - Monthly spending (past 6 months)
    - Spending by category
    - Average spending per hangout
    - Mood vs average spending
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # 1. Monthly spending
        cursor.execute("""
            SELECT strftime('%Y-%m', tanggal) as month, id
            FROM plans
            WHERE user_id = ?
            ORDER BY month ASC
        """, (user_id,))
        plans_by_month = {}
        for row in cursor.fetchall():
            m = row['month']
            pid = row['id']
            plans_by_month.setdefault(m, []).append(pid)
            
        monthly_spending = []
        months = sorted(list(plans_by_month.keys()))[-6:] # past 6 months
        for m in months:
            total = sum(calculate_plan_total(pid) for pid in plans_by_month[m])
            monthly_spending.append({'month': m, 'total': total})
            
        # 2. Category distribution
        cursor.execute("""
            SELECT pl.kategori, pi.harga_satuan, pi.jumlah
            FROM plan_items pi
            JOIN plan_locations pl ON pi.location_id = pl.id
            JOIN plans p ON pl.plan_id = p.id
            WHERE p.user_id = ?
        """, (user_id,))
        categories = {}
        for row in cursor.fetchall():
            cat = row['kategori'] if row['kategori'] else 'Lainnya'
            cost = row['harga_satuan'] * row['jumlah']
            categories[cat] = categories.get(cat, 0) + cost
            
        category_spending = [{'category': k, 'total': v} for k, v in categories.items()]
        
        # 3. Average spending
        cursor.execute("SELECT id FROM plans WHERE user_id = ?", (user_id,))
        all_pids = [r['id'] for r in cursor.fetchall()]
        total_spent = sum(calculate_plan_total(pid) for pid in all_pids)
        num_hangouts = len(all_pids)
        avg_per_hangout = total_spent / num_hangouts if num_hangouts > 0 else 0
        
        # 4. Mood vs Spending
        cursor.execute("SELECT id, mood FROM plans WHERE user_id = ?", (user_id,))
        plans_mood = [{'id': r['id'], 'mood': r['mood']} for r in cursor.fetchall()]
        mood_costs = {}
        mood_counts = {}
        for pm in plans_mood:
            c = calculate_plan_total(pm['id'])
            m = pm['mood']
            mood_costs[m] = mood_costs.get(m, 0) + c
            mood_counts[m] = mood_counts.get(m, 0) + 1
            
        mood_spending = []
        for m in mood_costs:
            mood_spending.append({
                'mood': m,
                'avg_cost': mood_costs[m] / mood_counts[m]
            })
            
        return {
            'monthly_spending': monthly_spending,
            'category_spending': category_spending,
            'avg_per_hangout': avg_per_hangout,
            'mood_spending': mood_spending,
            'total_spent': total_spent,
            'num_hangouts': num_hangouts
        }
    finally:
        conn.close()

def update_plan_details(plan_id: int, nama_rencana: str, tanggal: str, jumlah_teman: int, budget: int, transportasi: str, transport_cost: int) -> bool:
    """Updates the basic details of a plan in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE plans 
            SET nama_rencana = ?, tanggal = ?, jumlah_teman = ?, budget = ?, transportasi = ?, transport_cost = ?
            WHERE id = ?
        """, (nama_rencana, tanggal, jumlah_teman, budget, transportasi, transport_cost, plan_id))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def get_split_bill_checklist(plan_id: int) -> list:
    """Returns the list of paid statuses for friends in a split bill."""
    import os
    import json
    from src.config import BASE_DIR
    path = os.path.join(BASE_DIR, f"split_bill_paid_{plan_id}.json")
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_split_bill_checklist(plan_id: int, checklist: list) -> bool:
    """Saves the list of paid statuses for friends in a split bill."""
    import os
    import json
    from src.config import BASE_DIR
    path = os.path.join(BASE_DIR, f"split_bill_paid_{plan_id}.json")
    try:
        with open(path, 'w') as f:
            json.dump(checklist, f)
        return True
    except Exception:
        return False

def get_user_split_bills(user_id: int) -> list[dict]:
    """Returns a list of all plans for a user that have friends (jumlah_teman > 0) along with their split bill info and paid status."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM plans WHERE user_id = ? AND jumlah_teman > 0 ORDER BY tanggal DESC, id DESC", (user_id,))
        plans = [dict(row) for row in cursor.fetchall()]
        
        for plan in plans:
            plan_id = plan['id']
            plan['total_cost'] = calculate_plan_total(plan_id)
            
            cursor.execute("SELECT * FROM split_bills WHERE plan_id = ?", (plan_id,))
            sb_row = cursor.fetchone()
            plan['split_bill'] = dict(sb_row) if sb_row else None
            
        return plans
    finally:
        conn.close()

def get_split_bill_selected_items(plan_id: int) -> list[int]:
    """Returns the list of item IDs selected for split bill."""
    import os
    import json
    from src.config import BASE_DIR
    path = os.path.join(BASE_DIR, f"split_bill_selected_items_{plan_id}.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception:
        return []

def save_split_bill_selected_items(plan_id: int, selected_item_ids: list[int]) -> bool:
    """Saves the list of item IDs selected for split bill."""
    import os
    import json
    from src.config import BASE_DIR
    path = os.path.join(BASE_DIR, f"split_bill_selected_items_{plan_id}.json")
    try:
        with open(path, 'w') as f:
            json.dump(selected_item_ids, f)
        return True
    except Exception:
        return False
