from datetime import datetime
import random
import customtkinter as ctk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from src.components import (
    COLORS, FONTS, format_rupiah,
    CardFrame, PrimaryButton, SecondaryButton,
    CustomLabel, SubtitleLabel, MutedLabel
)
import src.auth as auth
import src.planner as planner

class DashboardFrame(ctk.CTkFrame):
    """Dashboard view listing summary, quick actions, and integrated stats."""
    def __init__(self, master, user, switch_view_callback):
        super().__init__(master, fg_color=COLORS["bg_main"])
        self.user = user
        self.switch_view = switch_view_callback
        self.figures = []
        
        # Grid layout
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0) # Space for charts row
        
        self.build_ui()
        
    def build_ui(self):
        # Fetch fresh user and plan data
        self.user = auth.get_user_by_id(self.user['id'])
        current_month = datetime.now().strftime("%Y-%m")
        monthly_spent = planner.get_monthly_spending(self.user['id'], current_month)
        all_plans = planner.get_user_plans(self.user['id'])
        active_plans = [p for p in all_plans if p['status'] != 'selesai' and p['status'] != 'dibatalkan']
        
        # Calculate/retrieve Health Score
        health_score = planner.save_or_update_health_score(self.user['id'], current_month)
        
        # 1. Header (Row 0, Spans columns)
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=2, padx=30, pady=(25, 15), sticky="ew")
        
        from src.components import HeaderLabel # Local import to avoid circular dependencies if any
        HeaderLabel(header_frame, text=f"Halo, {self.user['nama']}! 👋").pack(side="left")
        
        # Quick Action Button
        PrimaryButton(header_frame, text="+ Buat Rencana Baru", 
                      command=lambda: self.switch_view("buat_rencana")).pack(side="right")
        
        # 2. Main Panel (Left Column)
        left_panel = ctk.CTkFrame(self, fg_color="transparent")
        left_panel.grid(row=1, column=0, padx=(30, 15), pady=15, sticky="nsew")
        left_panel.grid_columnconfigure(0, weight=1)
        left_panel.grid_columnconfigure(1, weight=1)
        
        # Card Saldo
        saldo_card = CardFrame(left_panel)
        saldo_card.grid(row=0, column=0, padx=(0, 10), pady=(0, 20), sticky="ew")
        MutedLabel(saldo_card, text="SALDO SAAT INI", font=FONTS["caption_bold"]).pack(anchor="w", padx=20, pady=(15, 5))
        CustomLabel(saldo_card, text=format_rupiah(self.user['saldo']), font=("Segoe UI", 22, "bold"), 
                    text_color=COLORS["success"]).pack(anchor="w", padx=20, pady=(0, 15))
        
        # Card Pengeluaran Bulan Ini
        spending_card = CardFrame(left_panel)
        spending_card.grid(row=0, column=1, padx=(10, 0), pady=(0, 20), sticky="ew")
        MutedLabel(spending_card, text="PENGELUARAN BULAN INI", font=FONTS["caption_bold"]).pack(anchor="w", padx=20, pady=(15, 5))
        CustomLabel(spending_card, text=format_rupiah(monthly_spent), font=("Segoe UI", 22, "bold"), 
                    text_color=COLORS["warning"]).pack(anchor="w", padx=20, pady=(0, 15))
        
        # Card Rencana Aktif / Upcoming
        plans_summary_card = CardFrame(left_panel)
        plans_summary_card.grid(row=1, column=0, columnspan=2, padx=0, pady=(0, 20), sticky="ew")
        plans_summary_card.grid_columnconfigure(0, weight=1)
        plans_summary_card.grid_columnconfigure(1, weight=1)
        
        # Split plans summary info
        info_left = ctk.CTkFrame(plans_summary_card, fg_color="transparent")
        info_left.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        MutedLabel(info_left, text="RENCANA AKTIF", font=FONTS["caption_bold"]).pack(anchor="w")
        CustomLabel(info_left, text=f"{len(active_plans)} Rencana", font=FONTS["subtitle"]).pack(anchor="w")
        
        info_right = ctk.CTkFrame(plans_summary_card, fg_color="transparent")
        info_right.grid(row=0, column=1, padx=20, pady=15, sticky="w")
        MutedLabel(info_right, text="TOTAL HANGOUT BULAN INI", font=FONTS["caption_bold"]).pack(anchor="w")
        month_plans = [p for p in all_plans if p['tanggal'].startswith(current_month)]
        CustomLabel(info_right, text=f"{len(month_plans)} Sesi Nongkrong", font=FONTS["subtitle"]).pack(anchor="w")
        
        # Recent Plans List Frame
        recent_card = CardFrame(left_panel)
        recent_card.grid(row=2, column=0, columnspan=2, sticky="nsew")
        left_panel.grid_rowconfigure(2, weight=1)
        
        # Header recent plans
        recent_header = ctk.CTkFrame(recent_card, fg_color="transparent")
        recent_header.pack(fill="x", padx=20, pady=(15, 10))
        SubtitleLabel(recent_header, text="Rencana Nongkrong Terbaru").pack(side="left")
        SecondaryButton(recent_header, text="Lihat Semua", width=90, height=26,
                        command=lambda: self.switch_view("riwayat")).pack(side="right")
        
        # Plan list scrollable area
        scroll_plans = ctk.CTkScrollableFrame(recent_card, fg_color="transparent")
        scroll_plans.pack(fill="both", expand=True, padx=10, pady=(0, 15))
        
        if not all_plans:
            empty_frm = ctk.CTkFrame(scroll_plans, fg_color="transparent")
            empty_frm.pack(pady=40)
            
            ctk.CTkLabel(empty_frm, text="📭", font=("Segoe UI", 48)).pack(pady=5)
            MutedLabel(empty_frm, text="Belum ada rencana nongkrong yang dibuat.", font=FONTS["body_bold"]).pack(pady=2)
            MutedLabel(empty_frm, text="Yuk, susun rencana pertamamu untuk mulai memantau budget!").pack(pady=(0, 15))
            
            PrimaryButton(empty_frm, text="+ Buat Rencana Baru", width=180, 
                          command=lambda: self.switch_view("buat_rencana")).pack()
        else:
            for idx, plan in enumerate(all_plans[:4]):
                item_frame = ctk.CTkFrame(scroll_plans, fg_color="#1E293B" if idx % 2 == 0 else "transparent", corner_radius=6)
                item_frame.pack(fill="x", pady=4, ipady=8, padx=5)
                
                # Text Details
                details = ctk.CTkFrame(item_frame, fg_color="transparent")
                details.pack(side="left", padx=15)
                
                plan_name = plan['nama_rencana'] if plan['nama_rencana'] else f"Nongkrong #{plan['id']}"
                CustomLabel(details, text=plan_name, font=FONTS["body_bold"]).pack(anchor="w")
                
                # Format Date nicely
                date_obj = datetime.strptime(plan['tanggal'], "%Y-%m-%d")
                formatted_date = date_obj.strftime("%d %B %Y")
                
                friends_lbl = "Solo Hangout" if plan['jumlah_teman'] == 0 else f"Bersama {plan['jumlah_teman']} teman"
                MutedLabel(details, text=f"{formatted_date} • {friends_lbl}").pack(anchor="w")
                
                # Right elements: budget, total, action
                right_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
                right_frame.pack(side="right", padx=15)
                
                cost_text = format_rupiah(plan['total_cost'])
                status_color = COLORS["success"]
                if plan['total_cost'] > plan['budget']:
                    status_color = COLORS["danger"]
                
                CustomLabel(right_frame, text=cost_text, font=FONTS["body_bold"], text_color=status_color).pack(side="left", padx=(0, 20))
                
                # Status tag
                status_text = plan['status'].upper()
                tag_bg = "#064E3B" if plan['status'] == 'selesai' else "#7F1D1D" if plan['status'] == 'dibatalkan' else "#1E3A8A"
                tag_fg = "#A7F3D0" if plan['status'] == 'selesai' else "#FCA5A5" if plan['status'] == 'dibatalkan' else "#BFDBFE"
                
                status_tag = ctk.CTkLabel(right_frame, text=status_text, font=FONTS["caption_bold"],
                                          fg_color=tag_bg, text_color=tag_fg, corner_radius=4, width=65, height=20)
                status_tag.pack(side="left", padx=(0, 15))
                
                # Action Button to Detail Plan
                pid = plan['id']
                PrimaryButton(right_frame, text="Detail", width=60, height=24, font=FONTS["caption_bold"],
                              command=lambda p_id=pid: self.switch_view("detail_rencana", p_id)).pack(side="left")
                
        # 3. Sidebar Panel (Right Column)
        right_panel = ctk.CTkFrame(self, fg_color="transparent")
        right_panel.grid(row=1, column=1, padx=(15, 30), pady=15, sticky="nsew")
        right_panel.grid_columnconfigure(0, weight=1)
        
        # Budget Health Score Card
        health_card = CardFrame(right_panel)
        health_card.pack(fill="x", pady=(0, 20), ipady=10)
        
        SubtitleLabel(health_card, text="Kesehatan Finansial").pack(anchor="w", padx=20, pady=(15, 5))
        MutedLabel(health_card, text="Berdasarkan tren & pengeluaran bulan ini").pack(anchor="w", padx=20, pady=(0, 15))
        
        # Gauge Visual
        gauge_canvas = ctk.CTkCanvas(health_card, width=180, height=140, bg=COLORS["bg_card"], highlightthickness=0)
        gauge_canvas.pack(pady=5)
        
        # Draw background arc
        gauge_canvas.create_arc(20, 15, 160, 155, start=180, extent=-180, width=16, outline="#1E293B", style="arc")
        
        # Determine color of score
        if health_score < 40:
            score_color = COLORS["danger"]
        elif health_score < 70:
            score_color = COLORS["warning"]
        else:
            score_color = COLORS["success"]
            
        # Draw score arc
        extent_val = -180 * (health_score / 100.0)
        gauge_canvas.create_arc(20, 15, 160, 155, start=180, extent=extent_val, width=16, outline=score_color, style="arc")
        
        # Text inside gauge
        gauge_canvas.create_text(90, 80, text=str(health_score), fill=COLORS["text_main"], font=("Segoe UI", 36, "bold"))
        gauge_canvas.create_text(90, 115, text="SKOR KESEHATAN", fill=COLORS["text_muted"], font=FONTS["caption_bold"])
        
        # Recommendation preview text
        score_db = planner.get_saved_budget_health_score(self.user['id'], current_month)
        rec_msg = score_db['breakdown'].get('message', '') if score_db else ""
        
        rec_container = ctk.CTkFrame(health_card, fg_color="#1E293B", corner_radius=8)
        rec_container.pack(fill="x", padx=15, pady=10, ipady=5)
        
        rec_lbl = CustomLabel(rec_container, text=rec_msg, font=FONTS["caption"], justify="center", wraplength=300)
        rec_lbl.pack(padx=10, pady=8)
        
        SecondaryButton(health_card, text="Analisis Detail Skor", 
                        command=lambda: self.switch_view("detail_score", current_month)).pack(pady=5, padx=20, fill="x")
        
        # Quick Stats Overview
        stats_card = CardFrame(right_panel)
        stats_card.pack(fill="both", expand=True)
        
        SubtitleLabel(stats_card, text="Sekilas Statistik").pack(anchor="w", padx=20, pady=(15, 10))
        
        stats_data = planner.get_stats_data(self.user['id'])
        
        # Row layout for stats summary
        stats_row1 = ctk.CTkFrame(stats_card, fg_color="transparent")
        stats_row1.pack(fill="x", padx=20, pady=5)
        MutedLabel(stats_row1, text="Total Pengeluaran Historis:").pack(side="left")
        CustomLabel(stats_row1, text=format_rupiah(stats_data['total_spent']), font=FONTS["body_bold"]).pack(side="right")
        
        stats_row2 = ctk.CTkFrame(stats_card, fg_color="transparent")
        stats_row2.pack(fill="x", padx=20, pady=5)
        MutedLabel(stats_row2, text="Total Sesi Nongkrong:").pack(side="left")
        CustomLabel(stats_row2, text=f"{stats_data['num_hangouts']} kali", font=FONTS["body_bold"]).pack(side="right")
        
        stats_row3 = ctk.CTkFrame(stats_card, fg_color="transparent")
        stats_row3.pack(fill="x", padx=20, pady=5)
        MutedLabel(stats_row3, text="Rata-rata per Hangout:").pack(side="left")
        CustomLabel(stats_row3, text=format_rupiah(stats_data['avg_per_hangout']), font=FONTS["body_bold"]).pack(side="right")
        
        # Mini tip
        tip_box = ctk.CTkFrame(stats_card, fg_color="#1E3A8A", corner_radius=6)
        tip_box.pack(fill="x", padx=15, pady=(15, 10), ipady=5)
        CustomLabel(tip_box, text="💡 Tips Finansial", font=FONTS["caption_bold"], text_color="#93C5FD").pack(anchor="w", padx=10, pady=(5, 2))
        
        tips = [
            "Cobalah membagi tagihan secara merata agar menghemat pengeluaran.",
            "Nongkrong di awal bulan cenderung membuat pengeluaran membengkak.",
            "Emoji 😍 bisa meningkatkan pengeluaran hingga 35%. Waspadai mood belanja!",
            "Selalu sisihkan budget nongkrong sebelum merencanakan tempat."
        ]
        selected_tip = random.choice(tips)
        CustomLabel(tip_box, text=selected_tip, font=FONTS["caption"], text_color="#BFDBFE", wraplength=280).pack(anchor="w", padx=10, pady=(0, 5))
        
        # 4. Matplotlib charts render
        self.render_charts(self)

    def render_charts(self, parent_frame):
        # Card container for charts
        charts_card = CardFrame(parent_frame)
        charts_card.grid(row=2, column=0, columnspan=2, padx=30, pady=(10, 25), sticky="ew")
        charts_card.grid_columnconfigure(0, weight=1)
        charts_card.grid_columnconfigure(1, weight=1)
        
        # Subtitles for charts
        left_title_frame = ctk.CTkFrame(charts_card, fg_color="transparent")
        left_title_frame.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")
        SubtitleLabel(left_title_frame, text="Tren Pengeluaran Bulanan (Rp)").pack(anchor="w")
        
        right_title_frame = ctk.CTkFrame(charts_card, fg_color="transparent")
        right_title_frame.grid(row=0, column=1, padx=20, pady=(15, 5), sticky="w")
        SubtitleLabel(right_title_frame, text="Distribusi Pengeluaran Kategori").pack(anchor="w")
        
        # Canvas frames
        canvas_left_frame = ctk.CTkFrame(charts_card, fg_color="transparent", height=180)
        canvas_left_frame.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
        
        canvas_right_frame = ctk.CTkFrame(charts_card, fg_color="transparent", height=180)
        canvas_right_frame.grid(row=1, column=1, padx=15, pady=(0, 15), sticky="nsew")
        
        stats = planner.get_stats_data(self.user['id'])
        
        # Theme config
        plt.style.use('dark_background')
        
        # Chart 1: Monthly Spending (Bar)
        monthly_data = stats['monthly_spending']
        fig1, ax1 = plt.subplots(figsize=(4.5, 1.8), dpi=100)
        fig1.patch.set_facecolor('#13203A')
        ax1.set_facecolor('#13203A')
        
        if not monthly_data:
            ax1.text(0.5, 0.5, 'Belum ada data bulanan.', horizontalalignment='center', verticalalignment='center', color=COLORS["text_muted"])
        else:
            months = [d['month'] for d in monthly_data]
            totals = [d['total'] for d in monthly_data]
            bars = ax1.bar(months, totals, color=COLORS["primary"], width=0.4, edgecolor='#1E293B', linewidth=1)
            ax1.set_ylabel("Rupiah", fontsize=8, color=COLORS["text_muted"])
            ax1.tick_params(axis='both', labelsize=8, colors=COLORS["text_muted"])
            ax1.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: f"{int(x)/1000:.0f}k" if x >= 1000 else str(int(x))))
            
        fig1.tight_layout()
        canvas1 = FigureCanvasTkAgg(fig1, canvas_left_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True)
        
        # Chart 2: Category Spending (Pie)
        category_data = stats['category_spending']
        fig2, ax2 = plt.subplots(figsize=(4.5, 1.8), dpi=100)
        fig2.patch.set_facecolor('#13203A')
        ax2.set_facecolor('#13203A')
        
        self.figures = [fig1, fig2]
        
        if not category_data:
            ax2.text(0.5, 0.5, 'Belum ada data kategori.', horizontalalignment='center', verticalalignment='center', color=COLORS["text_muted"])
        else:
            labels = [d['category'] for d in category_data]
            totals = [d['total'] for d in category_data]
            colors_list = [COLORS["primary"], COLORS["success"], COLORS["warning"], COLORS["danger"], "#8B5CF6", "#EC4899"]
            
            wedges, texts, autotexts = ax2.pie(
                totals, 
                labels=labels, 
                autopct='%1.1f%%', 
                startangle=140, 
                colors=colors_list[:len(labels)],
                textprops=dict(color=COLORS["text_muted"], fontsize=8)
            )
            for at in autotexts:
                at.set_color(COLORS["text_main"])
                at.set_fontsize(8)
                
        fig2.tight_layout()
        canvas2 = FigureCanvasTkAgg(fig2, canvas_right_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True)

    def destroy(self):
        # Prevent memory leaks with pyplot
        try:
            for fig in self.figures:
                fig.clear()
                plt.close(fig)
        except Exception:
            pass
        super().destroy()
