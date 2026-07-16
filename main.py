import os
import sys

# Ensure project root is in Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from src.models.database import init_db
from src.views.components import COLORS, FONTS, format_rupiah, CustomLabel, MutedLabel, PrimaryButton, SecondaryButton, DangerButton
from src.views import (
    LoginRegisterFrame, DashboardFrame, CreatePlanFrame, 
    PlanDetailContainerFrame, BudgetHealthScoreView, HistoryFrame, ProfileFrame,
    SplitBillDashboardFrame
)
from src.config import APP_TITLE, WINDOW_SIZE, MIN_WINDOW_SIZE
from src.controllers.auth_controller import AuthController as auth

class HangoutPlannerApp(ctk.CTk):
    """Main application manager for Hangout Planner Desktop App."""
    def __init__(self):
        super().__init__()
        
        # Configure app window
        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        self.minsize(*MIN_WINDOW_SIZE)
        
        # Center the window on screen
        self.center_window()
        
        # Global style
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color=COLORS["bg_main"])
        
        # Session State
        self.current_user = None
        self.active_frame = None
        self.sidebar_frame = None
        self.content_frame = None
        
        # Initialize DB
        init_db()
        
        # Handle clean window exit to prevent background thread callbacks from raising errors after window destruction
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start at login screen
        self.show_login_screen()
        
    def on_closing(self):
        self.withdraw()
        self.quit()
        self.destroy()
        
    def center_window(self):
        self.update_idletasks()
        width, height = map(int, WINDOW_SIZE.split('x'))
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def show_login_screen(self):
        # Reset session
        self.current_user = None
        
        # Clear main layouts
        if self.sidebar_frame:
            self.sidebar_frame.destroy()
            self.sidebar_frame = None
        if self.content_frame:
            self.content_frame.destroy()
            self.content_frame = None
            
        if self.active_frame:
            self.active_frame.destroy()
            
        # Grid full window weight
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)
        
        # Load login frame
        self.active_frame = LoginRegisterFrame(self, on_login_success=self.handle_login_success)
        self.active_frame.grid(row=0, column=0, sticky="nsew")

    def handle_login_success(self, user):
        self.current_user = user
        self.active_frame.destroy()
        self.active_frame = None
        
        # Configure layout with sidebar and content area
        self.grid_columnconfigure(0, weight=0)  # Sidebar (fixed)
        self.grid_columnconfigure(1, weight=1)  # Content (dynamic)
        self.grid_rowconfigure(0, weight=1)
        
        # Draw permanent layouts
        self.build_sidebar()
        
        # Content frame wrapper
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        
        # Switch to dashboard
        self.switch_view("dashboard")

    def build_sidebar(self):
        if self.sidebar_frame:
            self.sidebar_frame.destroy()
            
        self.sidebar_frame = ctk.CTkFrame(
            self, 
            width=220, 
            fg_color=COLORS["bg_card"], 
            corner_radius=0, 
            border_color="#1E293B", 
            border_width=1
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        # Title/Logo
        logo_frm = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        logo_frm.pack(fill="x", padx=20, pady=(30, 25))
        
        ctk.CTkLabel(logo_frm, text="🔵 Hangout Planner", font=("Segoe UI", 18, "bold"), text_color=COLORS["text_main"]).pack(anchor="w")
        MutedLabel(logo_frm, text="Budget Smart, Nongkrong Aman").pack(anchor="w")
        
        # Separator line
        ctk.CTkFrame(self.sidebar_frame, height=1, fg_color="#1E293B").pack(fill="x", padx=15, pady=(0, 20))
        
        # Navigation Menu List
        self.nav_buttons = {}
        menus = [
            ("dashboard", "🏠  Dashboard", self.on_menu_dashboard),
            ("buat_rencana", "➕  Buat Rencana", self.on_menu_create_plan),
            ("split_bill_dashboard", "💸  Split Bill", self.on_menu_split_bill),
            ("riwayat", "📜  Riwayat Rencana", self.on_menu_history),
            ("profil", "👤  Profil & Akun", self.on_menu_profile)
        ]
        
        for view_name, label, cmd in menus:
            btn = ctk.CTkButton(
                self.sidebar_frame,
                text=label,
                anchor="w",
                font=FONTS["body_bold"],
                fg_color="transparent",
                text_color=COLORS["text_muted"],
                hover_color="#1E293B",
                corner_radius=6,
                height=36,
                command=cmd
            )
            btn.pack(fill="x", padx=15, pady=4)
            self.nav_buttons[view_name] = btn
            
        # Bottom area spacer
        spacer = ctk.CTkLabel(self.sidebar_frame, text="", fg_color="transparent")
        spacer.pack(fill="both", expand=True)
        
        # User details card at bottom
        user_card = ctk.CTkFrame(self.sidebar_frame, fg_color="#1E293B", corner_radius=8)
        user_card.pack(fill="x", padx=15, pady=(10, 20))
        
        self.side_name_lbl = CustomLabel(user_card, text=self.current_user['nama'], font=FONTS["caption_bold"])
        self.side_name_lbl.pack(anchor="w", padx=12, pady=(10, 2))
        
        self.side_saldo_lbl = CustomLabel(user_card, text=format_rupiah(self.current_user['saldo']), font=FONTS["caption_bold"], text_color=COLORS["success"])
        self.side_saldo_lbl.pack(anchor="w", padx=12, pady=(0, 10))

    def update_sidebar_saldo(self):
        if self.current_user:
            updated_user = auth.get_user_by_id(self.current_user['id'])
            if updated_user:
                self.current_user = updated_user
                if hasattr(self, 'side_saldo_lbl') and self.side_saldo_lbl:
                    self.side_saldo_lbl.configure(text=format_rupiah(updated_user['saldo']))

    def set_active_menu(self, active_view):
        for view_name, btn in self.nav_buttons.items():
            if view_name == active_view:
                btn.configure(fg_color=COLORS["primary"], text_color=COLORS["text_main"])
            else:
                btn.configure(fg_color="transparent", text_color=COLORS["text_muted"])

    # Sidebar Menu handlers
    def on_menu_dashboard(self):
        self.switch_view("dashboard")
        
    def on_menu_create_plan(self):
        self.switch_view("buat_rencana")
        
    def on_menu_split_bill(self):
        self.switch_view("split_bill_dashboard")
        
    def on_menu_history(self):
        self.switch_view("riwayat")
        
    def on_menu_profile(self):
        self.switch_view("profil")

    def handle_logout(self):
        if messagebox.askyesno("Keluar Akun", "Apakah Anda yakin ingin keluar dari aplikasi?"):
            self.show_login_screen()

    def switch_view(self, view_name, context_id=None):
        # Update sidebar saldo on any view navigation to keep it synchronized
        self.update_sidebar_saldo()
        
        # Determine back view for detail view
        back_view = "dashboard"
        if hasattr(self, "current_view_name") and self.current_view_name in ["dashboard", "riwayat", "split_bill_dashboard"]:
            back_view = self.current_view_name
            
        # Update current view name
        self.current_view_name = view_name
        
        # Destroy current active view in content area
        if self.active_frame:
            self.active_frame.destroy()
            self.active_frame = None
            
        # Highlight active menu if it is a main sidebar view
        if view_name in self.nav_buttons:
            self.set_active_menu(view_name)
        else:
            # Plan detail or health score detail (sub-views) - clear highlights
            for btn in self.nav_buttons.values():
                btn.configure(fg_color="transparent", text_color=COLORS["text_muted"])
                
        # Load new frame
        if view_name == "dashboard":
            self.active_frame = DashboardFrame(self.content_frame, self.current_user, self.switch_view)
            
        elif view_name == "buat_rencana":
            self.active_frame = CreatePlanFrame(self.content_frame, self.current_user, self.switch_view)
            
        elif view_name == "detail_rencana":
            if isinstance(context_id, tuple):
                plan_id, initial_tab = context_id
            else:
                plan_id, initial_tab = context_id, "info"
            self.active_frame = PlanDetailContainerFrame(self.content_frame, plan_id, self.current_user, self.switch_view, back_view, initial_tab)
            
        elif view_name == "split_bill_dashboard":
            self.active_frame = SplitBillDashboardFrame(self.content_frame, self.current_user, self.switch_view, context_id)
            
        elif view_name == "detail_score":
            self.active_frame = BudgetHealthScoreView(self.content_frame, self.current_user, context_id)
            
        elif view_name == "riwayat":
            self.active_frame = HistoryFrame(self.content_frame, self.current_user, self.switch_view)
            
        elif view_name == "profil":
            self.active_frame = ProfileFrame(
                self.content_frame, 
                self.current_user, 
                on_logout_callback=self.handle_logout,
                reload_main_sidebar=self.update_sidebar_saldo
            )
            
        if self.active_frame:
            self.active_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = HangoutPlannerApp()
    app.mainloop()
