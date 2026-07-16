import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from src.views.components import (
    COLORS, FONTS,
    CardFrame, PrimaryButton, SecondaryButton, SuccessButton,
    CustomEntry, CustomLabel, HeaderLabel, MutedLabel, StatusLabel
)
from src.controllers.auth_controller import AuthController as auth

class LoginRegisterFrame(ctk.CTkFrame):
    """Handles Login and Register forms in a clean, centered card design."""
    def __init__(self, master, on_login_success):
        super().__init__(master, fg_color=COLORS["bg_main"])
        self.on_login_success = on_login_success
        self.is_register_mode = False
        
        # Center container
        self.container = CardFrame(self, width=440, height=420)
        self.build_ui()
        
    def build_ui(self):
        # Clear container
        for widget in self.container.winfo_children():
            widget.destroy()
            
        # Determine card size dynamically based on mode
        card_width = 440
        card_height = 620 if self.is_register_mode else 440
        
        self.container.configure(width=card_width, height=card_height)
        self.container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Form Container
        self.form_panel = ctk.CTkFrame(self.container, fg_color="transparent")
        self.form_panel.pack(fill="both", expand=True, padx=30, pady=25)
        
        # 1. Branding Header
        logo_frame = ctk.CTkFrame(self.form_panel, fg_color="transparent")
        logo_frame.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(logo_frame, text="🔵 Hangout Planner", font=("Segoe UI", 22, "bold"), text_color=COLORS["text_main"]).pack(anchor="center")
        
        # 2. Form Title & Subtitle
        form_title = "Daftar Akun" if self.is_register_mode else "Masuk Akun"
        self.title_lbl = HeaderLabel(self.form_panel, text=form_title)
        self.title_lbl.pack(anchor="w", pady=(0, 2))
        
        form_subtitle = "Buat akun baru untuk mengelola budget" if self.is_register_mode else "Masuk untuk mengelola rencana hangout"
        self.subtitle_lbl = MutedLabel(self.form_panel, text=form_subtitle)
        self.subtitle_lbl.pack(anchor="w", pady=(0, 15))
        
        # 3. Form Fields Container
        self.form_frame = ctk.CTkFrame(self.form_panel, fg_color="transparent")
        self.form_frame.pack(fill="both", expand=True)
        
        # Error Label
        self.error_lbl = StatusLabel(self.form_frame, status_type="danger", text="", font=FONTS["caption_bold"])
        self.error_lbl.pack(anchor="w", pady=(0, 5))
        
        if self.is_register_mode:
            # Register Fields (Single vertical column layout)
            fields = [
                ("nama", "Nama Lengkap", "Nama Lengkap Anda"),
                ("email", "Email (Opsional)", "nama@email.com"),
                ("username", "Username", "Username unik"),
                ("password", "Password", "Minimal 6 karakter", True),
                ("confirm_password", "Konfirmasi Password", "Ulangi password", True),
                ("saldo", "Saldo Awal Dompet (Rp)", "Contoh: 500000")
            ]
            
            self.entries = {}
            for key, label, placeholder, *is_pwd in fields:
                CustomLabel(self.form_frame, text=label, font=FONTS["caption_bold"]).pack(anchor="w", pady=(0, 1))
                
                show_char = "*" if is_pwd else None
                entry = CustomEntry(self.form_frame, placeholder_text=placeholder, show=show_char, height=32)
                entry.pack(fill="x", pady=(0, 8))
                self.entries[key] = entry
                
            # Map entries to instance variables for handlers
            self.nama_entry = self.entries["nama"]
            self.email_entry = self.entries["email"]
            self.username_entry = self.entries["username"]
            self.password_entry = self.entries["password"]
            self.confirm_password_entry = self.entries["confirm_password"]
            self.saldo_entry = self.entries["saldo"]
            
            self.submit_btn = SuccessButton(self.form_frame, text="Daftar Sekarang", command=self.handle_register, height=34)
            self.submit_btn.pack(fill="x", pady=(8, 4))
            
            self.switch_btn = SecondaryButton(self.form_frame, text="Sudah Punya Akun? Masuk", command=self.toggle_mode, height=34)
            self.switch_btn.pack(fill="x")
        else:
            # Login Fields
            CustomLabel(self.form_frame, text="Username / Email", font=FONTS["caption_bold"]).pack(anchor="w", pady=(0, 2))
            self.username_entry = CustomEntry(self.form_frame, placeholder_text="Masukkan username atau email")
            self.username_entry.pack(fill="x", pady=(0, 15))
            
            CustomLabel(self.form_frame, text="Password", font=FONTS["caption_bold"]).pack(anchor="w", pady=(0, 2))
            self.password_entry = CustomEntry(self.form_frame, placeholder_text="Masukkan password Anda", show="*")
            self.password_entry.pack(fill="x", pady=(0, 25))
            
            # Action Buttons
            self.submit_btn = PrimaryButton(self.form_frame, text="Masuk", command=self.handle_login)
            self.submit_btn.pack(fill="x", pady=(0, 8))
            
            self.switch_btn = SecondaryButton(self.form_frame, text="Belum Punya Akun? Daftar", command=self.toggle_mode)
            self.switch_btn.pack(fill="x")

    def toggle_mode(self):
        self.is_register_mode = not self.is_register_mode
        self.build_ui()
        
    def show_error(self, message):
        self.error_lbl.configure(text=message)
        
    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            self.show_error("Username dan password wajib diisi.")
            return
            
        user = auth.login_user(username, password)
        if user:
            self.on_login_success(user)
        else:
            self.show_error("Username atau password salah.")
            
    def handle_register(self):
        nama = self.nama_entry.get().strip()
        email = self.email_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        saldo_str = self.saldo_entry.get().strip()
        
        if not nama or not username or not password or not confirm_password:
            self.show_error("Semua field wajib diisi.")
            return
            
        if password != confirm_password:
            self.show_error("Password dan konfirmasi password tidak cocok.")
            return
            
        if len(password) < 6:
            self.show_error("Password minimal 6 karakter.")
            return
            
        saldo = 0
        if saldo_str:
            try:
                saldo = int(saldo_str)
                if saldo < 0:
                    self.show_error("Saldo tidak boleh negatif.")
                    return
            except ValueError:
                self.show_error("Saldo harus berupa angka.")
                return
                
        success, msg = auth.register_user(nama, username, email, password, saldo)
        if success:
            messagebox.showinfo("Sukses", msg)
            self.is_register_mode = False
            self.build_ui()
        else:
            self.show_error(msg)
