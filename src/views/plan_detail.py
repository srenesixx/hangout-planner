from datetime import datetime
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from src.views.components import (
    COLORS, FONTS, format_rupiah,
    CardFrame, PrimaryButton, SecondaryButton, DangerButton, SuccessButton,
    CustomEntry, CustomLabel, HeaderLabel, MutedLabel, StatusLabel, SubtitleLabel
)
from src.controllers.planner_controller import PlannerController as planner
from src.controllers.auth_controller import AuthController as auth

class EstimateItemsView(ctk.CTkFrame):
    """Sub-view: item price estimator per location (F4)."""
    def __init__(self, master, plan_id, reload_parent):
        super().__init__(master, fg_color="transparent")
        self.plan_id = plan_id
        self.reload_parent = reload_parent
        
        self.locations_data = [] # stores dynamic inputs of locations and items
        
        self.build_ui()
        self.load_data()
        
    def build_ui(self):
        # Layout splits into details/inputs on top, list scrollable, totals at bottom
        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Bottom area for Totals & Action Buttons
        self.bottom_bar = CardFrame(self)
        self.bottom_bar.pack(fill="x", padx=10, pady=10, ipady=5)
        
        self.summary_lbl = CustomLabel(self.bottom_bar, text="Total Estimasi: Rp 0 / Budget: Rp 0", font=FONTS["subtitle"])
        self.summary_lbl.pack(side="left", padx=20, pady=10)
        
        self.warning_lbl = StatusLabel(self.bottom_bar, status_type="danger", text="⚠️ Pengeluaran melebihi budget!", font=FONTS["body_bold"])
        
        self.save_btn = SuccessButton(self.bottom_bar, text="Simpan Estimasi", command=self.save_all)
        self.save_btn.pack(side="right", padx=20, pady=10)
        
        # Add new location button at top of scroll
        self.add_loc_btn = SecondaryButton(self.scroll_container, text="+ Tambah Tempat Baru", command=self.add_location_widget)
        self.add_loc_btn.pack(anchor="w", padx=10, pady=10)

    def load_data(self):
        # Load from DB
        plan = planner.get_plan_details(self.plan_id)
        if not plan:
            return
            
        self.budget = plan['budget']
        self.transport_cost = plan['transport_cost']
        
        locs = plan['locations']
        if not locs:
            # Default add one empty location
            self.add_location_widget()
        else:
            for l in locs:
                loc_dict = {
                    'nama_tempat': l['nama_tempat'],
                    'kategori': l['kategori'],
                    'items': [{'nama_item': item['nama_item'], 'harga_satuan': item['harga_satuan'], 'jumlah': item['jumlah']} for item in l['items']]
                }
                self.add_location_widget(loc_dict)
                
        self.update_totals()

    def add_location_widget(self, data=None):
        loc_card = CardFrame(self.scroll_container)
        loc_card.pack(fill="x", pady=10, padx=10)
        
        # Location header inputs
        hdr_frame = ctk.CTkFrame(loc_card, fg_color="transparent")
        hdr_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        CustomLabel(hdr_frame, text="Nama Tempat:", font=FONTS["body_bold"]).pack(side="left", padx=(0, 5))
        loc_name_entry = CustomEntry(hdr_frame, placeholder_text="Contoh: Starbucks, McDonalds, Bioskop", width=180)
        loc_name_entry.pack(side="left", padx=(0, 15))
        
        CustomLabel(hdr_frame, text="Kategori:", font=FONTS["body_bold"]).pack(side="left", padx=(0, 5))
        cat_dropdown = ctk.CTkComboBox(
            hdr_frame,
            values=["Kafe", "Restoran/Makan", "Hiburan (Bioskop/Karaoke)", "Belanja", "Lainnya"],
            width=150,
            fg_color=COLORS["bg_main"],
            text_color=COLORS["text_main"],
            border_color="#334155",
            corner_radius=8
        )
        cat_dropdown.set("Kafe")
        cat_dropdown.pack(side="left")
        
        # Delete location button
        del_loc_btn = DangerButton(hdr_frame, text="Hapus Tempat", width=90, height=26, font=FONTS["caption_bold"],
                                   command=lambda: self.remove_location_widget(loc_card))
        del_loc_btn.pack(side="right")
        
        # Prepopulate data if loaded
        if data:
            loc_name_entry.insert(0, data['nama_tempat'])
            cat_dropdown.set(data['kategori'])
            
        # Items Area
        items_area = ctk.CTkFrame(loc_card, fg_color="transparent")
        items_area.pack(fill="x", padx=15, pady=5)
        
        # Header Row for Items
        item_hdr = ctk.CTkFrame(items_area, fg_color="transparent")
        item_hdr.pack(fill="x", pady=2)
        CustomLabel(item_hdr, text="Nama Item", font=FONTS["caption_bold"], width=180, anchor="w").pack(side="left", padx=2)
        CustomLabel(item_hdr, text="Harga Satuan (Rp)", font=FONTS["caption_bold"], width=110, anchor="w").pack(side="left", padx=2)
        CustomLabel(item_hdr, text="Jumlah", font=FONTS["caption_bold"], width=60, anchor="w").pack(side="left", padx=2)
        CustomLabel(item_hdr, text="Subtotal", font=FONTS["caption_bold"], width=100, anchor="w").pack(side="left", padx=2)
        
        items_list_frame = ctk.CTkFrame(items_area, fg_color="transparent")
        items_list_frame.pack(fill="x")
        
        # Add item button
        add_item_btn = SecondaryButton(loc_card, text="+ Tambah Item", width=110, height=26, font=FONTS["caption_bold"],
                                       command=lambda: self.add_item_row(items_list_frame))
        add_item_btn.pack(anchor="w", padx=15, pady=(5, 15))
        
        # Keep references in local structure
        loc_record = {
            'card': loc_card,
            'name_entry': loc_name_entry,
            'cat_dropdown': cat_dropdown,
            'items_frame': items_list_frame,
            'item_rows': []
        }
        self.locations_data.append(loc_record)
        
        # Load items if data available
        if data and data['items']:
            for item in data['items']:
                self.add_item_row(items_list_frame, item)
        else:
            # Default add one item row
            self.add_item_row(items_list_frame)
            
        # Bind focusout updates to recalculate total costs dynamically
        loc_name_entry.bind("<KeyRelease>", lambda e: self.update_totals())

    def remove_location_widget(self, card_widget):
        for idx, rec in enumerate(self.locations_data):
            if rec['card'] == card_widget:
                rec['card'].destroy()
                self.locations_data.pop(idx)
                break
        self.update_totals()

    def add_item_row(self, list_frame, item_data=None):
        row_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        row_frame.pack(fill="x", pady=2)
        
        item_entry = CustomEntry(row_frame, placeholder_text="Contoh: Kopi Susu, Nasi Goreng, Tiket", width=180)
        item_entry.pack(side="left", padx=2)
        
        price_entry = CustomEntry(row_frame, placeholder_text="Harga Satuan", width=110)
        price_entry.pack(side="left", padx=2)
        
        qty_entry = CustomEntry(row_frame, placeholder_text="Qty", width=60)
        qty_entry.pack(side="left", padx=2)
        
        subtotal_lbl = CustomLabel(row_frame, text="Rp 0", font=FONTS["body_bold"], width=100, anchor="w")
        subtotal_lbl.pack(side="left", padx=2)
        
        del_item_btn = DangerButton(row_frame, text="X", width=26, height=26, font=FONTS["caption_bold"],
                                    command=lambda: self.remove_item_row(list_frame, row_frame))
        del_item_btn.pack(side="left", padx=2)
        
        # Prepopulate data if loaded
        if item_data:
            item_entry.insert(0, item_data['nama_item'])
            price_entry.insert(0, str(item_data['harga_satuan']))
            qty_entry.insert(0, str(item_data['jumlah']))
            subtotal_lbl.configure(text=format_rupiah(item_data['harga_satuan'] * item_data['jumlah']))
            
        # Find which location matches this list_frame and add the row references
        for rec in self.locations_data:
            if rec['items_frame'] == list_frame:
                row_record = {
                    'frame': row_frame,
                    'item_entry': item_entry,
                    'price_entry': price_entry,
                    'qty_entry': qty_entry,
                    'subtotal_lbl': subtotal_lbl
                }
                rec['item_rows'].append(row_record)
                
                # Bind dynamic subtotal & totals calculations
                price_entry.bind("<KeyRelease>", lambda e, r=row_record: self.update_row_subtotal(r))
                qty_entry.bind("<KeyRelease>", lambda e, r=row_record: self.update_row_subtotal(r))
                break
                
        self.update_totals()

    def remove_item_row(self, list_frame, row_frame):
        for rec in self.locations_data:
            if rec['items_frame'] == list_frame:
                for idx, row in enumerate(rec['item_rows']):
                    if row['frame'] == row_frame:
                        row['frame'].destroy()
                        rec['item_rows'].pop(idx)
                        break
                break
        self.update_totals()

    def update_row_subtotal(self, row):
        try:
            price = int(row['price_entry'].get().strip() or 0)
            qty = int(row['qty_entry'].get().strip() or 1)
            subtotal = price * qty
            row['subtotal_lbl'].configure(text=format_rupiah(subtotal))
        except ValueError:
            row['subtotal_lbl'].configure(text="Rp -")
            
        self.update_totals()

    def get_total_costs(self) -> int:
        total = self.transport_cost
        for rec in self.locations_data:
            for row in rec['item_rows']:
                try:
                    price = int(row['price_entry'].get().strip() or 0)
                    qty = int(row['qty_entry'].get().strip() or 0)
                    total += (price * qty)
                except ValueError:
                    pass
        return total

    def update_totals(self):
        total = self.get_total_costs()
        
        self.summary_lbl.configure(
            text=f"Total Estimasi: {format_rupiah(total)}  (termasuk transport: {format_rupiah(self.transport_cost)}) / Budget: {format_rupiah(self.budget)}"
        )
        
        if total > self.budget:
            self.warning_lbl.pack(side="left", padx=10)
        else:
            self.warning_lbl.pack_forget()

    def save_all(self):
        # Construct list to save
        clean_data = []
        for idx, rec in enumerate(self.locations_data):
            loc_name = rec['name_entry'].get().strip()
            if not loc_name:
                messagebox.showerror("Error", f"Nama tempat pada panel #{idx+1} wajib diisi.")
                return
                
            loc_dict = {
                'nama_tempat': loc_name,
                'kategori': rec['cat_dropdown'].get(),
                'urutan': idx,
                'items': []
            }
            
            for row_idx, row in enumerate(rec['item_rows']):
                item_name = row['item_entry'].get().strip()
                if not item_name:
                    continue # skip blank item names
                    
                try:
                    price = int(row['price_entry'].get().strip() or 0)
                    qty = int(row['qty_entry'].get().strip() or 1)
                except ValueError:
                    messagebox.showerror("Error", f"Harga atau jumlah pada item '{item_name}' tidak valid.")
                    return
                    
                loc_dict['items'].append({
                    'nama_item': item_name,
                    'harga_satuan': price,
                    'jumlah': qty
                })
                
            clean_data.append(loc_dict)
            
        # Save to DB
        success = planner.save_locations_and_items(self.plan_id, clean_data)
        if success:
            messagebox.showinfo("Sukses", "Data estimasi item berhasil disimpan!")
            self.reload_parent() # updates details container totals
        else:
            messagebox.showerror("Error", "Gagal menyimpan estimasi item ke database.")


