import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
import csv
import os


# ─────────────────────────────────────────────────────────────
#  STOCK PRICE DICTIONARY  (Key Concept: dictionary)
#  Format: { "SYMBOL": price }
# ─────────────────────────────────────────────────────────────
STOCK_PRICES = {
    "AAPL":     180.00,
    "TSLA":     250.00,
    "GOOGL":    140.00,
    "MSFT":     415.00,
    "AMZN":     185.00,
    "NVDA":     875.00,
    "META":     500.00,
    "NFLX":     620.00,
    "RELIANCE": 2900.00,
    "TCS":      3800.00,
    "INFY":     1500.00,
    "WIPRO":    450.00,
}

COMPANY_NAMES = {
    "AAPL": "Apple Inc.",       "TSLA": "Tesla Inc.",
    "GOOGL": "Alphabet",        "MSFT": "Microsoft",
    "AMZN": "Amazon",           "NVDA": "NVIDIA",
    "META": "Meta Platforms",   "NFLX": "Netflix",
    "RELIANCE": "Reliance Ind.","TCS": "Tata Consultancy",
    "INFY": "Infosys",          "WIPRO": "Wipro",
}

# ── Theme colours ─────────────────────────────────────────────
BG_DARK   = "#0d2b2b"   # deep teal-black (window bg)
BG_MID    = "#133a3a"   # section frames
BG_PANEL  = "#1a4f4f"   # input panel
ACCENT    = "#f59e0b"   # amber accent (buttons, highlights)
ACCENT2   = "#0ea5e9"   # sky-blue secondary accent
TEXT_MAIN = "#f0fdf4"   # near-white
TEXT_DIM  = "#94a3b8"   # muted slate
ENTRY_BG  = "#0f3535"
LIST_SEL  = "#f59e0b"


# ─────────────────────────────────────────────────────────────
#  HELPER
# ─────────────────────────────────────────────────────────────
def calculate_investment(symbol: str, quantity: int) -> float:
    """Return total value for a given stock symbol and quantity."""
    price = STOCK_PRICES.get(symbol.upper(), 0)
    return price * quantity                          # Basic arithmetic


