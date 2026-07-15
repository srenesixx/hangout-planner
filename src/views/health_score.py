from datetime import datetime
import customtkinter as ctk

from src.components import (
    COLORS, FONTS,
    CardFrame, CustomLabel, HeaderLabel, SubtitleLabel, MutedLabel
)
import src.planner as planner

class BudgetHealthScoreView(ctk.CTkFrame):
    """View to display health score detailed analysis (F9)."""
    def __init__(self, master, user, target_month=None):
        super().__init__(master, fg_color=COLORS["bg_main"])
        self.user = user
        self.target_month = target_month if target_month else datetime.now().strftime("%Y-%m")
        
        self.build_ui()
        self.load_score_details()
        
    def build_ui(self):
        # 1. Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))
        
        HeaderLabel(header, text="Analisis Budget Health Score").pack(side="left")
        
        # Month selector dropdown
        self.month_dropdown = ctk.CTkComboBox(
            header,
            values=[datetime.now().strftime("%Y-%m")], # We can list others dynamically
            width=120, height=28,
            fg_color=COLORS["bg_card"],
            text_color=COLORS["text_main"],
            border_color="#334155",
            command=self.change_month
        )
        self.month_dropdown.pack(side="right", padx=10)
        CustomLabel(header, text="Periode:", font=FONTS["caption_bold"]).pack(side="right", padx=(0, 5))
        
        # 2. Main Content Split (Left: Gauge & Info, Right: Score breakdown list)
        self.split_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.split_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Left Panel (Gauge + recommendation)
        self.left_panel = CardFrame(self.split_frame)
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        # Gauge Visual Canvas
        self.gauge_canvas = ctk.CTkCanvas(self.left_panel, width=220, height=220, bg=COLORS["bg_card"], highlightthickness=0)
        self.gauge_canvas.pack(pady=20)
        
        # AI recommendation box
        self.rec_frm = ctk.CTkFrame(self.left_panel, fg_color="#1E293B", corner_radius=10)
        self.rec_frm.pack(fill="x", padx=20, pady=10, ipady=10)
        
        CustomLabel(self.rec_frm, text="Rekomendasi AI Co-pilot:", font=FONTS["body_bold"], text_color=COLORS["primary"]).pack(anchor="w", padx=15, pady=(10, 2))
        self.rec_lbl = CustomLabel(self.rec_frm, text="", font=FONTS["body"], justify="left", wraplength=380)
        self.rec_lbl.pack(anchor="w", padx=15, pady=(0, 10))
        
        # Right Panel (Breakdown components progress bars)
        self.right_panel = CardFrame(self.split_frame)
        self.right_panel.pack(side="right", fill="both", expand=True, padx=(15, 0))
        
        SubtitleLabel(self.right_panel, text="Rincian Komponen Skor").pack(anchor="w", padx=20, pady=(20, 5))
        MutedLabel(self.right_panel, text="Penilaian dihitung berdasarkan 4 kriteria utama").pack(anchor="w", padx=20, pady=(0, 20))
        
        # Components indicators
        self.components_frm = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.components_frm.pack(fill="both", expand=True, padx=20)

    def load_score_details(self):
        # Retrieve all user's historical periods for dropdown
        conn = planner.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT strftime('%Y-%m', tanggal) as mon FROM plans WHERE user_id = ? ORDER BY mon DESC", (self.user['id'],))
        periods = [r['mon'] for r in cursor.fetchall()]
        
        current_m = datetime.now().strftime("%Y-%m")
        if current_m not in periods:
            periods.append(current_m)
            
        self.month_dropdown.configure(values=periods)
        self.month_dropdown.set(self.target_month)
        
        # Get score
        score_db = planner.get_saved_budget_health_score(self.user['id'], self.target_month)
        if not score_db:
            score = planner.save_or_update_health_score(self.user['id'], self.target_month)
            score_db = planner.get_saved_budget_health_score(self.user['id'], self.target_month)
        else:
            score = score_db['score']
            
        breakdown = score_db['breakdown']
        
        # 1. Redraw Gauge
        self.gauge_canvas.delete("all")
        
        # Draw base arc
        self.gauge_canvas.create_arc(25, 25, 195, 195, start=135, extent=-270, width=18, outline="#1E293B", style="arc")
        
        # Determine score color
        if score < 40:
            score_color = COLORS["danger"]
        elif score < 70:
            score_color = COLORS["warning"]
        else:
            score_color = COLORS["success"]
            
        # Draw score level arc
        extent_val = -270 * (score / 100.0)
        self.gauge_canvas.create_arc(25, 25, 195, 195, start=135, extent=extent_val, width=18, outline=score_color, style="arc")
        
        # Inside texts
        self.gauge_canvas.create_text(110, 105, text=str(score), fill=COLORS["text_main"], font=("Segoe UI", 48, "bold"))
        self.gauge_canvas.create_text(110, 155, text="SKOR ANDA", fill=COLORS["text_muted"], font=FONTS["caption_bold"])
        
        # Set AI suggestion message
        self.rec_lbl.configure(text=breakdown.get('message', ''))
        
        # 2. Render breakdown components list (Progress bars)
        for w in self.components_frm.winfo_children():
            w.destroy()
            
        comps = [
            ("Rasio Pengeluaran vs Saldo", breakdown.get('ratio_score', 0), 30, "Mengevaluasi porsi saldo yang habis digunakan untuk hangout."),
            ("Frekuensi Hangout", breakdown.get('frequency_score', 0), 20, "Nongkrong yang terlalu sering dapat mengganggu kestabilan tabungan."),
            ("Konsistensi Budget Rencana", breakdown.get('consistency_score', 0), 25, "Apakah pengeluaran riil Anda sesuai dengan budget yang direncanakan."),
            ("Tren vs Bulan Lalu", breakdown.get('trend_score', 0), 25, "Menilai apakah Anda lebih hemat dibanding bulan sebelumnya.")
        ]
        
        for name, val, max_val, desc in comps:
            row = ctk.CTkFrame(self.components_frm, fg_color="transparent")
            row.pack(fill="x", pady=12)
            
            # Header info
            info_row = ctk.CTkFrame(row, fg_color="transparent")
            info_row.pack(fill="x")
            CustomLabel(info_row, text=name, font=FONTS["body_bold"]).pack(side="left")
            CustomLabel(info_row, text=f"{val} / {max_val} Poin", font=FONTS["body_bold"], text_color=COLORS["primary"]).pack(side="right")
            
            # Progress bar
            progress = val / max_val
            pb = ctk.CTkProgressBar(
                row, 
                progress_color=COLORS["success"] if progress >= 0.7 else COLORS["warning"] if progress >= 0.4 else COLORS["danger"],
                fg_color="#1E293B",
                height=8,
                corner_radius=4
            )
            pb.set(progress)
            pb.pack(fill="x", pady=(4, 2))
            
            MutedLabel(row, text=desc).pack(anchor="w")

    def change_month(self, val):
        self.target_month = val
        self.load_score_details()