class SplitBillView(ctk.CTkFrame):
    """Sub-view: split bill calculator with interactive location & item selector (F5)."""
    def __init__(self, master, plan_id, reload_parent, switch_view_callback):
        super().__init__(master, fg_color="transparent")
        self.plan_id = plan_id
        self.reload_parent = reload_parent
        self.switch_view = switch_view_callback
        
        self.loc_checkbox_vars = {}
        self.item_checkbox_vars = {}
        self.plan_data = None
        
        self.build_ui()
        self.load_data()
        
    def build_ui(self):
        # Main two-column container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Left Panel: Calculator
        self.left_panel = CardFrame(self.main_container, width=420, height=380)
        self.left_panel.pack(side="left", padx=15, pady=10, fill="both", expand=True)
        
        SubtitleLabel(self.left_panel, text="Kalkulator Split Bill").pack(pady=(20, 5))
        MutedLabel(self.left_panel, text="Bagi tagihan secara rata ke teman nongkrongmu").pack(pady=(0, 15))
        
        self.grid_frm = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.grid_frm.pack(fill="x", padx=30)
        
        CustomLabel(self.grid_frm, text="Total Tagihan (Rp)", font=FONTS["body_bold"]).pack(anchor="w", pady=(0, 4))
        self.bill_entry = CustomEntry(self.grid_frm, placeholder_text="Contoh: 150000")
        self.bill_entry.pack(fill="x", pady=(0, 12))
        
        CustomLabel(self.grid_frm, text="Jumlah Orang (Termasuk Anda)", font=FONTS["body_bold"]).pack(anchor="w", pady=(0, 4))
        self.people_entry = CustomEntry(self.grid_frm, placeholder_text="Contoh: 3")
        self.people_entry.pack(fill="x", pady=(0, 12))
        
        self.res_frm = ctk.CTkFrame(self.left_panel, fg_color="#1E293B", corner_radius=8)
        self.res_frm.pack(fill="x", padx=30, pady=(5, 12))
        
        self.res_lbl = CustomLabel(self.res_frm, text="Hasil Pembagian: Rp 0 / orang", font=FONTS["body_bold"], text_color=COLORS["success"])
        self.res_lbl.pack(pady=8)
        
        self.calc_btn = SuccessButton(self.left_panel, text="Hitung & Simpan Split Bill", command=self.calculate_and_save)
        self.calc_btn.pack(pady=(0, 10), padx=30, fill="x")
        
        # Shortcut button to view details
        PrimaryButton(self.left_panel, text="Buka Dashboard Pelunasan Teman", height=32,
                      command=lambda: self.switch_view("split_bill_dashboard", self.plan_id)).pack(pady=(0, 20), padx=30, fill="x")
                      
        self.bill_entry.bind("<KeyRelease>", self.run_split_calc)
        self.people_entry.bind("<KeyRelease>", self.run_split_calc)
        
        # Right Panel: Selection of Locations & Items
        self.right_panel = CardFrame(self.main_container, width=420, height=380)
        self.right_panel.pack(side="left", padx=15, pady=10, fill="both", expand=True)
        
        SubtitleLabel(self.right_panel, text="Pilih Tempat & Item untuk Split").pack(pady=(20, 2))
        MutedLabel(self.right_panel, text="Centang tempat/item yang ingin dimasukkan ke tagihan split").pack(pady=(0, 10))
        
        # Scrollable area for selector
        self.selector_scroll = ctk.CTkScrollableFrame(self.right_panel, fg_color="transparent", height=230)
        self.selector_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def load_data(self):
        plan = planner.get_plan_details(self.plan_id)
        if not plan:
            return
            
        self.plan_data = plan
        
        # Clear selector scroll
        for widget in self.selector_scroll.winfo_children():
            widget.destroy()
            
        # Get locations and items
        locations = plan.get('locations', [])
        
        # Load saved selection
        saved_items = planner.get_split_bill_selected_items(self.plan_id)
        # If first time, check all items by default
        is_first_time = len(saved_items) == 0 and not plan['split_bill']
        
        self.loc_checkbox_vars = {}
        self.item_checkbox_vars = {}
        
        if not locations:
            MutedLabel(self.selector_scroll, text="Tidak ada tempat atau item.\nSilakan tambah di tab Estimasi.").pack(pady=60)
        else:
            for loc in locations:
                loc_id = loc['id']
                loc_name = loc['nama_tempat']
                
                # Checkbox for Location
                loc_var = tk.BooleanVar(value=True)
                self.loc_checkbox_vars[loc_id] = loc_var
                
                loc_frm = ctk.CTkFrame(self.selector_scroll, fg_color="#1E293B", corner_radius=6)
                loc_frm.pack(fill="x", pady=4, ipady=4)
                
                # Location Row Header
                loc_cb = ctk.CTkCheckBox(
                    loc_frm,
                    text=f"📍 {loc_name}",
                    variable=loc_var,
                    fg_color=COLORS["primary"],
                    hover_color=COLORS["primary"],
                    font=FONTS["body_bold"],
                    text_color=COLORS["primary"],
                    checkbox_width=18,
                    checkbox_height=18,
                    command=lambda l_id=loc_id: self.toggle_location_items(l_id)
                )
                loc_cb.pack(anchor="w", padx=10, pady=4)
                
                # Items
                for item in loc['items']:
                    item_id = item['id']
                    item_name = item['nama_item']
                    qty = item['jumlah']
                    price = item['harga_satuan']
                    subtotal = price * qty
                    
                    # Determine checked state
                    if is_first_time:
                        item_checked = True
                    else:
                        item_checked = item_id in saved_items
                        
                    item_var = tk.BooleanVar(value=item_checked)
                    self.item_checkbox_vars[item_id] = (item_var, subtotal, loc_id)
                    
                    item_row = ctk.CTkFrame(loc_frm, fg_color="transparent")
                    item_row.pack(fill="x", padx=25, pady=1)
                    
                    item_cb = ctk.CTkCheckBox(
                        item_row,
                        text=f"{item_name} ({qty}x)",
                        variable=item_var,
                        fg_color=COLORS["success"],
                        hover_color=COLORS["success"],
                        font=FONTS["caption"],
                        text_color=COLORS["text_main"],
                        checkbox_width=16,
                        checkbox_height=16,
                        command=self.recalculate_from_selection
                    )
                    item_cb.pack(side="left")
                    
                    CustomLabel(item_row, text=format_rupiah(subtotal), font=FONTS["caption_bold"], text_color=COLORS["success"]).pack(side="right", padx=5)
                    
                # Update location checkbox state initially based on its items
                self.update_loc_var_from_items(loc_id)
                
        # Fill entry values
        total_val = plan['total_cost']
        default_people = plan['jumlah_teman'] + 1
        
        if plan['split_bill']:
            total_val = plan['split_bill']['total_tagihan']
            default_people = plan['split_bill']['jumlah_orang']
        else:
            # If no split bill saved yet, calculate initial sum of checked items
            total_val = self.sum_checked_items()
            
        self.bill_entry.delete(0, "end")
        self.bill_entry.insert(0, str(total_val))
        self.people_entry.delete(0, "end")
        self.people_entry.insert(0, str(default_people))
        
        self.run_split_calc()

    def run_split_calc(self, event=None):
        try:
            total = int(self.bill_entry.get().strip() or 0)
            people = int(self.people_entry.get().strip() or 1)
            
            if people < 1:
                people = 1
                
            per_person = int(round(total / people))
            self.res_lbl.configure(text=f"Hasil Pembagian: {format_rupiah(per_person)} / orang")
            return per_person
        except ValueError:
            self.res_lbl.configure(text="Masukkan angka nominal yang valid!")
            return 0

    def toggle_location_items(self, loc_id):
        state = self.loc_checkbox_vars[loc_id].get()
        for item_id, (var, subtotal, l_id) in self.item_checkbox_vars.items():
            if l_id == loc_id:
                var.set(state)
        self.recalculate_from_selection()
        
    def update_loc_var_from_items(self, loc_id):
        items = [var for item_id, (var, _, l_id) in self.item_checkbox_vars.items() if l_id == loc_id]
        if not items:
            return
        all_checked = all(v.get() for v in items)
        self.loc_checkbox_vars[loc_id].set(all_checked)
        
    def recalculate_from_selection(self):
        for loc_id in self.loc_checkbox_vars.keys():
            self.update_loc_var_from_items(loc_id)
            
        total = self.sum_checked_items()
        self.bill_entry.delete(0, "end")
        self.bill_entry.insert(0, str(total))
        self.run_split_calc()
        
    def sum_checked_items(self):
        total = 0
        for item_id, (var, subtotal, _) in self.item_checkbox_vars.items():
            if var.get():
                total += subtotal
        return total

    def calculate_and_save(self):
        try:
            total = int(self.bill_entry.get().strip())
            people = int(self.people_entry.get().strip())
            
            if total < 0 or people <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Masukkan total tagihan dan jumlah orang yang valid (> 0).")
            return
            
        per_person = int(round(total / people))
        success = planner.save_split_bill(self.plan_id, total, people, per_person)
        if success:
            selected_ids = [item_id for item_id, (var, _, _) in self.item_checkbox_vars.items() if var.get()]
            planner.save_split_bill_selected_items(self.plan_id, selected_ids)
            
            messagebox.showinfo("Sukses", "Split bill berhasil dihitung dan disimpan!")
            self.reload_parent()
            self.load_data()
        else:
            messagebox.showerror("Error", "Gagal menyimpan split bill.")


