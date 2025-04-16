import tkinter as tk
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("650x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#222222")
        
        self.current_expression = ""
        self.total_expression = ""
        self.is_dark_mode = True
        self.history = []
        
        self.dark_colors = {
            "bg": "#222222",
            "display_bg": "#1a1a1a",
            "history_bg": "#1a1a1a",
            "btn_bg": "#333333",
            "btn_fg": "white",
            "digit_btn_bg": "#444444",
            "operator_btn_bg": "#555555",
            "special_btn_bg": "#8E44AD",
            "equals_btn_bg": "#FF9500",
            "fg": "white",
            "border": "#444444"
        }
        
        self.light_colors = {
            "bg": "#f5f5f5",
            "display_bg": "white",
            "history_bg": "white",
            "btn_bg": "#e6e6e6",
            "btn_fg": "black",
            "digit_btn_bg": "#f8f8f8",
            "operator_btn_bg": "#e0e0e0",
            "special_btn_bg": "#d4bbea",
            "equals_btn_bg": "#ffcc99",
            "fg": "black",
            "border": "#dddddd"
        }
        
        self.colors = self.dark_colors
        
        self.key_mapping = {
            "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
            "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",
            "KP_0": "0", "KP_1": "1", "KP_2": "2", "KP_3": "3", "KP_4": "4",
            "KP_5": "5", "KP_6": "6", "KP_7": "7", "KP_8": "8", "KP_9": "9",
            "plus": "+", "KP_Add": "+", 
            "minus": "-", "KP_Subtract": "-",
            "asterisk": "*", "KP_Multiply": "*",
            "slash": "/", "KP_Divide": "/",
            "period": ".", "KP_Decimal": ".",
            "asciicircum": "^",
            "percent": "%",
            "parenleft": "(", "parenright": ")",
            "Return": "=", "KP_Enter": "=",
            "BackSpace": "backspace",
            "Escape": "clear",
            "e": "e",
            "p": "π",
            "s": "sin(",
            "c": "cos(",
            "t": "tan(",
            "l": "log(",
            "n": "ln(",
            "r": "sqrt("
        }
        
        self.create_layout()
        self.bind_keys()
        
    def bind_keys(self):
        """Bind keyboard keys to calculator functions"""
        self.root.bind("<Key>", self.key_pressed)
        
    def key_pressed(self, event):
        """Handle keyboard input"""
        key = event.keysym
        
        if key in self.key_mapping:
            value = self.key_mapping[key]
            if value == "=":
                self.evaluate()
            elif value == "backspace":
                self.backspace()
            elif value == "clear":
                self.clear()
            else:
                self.add_to_expression(value)
        
    def create_layout(self):
        self.main_frame = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.display_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        self.display_frame.pack(fill=tk.X, pady=10)
        
        self.history_frame = tk.Frame(self.main_frame, bg=self.colors["history_bg"], width=200, 
                                    bd=1, relief=tk.SOLID, borderwidth=1, 
                                    highlightbackground=self.colors["border"])
        self.history_frame.pack(side=tk.LEFT, fill=tk.BOTH, pady=5, padx=5)
        self.history_frame.pack_propagate(False)
        
        self.history_label = tk.Label(self.history_frame, text="History", font=("Arial", 12, "bold"), 
                                     bg=self.colors["history_bg"], fg=self.colors["fg"])
        self.history_label.pack(anchor="w", pady=5, padx=5)
        
        self.history_scrollbar = tk.Scrollbar(self.history_frame)
        self.history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(self.history_frame, bg=self.colors["history_bg"], 
                                         fg=self.colors["fg"], width=25, height=15,
                                         bd=0, highlightthickness=0,
                                         font=("Arial", 10),
                                         yscrollcommand=self.history_scrollbar.set)
        self.history_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.history_scrollbar.config(command=self.history_listbox.yview)
        
        self.calculator_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        self.calculator_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        display_container = tk.Frame(self.display_frame, bg=self.colors["display_bg"], 
                                  bd=1, relief=tk.SOLID, borderwidth=1, 
                                  highlightbackground=self.colors["border"])
        display_container.pack(fill=tk.X, padx=5)
        
        self.total_expression_label = tk.Label(display_container, text="", anchor="e", 
                                             bg=self.colors["display_bg"], fg=self.colors["fg"],
                                             font=("Arial", 12), padx=10, pady=5)
        self.total_expression_label.pack(fill=tk.X)
        
        self.current_expression_label = tk.Label(display_container, text="0", anchor="e", 
                                               bg=self.colors["display_bg"], fg=self.colors["fg"],
                                               font=("Arial", 24, "bold"), padx=10, pady=5)
        self.current_expression_label.pack(fill=tk.X)
        
        self.buttons_frame = tk.Frame(self.calculator_frame, bg=self.colors["bg"])
        self.buttons_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.theme_button = tk.Button(self.display_frame, text="☀️ Light Mode", 
                                    bg=self.colors["btn_bg"], fg=self.colors["btn_fg"],
                                    font=("Arial", 10), width=12, 
                                    bd=0, borderwidth=1, relief=tk.SOLID,
                                    highlightbackground=self.colors["border"],
                                    activebackground=self.colors["btn_bg"],
                                    activeforeground=self.colors["btn_fg"],
                                    command=self.toggle_theme)
        self.theme_button.pack(side=tk.RIGHT, padx=5)
        
        self.create_buttons()
        
    def create_buttons(self):
        self.buttons_frame.columnconfigure(tuple(range(5)), weight=1, uniform="column")
        self.buttons_frame.rowconfigure(tuple(range(7)), weight=1, uniform="row")
        
        self.create_button("sin", 0, 0, bg=self.colors["special_btn_bg"], func=lambda: self.add_to_expression("sin("))
        self.create_button("cos", 0, 1, bg=self.colors["special_btn_bg"], func=lambda: self.add_to_expression("cos("))
        self.create_button("tan", 0, 2, bg=self.colors["special_btn_bg"], func=lambda: self.add_to_expression("tan("))
        self.create_button("log", 0, 3, bg=self.colors["special_btn_bg"], func=lambda: self.add_to_expression("log("))
        self.create_button("ln", 0, 4, bg=self.colors["special_btn_bg"], func=lambda: self.add_to_expression("ln("))
        
        self.create_button("(", 1, 0, bg=self.colors["operator_btn_bg"])
        self.create_button(")", 1, 1, bg=self.colors["operator_btn_bg"])
        self.create_button("π", 1, 2, bg=self.colors["special_btn_bg"], func=lambda: self.add_to_expression("π"))
        self.create_button("e", 1, 3, bg=self.colors["special_btn_bg"], func=lambda: self.add_to_expression("e"))
        self.create_button("^", 1, 4, bg=self.colors["operator_btn_bg"], func=lambda: self.add_to_expression("^"))
        
        self.create_button("C", 2, 0, bg=self.colors["special_btn_bg"], func=self.clear)
        self.create_button("⌫", 2, 1, bg=self.colors["special_btn_bg"], func=self.backspace)
        self.create_button("√", 2, 2, bg=self.colors["operator_btn_bg"], func=lambda: self.add_to_expression("sqrt("))
        self.create_button("%", 2, 3, bg=self.colors["operator_btn_bg"])
        self.create_button("÷", 2, 4, bg=self.colors["operator_btn_bg"], func=lambda: self.add_to_expression("/"))
        
        self.create_button("7", 3, 0, bg=self.colors["digit_btn_bg"])
        self.create_button("8", 3, 1, bg=self.colors["digit_btn_bg"])
        self.create_button("9", 3, 2, bg=self.colors["digit_btn_bg"])
        self.create_button("×", 3, 4, bg=self.colors["operator_btn_bg"], func=lambda: self.add_to_expression("*"))
        
        self.create_button("4", 4, 0, bg=self.colors["digit_btn_bg"])
        self.create_button("5", 4, 1, bg=self.colors["digit_btn_bg"])
        self.create_button("6", 4, 2, bg=self.colors["digit_btn_bg"])
        self.create_button("-", 4, 4, bg=self.colors["operator_btn_bg"])
        
        self.create_button("1", 5, 0, bg=self.colors["digit_btn_bg"])
        self.create_button("2", 5, 1, bg=self.colors["digit_btn_bg"])
        self.create_button("3", 5, 2, bg=self.colors["digit_btn_bg"])
        self.create_button("+", 5, 4, bg=self.colors["operator_btn_bg"])
        
        self.create_button("0", 6, 0, bg=self.colors["digit_btn_bg"], columnspan=2)
        self.create_button(".", 6, 2, bg=self.colors["digit_btn_bg"])
        self.create_button("=", 6, 4, bg=self.colors["equals_btn_bg"], func=self.evaluate)
        
    def create_button(self, text, row, column, bg, fg=None, func=None, columnspan=1):
        if fg is None:
            fg = self.colors["btn_fg"]
        
        if func is None:
            func = lambda: self.add_to_expression(text)
            
        button = tk.Button(self.buttons_frame, text=text, font=("Arial", 14, "bold"),
                         bg=bg, fg=fg, bd=0, borderwidth=1, relief=tk.RAISED,
                         highlightbackground=self.colors["border"],
                         activebackground=bg, activeforeground=fg,
                         command=func)
        button.grid(row=row, column=column, columnspan=columnspan, sticky="nsew", padx=4, pady=4, ipadx=2, ipady=2)
        return button
        
    def add_to_expression(self, value):
        self.current_expression += value
        self.update_display()
    
    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_display()
    
    def backspace(self):
        self.current_expression = self.current_expression[:-1]
        self.update_display()
    
    def evaluate(self):
        if not self.current_expression:
            return
            
        self.total_expression = self.current_expression
        
        expression = self.current_expression
        expression = expression.replace("π", str(math.pi))
        expression = expression.replace("e", str(math.e))
        expression = expression.replace("^", "**")
        expression = expression.replace("sin(", "math.sin(")
        expression = expression.replace("cos(", "math.cos(")
        expression = expression.replace("tan(", "math.tan(")
        expression = expression.replace("log(", "math.log10(")
        expression = expression.replace("ln(", "math.log(")
        expression = expression.replace("sqrt(", "math.sqrt(")
        
        try:
            result = eval(expression)
            history_entry = f"{self.total_expression} = {result}"
            self.history.append(history_entry)
            self.history_listbox.insert(tk.END, history_entry)
            self.history_listbox.see(tk.END)
            
            self.current_expression = str(result)
            self.update_display()
        except Exception as e:
            self.current_expression = "Error"
            self.update_display()
    
    def update_display(self):
        if not self.current_expression:
            self.current_expression_label.config(text="0")
        else:
            self.current_expression_label.config(text=self.current_expression)
        self.total_expression_label.config(text=self.total_expression)
    
    def toggle_theme(self):
        if self.is_dark_mode:
            self.colors = self.light_colors
            self.theme_button.config(text="🌙 Dark Mode")
        else:
            self.colors = self.dark_colors
            self.theme_button.config(text="☀️ Light Mode")
        
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()
    
    def apply_theme(self):
        self.root.configure(bg=self.colors["bg"])
        self.main_frame.config(bg=self.colors["bg"])
        self.display_frame.config(bg=self.colors["bg"])
        self.history_frame.config(bg=self.colors["history_bg"], highlightbackground=self.colors["border"])
        self.calculator_frame.config(bg=self.colors["bg"])
        self.buttons_frame.config(bg=self.colors["bg"])
        
        self.total_expression_label.config(bg=self.colors["display_bg"], fg=self.colors["fg"])
        self.current_expression_label.config(bg=self.colors["display_bg"], fg=self.colors["fg"])
        self.history_label.config(bg=self.colors["history_bg"], fg=self.colors["fg"])
        self.history_listbox.config(bg=self.colors["history_bg"], fg=self.colors["fg"])
        self.theme_button.config(bg=self.colors["btn_bg"], fg=self.colors["btn_fg"], 
                               highlightbackground=self.colors["border"],
                               activebackground=self.colors["btn_bg"],
                               activeforeground=self.colors["btn_fg"])
        
        for widget in self.buttons_frame.winfo_children():
            if isinstance(widget, tk.Button):
                text = widget.cget("text")
                if text.isdigit() or text == ".":
                    widget.config(bg=self.colors["digit_btn_bg"], fg=self.colors["btn_fg"], 
                                highlightbackground=self.colors["border"],
                                activebackground=self.colors["digit_btn_bg"],
                                activeforeground=self.colors["btn_fg"])
                elif text in ["+", "-", "×", "÷", "(", ")", "^", "%"]:
                    widget.config(bg=self.colors["operator_btn_bg"], fg=self.colors["btn_fg"], 
                                highlightbackground=self.colors["border"],
                                activebackground=self.colors["operator_btn_bg"],
                                activeforeground=self.colors["btn_fg"])
                elif text == "=":
                    widget.config(bg=self.colors["equals_btn_bg"], fg=self.colors["btn_fg"], 
                                highlightbackground=self.colors["border"],
                                activebackground=self.colors["equals_btn_bg"],
                                activeforeground=self.colors["btn_fg"])
                elif text in ["C", "⌫"]:
                    widget.config(bg=self.colors["special_btn_bg"], fg=self.colors["btn_fg"], 
                                highlightbackground=self.colors["border"],
                                activebackground=self.colors["special_btn_bg"],
                                activeforeground=self.colors["btn_fg"])
                else:
                    widget.config(fg=self.colors["btn_fg"], highlightbackground=self.colors["border"])

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()