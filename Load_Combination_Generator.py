import re
import tkinter as tk
from tkinter import ttk, messagebox
from itertools import product

class LoadCombinationGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Load Combination Generator")
        self.root.geometry("1400x600+40+40")

        self.create_widgets()
        self.setup_key_navigation()

    def _display_case_name(self, case_name: str) -> str:
        """
        Return a display-friendly case name: strip the trailing '1' suffix for display only.
        Examples:
            'wind1' -> 'wind'
            'dead2' -> 'dead2'
            'live'  -> 'live'
        """
        m = re.match(r"^(.*?)(\d+)$", case_name)
        if m:
            base, num = m.group(1), m.group(2)
            return base if num == "1" else f"{base}{num}"
        return case_name

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        table_container = ttk.Frame(main_frame)
        table_container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(table_container, height=400)
        v_scroll = ttk.Scrollbar(table_container, orient="vertical", command=canvas.yview)
        h_scroll = ttk.Scrollbar(table_container, orient="horizontal", command=canvas.xview)
        canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")

        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

        self.scrollable_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        def configure_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.scrollable_frame.bind("<Configure>", configure_scrollregion)

        self.rows = 14
        self.cols = 12
        self.all_entries = []
        self.grid_positions = {}

        headers = [""] + [f"Case {i}" for i in range(1, self.cols)]
        for col, header in enumerate(headers):
            lbl = ttk.Label(self.scrollable_frame, text=header, font=('Arial', 10, 'bold'))
            lbl.grid(row=0, column=col, padx=5, pady=5, sticky='nsew')

        self.name_entries = []
        for col in range(1, self.cols):
            entry = ttk.Entry(self.scrollable_frame, width=15)
            entry.grid(row=1, column=col, padx=5, pady=5, sticky='nsew')
            self.name_entries.append(entry)
            self.all_entries.append(entry)
            self.grid_positions[entry] = (1, col)

        self.type_combos = []
        load_types = ["Dead", "Live", "Wind", "Seismic", "Snow", "Roof Live", "Dust", "Temperature", "Accidental",
                      "Crane Hook", "Mass", "None"]
        for col in range(1, self.cols):
            combo = ttk.Combobox(self.scrollable_frame, values=load_types, state="readonly", width=13)
            combo.current(0)
            combo.grid(row=2, column=col, padx=5, pady=5, sticky='nsew')
            self.type_combos.append(combo)
            self.grid_positions[combo] = (2, col)
            self.all_entries.append(combo)

        self.coeff_entries = []
        for row in range(3, self.rows - 1):
            row_entries = []
            ttk.Label(self.scrollable_frame, text=f"Comb {row - 2}").grid(row=row, column=0, padx=5, pady=5)

            for col in range(1, self.cols):
                entry = ttk.Entry(self.scrollable_frame, width=15)
                entry.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
                row_entries.append(entry)
                self.all_entries.append(entry)
                self.grid_positions[entry] = (row, col)
            self.coeff_entries.append(row_entries)

        ttk.Label(self.scrollable_frame, text="Subcase").grid(row=self.rows - 1, column=0, padx=5, pady=5, sticky='nsew')
        self.subcase_entries = []
        for col in range(1, self.cols):
            entry = tk.Entry(self.scrollable_frame, width=15, bg="light green")
            entry.grid(row=self.rows - 1, column=col, padx=5, pady=5, sticky='nsew')
            self.subcase_entries.append(entry)
            self.all_entries.append(entry)
            self.grid_positions[entry] = (self.rows - 1, col)

        for col in range(self.cols):
            self.scrollable_frame.grid_columnconfigure(col, weight=1)

        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(5, 0))

        control_row1 = ttk.Frame(control_frame)
        control_row1.pack(fill=tk.X)

        ttk.Label(control_row1, text="Start Load:").pack(side=tk.LEFT, padx=2)
        self.start_load_entry = ttk.Entry(control_row1, width=8)
        self.start_load_entry.insert(0, "1")
        self.start_load_entry.pack(side=tk.LEFT, padx=2)
        self.all_entries.append(self.start_load_entry)
        self.grid_positions[self.start_load_entry] = (self.rows, 1)

        ttk.Label(control_row1, text="Start Combination:").pack(side=tk.LEFT, padx=2)
        self.start_comb_entry = ttk.Entry(control_row1, width=8)
        self.start_comb_entry.insert(0, "101")
        self.start_comb_entry.pack(side=tk.LEFT, padx=2)
        self.all_entries.append(self.start_comb_entry)
        self.grid_positions[self.start_comb_entry] = (self.rows, 2)

        stats_frame = ttk.Frame(control_row1)
        stats_frame.pack(side=tk.LEFT, padx=10)

        ttk.Label(stats_frame, text="Total Load Cases:").pack(side=tk.LEFT, padx=2)
        self.total_load_label = ttk.Entry(stats_frame, width=10, font=('Arial', 10, 'bold'), state="readonly")
        self.total_load_label.pack(side=tk.LEFT, padx=2)

        ttk.Label(stats_frame, text="Total Combinations:").pack(side=tk.LEFT, padx=2)
        self.total_comb_label = ttk.Entry(stats_frame, width=10, font=('Arial', 10, 'bold'), state="readonly")
        self.total_comb_label.pack(side=tk.LEFT, padx=2)

        control_row2 = ttk.Frame(control_frame)
        control_row2.pack(fill=tk.X, pady=(5, 0))

        self.generate_btn = ttk.Button(control_row2, text="Generate", command=self.generate, padding=(20, 5))
        self.generate_btn.pack(side=tk.LEFT, padx=10)
        self.grid_positions[self.generate_btn] = (self.rows, 3)

        self.clear_btn = ttk.Button(control_row2, text="Clear", command=self.clear_all, padding=(20, 5))
        self.clear_btn.pack(side=tk.LEFT, padx=10)
        self.grid_positions[self.clear_btn] = (self.rows, 4)

    def setup_key_navigation(self):
        for widget in list(self.all_entries):
            if widget in self.grid_positions:
                row, col = self.grid_positions[widget]

                widget.bind('<Up>', lambda e, r=row, c=col: self.focus_adjacent_widget(r - 1, c))
                widget.bind('<Down>', lambda e, r=row, c=col: self.focus_adjacent_widget(r + 1, c))
                widget.bind('<Left>', lambda e, r=row, c=col: self.focus_adjacent_widget(r, c - 1))
                widget.bind('<Right>', lambda e, r=row, c=col: self.focus_adjacent_widget(r, c + 1))

        # navigation for control buttons/entries
        try:
            self.start_comb_entry.bind('<Down>', lambda e: self.generate_btn.focus_set())
            self.generate_btn.bind('<Up>', lambda e: self.start_comb_entry.focus_set())
            self.generate_btn.bind('<Right>', lambda e: self.clear_btn.focus_set())
            self.generate_btn.bind('<Left>', lambda e: self.start_comb_entry.focus_set())
            self.clear_btn.bind('<Right>', lambda e: None)
            self.clear_btn.bind('<Left>', lambda e: self.generate_btn.focus_set())
        except Exception:
            pass

    def focus_adjacent_widget(self, row, col):
        for widget, (r, c) in self.grid_positions.items():
            if r == row and c == col:
                try:
                    widget.focus_set()
                except Exception:
                    pass
                return

        min_distance = float('inf')
        nearest_widget = None

        for widget, (r, c) in self.grid_positions.items():
            distance = (r - row) ** 2 + (c - col) ** 2
            if distance < min_distance:
                min_distance = distance
                nearest_widget = widget

        if nearest_widget:
            try:
                nearest_widget.focus_set()
            except Exception:
                pass

    def clear_all(self):
        for entry in self.name_entries:
            entry.delete(0, tk.END)

        for combo in self.type_combos:
            combo.current(0)

        for row in self.coeff_entries:
            for entry in row:
                entry.delete(0, tk.END)

        for entry in self.subcase_entries:
            entry.delete(0, tk.END)

        self.start_load_entry.delete(0, tk.END)
        self.start_load_entry.insert(0, "1")
        self.start_comb_entry.delete(0, tk.END)
        self.start_comb_entry.insert(0, "101")

        self.total_load_label.config(state="normal")
        self.total_load_label.delete(0, tk.END)
        self.total_load_label.config(state="readonly")
        self.total_comb_label.config(state="normal")
        self.total_comb_label.delete(0, tk.END)
        self.total_comb_label.config(state="readonly")

    def generate(self):
        try:
            start_load = int(self.start_load_entry.get())
            start_comb = int(self.start_comb_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid starting numbers")
            return

        load_cases = []
        load_case_groups = {}
        current_load = start_load

        for col in range(self.cols - 1):
            base_name = self.name_entries[col].get().strip()
            ltype = self.type_combos[col].get().strip()
            try:
                subcases = int(self.subcase_entries[col].get() or "1")
            except ValueError:
                subcases = 1

            if base_name and ltype:
                group = []
                for i in range(1, subcases + 1):
                    case_name = f"{base_name}{i}"
                    load_cases.append(f"LOAD {current_load} LOADTYPE {ltype} TITLE {case_name}")
                    group.append((current_load, case_name))
                    current_load += 1
                load_case_groups[col] = group

        combinations = []
        current_comb = start_comb

        for row in self.coeff_entries:
            coeffs = []
            for col in range(self.cols - 1):
                try:
                    coeff = float(row[col].get() or "0")
                except ValueError:
                    coeff = 0
                coeffs.append(coeff)

            active_cols = [col for col, coeff in enumerate(coeffs) if coeff != 0]
            if not active_cols:
                continue

            subcase_options = []
            for col in active_cols:
                if col in load_case_groups:
                    subcase_options.append(load_case_groups[col])
                else:
                    base_name = self.name_entries[col].get().strip()
                    subcase_options.append([(0, f"{base_name}1")])

            for permutation in product(*subcase_options):
                expr_parts = []
                factor_parts = []
                # coeffs for active columns in same order
                coeffs_for_active = [coeffs[col] for col in active_cols]
                for (load_num, case_name), coeff in zip(permutation, coeffs_for_active):
                    sign = "+" if coeff >= 0 else "-"
                    abs_coeff = abs(coeff)
                    display_name = self._display_case_name(case_name)
                    expr_parts.append(f"{sign} {abs_coeff} {display_name}")
                    factor_parts.append(f"{load_num} {coeff}")

                if expr_parts:
                    comb_def = f"LOAD COMB {current_comb} COMB -{' '.join(expr_parts)}".replace(" -+", " -")
                    factors_line = f"{' '.join(factor_parts)}"

                    combinations.append(comb_def)
                    combinations.append(factors_line)
                    current_comb += 1

        total_loads = len(load_cases)
        total_combs = len(combinations) // 2

        self.total_load_label.config(state="normal")
        self.total_load_label.delete(0, tk.END)
        self.total_load_label.insert(0, str(total_loads))
        self.total_load_label.config(state="readonly")

        self.total_comb_label.config(state="normal")
        self.total_comb_label.delete(0, tk.END)
        self.total_comb_label.insert(0, str(total_combs))
        self.total_comb_label.config(state="readonly")

        output = ["**** Load Case ****", ""] + load_cases + ["", "*** Load Combinations ***", ""] + combinations

        self.show_output(output)

    def show_output(self, output):
        output_window = tk.Toplevel(self.root)
        output_window.title("Generated Combinations")
        output_window.geometry("800x600")

        text_frame = ttk.Frame(output_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        text = tk.Text(text_frame, wrap=tk.WORD, font=("Courier New", 10), state="normal")
        scrollbar = ttk.Scrollbar(text_frame, command=text.yview)
        text.config(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        text.insert(tk.END, "\n".join(output))
        text.config(state="disabled")

        def copy_to_clipboard():
            self.root.clipboard_clear()
            self.root.clipboard_append("\n".join(output))
            messagebox.showinfo("Copied", "STAAD.Pro commands copied to clipboard!")

        ttk.Button(output_window, text="Copy to Clipboard", command=copy_to_clipboard).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = LoadCombinationGenerator(root)
    root.mainloop()