# ─────────────────────────────────────────────────────────────
#  MAIN APPLICATION CLASS
# ─────────────────────────────────────────────────────────────
class StockTrackerApp:
    def _init_(self, root: tk.Tk):
        self.root = root
        self.root.title("Stock Portfolio Tracker  —  Option 2")
        self.root.geometry("700x640")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(False, False)

        # Portfolio data: list of dicts
        self.portfolio: list[dict] = []

        self._build_header()
        self._build_available_symbols()
        self._build_input_section()
        self._build_listbox_section()
        self._build_total_section()
        self._build_buttons()
        self._build_footer()

    # ── Layout builders ──────────────────────────────────────

    def _build_header(self):
        header = tk.Frame(self.root, bg=ACCENT, height=58)
        header.pack(fill=tk.X)
        tk.Label(
            header,
            text="📊  STOCK PORTFOLIO TRACKER",
            font=("Helvetica", 17, "bold"),
            bg=ACCENT,
            fg="#0d2b2b",
        ).pack(pady=14)

    def _build_available_symbols(self):
        """Show a read-only list of valid symbols so user knows what to type."""
        frame = tk.LabelFrame(
            self.root,
            text="  Available Symbols (type any below)  ",
            font=("Arial", 9, "bold"),
            bg=BG_DARK, fg=TEXT_DIM,
            bd=1, relief=tk.GROOVE,
        )
        frame.pack(fill=tk.X, padx=14, pady=(10, 0))

        symbols_text = "   ".join(sorted(STOCK_PRICES.keys()))
        tk.Label(
            frame,
            text=symbols_text,
            font=("Courier", 10),
            bg=BG_DARK,
            fg=ACCENT,
            wraplength=650,
            justify=tk.LEFT,
        ).pack(anchor="w", padx=10, pady=6)

    def _build_input_section(self):
        """
        Input area — user TYPES stock symbol and quantity manually.
        (No dropdown / combobox — satisfies Option 2 requirement.)
        """
        frame = tk.LabelFrame(
            self.root,
            text="  Add Stock  ",
            font=("Arial", 11, "bold"),
            bg=BG_PANEL, fg=TEXT_DIM,
            bd=1, relief=tk.GROOVE,
        )
        frame.pack(fill=tk.X, padx=14, pady=(8, 4))

        inner = tk.Frame(frame, bg=BG_PANEL)
        inner.pack(padx=12, pady=10, fill=tk.X)

        # ── Stock symbol — manual text entry ──────────────────
        tk.Label(inner, text="Stock Symbol:", font=("Arial", 11),
                 bg=BG_PANEL, fg=TEXT_MAIN).grid(row=0, column=0, sticky="w", padx=(0, 8))

        self.symbol_var = tk.StringVar()
        sym_entry = tk.Entry(
            inner,
            textvariable=self.symbol_var,
            font=("Arial", 13, "bold"),
            bg=ENTRY_BG, fg=ACCENT,
            insertbackground=ACCENT,
            relief=tk.FLAT,
            width=10,
        )
        sym_entry.grid(row=0, column=1, ipady=6, padx=(0, 24))
        sym_entry.bind("<Return>", lambda e: self.qty_entry.focus())

        # ── Quantity — manual text entry ──────────────────────
        tk.Label(inner, text="Quantity:", font=("Arial", 11),
                 bg=BG_PANEL, fg=TEXT_MAIN).grid(row=0, column=2, sticky="w", padx=(0, 8))

        self.qty_var = tk.StringVar()
        self.qty_entry = tk.Entry(
            inner,
            textvariable=self.qty_var,
            font=("Arial", 13),
            bg=ENTRY_BG, fg=TEXT_MAIN,
            insertbackground="white",
            relief=tk.FLAT,
            width=8,
        )
        self.qty_entry.grid(row=0, column=3, ipady=6, padx=(0, 20))
        self.qty_entry.bind("<Return>", self._add_stock)

        # ── Add button ────────────────────────────────────────
        tk.Button(
            inner,
            text="＋  Add Stock",
            font=("Arial", 11, "bold"),
            bg=ACCENT2, fg="white",
            activebackground="#0284c7",
            relief=tk.FLAT,
            cursor="hand2",
            padx=10, pady=4,
            command=self._add_stock,
        ).grid(row=0, column=4)

    def _build_listbox_section(self):
        """
        Listbox (not Treeview) to display portfolio holdings.
        Satisfies Option 2 requirement.
        """
        outer = tk.Frame(self.root, bg=BG_DARK)
        outer.pack(fill=tk.BOTH, expand=True, padx=14, pady=6)

        # Column header row (plain labels — Listbox has no built-in headers)
        header_frame = tk.Frame(outer, bg=BG_MID)
        header_frame.pack(fill=tk.X)
        headers = [("SYMBOL", 80), ("COMPANY", 200), ("QTY", 60),
                   ("PRICE", 110), ("TOTAL VALUE", 120)]
        for h_text, w in headers:
            tk.Label(
                header_frame,
                text=h_text,
                font=("Arial", 10, "bold"),
                bg=BG_MID, fg=TEXT_DIM,
                width=w // 8,          # approximate char width
                anchor="w",
            ).pack(side=tk.LEFT, padx=4, pady=4)

        # Listbox + scrollbar
        lb_frame = tk.Frame(outer, bg=BG_DARK)
        lb_frame.pack(fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(
            lb_frame,
            font=("Courier", 11),
            bg=BG_MID,
            fg=TEXT_MAIN,
            selectbackground=LIST_SEL,
            selectforeground=BG_DARK,
            activestyle="none",
            relief=tk.FLAT,
            bd=0,
            height=10,
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        sb = tk.Scrollbar(lb_frame, orient=tk.VERTICAL,
                          command=self.listbox.yview, bg=BG_DARK)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.configure(yscrollcommand=sb.set)

    def _build_total_section(self):
        """
        Total display + dedicated Calculate Total button.
        Total is NOT updated automatically — user clicks the button.
        Satisfies Option 2 requirement.
        """
        frame = tk.Frame(self.root, bg=BG_MID)
        frame.pack(fill=tk.X, padx=14, pady=4)

        # Calculate Total button (separate, as required)
        tk.Button(
            frame,
            text="🧮  Calculate Total",
            font=("Arial", 12, "bold"),
            bg=ACCENT, fg=BG_DARK,
            activebackground="#d97706",
            relief=tk.FLAT,
            cursor="hand2",
            padx=14, pady=6,
            command=self._calculate_total,
        ).pack(side=tk.LEFT, padx=14, pady=10)

        tk.Label(frame, text="Portfolio Value:",
                 font=("Arial", 12, "bold"),
                 bg=BG_MID, fg=TEXT_DIM).pack(side=tk.LEFT, padx=(20, 8))

        self.total_var = tk.StringVar(value="—  (press Calculate)")
        tk.Label(
            frame,
            textvariable=self.total_var,
            font=("Helvetica", 18, "bold"),
            bg=BG_MID, fg=ACCENT,
        ).pack(side=tk.LEFT)

        self.holding_count_var = tk.StringVar(value="")
        tk.Label(frame, textvariable=self.holding_count_var,
                 font=("Arial", 10), bg=BG_MID, fg=TEXT_DIM).pack(side=tk.LEFT, padx=10)

    def _build_buttons(self):
        """Action buttons: Save TXT, Save CSV, Remove Selected, Clear All."""
        frame = tk.Frame(self.root, bg=BG_DARK)
        frame.pack(fill=tk.X, padx=14, pady=(2, 6))

        buttons = [
            ("💾 Save TXT",        "#3b82f6", "#2563eb", self._save_txt),
            ("📊 Save CSV",        "#8b5cf6", "#7c3aed", self._save_csv),
            ("🗑️ Remove Selected", "#ef4444", "#dc2626", self._remove_selected),
            ("✖️ Clear All",       "#475569", "#334155", self._clear_all),
        ]
        for text, bg, active, cmd in buttons:
            tk.Button(
                frame,
                text=text,
                font=("Arial", 10, "bold"),
                bg=bg, fg="white",
                activebackground=active,
                activeforeground="white",
                relief=tk.FLAT,
                cursor="hand2",
                padx=10, pady=5,
                command=cmd,
            ).pack(side=tk.LEFT, padx=(0, 8))

    def _build_footer(self):
        tk.Label(
            self.root,
            text="Task 2 · Option 2 GUI  |  Python & Tkinter  |  Prices hardcoded for demo",
            font=("Arial", 8),
            bg=BG_MID, fg="#475569",
            pady=4,
        ).pack(fill=tk.X, side=tk.BOTTOM)

    # ── Core Logic ───────────────────────────────────────────

    def _add_stock(self, event=None):
        """
        Read symbol + quantity from Entry widgets, validate,
        calculate value, and append to Listbox.
        Key Concepts: dictionary lookup, arithmetic, input/output.
        """
        symbol   = self.symbol_var.get().upper().strip()
        qty_text = self.qty_var.get().strip()

        # ── Validation ────────────────────────────────────────
        if not symbol:
            messagebox.showwarning("Missing Symbol", "Please type a stock symbol.")
            return
        if symbol not in STOCK_PRICES:
            valid = ", ".join(sorted(STOCK_PRICES.keys()))
            messagebox.showerror(
                "Unknown Symbol",
                f"'{symbol}' is not recognised.\n\nValid symbols:\n{valid}",
            )
            return
        if not qty_text:
            messagebox.showwarning("Missing Quantity", "Please enter a quantity.")
            return
        if not qty_text.isdigit() or int(qty_text) <= 0:
            messagebox.showerror("Invalid Quantity",
                                 "Quantity must be a positive whole number.")
            return

        quantity = int(qty_text)                              # Input
        price    = STOCK_PRICES[symbol]                       # Dictionary lookup
        value    = calculate_investment(symbol, quantity)     # Arithmetic
        label    = COMPANY_NAMES.get(symbol, symbol)

        # Add to internal portfolio list
        self.portfolio.append({
            "symbol": symbol, "label": label,
            "qty": quantity, "price": price, "value": value,
        })

        # Build a formatted string for the Listbox row (Output)
        row_str = (
            f"{symbol:<8}  {label:<20}  "
            f"{quantity:>5}  {price:>12,.2f}  {value:>14,.2f}"
        )
        self.listbox.insert(tk.END, row_str)

        # Alternate row colours for readability
        idx = self.listbox.size() - 1
        self.listbox.itemconfig(idx, bg="#1a4f4f" if idx % 2 == 0 else "#133a3a")

        # Reset inputs; remind user to press Calculate
        self.symbol_var.set("")
        self.qty_var.set("")
        self.total_var.set("—  (press Calculate)")
        self.holding_count_var.set("")
        self.symbol_var.set("")

    def _calculate_total(self):
        """
        Separately calculates and displays the portfolio total.
        Called ONLY when user clicks 'Calculate Total'.
        Key Concept: arithmetic, output.
        """
        if not self.portfolio:
            messagebox.showinfo("Empty Portfolio", "Add some stocks first.")
            return

        total = sum(row["value"] for row in self.portfolio)   # Arithmetic
        self.total_var.set(f"{total:,.2f}")
        n = len(self.portfolio)
        self.holding_count_var.set(f"({n} holding{'s' if n != 1 else ''})")

    def _remove_selected(self):
        """Remove the highlighted Listbox row from the portfolio."""
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showinfo("Nothing Selected",
                                "Click a stock row in the list to select it first.")
            return
        # Remove in reverse order so indices stay valid
        for idx in reversed(selected):
            self.listbox.delete(idx)
            self.portfolio.pop(idx)

        # Reset total display since it's now stale
        self.total_var.set("—  (press Calculate)")
        self.holding_count_var.set("")

    def _clear_all(self):
        """Clear the entire portfolio."""
        if not self.portfolio:
            return
        if messagebox.askyesno("Clear Portfolio", "Remove all holdings?"):
            self.listbox.delete(0, tk.END)
            self.portfolio.clear()
            self.total_var.set("—  (press Calculate)")
            self.holding_count_var.set("")

    # ── File Handling (Key Concept: file handling) ───────────

    def _save_txt(self):
        """Save portfolio report as a plain .txt file."""
        if not self.portfolio:
            messagebox.showinfo("Nothing to Save", "Add some stocks first.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            title="Save Portfolio as TXT",
        )
        if not path:
            return

        total = sum(r["value"] for r in self.portfolio)
        now   = datetime.now().strftime("%d-%m-%Y  %I:%M %p")

        with open(path, "w", encoding="utf-8") as f:         # File handling
            f.write("=" * 54 + "\n")
            f.write("        STOCK PORTFOLIO REPORT\n")
            f.write(f"        Generated: {now}\n")
            f.write("=" * 54 + "\n\n")
            f.write(f"{'Symbol':<10} {'Qty':>6}  {'Price':>12}  {'Value':>14}\n")
            f.write("-" * 50 + "\n")
            for r in self.portfolio:
                f.write(
                    f"{r['symbol']:<10} {r['qty']:>6}  "
                    f"{r['price']:>12,.2f}  {r['value']:>14,.2f}\n"
                )
            f.write("-" * 50 + "\n")
            f.write(f"{'TOTAL':>38}  {total:>14,.2f}\n\n")
            f.write("Prices are hardcoded for demo purposes.\n")

        messagebox.showinfo("Saved", f"Report saved:\n{os.path.basename(path)}")

    def _save_csv(self):
        """Save portfolio as a .csv file."""
        if not self.portfolio:
            messagebox.showinfo("Nothing to Save", "Add some stocks first.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title="Save Portfolio as CSV",
        )
        if not path:
            return

        total = sum(r["value"] for r in self.portfolio)

        with open(path, "w", newline="", encoding="utf-8") as f:  # File handling
            writer = csv.writer(f)
            writer.writerow(["Symbol", "Company", "Quantity", "Price", "Total Value"])
            for r in self.portfolio:
                writer.writerow([r["symbol"], r["label"], r["qty"],
                                  f"{r['price']:.2f}", f"{r['value']:.2f}"])
            writer.writerow([])
            writer.writerow(["", "", "", "TOTAL", f"{total:.2f}"])

        messagebox.showinfo("Saved", f"CSV saved:\n{os.path.basename(path)}")


# ─────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────
if _name_ == "_main_":
    root = tk.Tk()
    StockTrackerApp(root)
    root.mainloop()