class SmartBudgetView(ctk.CTkFrame):
    """Sub-view: smart budget analysis (F6)."""
    def __init__(self, master, plan_id, user_id):
        super().__init__(master, fg_color="transparent")
        self.plan_id = plan_id
        self.user_id = user_id
        
        self.build_ui()
        self.load_data()
        
    def build_ui(self):
        self.panel = CardFrame(self, width=550, height=420)
        self.panel.place(relx=0.5, rely=0.5, anchor="center")
        
        SubtitleLabel(self.panel, text="Analisis Smart Budget").pack(pady=(25, 5))
        MutedLabel(self.panel, text="Evaluasi kelayakan rencana nongkrong terhadap saldo saat ini").pack(pady=(0, 20))
        
        # Grid display details
        grid_frm = ctk.CTkFrame(self.panel, fg_color="transparent")
        grid_frm.pack(fill="x", padx=50, pady=10)
        
        # Row 0: User Saldo
        r0 = ctk.CTkFrame(grid_frm, fg_color="transparent")
        r0.pack(fill="x", pady=6)
        MutedLabel(r0, text="Saldo Anda saat ini:").pack(side="left")
        self.saldo_lbl = CustomLabel(r0, text="Rp 0", font=FONTS["body_bold"], text_color=COLORS["success"])
        self.saldo_lbl.pack(side="right")
        
        # Row 1: Plan Cost
        r1 = ctk.CTkFrame(grid_frm, fg_color="transparent")
        r1.pack(fill="x", pady=6)
        MutedLabel(r1, text="Total Estimasi Rencana:").pack(side="left")
        self.cost_lbl = CustomLabel(r1, text="Rp 0", font=FONTS["body_bold"])
        self.cost_lbl.pack(side="right")
        
        # Row 2: Budget Allocated
        r2 = ctk.CTkFrame(grid_frm, fg_color="transparent")
        r2.pack(fill="x", pady=6)
        MutedLabel(r2, text="Budget yang Anda siapkan:").pack(side="left")
        self.budget_lbl = CustomLabel(r2, text="Rp 0", font=FONTS["body_bold"])
        self.budget_lbl.pack(side="right")
        
        # Status Card Box
        self.status_box = ctk.CTkFrame(self.panel, fg_color="#1E293B", corner_radius=10, border_color="#334155", border_width=1)
        self.status_box.pack(fill="both", expand=True, padx=40, pady=(15, 25))
        
        self.status_tag = StatusLabel(self.status_box, status_type="info", text="MEMPROSES...", font=("Segoe UI", 18, "bold"))
        self.status_tag.pack(pady=(15, 5))
        
        self.rec_text = CustomLabel(self.status_box, text="", font=FONTS["body"], wraplength=420, justify="center")
        self.rec_text.pack(pady=(5, 15), padx=20)

    def load_data(self):
        user = auth.get_user_by_id(self.user_id)
        plan = planner.get_plan_details(self.plan_id)
        if not user or not plan:
            return
            
        saldo = user['saldo']
        cost = plan['total_cost']
        budget = plan['budget']
        
        self.saldo_lbl.configure(text=format_rupiah(saldo))
        self.cost_lbl.configure(text=format_rupiah(cost))
        self.budget_lbl.configure(text=format_rupiah(budget))
        
        # Smart Budget Logic
        # Compares plan cost to user saldo
        if saldo <= 0:
            percentage = 100
        else:
            percentage = (cost / saldo) * 100
            
        if percentage < 30:
            # Aman
            self.status_tag.configure(text="Aman, Lanjut Nongkrong! 🎉", text_color=COLORS["success"])
            self.status_box.configure(border_color=COLORS["success"])
            self.rec_text.configure(
                text=f"Rencana nongkrong ini memakan sekitar {percentage:.1f}% saldo Anda. Finansial Anda dalam kondisi sangat aman untuk hiburan ini."
            )
        elif percentage <= 60:
            # Cukup / Waspada
            self.status_tag.configure(text="Cukup, Perhatikan Pengeluaran Lain! 👍", text_color=COLORS["warning"])
            self.status_box.configure(border_color=COLORS["warning"])
            self.rec_text.configure(
                text=f"Rencana nongkrong memakan {percentage:.1f}% saldo Anda. Masih dalam batas wajar, namun pastikan kebutuhan primer Anda lainnya sudah terpenuhi terlebih dahulu."
            )
        else:
            # Jangan dipaksain
            self.status_tag.configure(text="Agak Berat, Coba Kurangi Budget! ⚠️", text_color=COLORS["danger"])
            self.status_box.configure(border_color=COLORS["danger"])
            self.rec_text.configure(
                text=f"Peringatan! Rencana ini memakan {percentage:.1f}% saldo Anda. Sangat tidak disarankan. Coba hapus beberapa item, cari tempat alternatif, atau tunda sesi nongkrong ini."
            )


