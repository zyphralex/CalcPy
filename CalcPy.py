import tkinter as tk

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Calc")
        self.root.geometry("400x600")

        self.theme = "dark"
        self.button_style = "square"
        self.button_border = True

        self.themes = {
            "dark": {
                "bg": "#23272a",
                "entry_bg": "#2c2f33",
                "entry_fg": "#ffffff",
                "btn_bg": "#36393f",
                "btn_fg": "#ffffff",
                "btn_active_bg": "#7289da",
            },
            "light": {
                "bg": "#f0f0f0",
                "entry_bg": "#ffffff",
                "entry_fg": "#000000",
                "btn_bg": "#dcdcdc",
                "btn_fg": "#000000",
                "btn_active_bg": "#a9a9a9",
            }
        }

        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=True)

        self.calc_frame = tk.Frame(self.container)
        self.calc_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.settings_frame = tk.Frame(self.container)
        self.settings_frame.place(relx=1, rely=0, relwidth=1, relheight=1)

        self.build_calculator()
        self.build_settings()
        self.apply_theme()

    def build_calculator(self):
        self.entry = tk.Entry(self.calc_frame, font=("Segoe UI", 30), bd=0,
                              justify="right", insertbackground="#fff")
        self.entry.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=20, ipady=10)

        buttons = [
            ('C', self.clear), ('⌫', self.backspace), ('%', lambda: self.add_operation('%')), ('/', lambda: self.add_operation('/')),
            ('7', lambda: self.add_digit('7')), ('8', lambda: self.add_digit('8')), ('9', lambda: self.add_digit('9')), ('*', lambda: self.add_operation('*')),
            ('4', lambda: self.add_digit('4')), ('5', lambda: self.add_digit('5')), ('6', lambda: self.add_digit('6')), ('-', lambda: self.add_operation('-')),
            ('1', lambda: self.add_digit('1')), ('2', lambda: self.add_digit('2')), ('3', lambda: self.add_digit('3')), ('+', lambda: self.add_operation('+')),
            ('+/-', self.negate), ('0', lambda: self.add_digit('0')), ('.', lambda: self.add_digit('.')), ('=', self.calculate)
        ]

        self.buttons = []
        row = 1
        col = 0
        for (text, command) in buttons:
            btn = tk.Button(self.calc_frame, text=text, command=command)
            btn.grid(row=row, column=col, sticky="nsew", padx=6, pady=6, ipadx=2, ipady=9)
            self.buttons.append(btn)
            col += 1
            if col > 3:
                col = 0
                row += 1

        self.settings_button = tk.Button(self.calc_frame, text="⚙ Настройки", command=self.show_settings)
        self.settings_button.grid(row=row, column=0, columnspan=4, sticky="nsew", padx=6, pady=6, ipadx=2, ipady=9)

        for i in range(row + 1):
            self.calc_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.calc_frame.grid_columnconfigure(i, weight=1)

    def build_settings(self):
        back_btn = tk.Button(self.settings_frame, text="← Назад", command=self.show_calculator)
        back_btn.pack(pady=10, fill="x", padx=10)

        self.theme_var = tk.StringVar(value=self.theme)
        theme_label = tk.Label(self.settings_frame, text="Тема:")
        theme_label.pack(anchor="w", padx=10)
        light_rb = tk.Radiobutton(self.settings_frame, text="Светлая", variable=self.theme_var, value="light", command=self.change_theme)
        dark_rb = tk.Radiobutton(self.settings_frame, text="Тёмная", variable=self.theme_var, value="dark", command=self.change_theme)
        light_rb.pack(anchor="w", padx=20)
        dark_rb.pack(anchor="w", padx=20)

        self.style_var = tk.StringVar(value=self.button_style)
        style_label = tk.Label(self.settings_frame, text="Стиль кнопок:")
        style_label.pack(anchor="w", padx=10, pady=(20, 0))
        square_rb = tk.Radiobutton(self.settings_frame, text="Квадратные", variable=self.style_var, value="square", command=self.change_style)
        round_rb = tk.Radiobutton(self.settings_frame, text="Округлые", variable=self.style_var, value="round", command=self.change_style)
        square_rb.pack(anchor="w", padx=20)
        round_rb.pack(anchor="w", padx=20)

        self.border_var = tk.BooleanVar(value=self.button_border)
        border_cb = tk.Checkbutton(self.settings_frame, text="Показывать обводку кнопок", variable=self.border_var, command=self.change_border)
        border_cb.pack(anchor="w", padx=10, pady=(20, 0))

    def apply_theme(self):
        t = self.themes[self.theme]
        self.root.configure(bg=t["bg"])
        self.container.configure(bg=t["bg"])
        self.calc_frame.configure(bg=t["bg"])
        self.settings_frame.configure(bg=t["bg"])

        self.entry.configure(bg=t["entry_bg"], fg=t["entry_fg"])

        for btn in self.buttons + [self.settings_button]:
            btn.configure(bg=t["btn_bg"], fg=t["btn_fg"], activebackground=t["btn_active_bg"])
            if self.button_style == "round":
                btn.configure(relief="flat")
                if self.button_border:
                    btn.configure(highlightthickness=2, highlightbackground=t["btn_fg"], highlightcolor=t["btn_fg"])
                else:
                    btn.configure(highlightthickness=0)
                btn.configure(borderwidth=0)
            else:
                btn.configure(relief="raised")
                if self.button_border:
                    btn.configure(borderwidth=1)
                else:
                    btn.configure(borderwidth=0)
                btn.configure(highlightthickness=0)

    def change_theme(self):
        self.theme = self.theme_var.get()
        self.apply_theme()

    def change_style(self):
        self.button_style = self.style_var.get()
        self.apply_theme()

    def change_border(self):
        self.button_border = self.border_var.get()
        self.apply_theme()

    def animate_frame(self, frame_out, frame_in, step=0):
        if step > 20:
            frame_out.place_forget()
            frame_in.place(relx=0, rely=0, relwidth=1, relheight=1)
            return
        delta = step / 20
        frame_out.place(relx=-delta, rely=0, relwidth=1, relheight=1)
        frame_in.place(relx=1 - delta, rely=0, relwidth=1, relheight=1)
        self.root.after(15, lambda: self.animate_frame(frame_out, frame_in, step + 1))

    def show_settings(self):
        self.animate_frame(self.calc_frame, self.settings_frame)

    def show_calculator(self):
        self.animate_frame(self.settings_frame, self.calc_frame)

    def add_digit(self, digit):
        value = self.entry.get()
        if value == "Ошибка":
            value = ""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value + digit)

    def add_operation(self, op):
        value = self.entry.get()
        if not value:
            if op == '-':
                self.entry.insert(0, '-')
            return
        if value[-1] in "+-*/%":
            value = value[:-1]
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value + op)

    def calculate(self):
        try:
            value = self.entry.get()
            if '%' in value:
                value = value.replace('%', '/100')
            result = eval(value)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(result))
        except:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Ошибка")

    def clear(self):
        self.entry.delete(0, tk.END)

    def backspace(self):
        value = self.entry.get()
        if value != "":
            self.entry.delete(len(value)-1, tk.END)

    def negate(self):
        value = self.entry.get()
        if value:
            try:
                if value[0] == '-':
                    self.entry.delete(0)
                    self.entry.insert(0, value[1:])
                else:
                    self.entry.delete(0)
                    self.entry.insert(0, '-' + value)
            except:
                self.entry.delete(0, tk.END)
                self.entry.insert(0, "Ошибка")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
