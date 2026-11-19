import tkinter as tk
from tkinter import font

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("ماشین حساب")
        self.root.geometry("360x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        # متغیرها
        self.current_input = "0"
        self.previous_input = ""
        self.operator = None
        self.new_input = True

        # فونت‌ها
        self.display_font = font.Font(family="Helvetica", size=32, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=16, weight="bold")

        self.create_widgets()

    def create_widgets(self):
        # صفحه نمایش
        self.display = tk.Entry(
            self.root,
            font=self.display_font,
            bg="#2a2a3c",
            fg="#ffffff",
            bd=0,
            justify="right",
            insertbackground="white",
        )
        self.display.insert(0, "0")
        self.display.grid(row=0, column=0, columnspan=4, padx=15, pady=(20, 15),
                         ipady=20, sticky="nsew")

        # رنگ دکمه‌ها
        colors = {
            "num": "#3a3a4c",
            "op": "#ff9f43",
            "func": "#e056fd",
            "equals": "#26de81",
        }

        # دکمه‌ها: (متن, سطر, ستون, نوع)
        buttons = [
            ("C", 1, 0, "func"), ("±", 1, 1, "func"), ("%", 1, 2, "func"), ("÷", 1, 3, "op"),
            ("7", 2, 0, "num"), ("8", 2, 1, "num"), ("9", 2, 2, "num"), ("×", 2, 3, "op"),
            ("4", 3, 0, "num"), ("5", 3, 1, "num"), ("6", 3, 2, "num"), ("−", 3, 3, "op"),
            ("1", 4, 0, "num"), ("2", 4, 1, "num"), ("3", 4, 2, "num"), ("+", 4, 3, "op"),
            ("0", 5, 0, "num"), (".", 5, 1, "num"), ("⌫", 5, 2, "func"), ("=", 5, 3, "equals"),
        ]

        for (text, row, col, kind) in buttons:
            fg_color = "#ffffff" if kind != "func" else "#ffffff"
            btn = tk.Button(
                self.root,
                text=text,
                font=self.button_font,
                bg=colors[kind],
                fg=fg_color,
                activebackground="#555577",
                activeforeground="#ffffff",
                bd=0,
                relief="flat",
                command=lambda t=text: self.on_button_click(t),
            )
            btn.grid(row=row, column=col, padx=6, pady=6, ipadx=10, ipady=15, sticky="nsew")

        # تنظیم وزن گرید
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(1, 6):
            self.root.grid_rowconfigure(i, weight=1)

    def on_button_click(self, char):
        if char.isdigit():
            self.handle_digit(char)
        elif char == ".":
            self.handle_dot()
        elif char in ("+", "−", "×", "÷"):
            self.handle_operator(char)
        elif char == "=":
            self.handle_equals()
        elif char == "C":
            self.handle_clear()
        elif char == "⌫":
            self.handle_backspace()
        elif char == "±":
            self.handle_sign()
        elif char == "%":
            self.handle_percent()

        self.update_display()

    def handle_digit(self, digit):
        if self.new_input:
            self.current_input = digit
            self.new_input = False
        else:
            if self.current_input == "0":
                self.current_input = digit
            else:
                self.current_input += digit

    def handle_dot(self):
        if self.new_input:
            self.current_input = "0."
            self.new_input = False
        elif "." not in self.current_input:
            self.current_input += "."

    def handle_operator(self, op):
        if self.operator and not self.new_input:
            self.handle_equals()
        self.previous_input = self.current_input
        self.operator = op
        self.new_input = True

    def handle_equals(self):
        if self.operator is None or self.previous_input == "":
            return
        try:
            num1 = float(self.previous_input)
            num2 = float(self.current_input)
            if self.operator == "+":
                result = num1 + num2
            elif self.operator == "−":
                result = num1 - num2
            elif self.operator == "×":
                result = num1 * num2
            elif self.operator == "÷":
                if num2 == 0:
                    self.current_input = "خطا"
                    self.operator = None
                    self.previous_input = ""
                    self.new_input = True
                    return
                result = num1 / num2

            # حذف .0 اضافی
            if result == int(result):
                self.current_input = str(int(result))
            else:
                self.current_input = str(round(result, 10))
        except Exception:
            self.current_input = "خطا"

        self.operator = None
        self.previous_input = ""
        self.new_input = True

    def handle_clear(self):
        self.current_input = "0"
        self.previous_input = ""
        self.operator = None
        self.new_input = True

    def handle_backspace(self):
        if self.new_input:
            return
        self.current_input = self.current_input[:-1]
        if self.current_input == "" or self.current_input == "-":
            self.current_input = "0"
            self.new_input = True

    def handle_sign(self):
        if self.current_input in ("0", "خطا"):
            return
        if self.current_input.startswith("-"):
            self.current_input = self.current_input[1:]
        else:
            self.current_input = "-" + self.current_input

    def handle_percent(self):
        try:
            value = float(self.current_input) / 100
            if value == int(value):
                self.current_input = str(int(value))
            else:
                self.current_input = str(value)
        except ValueError:
            pass

    def update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, self.current_input)


if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()