class MoodBudgetView(ctk.CTkFrame):
    """Sub-view: Mood budget simulation (F7)."""
    def __init__(self, master, plan_id, reload_parent):
        super().__init__(master, fg_color="transparent")
        self.plan_id = plan_id
        self.reload_parent = reload_parent
        
        # Mood list config
        self.moods = [
            {"emoji": "😍", "label": "Sangat Senang", "effect": 0.35, "desc": "Biasanya kalau lagi senang banget, belanja jadi sangat royal (+35%)"},
            {"emoji": "🤩", "label": "Excited / Bersemangat", "effect": 0.25, "desc": "Lagi excited nih, pengeluaran naik cukup banyak (+25%)"},
            {"emoji": "🙂", "label": "Senang", "effect": 0.10, "desc": "Mood positif, belanja sedikit meningkat (+10%)"},
            {"emoji": "😐", "label": "Netral", "effect": 0.00, "desc": "Baseline pengeluaran normal, belanja sesuai rencana (0%)"},
            {"emoji": "😭", "label": "Sedih / Stres (Impulsif)", "effect": 0.20, "desc": "Belanja impulsif sebagai retail therapy saat stres (+20%)"}
        ]
        
        self.build_ui()
        self.load_data()
        
    def build_ui(self):
        self.panel = CardFrame(self, width=550, height=440)
        self.panel.place(relx=0.5, rely=0.5, anchor="center")
        
        SubtitleLabel(self.panel, text="Analisis Mood Budget").pack(pady=(20, 5))
        MutedLabel(self.panel, text="Suasana hati (mood) sering memengaruhi pola belanja impulsif Anda.").pack(pady=(0, 20))
        
        # Slider section
        slider_frm = ctk.CTkFrame(self.panel, fg_color="transparent")
        slider_frm.pack(fill="x", padx=40, pady=10)
        
        # Slider header display
        self.mood_disp_lbl = CustomLabel(slider_frm, text="😐 Netral", font=("Segoe UI", 20, "bold"), text_color=COLORS["primary"])
        self.mood_disp_lbl.pack(pady=5)
        
        # Tkinter Slider (0 to 4 integers)
        self.slider = ctk.CTkSlider(
            slider_frm, 
            from_=0, 
            to=4, 
            number_of_steps=4,
            command=self.handle_slider_move,
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_hover"]
        )
        self.slider.pack(fill="x", pady=15)
        
        # Emoji labels below slider
        labels_frm = ctk.CTkFrame(slider_frm, fg_color="transparent")
        labels_frm.pack(fill="x")
        
        # Place emoji labels horizontally aligned with steps (with smart anchors to prevent cutting off)
        labels = ["😍", "🤩", "🙂", "😐", "😭"]
        for idx, em in enumerate(labels):
            lbl = ctk.CTkLabel(labels_frm, text=em, font=("Segoe UI", 16))
            anchor_pos = "w" if idx == 0 else "e" if idx == 4 else "center"
            lbl.place(relx=idx*0.25, anchor=anchor_pos, y=10)
            
        # Divider height buffer
        ctk.CTkLabel(slider_frm, text="", height=15, fg_color="transparent").pack()
        
        # Info Box (Fixed size with pack_propagate(False) to prevent vertical jitter during slide updates)
        self.info_box = ctk.CTkFrame(self.panel, fg_color="#1E293B", corner_radius=8, width=470, height=75)
        self.info_box.pack(fill="x", padx=40, pady=10)
        self.info_box.pack_propagate(False)
        
        self.mood_desc_lbl = CustomLabel(self.info_box, text="", font=FONTS["caption"], wraplength=420, justify="center")
        self.mood_desc_lbl.pack(expand=True, fill="both", padx=15, pady=5)
        
        # Calculation displays
        self.cost_frm = ctk.CTkFrame(self.panel, fg_color="transparent")
        self.cost_frm.pack(fill="x", padx=40, pady=10)
        
        self.normal_cost_lbl = CustomLabel(self.cost_frm, text="Estimasi Normal: Rp 0", font=FONTS["body_bold"])
        self.normal_cost_lbl.pack(side="left")
        
        self.projected_cost_lbl = CustomLabel(self.cost_frm, text="Proyeksi Realistis: Rp 0", font=FONTS["body_bold"], text_color=COLORS["warning"])
        self.projected_cost_lbl.pack(side="right")
        
        # Apply button
        self.apply_btn = SuccessButton(self.panel, text="Terapkan Mood ke Rencana", command=self.save_mood_settings)
        self.apply_btn.pack(pady=15, padx=40, fill="x")

    def load_data(self):
        plan = planner.get_plan_details(self.plan_id)
        if not plan:
            return
            
        self.normal_cost = plan['total_cost']
        
        # Set slider to current mood
        current_mood = plan['mood']
        current_idx = 3 # default 😐
        for i, m in enumerate(self.moods):
            if m['emoji'] == current_mood:
                current_idx = i
                break
                
        self.slider.set(current_idx)
        self.handle_slider_move(current_idx)

    def handle_slider_move(self, val):
        idx = int(round(float(val)))
        mood_info = self.moods[idx]
        
        # Update labels
        self.mood_disp_lbl.configure(text=f"{mood_info['emoji']} {mood_info['label']}")
        self.mood_desc_lbl.configure(text=mood_info['desc'])
        
        # Calculate projected
        proj_cost = self.normal_cost * (1 + mood_info['effect'])
        
        self.normal_cost_lbl.configure(text=f"Estimasi Normal: {format_rupiah(self.normal_cost)}")
        self.projected_cost_lbl.configure(text=f"Proyeksi Realistis: {format_rupiah(proj_cost)}")
        
        # Color display based on positive/negative effects
        if mood_info['effect'] > 0:
            self.projected_cost_lbl.configure(text_color=COLORS["warning"])
        else:
            self.projected_cost_lbl.configure(text_color=COLORS["success"])

    def save_mood_settings(self):
        idx = int(round(self.slider.get()))
        mood_info = self.moods[idx]
        
        success = planner.update_plan_mood(self.plan_id, mood_info['emoji'], mood_info['effect'])
        if success:
            messagebox.showinfo("Sukses", f"Mood {mood_info['emoji']} berhasil diterapkan ke rencana!")
            self.reload_parent()
        else:
            messagebox.showerror("Error", "Gagal memperbarui mood rencana.")


