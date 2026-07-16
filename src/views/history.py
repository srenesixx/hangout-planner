from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox

from src.views.components import (
    COLORS, FONTS, format_rupiah,
    CardFrame, PrimaryButton, SecondaryButton, SuccessButton, DangerButton,
    CustomLabel, HeaderLabel, MutedLabel
)
from src.controllers.planner_controller import PlannerController as planner

class HistoryFrame(ctk.CTkFrame):
    """View displaying historical hangout plans (F10)."""
    def __init__(self, master, user, switch_view_callback):
        super().__init__(master, fg_color=COLORS["bg_main"])
        self.user = user
        self.switch_view = switch_view_callback
        self.current_filter = None
        
        self.build_ui()
        self.load_history()
        
    def build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(25, 10))
        HeaderLabel(header, text="Riwayat Rencana Nongkrong").pack(side="left")
        MutedLabel(header, text="Daftar semua rencana hangout yang sudah lewat atau sedang dirancang").pack(side="left", padx=20, pady=8)
        
        # Filter buttons frame
        self.filter_frm = ctk.CTkFrame(self, fg_color="transparent")
        self.filter_frm.pack(fill="x", padx=30, pady=5)
        
        self.filter_all_btn = PrimaryButton(self.filter_frm, text="Semua", width=70, height=28, command=lambda: self.apply_filter(None))
        self.filter_all_btn.pack(side="left", padx=(0, 8))
        
        self.filter_draft_btn = SecondaryButton(self.filter_frm, text="Draft", width=70, height=28, command=lambda: self.apply_filter("draft"))
        self.filter_draft_btn.pack(side="left", padx=8)
        
        self.filter_selesai_btn = SecondaryButton(self.filter_frm, text="Selesai", width=70, height=28, command=lambda: self.apply_filter("selesai"))
        self.filter_selesai_btn.pack(side="left", padx=8)
        
        self.filter_cancel_btn = SecondaryButton(self.filter_frm, text="Dibatalkan", width=80, height=28, command=lambda: self.apply_filter("dibatalkan"))
        self.filter_cancel_btn.pack(side="left", padx=8)
        
        # Main table container card
        self.table_card = CardFrame(self)
        self.table_card.pack(fill="both", expand=True, padx=30, pady=(10, 30))
        
        # Scrollable table container
        self.scroll_table = ctk.CTkScrollableFrame(self.table_card, fg_color="transparent")
        self.scroll_table.pack(fill="both", expand=True, padx=10, pady=10)

    def load_history(self, filter_status=None):
        # Clear existing
        for widget in self.scroll_table.winfo_children():
            widget.destroy()
            
        plans = planner.get_user_plans(self.user['id'], filter_status)
        
        if not plans:
            MutedLabel(self.scroll_table, text="Tidak ada rencana yang cocok dengan filter ini.").pack(pady=40)
            return
            
        # Columns widths configuration
        w_nama = 150
        w_tgl = 100
        w_teman = 80
        w_budget = 100
        w_biaya = 100
        w_status = 100
        w_aksi = 75
        
        # Draw header row for table
        tbl_hdr = ctk.CTkFrame(self.scroll_table, fg_color="#13203A")
        tbl_hdr.pack(fill="x", pady=(0, 6), ipady=4)
        
        CustomLabel(tbl_hdr, text="NAMA RENCANA", font=FONTS["caption_bold"], width=w_nama, anchor="w").pack(side="left", padx=10)
        CustomLabel(tbl_hdr, text="TANGGAL", font=FONTS["caption_bold"], width=w_tgl, anchor="w").pack(side="left", padx=5)
        CustomLabel(tbl_hdr, text="TEMAN", font=FONTS["caption_bold"], width=w_teman, anchor="w").pack(side="left", padx=5)
        CustomLabel(tbl_hdr, text="BUDGET", font=FONTS["caption_bold"], width=w_budget, anchor="w").pack(side="left", padx=5)
        CustomLabel(tbl_hdr, text="TOTAL BIAYA", font=FONTS["caption_bold"], width=w_biaya, anchor="w").pack(side="left", padx=5)
        CustomLabel(tbl_hdr, text="STATUS", font=FONTS["caption_bold"], width=w_status, anchor="w").pack(side="left", padx=5)
        CustomLabel(tbl_hdr, text="AKSI", font=FONTS["caption_bold"], width=w_aksi, anchor="w").pack(side="left", padx=5)
        
        # Draw data rows
        for idx, plan in enumerate(plans):
            row_bg = "#1E293B" if idx % 2 == 0 else "transparent"
            row_frm = ctk.CTkFrame(self.scroll_table, fg_color=row_bg, corner_radius=6)
            row_frm.pack(fill="x", pady=2, ipady=6)
            
            p_name = plan['nama_rencana'] if plan['nama_rencana'] else f"Rencana #{plan['id']}"
            CustomLabel(row_frm, text=p_name, font=FONTS["body_bold"], width=w_nama, anchor="w").pack(side="left", padx=10)
            
            # Format date
            date_obj = datetime.strptime(plan['tanggal'], "%Y-%m-%d")
            formatted_date = date_obj.strftime("%d %b %Y")
            CustomLabel(row_frm, text=formatted_date, font=FONTS["body"], width=w_tgl, anchor="w").pack(side="left", padx=5)
            
            # Friends
            friends_text = "Solo" if plan['jumlah_teman'] == 0 else f"{plan['jumlah_teman']} Teman"
            CustomLabel(row_frm, text=friends_text, font=FONTS["body"], width=w_teman, anchor="w").pack(side="left", padx=5)
            
            # Budget
            CustomLabel(row_frm, text=format_rupiah(plan['budget']), font=FONTS["body"], width=w_budget, anchor="w").pack(side="left", padx=5)
            
            # Total Cost
            cost_color = COLORS["text_main"]
            if plan['total_cost'] > plan['budget']:
                cost_color = COLORS["danger"]
            CustomLabel(row_frm, text=format_rupiah(plan['total_cost']), font=FONTS["body_bold"], text_color=cost_color, width=w_biaya, anchor="w").pack(side="left", padx=5)
            
            # Status Dropdown
            status_var = plan['status'].capitalize()
            status_dropdown = ctk.CTkComboBox(
                row_frm,
                values=["Draft", "Selesai", "Dibatalkan"],
                width=w_status, height=24,
                fg_color=COLORS["bg_main"],
                text_color=COLORS["text_main"],
                border_color="#334155",
                font=FONTS["caption_bold"],
                command=lambda val, p_id=plan['id']: self.change_plan_status_dropdown(p_id, val)
            )
            status_dropdown.set(status_var)
            status_dropdown.pack(side="left", padx=5)
            
            # Action button
            pid = plan['id']
            PrimaryButton(row_frm, text="Detail", width=w_aksi, height=24, font=FONTS["caption_bold"],
                          command=lambda p_id=pid: self.switch_view("detail_rencana", p_id)).pack(side="left", padx=5)

    def change_plan_status_dropdown(self, plan_id, val):
        status_db = val.lower()
        if planner.update_plan_status(plan_id, status_db):
            messagebox.showinfo("Sukses", f"Status rencana berhasil diubah menjadi '{val}'.")
            self.load_history(self.current_filter)
        else:
            messagebox.showerror("Error", "Gagal memperbarui status rencana.")

    def apply_filter(self, status):
        self.current_filter = status
        # Configure filters visual active state
        self.filter_all_btn.configure(fg_color="transparent", text_color=COLORS["primary"], border_color=COLORS["primary"])
        self.filter_draft_btn.configure(fg_color="transparent", text_color=COLORS["primary"], border_color=COLORS["primary"])
        self.filter_selesai_btn.configure(fg_color="transparent", text_color=COLORS["primary"], border_color=COLORS["primary"])
        self.filter_cancel_btn.configure(fg_color="transparent", text_color=COLORS["primary"], border_color=COLORS["primary"])
        
        if status is None:
            self.filter_all_btn.configure(fg_color=COLORS["primary"], text_color=COLORS["text_main"])
        elif status == "draft":
            self.filter_draft_btn.configure(fg_color=COLORS["primary"], text_color=COLORS["text_main"])
        elif status == "selesai":
            self.filter_selesai_btn.configure(fg_color=COLORS["primary"], text_color=COLORS["text_main"])
        elif status == "dibatalkan":
            self.filter_cancel_btn.configure(fg_color=COLORS["primary"], text_color=COLORS["text_main"])
            
        self.load_history(status)
