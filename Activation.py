from tkinter import messagebox
import tkinter as tk


class ActivationFrame:
    def __init__(self, parent, app):
        self.frame = tk.Frame(parent, bg='lightblue')
        self.app = app
        self.setup_ui()

    def setup_ui(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.app.context_menu.create_context_menu()

        for i in range(8):
            self.frame.grid_rowconfigure(i, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        title_label = tk.Label(
            self.frame,
            text="Активация полного доступа",
            font=('Arial', 18),
            bg='lightblue',
            fg='black'
        )
        title_label.grid(row=0, column=0, pady=20, sticky='s')

        generated_code = self.app.license_generator.generate_key()

        code_label = tk.Label(
            self.frame,
            text="Ваш код активации:",
            font=('Arial', 14),
            bg='lightblue',
            fg='black'
        )
        code_label.grid(row=1, column=0, pady=10, sticky='s')

        code_display = tk.Entry(
            self.frame,
            font=('Arial', 16, 'bold'),
            justify='center',
            width=30,
            state='readonly',
            bg='white',
            fg='black'
        )
        code_display.grid(row=2, column=0, pady=5, sticky='n')
        code_display.configure(state='normal')
        code_display.delete(0, tk.END)
        code_display.insert(0, generated_code)
        code_display.configure(state='readonly')

        input_label = tk.Label(
            self.frame,
            text="Введите код активации:",
            font=('Arial', 14),
            bg='lightblue',
            fg='black'
        )
        input_label.grid(row=3, column=0, pady=20, sticky='s')

        self.code_entry = tk.Entry(
            self.frame,
            font=('Arial', 16),
            justify='center',
            width=30,
            bg='white',
            fg='black'
        )
        self.code_entry.grid(row=4, column=0, pady=5, sticky='n')
        self.code_entry.focus()

        self.app.context_menu.bind_to_widgets([self.code_entry, code_display])

        start_button = tk.Button(
            self.frame,
            text="Начать",
            font=('Arial', 14, 'bold'),
            bg='green',
            fg='white',
            width=20,
            height=2,
            command=self.start_click
        )
        start_button.grid(row=5, column=0, pady=20, sticky='n')

        self.frame.winfo_toplevel().bind('<Return>', lambda event: self.start_click())

        back_button = tk.Button(
            self.frame,
            text="Назад",
            font=('Arial', 12),
            bg='grey',
            fg='white',
            width=15,
            height=1,
            command=self.go_back
        )
        back_button.grid(row=6, column=0, pady=10, sticky='n')

    def start_click(self):
        entered_code = self.code_entry.get().strip()
        if entered_code:
            if self.app.license_generator.validate_code(entered_code):
                self.app.is_premium = True
                self.app.show_main_menu()
            else:
                messagebox.showerror("Ошибка", "Неверный код активации. Пожалуйста, проверьте код и попробуйте снова.")
        else:
            messagebox.showwarning("Ошибка", "Пожалуйста, введите код активации")

    def go_back(self):
        self.app.setup_main_screen()
