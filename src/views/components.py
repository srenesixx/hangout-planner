import customtkinter as ctk

# Color Palette defined by PRD
COLORS = {
    "bg_main": "#0B1220",
    "bg_card": "#13203A",
    "primary": "#3B82F6",
    "primary_hover": "#1D4ED8",
    "text_muted": "#94A3B8",
    "text_main": "#F8FAFC",
    "success": "#22C55E",
    "warning": "#F59E0B",
    "danger": "#EF4444"
}

# Typography
FONTS = {
    "title": ("Segoe UI", 24, "bold"),
    "subtitle": ("Segoe UI", 16, "bold"),
    "body": ("Segoe UI", 13, "normal"),
    "body_bold": ("Segoe UI", 13, "bold"),
    "caption": ("Segoe UI", 11, "normal"),
    "caption_bold": ("Segoe UI", 11, "bold")
}

def format_rupiah(value: int | float) -> str:
    """Formats a number into Indonesian Rupiah format (e.g. Rp 150.000)."""
    try:
        return f"Rp {int(value):,}".replace(",", ".")
    except (ValueError, TypeError):
        return "Rp 0"

def parse_rupiah(val_str: str) -> int:
    """Parses a rupiah input string back to integer."""
    clean_str = val_str.replace("Rp", "").replace(".", "").replace(",", "").replace(" ", "").strip()
    try:
        return int(clean_str) if clean_str else 0
    except ValueError:
        return 0

class CardFrame(ctk.CTkFrame):
    """A styled card container for group of widgets."""
    def __init__(self, master, **kwargs):
        super().__init__(
            master, 
            fg_color=COLORS["bg_card"],
            corner_radius=12,
            border_color="#1E293B",
            border_width=1,
            **kwargs
        )

class PrimaryButton(ctk.CTkButton):
    """A styled primary button with blue accent."""
    def __init__(self, master, **kwargs):
        height = kwargs.pop("height", 36)
        font = kwargs.pop("font", FONTS["body_bold"])
        super().__init__(
            master,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color=COLORS["text_main"],
            font=font,
            corner_radius=8,
            height=height,
            **kwargs
        )

class SecondaryButton(ctk.CTkButton):
    """A styled secondary button with a outline design or muted color."""
    def __init__(self, master, **kwargs):
        height = kwargs.pop("height", 36)
        font = kwargs.pop("font", FONTS["body_bold"])
        super().__init__(
            master,
            fg_color="transparent",
            border_color=COLORS["primary"],
            border_width=1.5,
            hover_color="#1E293B",
            text_color=COLORS["primary"],
            font=font,
            corner_radius=8,
            height=height,
            **kwargs
        )

class DangerButton(ctk.CTkButton):
    """A styled button for delete/danger actions."""
    def __init__(self, master, **kwargs):
        height = kwargs.pop("height", 36)
        font = kwargs.pop("font", FONTS["body_bold"])
        super().__init__(
            master,
            fg_color=COLORS["danger"],
            hover_color="#DC2626",
            text_color=COLORS["text_main"],
            font=font,
            corner_radius=8,
            height=height,
            **kwargs
        )

class SuccessButton(ctk.CTkButton):
    """A styled button for success/save actions."""
    def __init__(self, master, **kwargs):
        height = kwargs.pop("height", 36)
        font = kwargs.pop("font", FONTS["body_bold"])
        super().__init__(
            master,
            fg_color=COLORS["success"],
            hover_color="#16A34A",
            text_color=COLORS["text_main"],
            font=font,
            corner_radius=8,
            height=height,
            **kwargs
        )

class CustomEntry(ctk.CTkEntry):
    """A styled text entry field."""
    def __init__(self, master, **kwargs):
        height = kwargs.pop("height", 36)
        super().__init__(
            master,
            fg_color=COLORS["bg_main"],
            text_color=COLORS["text_main"],
            border_color="#334155",
            placeholder_text_color=COLORS["text_muted"],
            font=FONTS["body"],
            corner_radius=8,
            height=height,
            **kwargs
        )

class CustomLabel(ctk.CTkLabel):
    """A wrapper for label with default body font and color."""
    def __init__(self, master, **kwargs):
        # Allow custom font/color overrides, otherwise use defaults
        font = kwargs.pop("font", FONTS["body"])
        text_color = kwargs.pop("text_color", COLORS["text_main"])
        super().__init__(
            master,
            font=font,
            text_color=text_color,
            **kwargs
        )

class HeaderLabel(CustomLabel):
    """A large title label."""
    def __init__(self, master, **kwargs):
        font = kwargs.pop("font", FONTS["title"])
        text_color = kwargs.pop("text_color", COLORS["text_main"])
        super().__init__(
            master,
            font=font,
            text_color=text_color,
            **kwargs
        )

class SubtitleLabel(CustomLabel):
    """A medium subtitle label."""
    def __init__(self, master, **kwargs):
        font = kwargs.pop("font", FONTS["subtitle"])
        text_color = kwargs.pop("text_color", COLORS["text_main"])
        super().__init__(
            master,
            font=font,
            text_color=text_color,
            **kwargs
        )

class MutedLabel(CustomLabel):
    """A label for muted/secondary text."""
    def __init__(self, master, **kwargs):
        font = kwargs.pop("font", FONTS["caption"])
        text_color = kwargs.pop("text_color", COLORS["text_muted"])
        super().__init__(
            master,
            font=font,
            text_color=text_color,
            **kwargs
        )

class StatusLabel(CustomLabel):
    """A label that colorizes based on status (aman, waspada, bahaya)."""
    def __init__(self, master, status_type="info", **kwargs):
        # status_type: 'success', 'warning', 'danger', 'info'
        color = COLORS["text_main"]
        if status_type == "success":
            color = COLORS["success"]
        elif status_type == "warning":
            color = COLORS["warning"]
        elif status_type == "danger":
            color = COLORS["danger"]
        elif status_type == "info":
            color = COLORS["primary"]
            
        font = kwargs.pop("font", FONTS["body_bold"])
        text_color = kwargs.pop("text_color", color)
        super().__init__(
            master,
            text_color=text_color,
            font=font,
            **kwargs
        )
