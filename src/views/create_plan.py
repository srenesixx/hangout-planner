from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox

from src.views.components import (
    COLORS, FONTS,
    CardFrame, SecondaryButton, SuccessButton,
    CustomEntry, CustomLabel, HeaderLabel, MutedLabel
)
from src.controllers.planner_controller import PlannerController as planner

class CreatePlanFrame(ctk.CTkFrame):
    """View to design a new hangout plan."""
    def __init__(self, master, user, switch_view_callback):
        super().__init__(master, fg_color=COLORS["bg_main"])
        self.user = user
        self.switch_view = switch_view_callback
        
        self.build_ui()
        
    def build_ui(self):
        # Center card container
        self.container = CardFrame(self)
        self.container.pack(pady=40, padx=50, fill="both", expand=True)
        
        # Header
        HeaderLabel(self.container, text="Buat Rencana Nongkrong Baru").pack(pady=(20, 5))
        MutedLabel(self.container, text="Tentukan tempat, tanggal, budget, dan moda transportasi.").pack(pady=(0, 20))
        
        # Form Container (2 columns grid)
        self.form_grid = ctk.CTkFrame(self.container, fg_color="transparent")
        self.form_grid.pack(fill="both", expand=True, padx=40, pady=10)
        self.form_grid.grid_columnconfigure(0, weight=1)
        self.form_grid.grid_columnconfigure(1, weight=1)
        
        # Col 0: Detail Rencana
        col0 = ctk.CTkFrame(self.form_grid, fg_color="transparent")
        col0.grid(row=0, column=0, padx=(0, 20), sticky="nsew")
        
        CustomLabel(col0, text="Nama Rencana / Label", font=FONTS["body_bold"]).pack(anchor="w", pady=(0, 4))
        self.name_entry = CustomEntry(col0, placeholder_text="Misalnya: Buka Puasa, Me Time, Kopi Santai")
        self.name_entry.pack(fill="x", pady=(0, 15))
        
        CustomLabel(col0, text="Tanggal Kegiatan", font=FONTS["body_bold"]).pack(anchor="w", pady=(0, 4))
        
        # Row frame for date dropdowns
        date_frm = ctk.CTkFrame(col0, fg_color="transparent")
        date_frm.pack(fill="x", pady=(0, 15))
        
        today = datetime.now()
        months_list = [
            "Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        ]
        
        # Day Dropdown
        self.day_dropdown = ctk.CTkComboBox(
            date_frm,
            values=[f"{i:02d}" for i in range(1, 32)],
            width=80,
            fg_color=COLORS["bg_main"],
            text_color=COLORS["text_main"],
            border_color="#334155",
            corner_radius=8
        )
        self.day_dropdown.set(f"{today.day:02d}")
        self.day_dropdown.pack(side="left", padx=(0, 10))
        
        # Month Dropdown
        self.month_dropdown = ctk.CTkComboBox(
            date_frm,
            values=months_list,
            width=130,
            fg_color=COLORS["bg_main"],
            text_color=COLORS["text_main"],
            border_color="#334155",
            corner_radius=8
        )
        self.month_dropdown.set(months_list[today.month - 1])
        self.month_dropdown.pack(side="left", padx=(0, 10))
        
        # Year Dropdown
        self.year_dropdown = ctk.CTkComboBox(
            date_frm,
            values=[str(y) for y in range(2025, 2031)],
            width=90,
            fg_color=COLORS["bg_main"],
            text_color=COLORS["text_main"],
            border_color="#334155",
            corner_radius=8
        )
        self.year_dropdown.set(str(today.year))
        self.year_dropdown.pack(side="left")
        
        CustomLabel(col0, text="Jumlah Teman (di luar Anda)", font=FONTS["body_bold"]).pack(anchor="w", pady=(0, 4))
        self.friends_entry = CustomEntry(col0, placeholder_text="Masukkan angka (0 untuk Solo Hangout)")
        self.friends_entry.insert(0, "0")
        self.friends_entry.pack(fill="x", pady=(0, 5))
        self.solo_lbl = MutedLabel(col0, text="Status: Solo Hangout (Nongkrong Sendiri)", text_color=COLORS["primary"])
        self.solo_lbl.pack(anchor="w", pady=(0, 15))
        
        # Bind change listener to friends entry to update Solo Hangout label
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
        self.transport_dropdown.set("Motor Pribadi")
        self.transport_dropdown.pack(fill="x", pady=(0, 15))
        
        CustomLabel(col1, text="Estimasi Biaya Transportasi (Rp)", font=FONTS["body_bold"]).pack(anchor="w", pady=(0, 4))
        self.transport_cost_entry = CustomEntry(col1, placeholder_text="Contoh: 15000 (0 jika jalan kaki / gratis)")
        self.transport_cost_entry.insert(0, "0")
        self.transport_cost_entry.pack(fill="x", pady=(0, 15))
        
        # Action Buttons frame
        btn_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        btn_frame.pack(fill="x", padx=40, pady=25)
        
        SecondaryButton(btn_frame, text="Kembali ke Dashboard", command=lambda: self.switch_view("dashboard")).pack(side="left", padx=5)
        SuccessButton(btn_frame, text="Lanjutkan ke Estimasi Item →", command=self.handle_save).pack(side="right", padx=5)

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
            
    def handle_save(self):
        name = self.name_entry.get().strip()
        
        # Get date from dropdowns automatically
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
        
        friends_str = self.friends_entry.get().strip()
        budget_str = self.budget_entry.get().strip()
        transport = self.transport_dropdown.get()
        transport_cost_str = self.transport_cost_entry.get().strip()
        
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
            
        # Create plan in SQLite database
        plan_id = planner.create_plan(
            user_id=self.user['id'],
            nama_rencana=name,
            tanggal=date_str,
            jumlah_teman=friends,
            budget=budget,
            transportasi=transport,
            transport_cost=transport_cost
        )
        
        if plan_id:
            messagebox.showinfo("Sukses", "Rencana berhasil dibuat! Silakan tambahkan estimasi pengeluaran per tempat.")
            # Switch to Detail Plan view (active context)
            self.switch_view("detail_rencana", plan_id)
        else:
            messagebox.showerror("Error", "Gagal menyimpan rencana ke database.")
