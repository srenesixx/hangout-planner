import hashlib
import os
import sqlite3
from src.models.database import get_connection

def hash_password(password: str) -> str:
    """Hashes a password using SHA256 with a unique salt."""
    salt = os.urandom(16).hex()
    pwd_hash = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
    return f"{salt}${pwd_hash}"

def verify_password(stored_password_hash: str, password: str) -> bool:
    """Verifies a password against a stored hash."""
    try:
        salt, pwd_hash = stored_password_hash.split('$')
        check_hash = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
        return pwd_hash == check_hash
    except Exception:
        return False

def register_user(nama: str, username: str, email: str, password: str, initial_saldo: int = 0) -> tuple[bool, str]:
    """
    Registers a new user.
    Returns (success, message).
    """
    if not nama or not username or not password:
        return False, "Nama, username, dan password wajib diisi."
    
    if len(password) < 6:
        return False, "Password minimal harus 6 karakter."
        
    password_hash = hash_password(password)
    email = email.strip() if email else None
    username = username.strip().lower()
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (nama, username, email, password_hash, saldo) VALUES (?, ?, ?, ?, ?)",
            (nama.strip(), username, email, password_hash, initial_saldo)
        )
        user_id = cursor.lastrowid
        conn.commit()
        return True, "Registrasi berhasil! Silakan masuk."
    except sqlite3.IntegrityError as e:
        err_msg = str(e).lower()
        if "username" in err_msg:
            return False, "Username sudah terdaftar."
        elif "email" in err_msg:
            return False, "Email sudah terdaftar."
        else:
            return False, "Username atau Email sudah terdaftar."
    finally:
        conn.close()

def login_user(username_or_email: str, password: str) -> dict | None:
    """
    Authenticates a user.
    Returns the user dict if successful, or None.
    """
    if not username_or_email or not password:
        return None
        
    username_or_email = username_or_email.strip().lower()
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Search by username or email
        cursor.execute(
            "SELECT * FROM users WHERE LOWER(username) = ? OR LOWER(email) = ?",
            (username_or_email, username_or_email)
        )
        user_row = cursor.fetchone()
        
        if user_row and verify_password(user_row['password_hash'], password):
            # Convert row to dict
            user_dict = dict(user_row)
            # Remove password hash for safety
            user_dict.pop('password_hash', None)
            return user_dict
        return None
    finally:
        conn.close()

def get_user_by_id(user_id: int) -> dict | None:
    """Gets user details by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            user_dict = dict(row)
            user_dict.pop('password_hash', None)
            return user_dict
        return None
    finally:
        conn.close()

def update_saldo(user_id: int, new_saldo: int) -> bool:
    """Updates the user's current balance (saldo)."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET saldo = ? WHERE id = ?", (new_saldo, user_id))
        conn.commit()
        return cursor.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close()

def change_password(user_id: int, current_password: str, new_password: str) -> tuple[bool, str]:
    """
    Changes user's password.
    Returns (success, message).
    """
    if not current_password or not new_password:
        return False, "Password lama dan password baru harus diisi."
    if len(new_password) < 6:
        return False, "Password baru minimal 6 karakter."
        
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT password_hash FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if not row:
            return False, "User tidak ditemukan."
            
        if not verify_password(row['password_hash'], current_password):
            return False, "Password lama salah."
            
        new_hash = hash_password(new_password)
        cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, user_id))
        conn.commit()
        return True, "Password berhasil diubah."
    finally:
        conn.close()
