
import tkinter as tk
from tkinter import ttk

from .generator import generate_password
from .strength import analyze_password


class PasswordGeneratorApp:
    """Main SecurePass desktop application."""

    BACKGROUND = "#0F172A"
    CARD = "#1E293B"
    INPUT = "#334155"
    TEXT = "#F8FAFC"
    MUTED = "#94A3B8"
    ACCENT = "#0EA5E9"

    def __init__(self, root):
        self.root = root
        self.root.title("SecurePass | Password Generator")
        self.root.geometry("620x700")
        self.root.minsize(540, 650)
        self.root.configure(bg=self.BACKGROUND)

        self.password_var = tk.StringVar()
        self.length_var = tk.IntVar(value=16)

        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)

        self.build_interface()
        self.update_strength()

    def build_interface(self):
        """Create all interface components."""

        main = tk.Frame(self.root, bg=self.BACKGROUND)
        main.pack(fill="both", expand=True, padx=35, pady=25)

        # Header
        tk.Label(
            main,
            text="SecurePass",
            font=("Segoe UI", 27, "bold"),
            bg=self.BACKGROUND,
            fg=self.TEXT
        ).pack()

        tk.Label(
            main,
            text="CREATE STRONG AND SECURE PASSWORDS",
            font=("Segoe UI", 9, "bold"),
            bg=self.BACKGROUND,
            fg=self.ACCENT
        ).pack(pady=(2, 25))

        # Password display card
        password_card = tk.Frame(
            main, bg=self.CARD, padx=20, pady=18
        )
        password_card.pack(fill="x", pady=(0, 18))

        tk.Label(
            password_card,
            text="YOUR PASSWORD",
            font=("Segoe UI", 9, "bold"),
            bg=self.CARD,
            fg=self.MUTED
        ).pack(anchor="w")

        password_row = tk.Frame(password_card, bg=self.CARD)
        password_row.pack(fill="x", pady=(10, 5))

        self.password_entry = tk.Entry(
            password_row,
            textvariable=self.password_var,
            font=("Consolas", 15),
            bg=self.INPUT,
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief="flat",
            bd=0
        )
        self.password_entry.pack(
            side="left", fill="x", expand=True, ipady=12, padx=(0, 10)
        )

        self.copy_button = tk.Button(
            password_row,
            text="Copy",
            command=self.copy_password,
            font=("Segoe UI", 10, "bold"),
            bg=self.ACCENT,
            fg="white",
            activebackground="#0284C7",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=9
        )
        self.copy_button.pack(side="right")

        self.copy_status = tk.Label(
            password_card,
            text="",
            font=("Segoe UI", 9),
            bg=self.CARD,
            fg="#34D399"
        )
        self.copy_status.pack(anchor="w")

        self.password_entry.bind(
            "<KeyRelease>", lambda event: self.update_strength()
        )

        # Strength analyzer card
        strength_card = tk.Frame(
            main, bg=self.CARD, padx=20, pady=18
        )
        strength_card.pack(fill="x", pady=(0, 18))

        strength_header = tk.Frame(strength_card, bg=self.CARD)
        strength_header.pack(fill="x")

        tk.Label(
            strength_header,
            text="Password strength",
            font=("Segoe UI", 11, "bold"),
            bg=self.CARD,
            fg=self.TEXT
        ).pack(side="left")

        self.strength_label = tk.Label(
            strength_header,
            text="Not analyzed",
            font=("Segoe UI", 10, "bold"),
            bg=self.CARD,
            fg=self.MUTED
        )
        self.strength_label.pack(side="right")

        self.strength_progress = ttk.Progressbar(
            strength_card,
            maximum=100,
            mode="determinate",
            length=400,
            style="Strength.Horizontal.TProgressbar"
        )
        self.strength_progress.pack(fill="x", pady=15)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Strength.Horizontal.TProgressbar",
            troughcolor=self.INPUT,
            background="#34D399",
            bordercolor=self.CARD,
            lightcolor="#34D399",
            darkcolor="#34D399"
        )

        self.suggestions_label = tk.Label(
            strength_card,
            text="",
            font=("Segoe UI", 9),
            bg=self.CARD,
            fg=self.MUTED,
            justify="left",
            wraplength=480
        )
        self.suggestions_label.pack(anchor="w")

        # Settings card
        settings_card = tk.Frame(
            main, bg=self.CARD, padx=20, pady=18
        )
        settings_card.pack(fill="x", pady=(0, 18))

        tk.Label(
            settings_card,
            text="Password settings",
            font=("Segoe UI", 12, "bold"),
            bg=self.CARD,
            fg=self.TEXT
        ).pack(anchor="w", pady=(0, 12))

        length_row = tk.Frame(settings_card, bg=self.CARD)
        length_row.pack(fill="x", pady=(0, 12))

        tk.Label(
            length_row,
            text="Password length",
            font=("Segoe UI", 10),
            bg=self.CARD,
            fg=self.TEXT
        ).pack(side="left")

        tk.Spinbox(
            length_row,
            from_=8,
            to=64,
            textvariable=self.length_var,
            width=6,
            font=("Segoe UI", 11),
            bg=self.INPUT,
            fg=self.TEXT,
            buttonbackground=self.INPUT,
            insertbackground=self.TEXT,
            relief="flat"
        ).pack(side="right")

        options = [
            ("Uppercase letters (A-Z)", self.uppercase_var),
            ("Lowercase letters (a-z)", self.lowercase_var),
            ("Numbers (0-9)", self.digits_var),
            ("Symbols (!@#$...)", self.symbols_var)
        ]

        for label, variable in options:
            tk.Checkbutton(
                settings_card,
                text=label,
                variable=variable,
                font=("Segoe UI", 10),
                bg=self.CARD,
                fg=self.TEXT,
                activebackground=self.CARD,
                activeforeground=self.TEXT,
                selectcolor=self.INPUT,
                relief="flat",
                cursor="hand2"
            ).pack(anchor="w", pady=3)

        # Generate button
        tk.Button(
            main,
            text="GENERATE PASSWORD",
            command=self.generate,
            font=("Segoe UI", 11, "bold"),
            bg=self.ACCENT,
            fg="white",
            activebackground="#0284C7",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            pady=13
        ).pack(fill="x")

        tk.Label(
            main,
            text="SecurePass | Built with Python and Tkinter",
            font=("Segoe UI", 8),
            bg=self.BACKGROUND,
            fg=self.MUTED
        ).pack(pady=(18, 0))

    def generate(self):
        """Generate a password using the selected settings."""

        try:
            password = generate_password(
                length=self.length_var.get(),
                use_uppercase=self.uppercase_var.get(),
                use_lowercase=self.lowercase_var.get(),
                use_digits=self.digits_var.get(),
                use_symbols=self.symbols_var.get()
            )

            self.password_var.set(password)
            self.copy_status.config(text="")
            self.update_strength()

        except (ValueError, tk.TclError) as error:
            self.copy_status.config(
                text=str(error),
                fg="#F87171"
            )

    def copy_password(self):
        """Copy the generated password to the clipboard."""

        password = self.password_var.get()

        if not password:
            self.copy_status.config(
                text="Generate a password first.",
                fg="#F87171"
            )
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        self.root.update()

        self.copy_status.config(
            text="Password copied successfully!",
            fg="#34D399"
        )

    def update_strength(self):
        """Analyze the current password and update the strength display."""

        password = self.password_var.get()
        result = analyze_password(password)

        self.strength_progress["value"] = result["score"]

        colors = {
            "Very Weak": "#F87171",
            "Weak": "#F97316",
            "Medium": "#FBBF24",
            "Strong": "#34D399"
        }

        level = result["level"]
        color = colors.get(level, self.MUTED)

        self.strength_label.config(
            text=f"{level} - {result['score']}/100",
            fg=color
        )

        style = ttk.Style()
        style.configure(
            "Strength.Horizontal.TProgressbar",
            background=color,
            lightcolor=color,
            darkcolor=color
        )

        suggestions = result["suggestions"]

        if suggestions:
            text = "Suggestions:\n" + "\n".join(
                f"• {suggestion}" for suggestion in suggestions
            )
        else:
            text = "All criteria satisfied!"

        self.suggestions_label.config(text=text)


def run_app():
    root = tk.Tk()
    PasswordGeneratorApp(root)
    root.mainloop()
