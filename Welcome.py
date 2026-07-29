import tkinter as tk


class WelcomeScreenFrame:
    def __init__(self, parent, app):
        self.frame = tk.Frame(parent, bg='lightblue')
        self.app = app
        self.setup_ui()

    def setup_ui(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.app.context_menu.create_context_menu()

        for i in range(10):
            self.frame.grid_rowconfigure(i, weight=1)
            self.frame.grid_columnconfigure(0, weight=1)

        title_label = tk.Label(
            self.frame,
            text="Готовы ли вы контролировать свой стресс?",
            font=('Arial', 18, 'bold'),
            bg='lightblue',
            fg='black'
        )
        title_label.grid(row=1, column=0, pady=20, sticky='n')

        free_button = tk.Button(
            self.frame,
            text="Попробовать бесплатно прямо сейчас",
            font=('Arial', 14),
            bg='green',
            fg='white',
            width=35,
            height=3,
            command=self.app.free_version_click
        )
        free_button.grid(row=2, column=0, pady=15, sticky='n')

        premium_button = tk.Button(
            self.frame,
            text="Включить защиту от стресса",
            font=('Arial', 14),
            bg='green',
            fg='white',
            width=35,
            height=3,
            command=self.app.premium_version_click
        )
        premium_button.grid(row=3, column=0, pady=15, sticky='n')
