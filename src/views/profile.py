import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from src.views.components import (
    COLORS, FONTS, format_rupiah,
    CardFrame, PrimaryButton, SecondaryButton, DangerButton, SuccessButton,
    CustomEntry, CustomLabel, HeaderLabel, MutedLabel, SubtitleLabel
)
from src.controllers.auth_controller import AuthController as auth

class ProfileFrame(ctk.CTkFrame):
    """Profile & settings options page (F10)."""
    def __init__(self, master, user, on_logout_callback, reload_main_sidebar):
        super().__init__(master, fg_color=COLORS["bg_main"])
        self.user = user
        self.on_logout = on_logout_callback
        self.reload_sidebar = reload_main_sidebar
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.build_ui()
        self.load_profile_details()
        
    def build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, padx=30, pady=(25, 10), sticky="ew")
        HeaderLabel(header, text="Manajemen Profil").pack(side="left")
        MutedLabel(header, text="Perbarui saldo akun atau ubah password keamanan").pack(side="left", padx=20, pady=8)
        
        # 1. Left Card: Saldo Update / Top Up
        self.card_saldo = CardFrame(self)
        self.card_saldo.grid(row=1, column=0, padx=(30, 15), pady=15, sticky="nsew")
        
        SubtitleLabel(self.card_saldo, text="Informasi & Top Up Saldo").pack(anchor="w", padx=20, pady=(15, 5))
        MutedLabel(self.card_saldo, text="Kelola total saldo aktif dompet Anda").pack(anchor="w", padx=20, pady=(0, 20))
        
        # Data rows
        info_row1 = ctk.CTkFrame(self.card_saldo, fg_color="transparent")
        info_row1.pack(fill="x", padx=20, pady=6)
        MutedLabel(info_row1, text="Nama Pengguna:").pack(side="left")
        self.nama_lbl = CustomLabel(info_row1, text="-", font=FONTS["body_bold"])
        self.nama_lbl.pack(side="right")
        
        info_row2 = ctk.CTkFrame(self.card_saldo, fg_color="transparent")
        info_row2.pack(fill="x", padx=20, pady=6)
        MutedLabel(info_row2, text="Username:").pack(side="left")
        self.username_lbl = CustomLabel(info_row2, text="-", font=FONTS["body_bold"])
        self.username_lbl.pack(side="right")
        
        info_row3 = ctk.CTkFrame(self.card_saldo, fg_color="transparent")
        info_row3.pack(fill="x", padx=20, pady=6)
        MutedLabel(info_row3, text="Email:").pack(side="left")
        self.email_lbl = CustomLabel(info_row3, text="-", font=FONTS["body_bold"])
        self.email_lbl.pack(side="right")
        
        info_row4 = ctk.CTkFrame(self.card_saldo, fg_color="transparent")
        info_row4.pack(fill="x", padx=20, pady=(6, 20))
        MutedLabel(info_row4, text="Saldo Aktif Saat Ini:").pack(side="left")
        self.saldo_lbl = CustomLabel(info_row4, text="Rp 0", font=FONTS["subtitle"], text_color=COLORS["success"])
        self.saldo_lbl.pack(side="right")
        
        # Top-up form
        self.topup_frm = ctk.CTkFrame(self.card_saldo, fg_color="transparent")
        self.topup_frm.pack(fill="x", padx=20, pady=10)
        
        CustomLabel(self.topup_frm, text="Nominal Top-up / Set Saldo Baru (Rp)", font=FONTS["body_bold"]).pack(anchor="w", pady=(0, 4))
        self.saldo_input = CustomEntry(self.topup_frm, placeholder_text="Masukkan nominal saldo baru (misal: 1000000)")
        self.saldo_input.pack(fill="x", pady=(0, 12))
        
        # Action Buttons
        self.save_saldo_btn = SuccessButton(self.card_saldo, text="Perbarui Saldo", command=self.handle_saldo_update)
        self.save_saldo_btn.pack(pady=(5, 20), padx=20, fill="x")
        
        # 2. Right Card: Password Update
        self.card_pwd = CardFrame(self)
        self.card_pwd.grid(row=1, column=1, padx=(15, 30), pady=15, sticky="nsew")
        
        SubtitleLabel(self.card_pwd, text="Ubah Password").pack(anchor="w", padx=20, pady=(15, 5))
        MutedLabel(self.card_pwd, text="Ubah password Anda untuk menjaga keamanan data lokal").pack(anchor="w", padx=20, pady=(0, 20))
        
        self.pwd_frm = ctk.CTkFrame(self.card_pwd, fg_color="transparent")
        self.pwd_frm.pack(fill="x", padx=20, pady=10)
        
        CustomLabel(self.pwd_frm, text="Password Lama", font=FONTS["body_bold"]).pack(anchor="w", pady=(0, 4))
        self.old_pwd_input = CustomEntry(self.pwd_frm, placeholder_text="Masukkan password saat ini", show="*")
        self.old_pwd_input.pack(fill="x", pady=(0, 12))
        
        CustomLabel(self.pwd_frm, text="Password Baru", font=FONTS["body_bold"]).pack(anchor="w", pady=(0, 4))
        self.new_pwd_input = CustomEntry(self.pwd_frm, placeholder_text="Minimal 6 karakter", show="*")
        self.new_pwd_input.pack(fill="x", pady=(0, 12))
        
        self.change_pwd_btn = PrimaryButton(self.card_pwd, text="Simpan Password Baru", command=self.handle_password_change)
        self.change_pwd_btn.pack(pady=(5, 10), padx=20, fill="x")
        
        # Log out frame at bottom
        self.logout_btn = DangerButton(self.card_pwd, text="Keluar Akun (Log Out)", command=self.on_logout)
        self.logout_btn.pack(pady=(10, 20), padx=20, fill="x")

    def load_profile_details(self):
        user_info = auth.get_user_by_id(self.user['id'])
        if not user_info:
            return
            
        self.user = user_info
        
        self.nama_lbl.configure(text=user_info['nama'])
        self.username_lbl.configure(text=user_info['username'])
        self.email_lbl.configure(text=user_info['email'] if user_info['email'] else "-")
        self.saldo_lbl.configure(text=format_rupiah(user_info['saldo']))

    def handle_saldo_update(self):
        val_str = self.saldo_input.get().strip()
        if not val_str:
            messagebox.showerror("Error", "Nominal saldo wajib diisi.")
            return
            
        try:
            val = int(val_str)
            if val < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Nominal saldo harus berupa angka bulat positif.")
            return
            
        success = auth.update_saldo(self.user['id'], val)
        if success:
            messagebox.showinfo("Sukses", "Saldo berhasil diperbarui!")
            self.saldo_input.delete(0, tk.END)
            self.load_profile_details()
            self.reload_sidebar()
        else:
            messagebox.showerror("Error", "Gagal memperbarui saldo.")

    def handle_password_change(self):
        old_pwd = self.old_pwd_input.get()
        new_pwd = self.new_pwd_input.get()
        
        if not old_pwd or not new_pwd:
            messagebox.showerror("Error", "Seluruh password form wajib diisi.")
            return
            
        success, msg = auth.change_password(self.user['id'], old_pwd, new_pwd)
        if success:
            messagebox.showinfo("Sukses", msg)
            self.old_pwd_input.delete(0, tk.END)
            self.new_pwd_input.delete(0, tk.END)
        else:
            messagebox.showerror("Error", msg)