class BasicPlanInfoView(ctk.CTkFrame):
    """Sub-view: View and edit basic details of a plan (F3)."""
    def __init__(self, master, plan_id, reload_parent):
        super().__init__(master, fg_color="transparent")
        self.plan_id = plan_id
        self.reload_parent = reload_parent
        
        self.build_ui()
        self.load_data()
        
    def build_ui(self):
        # Card container
        self.container = CardFrame(self)
        self.container.pack(pady=15, padx=30, fill="both", expand=True)
        
        # Grid layout (2 columns)
        self.form_grid = ctk.CTkFrame(self.container, fg_color="transparent")
        self.form_grid.pack(fill="both", expand=True, padx=30, pady=15)
        self.form_grid.grid_columnconfigure(0, weight=1)
        self.form_grid.grid_columnconfigure(1, weight=1)
        
        # Col 0: Detail Rencana
        col0 = ctk.CTkFrame(self.form_grid, fg_color="transparent")
        col0.grid(row=0, column=0, padx=(0, 20), sticky="nsew")
        
        CustomLabel(col0, text="Nama Rencana / Label", font=FONTS["body_bold"]).pack(anchor="w", pady=(0, 4))
        self.name_entry = CustomEntry(col0, placeholder_text="Misalnya: Buka Puasa, Me Time, Kopi Santai")
        self.name_entry.pack(fill="x", pady=(0, 15))
        
        CustomLabel(col0, text="Tanggal Kegiatan", font=FONTS["body_bold"]).pack(anchor="w", pady=(0, 4))
        
        # Date dropdowns
        date_frm = ctk.CTkFrame(col0, fg_color="transparent")
        date_frm.pack(fill="x", pady=(0, 15))
        
        months_list = [
            "Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        ]
        
        self.day_dropdown = ctk.CTkComboBox(
            date_frm,
            values=[f"{i:02d}" for i in range(1, 32)],
            width=80,
            fg_color=COLORS["bg_main"],
            text_color=COLORS["text_main"],
            border_color="#334155",
            corner_radius=8
        )
        self.day_dropdown.pack(side="left", padx=(0, 10))
        
        self.month_dropdown = ctk.CTkComboBox(
            date_frm,
            values=months_list,
            width=130,
            fg_color=COLORS["bg_main"],
            text_color=COLORS["text_main"],
            border_color="#334155",
            corner_radius=8
        )
        self.month_dropdown.pack(side="left", padx=(0, 10))
        
        self.year_dropdown = ctk.CTkComboBox(
            date_frm,
            values=[str(y) for y in range(2025, 2031)],
            width=90,
            fg_color=COLORS["bg_main"],
            text_color=COLORS["text_main"],
            border_color="#334155",
            corner_radius=8
        )
        self.year_dropdown.pack(side="left")
        
        CustomLabel(col0, text="Jumlah Teman (di luar Anda)", font=FONTS["body_bold"]).pack(anchor="w", pady=(0, 4))
        self.friends_entry = CustomEntry(col0, placeholder_text="Masukkan angka (0 untuk Solo Hangout)")
        self.friends_entry.pack(fill="x", pady=(0, 5))
        self.solo_lbl = MutedLabel(col0, text="Status: Solo Hangout", text_color=COLORS["primary"])
        self.solo_lbl.pack(anchor="w", pady=(0, 15))
        self.friends_entry.bind("<KeyRelease>", self.update_friends_status)
        
        # Col 1: Keuangan & Transport
        col1 = ctk.CTkFrame(self.form_grid, fg_color="transparent")
        col1.grid(row=0, column=1, padx=(20, 0), sticky="nsew")
        
        CustomLabel(col1, text="Alokasi Budget (Rp)", font=FONTS["body_bold"]).pack(anchor="w", pady=(0, 4))
        self.budget_entry = CustomEntry(col1, placeholder_text="Contoh: 150000")
        self.budget_entry.pack(fill="x", pady=(0, 15))
        
        CustomLabel(col1, text="Jenis Transportasi", font=FONTS["body_bold"]).pack(anchor="w", pady=(0, 4))
        self.transport_dropdown = ctk.CTkComboBox(
            col1, 
            values=["Motor Pribadi", "Mobil Pribadi", "Ojek Online (Motor)", "Taksi Online (Mobil)", "KRL / TransJakarta", "Jalan Kaki"],
            fg_color=COLORS["bg_main"],
            text_color=COLORS["text_main"],
            border_color="#334155",
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_hover"],
            font=FONTS["body"],
            corner_radius=8,
            height=36
        )
        self.transport_dropdown.pack(fill="x", pady=(0, 15))
        
        CustomLabel(col1, text="Estimasi Biaya Transportasi (Rp)", font=FONTS["body_bold"]).pack(anchor="w", pady=(0, 4))
        self.transport_cost_entry = CustomEntry(col1, placeholder_text="Contoh: 15000")
        self.transport_cost_entry.pack(fill="x", pady=(0, 15))
        
        # Save button
        self.save_btn = SuccessButton(self.container, text="Simpan Perubahan Info Rencana", command=self.save_changes)
        self.save_btn.pack(pady=(0, 20), padx=30, fill="x")

    def update_friends_status(self, event=None):
        try:
            val = int(self.friends_entry.get().strip())
            if val == 0:
                self.solo_lbl.configure(text="Status: Solo Hangout (Nongkrong Sendiri)", text_color=COLORS["primary"])
            elif val > 0:
                self.solo_lbl.configure(text=f"Status: Hangout Grup (Anda + {val} Teman)", text_color=COLORS["success"])
            else:
                self.solo_lbl.configure(text="Jumlah teman tidak boleh negatif!", text_color=COLORS["danger"])
        except ValueError:
            self.solo_lbl.configure(text="Masukkan angka yang valid!", text_color=COLORS["danger"])

    def load_data(self):
        plan = planner.get_plan_details(self.plan_id)
        if not plan:
            return
            
        self.name_entry.insert(0, plan['nama_rencana'] or "")
        self.friends_entry.insert(0, str(plan['jumlah_teman']))
        self.budget_entry.insert(0, str(plan['budget']))
        self.transport_dropdown.set(plan['transportasi'] or "Motor Pribadi")
        self.transport_cost_entry.insert(0, str(plan['transport_cost']))
        self.update_friends_status()
        
        # Set date dropdowns
        try:
            date_obj = datetime.strptime(plan['tanggal'], "%Y-%m-%d")
            months_list = [
                "Januari", "Februari", "Maret", "April", "Mei", "Juni",
                "Juli", "Agustus", "September", "Oktober", "November", "Desember"
            ]
            self.day_dropdown.set(f"{date_obj.day:02d}")
            self.month_dropdown.set(months_list[date_obj.month - 1])
            self.year_dropdown.set(str(date_obj.year))
        except Exception:
            pass

    def save_changes(self):
        name = self.name_entry.get().strip()
        friends_str = self.friends_entry.get().strip()
        budget_str = self.budget_entry.get().strip()
        transport = self.transport_dropdown.get()
        transport_cost_str = self.transport_cost_entry.get().strip()
        
        # Parse date from dropdowns
        month_mapping = {
            "Januari": "01", "Februari": "02", "Maret": "03", "April": "04",
            "Mei": "05", "Juni": "06", "Juli": "07", "Agustus": "08",
            "September": "09", "Oktober": "10", "November": "11", "Desember": "12"
        }
        day = self.day_dropdown.get()
        month_name = self.month_dropdown.get()
        month = month_mapping.get(month_name, "01")
        year = self.year_dropdown.get()
        date_str = f"{year}-{month}-{day}"
        
        # Validation
        if not name:
            messagebox.showerror("Error", "Nama Rencana wajib diisi.")
            return
            
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", f"Tanggal {date_str} tidak valid! Harap periksa kembali tanggal yang Anda pilih.")
            return
            
        try:
            friends = int(friends_str)
            if friends < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Jumlah teman harus berupa angka bulat positif (atau 0).")
            return
            
        try:
            budget = int(budget_str)
            if budget <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Budget harus berupa angka nominal lebih dari 0.")
            return
            
        try:
            transport_cost = int(transport_cost_str)
            if transport_cost < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Biaya transportasi harus berupa angka nominal positif (atau 0).")
            return
            
        success = planner.update_plan_details(self.plan_id, name, date_str, friends, budget, transport, transport_cost)
        if success:
            messagebox.showinfo("Sukses", "Detail rencana berhasil diperbarui!")
            self.reload_parent()
        else:
            messagebox.showerror("Error", "Gagal memperbarui detail rencana.")


class PlanDetailContainerFrame(ctk.CTkFrame):
    """Container managing details of a plan with sub-tabs."""
    def __init__(self, master, plan_id, user, switch_view_callback, back_view="dashboard", initial_tab="info"):
        super().__init__(master, fg_color=COLORS["bg_main"])
        self.plan_id = plan_id
        self.user = user
        self.switch_view = switch_view_callback
        self.back_view = back_view
        self.current_tab = initial_tab
        
        self.build_ui()
        self.load_plan_header()
        self.switch_tab(initial_tab)
        
    def build_ui(self):
        # 1. Plan Header Frame
        self.hdr_frame = CardFrame(self)
        self.hdr_frame.pack(fill="x", padx=30, pady=(20, 10))
        
        left_info = ctk.CTkFrame(self.hdr_frame, fg_color="transparent")
        left_info.pack(side="left", padx=20, pady=15)
        
        self.plan_title_lbl = HeaderLabel(left_info, text="Memuat Rencana...")
        self.plan_title_lbl.pack(anchor="w")
        
        self.plan_meta_lbl = MutedLabel(left_info, text="Tanggal: - • Budget: -")
        self.plan_meta_lbl.pack(anchor="w")
        
        right_actions = ctk.CTkFrame(self.hdr_frame, fg_color="transparent")
        right_actions.pack(side="right", padx=20, pady=15)
        
        # Status Dropdown
        CustomLabel(right_actions, text="Status Rencana:", font=FONTS["caption_bold"]).pack(side="left", padx=(0, 5))
        self.status_dropdown = ctk.CTkComboBox(
            right_actions,
            values=["Draft", "Selesai", "Dibatalkan"],
            width=110, height=28,
            fg_color=COLORS["bg_main"],
            text_color=COLORS["text_main"],
            border_color="#334155",
            command=self.change_plan_status
        )
        self.status_dropdown.pack(side="left", padx=(0, 15))
        
        SecondaryButton(right_actions, text="Kembali", width=80, height=28, command=lambda: self.switch_view(self.back_view)).pack(side="right")
        
        # Delete Plan button
        DangerButton(right_actions, text="Hapus", width=70, height=28, command=self.confirm_delete_plan).pack(side="right", padx=10)
        
        # 2. Tabs Navigation Bar
        self.tabs_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.tabs_bar.pack(fill="x", padx=30, pady=5)
        
        self.tab_info_btn = SecondaryButton(self.tabs_bar, text="1. Detail Rencana", height=32, command=lambda: self.switch_tab("info"))
        self.tab_info_btn.pack(side="left", padx=(0, 10))
        
        self.tab_est_btn = SecondaryButton(self.tabs_bar, text="2. Estimasi Item", height=32, command=lambda: self.switch_tab("estimasi"))
        self.tab_est_btn.pack(side="left", padx=10)
        
        self.tab_sb_btn = SecondaryButton(self.tabs_bar, text="3. Split Bill", height=32, command=lambda: self.switch_tab("split_bill"))
        self.tab_sb_btn.pack(side="left", padx=10)
        
        self.tab_sm_btn = SecondaryButton(self.tabs_bar, text="4. Smart Budget", height=32, command=lambda: self.switch_tab("smart_budget"))
        self.tab_sm_btn.pack(side="left", padx=10)
        
        self.tab_mood_btn = SecondaryButton(self.tabs_bar, text="5. Mood Budget", height=32, command=lambda: self.switch_tab("mood_budget"))
        self.tab_mood_btn.pack(side="left", padx=10)
        
        # 3. Content Frame Area
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=30, pady=(5, 20))
 
    def load_plan_header(self):
        plan = planner.get_plan_details(self.plan_id)
        if not plan:
            return
            
        p_name = plan['nama_rencana'] if plan['nama_rencana'] else f"Rencana #{self.plan_id}"
        self.plan_title_lbl.configure(text=p_name)
        
        date_obj = datetime.strptime(plan['tanggal'], "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d %B %Y")
        
        meta = f"Tanggal: {formatted_date}  •  Budget Rencana: {format_rupiah(plan['budget'])}  •  Total Biaya: {format_rupiah(plan['total_cost'])}"
        self.plan_meta_lbl.configure(text=meta)
        
        # Dropdown status
        self.status_dropdown.set(plan['status'].capitalize())
 
    def change_plan_status(self, val):
        status_db = val.lower()
        success = planner.update_plan_status(self.plan_id, status_db)
        if success:
            messagebox.showinfo("Sukses", f"Status rencana diubah menjadi '{val}'.")
            self.load_plan_header()
        else:
            messagebox.showerror("Error", "Gagal memperbarui status rencana.")
 
    def confirm_delete_plan(self):
        if messagebox.askyesno("Hapus Rencana", "Apakah Anda yakin ingin menghapus rencana ini beserta seluruh datanya?"):
            if planner.delete_plan(self.plan_id):
                messagebox.showinfo("Sukses", "Rencana berhasil dihapus.")
                self.switch_view("dashboard")
            else:
                messagebox.showerror("Error", "Gagal menghapus rencana.")
 
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
 
    def switch_tab(self, tab_name):
        self.current_tab = tab_name
        self.clear_content()
        
        # Reset buttons styles (transparent unless active)
        for btn in [self.tab_info_btn, self.tab_est_btn, self.tab_sb_btn, self.tab_sm_btn, self.tab_mood_btn]:
            btn.configure(fg_color="transparent", text_color=COLORS["primary"], border_color=COLORS["primary"])
            
        if tab_name == "info":
            self.tab_info_btn.configure(fg_color=COLORS["primary"], text_color=COLORS["text_main"])
            view = BasicPlanInfoView(self.content_frame, self.plan_id, self.load_plan_header)
            view.pack(fill="both", expand=True)
            
        elif tab_name == "estimasi":
            self.tab_est_btn.configure(fg_color=COLORS["primary"], text_color=COLORS["text_main"])
            view = EstimateItemsView(self.content_frame, self.plan_id, self.load_plan_header)
            view.pack(fill="both", expand=True)
            
        elif tab_name == "split_bill":
            self.tab_sb_btn.configure(fg_color=COLORS["primary"], text_color=COLORS["text_main"])
            view = SplitBillView(self.content_frame, self.plan_id, self.load_plan_header, self.switch_view)
            view.pack(fill="both", expand=True)
            
        elif tab_name == "smart_budget":
            self.tab_sm_btn.configure(fg_color=COLORS["primary"], text_color=COLORS["text_main"])
            view = SmartBudgetView(self.content_frame, self.plan_id, self.user['id'])
            view.pack(fill="both", expand=True)
            
        elif tab_name == "mood_budget":
            self.tab_mood_btn.configure(fg_color=COLORS["primary"], text_color=COLORS["text_main"])
            view = MoodBudgetView(self.content_frame, self.plan_id, self.load_plan_header)
            view.pack(fill="both", expand=True)
