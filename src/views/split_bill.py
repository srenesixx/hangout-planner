import tkinter as tk
import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
from src.components import (
    COLORS, FONTS, format_rupiah, CardFrame, 
    PrimaryButton, SecondaryButton, SuccessButton, CustomLabel, HeaderLabel, MutedLabel, SubtitleLabel
)
import src.planner as planner

class SplitBillDashboardFrame(ctk.CTkFrame):
    """View displaying global split bill management (F5/sidebar)."""
    def __init__(self, master, user, switch_view_callback, initial_plan_id=None):
        super().__init__(master, fg_color=COLORS["bg_main"])
        self.user = user
        self.switch_view = switch_view_callback
        self.active_plan_id = initial_plan_id
        
        if initial_plan_id:
            self.show_detail_view(initial_plan_id)
        else:
            self.show_list_view()
            
    def show_list_view(self):
        # Clear frame
        for widget in self.winfo_children():
            widget.destroy()        
        self.active_plan_id = None

        # 1. Header Section
        self.hdr_frm = ctk.CTkFrame(self, fg_color="transparent")
        self.hdr_frm.pack(fill="x", padx=30, pady=(25, 15))
        
        HeaderLabel(self.hdr_frm, text="Manajemen Split Bill").pack(anchor="w")
        MutedLabel(self.hdr_frm, text="Pantau tagihan bersama dan status pelunasan teman nongkrongmu").pack(anchor="w")
        
        # 2. Stats Dashboard Cards (Grid layout)
        self.stats_container = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_container.pack(fill="x", padx=30, pady=(0, 15))
        
        # Stat 1: Total Tagihan Bersama
        self.card_total = CardFrame(self.stats_container)
        self.card_total.pack(side="left", fill="both", expand=True, padx=(0, 10))
        MutedLabel(self.card_total, text="TOTAL TAGIHAN BERSAMA", font=FONTS["caption_bold"]).pack(anchor="w", padx=15, pady=(12, 2))
        self.total_tagihan_lbl = CustomLabel(self.card_total, text="Rp 0", font=("Segoe UI", 20, "bold"), text_color=COLORS["primary"])
        self.total_tagihan_lbl.pack(anchor="w", padx=15, pady=(0, 12))
        
        # Stat 2: Total Piutang (Belum Bayar)
        self.card_piutang = CardFrame(self.stats_container)
        self.card_piutang.pack(side="left", fill="both", expand=True, padx=10)
        MutedLabel(self.card_piutang, text="PIUTANG TEMAN (BELUM LUNAS)", font=FONTS["caption_bold"]).pack(anchor="w", padx=15, pady=(12, 2))
        self.total_piutang_lbl = CustomLabel(self.card_piutang, text="Rp 0", font=("Segoe UI", 20, "bold"), text_color=COLORS["danger"])
        self.total_piutang_lbl.pack(anchor="w", padx=15, pady=(0, 12))
        
        # Stat 3: Rencana Aktif dengan Teman
        self.card_rencana = CardFrame(self.stats_container)
        self.card_rencana.pack(side="left", fill="both", expand=True, padx=(10, 0))
        MutedLabel(self.card_rencana, text="RENCANA HANGOUT GRUP", font=FONTS["caption_bold"]).pack(anchor="w", padx=15, pady=(12, 2))
        self.total_plans_lbl = CustomLabel(self.card_rencana, text="0 Rencana", font=("Segoe UI", 20, "bold"), text_color=COLORS["success"])
        self.total_plans_lbl.pack(anchor="w", padx=15, pady=(0, 12))
        
        # 3. Main List Card
        self.list_card = CardFrame(self)
        self.list_card.pack(fill="both", expand=True, padx=30, pady=(10, 30))
        
        list_header_frm = ctk.CTkFrame(self.list_card, fg_color="transparent")
        list_header_frm.pack(fill="x", padx=20, pady=(20, 10))
        SubtitleLabel(list_header_frm, text="Daftar Rincian Rencana & Pelunasan").pack(side="left")
        
        # Scrollable table container
        self.scroll_table = ctk.CTkScrollableFrame(
            self.list_card,
            fg_color="transparent",
            border_color="#1E293B",
            border_width=0
        )
        self.scroll_table.pack(fill="both", expand=True, padx=10, pady=(0, 15))
        
        self.load_data()
        
    def load_data(self):
        plans = planner.get_user_split_bills(self.user['id'])
        
        total_tagihan = 0
        total_piutang = 0
        plans_count = len(plans)
        
        if not plans:
            self.total_tagihan_lbl.configure(text="Rp 0")
            self.total_piutang_lbl.configure(text="Rp 0")
            self.total_plans_lbl.configure(text="0 Rencana")
            MutedLabel(self.scroll_table, text="Tidak ada rencana nongkrong dengan teman (grup).").pack(pady=60)
            return
            
        # Draw header row for table
        w_nama = 180
        w_tgl = 100
        w_tagihan = 120
        w_pembagian = 120
        w_status = 150
        w_aksi = 80
        
        tbl_hdr = ctk.CTkFrame(self.scroll_table, fg_color="#13203A")
        tbl_hdr.pack(fill="x", pady=(0, 6), ipady=4)
        
        CustomLabel(tbl_hdr, text="NAMA RENCANA", font=FONTS["caption_bold"], width=w_nama, anchor="w").pack(side="left", padx=10)
        CustomLabel(tbl_hdr, text="TANGGAL", font=FONTS["caption_bold"], width=w_tgl, anchor="w").pack(side="left", padx=5)
        CustomLabel(tbl_hdr, text="TOTAL TAGIHAN", font=FONTS["caption_bold"], width=w_tagihan, anchor="w").pack(side="left", padx=5)
        CustomLabel(tbl_hdr, text="BAGI PER ORANG", font=FONTS["caption_bold"], width=w_pembagian, anchor="w").pack(side="left", padx=5)
        CustomLabel(tbl_hdr, text="PELUNASAN TEMAN", font=FONTS["caption_bold"], width=w_status, anchor="w").pack(side="left", padx=5)
        CustomLabel(tbl_hdr, text="AKSI", font=FONTS["caption_bold"], width=w_aksi, anchor="w").pack(side="left", padx=5)
        
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
            
            sb = plan['split_bill']
            if sb:
                total_tagihan += sb['total_tagihan']
                txt_tagihan = format_rupiah(sb['total_tagihan'])
                txt_pembagian = format_rupiah(sb['per_orang'])
                
                saved_checklist = planner.get_split_bill_checklist(plan['id'])
                num_friends = plan['jumlah_teman']
                
                paid_count = sum(1 for item in saved_checklist if item.get("paid", False))
                unpaid_count = num_friends - paid_count
                
                total_piutang += unpaid_count * sb['per_orang']
                
                txt_status = f"{paid_count} / {num_friends} Lunas"
                status_color = COLORS["success"] if paid_count == num_friends else COLORS["primary"]
            else:
                txt_tagihan = "Belum diatur"
                txt_pembagian = "-"
                txt_status = "Kalkulasi Kosong"
                status_color = COLORS["text_muted"]
                
            CustomLabel(row_frm, text=txt_tagihan, font=FONTS["body"], width=w_tagihan, anchor="w").pack(side="left", padx=5)
            CustomLabel(row_frm, text=txt_pembagian, font=FONTS["body_bold"], text_color=COLORS["success"] if sb else COLORS["text_main"], width=w_pembagian, anchor="w").pack(side="left", padx=5)
            CustomLabel(row_frm, text=txt_status, font=FONTS["body_bold"], text_color=status_color, width=w_status, anchor="w").pack(side="left", padx=5)
            
            pid = plan['id']
            PrimaryButton(row_frm, text="Kelola", width=w_aksi, height=24, font=FONTS["caption_bold"],
                          command=lambda p_id=pid: self.show_detail_view(p_id)).pack(side="left", padx=5)
            
        self.total_tagihan_lbl.configure(text=format_rupiah(total_tagihan))
        self.total_piutang_lbl.configure(text=format_rupiah(total_piutang))
        self.total_plans_lbl.configure(text=f"{plans_count} Rencana")

    def show_detail_view(self, plan_id):
        self.active_plan_id = plan_id
        
        # Clear main container
        for widget in self.winfo_children():
            widget.destroy()
            
        # Top Bar
        top_frm = ctk.CTkFrame(self, fg_color="transparent")
        top_frm.pack(fill="x", padx=30, pady=(20, 10))
        
        SecondaryButton(top_frm, text="← Kembali ke Daftar", width=140, height=28, command=self.show_list_view).pack(side="left", padx=(0, 15))
        self.detail_title_lbl = HeaderLabel(top_frm, text="Memuat Rencana...")
        self.detail_title_lbl.pack(side="left")
        
        # Main 2-column container
        self.detail_container = ctk.CTkFrame(self, fg_color="transparent")
        self.detail_container.pack(fill="both", expand=True, padx=30, pady=(10, 20))
        
        # Left Panel: Locations & Expenses
        self.left_panel = CardFrame(self.detail_container)
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        SubtitleLabel(self.left_panel, text="Rincian Pengeluaran & Tempat").pack(pady=(15, 2), padx=20, anchor="w")
        MutedLabel(self.left_panel, text="Tempat nongkrong yang dikunjungi beserta rincian item pengeluaran").pack(pady=(0, 10), padx=20, anchor="w")
        
        self.expenses_scroll = ctk.CTkScrollableFrame(self.left_panel, fg_color="transparent")
        self.expenses_scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Right Panel: Checklist Status
        self.right_panel = CardFrame(self.detail_container, width=380)
        self.right_panel.pack(side="right", fill="both", padx=(15, 0))
        
        SubtitleLabel(self.right_panel, text="Status Pelunasan Teman").pack(pady=(15, 2), padx=20, anchor="w")
        self.desc_lbl = MutedLabel(self.right_panel, text="Status pelunasan dari masing-masing teman")
        self.desc_lbl.pack(pady=(0, 10), padx=20, anchor="w")
        
        self.checklist_scroll = ctk.CTkScrollableFrame(self.right_panel, fg_color="transparent", height=180)
        self.checklist_scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.save_checklist_btn = PrimaryButton(self.right_panel, text="Simpan Status Pelunasan", command=self.save_checklist)
        self.save_checklist_btn.pack(pady=(0, 20), padx=20, fill="x")
        
        self.load_detail_data(plan_id)

    def load_detail_data(self, plan_id):
        plan = planner.get_plan_details(plan_id)
        if not plan:
            return
            
        self.plan_data = plan
        p_name = plan['nama_rencana'] if plan['nama_rencana'] else f"Rencana #{plan['id']}"
        self.detail_title_lbl.configure(text=f"Detail Split Bill: {p_name}")
        
        # Clear left scrollable area
        for widget in self.expenses_scroll.winfo_children():
            widget.destroy()
            
        # Draw locations and items
        locations = plan.get('locations', [])
        if not locations:
            MutedLabel(self.expenses_scroll, text="Tidak ada estimasi tempat/item untuk rencana ini.").pack(pady=40)
        else:
            for loc in locations:
                loc_frm = ctk.CTkFrame(self.expenses_scroll, fg_color="#1E293B", corner_radius=8)
                loc_frm.pack(fill="x", pady=6, ipady=6)
                
                # Location Header
                CustomLabel(loc_frm, text=f"📍 {loc['nama_tempat']}", font=FONTS["body_bold"], text_color=COLORS["primary"]).pack(anchor="w", padx=12, pady=4)
                
                # Items list
                for item in loc['items']:
                    item_frm = ctk.CTkFrame(loc_frm, fg_color="transparent")
                    item_frm.pack(fill="x", padx=20, pady=2)
                    
                    item_text = f"• {item['nama_item']} ({item['jumlah']}x)"
                    CustomLabel(item_frm, text=item_text, font=FONTS["caption"]).pack(side="left")
                    
                    sub = item['harga_satuan'] * item['jumlah']
                    CustomLabel(item_frm, text=format_rupiah(sub), font=FONTS["caption_bold"], text_color=COLORS["success"]).pack(side="right")
                    
                # Subtotal location
                ctk.CTkFrame(loc_frm, height=1, fg_color="#334155").pack(fill="x", padx=15, pady=6)
                sub_frm = ctk.CTkFrame(loc_frm, fg_color="transparent")
                sub_frm.pack(fill="x", padx=15)
                CustomLabel(sub_frm, text="Subtotal Tempat:", font=FONTS["caption_bold"]).pack(side="left")
                CustomLabel(sub_frm, text=format_rupiah(loc['subtotal']), font=FONTS["caption_bold"], text_color=COLORS["primary"]).pack(side="right")
                
        # Transport Expense
        trans_frm = ctk.CTkFrame(self.expenses_scroll, fg_color="#1E293B", corner_radius=8)
        trans_frm.pack(fill="x", pady=6, ipady=6)
        CustomLabel(trans_frm, text="🚗 Transportasi", font=FONTS["body_bold"], text_color=COLORS["primary"]).pack(anchor="w", padx=12, pady=4)
        
        t_mode = plan['transportasi'] if plan['transportasi'] else "Tidak ditentukan"
        t_cost = plan['transport_cost']
        
        trans_item_frm = ctk.CTkFrame(trans_frm, fg_color="transparent")
        trans_item_frm.pack(fill="x", padx=20)
        CustomLabel(trans_item_frm, text=f"Metode: {t_mode}", font=FONTS["caption"]).pack(side="left")
        CustomLabel(trans_item_frm, text=format_rupiah(t_cost), font=FONTS["caption_bold"], text_color=COLORS["success"]).pack(side="right")
        
        # Summary estimation cost
        total_frm = ctk.CTkFrame(self.expenses_scroll, fg_color="transparent")
        total_frm.pack(fill="x", pady=(15, 0))
        CustomLabel(total_frm, text="TOTAL ESTIMASI PENGELUARAN:", font=FONTS["body_bold"]).pack(side="left")
        CustomLabel(total_frm, text=format_rupiah(plan['total_cost']), font=FONTS["body_bold"], text_color=COLORS["success"]).pack(side="right")
        
        # 2. Populate Checklist Right Panel
        self.load_checklist()

    def load_checklist(self):
        for widget in self.checklist_scroll.winfo_children():
            widget.destroy()
            
        plan = self.plan_data
        num_friends = plan['jumlah_teman']
        
        if num_friends == 0:
            MutedLabel(self.checklist_scroll, text="Solo Hangout:\nSeluruh tagihan ditanggung sendiri.").pack(pady=40)
            self.save_checklist_btn.configure(state="disabled")
            return
            
        self.save_checklist_btn.configure(state="normal")
        
        saved_checklist = planner.get_split_bill_checklist(plan['id'])
        
        sb = plan['split_bill']
        if sb:
            total = sb['total_tagihan']
            people = sb['jumlah_orang']
            per_person = sb['per_orang']
            self.desc_lbl.configure(text=f"Total: {format_rupiah(total)} / {people} orang = {format_rupiah(per_person)} per orang")
        else:
            total = plan['total_cost']
            people = num_friends + 1
            per_person = int(round(total / people))
            self.desc_lbl.configure(text=f"Estimasi: {format_rupiah(total)} / {people} orang = {format_rupiah(per_person)} per orang\n(Kalkulasi belum disimpan)")
            
        self.checkbox_vars = []
        for i in range(1, num_friends + 1):
            friend_name = f"Teman #{i}"
            
            is_paid = False
            for item in saved_checklist:
                if item.get("name") == friend_name:
                    is_paid = item.get("paid", False)
                    break
                    
            row_frm = ctk.CTkFrame(self.checklist_scroll, fg_color="transparent")
            row_frm.pack(fill="x", pady=4)
            
            CustomLabel(row_frm, text=friend_name, font=FONTS["body_bold"]).pack(side="left", padx=5)
            CustomLabel(row_frm, text=f"({format_rupiah(per_person)})", font=FONTS["caption"], text_color=COLORS["text_muted"]).pack(side="left", padx=5)
            
            cb_var = tk.BooleanVar(value=is_paid)
            cb = ctk.CTkCheckBox(
                row_frm,
                text="Lunas",
                variable=cb_var,
                fg_color=COLORS["success"],
                hover_color=COLORS["success"],
                font=FONTS["caption_bold"],
                text_color=COLORS["text_main"],
                checkbox_width=20,
                checkbox_height=20,
                corner_radius=4
            )
            cb.pack(side="right", padx=5)
            self.checkbox_vars.append((friend_name, cb_var))

    def save_checklist(self):
        checklist = []
        for friend_name, var in self.checkbox_vars:
            checklist.append({
                "name": friend_name,
                "paid": var.get()
            })
            
        if planner.save_split_bill_checklist(self.active_plan_id, checklist):
            messagebox.showinfo("Sukses", "Status pelunasan berhasil disimpan!")
            self.load_detail_data(self.active_plan_id)
        else:
            messagebox.showerror("Error", "Gagal menyimpan status pelunasan.")
