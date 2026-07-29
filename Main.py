import tkinter as tk


class MainMenuFrame:
    def __init__(self, parent, app):
        self.frame = tk.Frame(parent, bg='lightblue')
        self.app = app
        self.setup_ui()

    def setup_ui(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        for i in range(8):
            self.frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.frame.grid_columnconfigure(i, weight=1)

        title_label = tk.Label(
            self.frame,
            text="Оценка уровня стресса",
            font=('Arial', 18, 'bold'),
            bg='lightblue',
            fg='black'
        )
        title_label.grid(row=0, column=0, columnspan=4, pady=30, sticky='s')

        buttons_frame = tk.Frame(self.frame, bg='lightblue')
        buttons_frame.grid(row=1, column=0, columnspan=4, rowspan=3, pady=20, sticky='nsew')

        for i in range(3):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(2):
            buttons_frame.grid_columnconfigure(i, weight=1)

        sleep_button = tk.Button(
            buttons_frame,
            text="Сон",
            font=('Arial', 14),
            bg='green',
            fg='white',
            width=18,
            height=2,
            command=self.app.show_sleep_frame
        )
        sleep_button.grid(row=0, column=0, pady=15, padx=10, sticky='e')

        food_button = tk.Button(
            buttons_frame,
            text="Питание",
            font=('Arial', 14),
            bg='green',
            fg='white',
            width=18,
            height=2,
            command=self.app.show_food_frame
        )
        food_button.grid(row=0, column=1, pady=15, padx=10, sticky='w')

        activity_button = tk.Button(
            buttons_frame,
            text="Активность",
            font=('Arial', 14),
            bg='green',
            fg='white',
            width=18,
            height=2,
            command=self.app.show_activity_frame
        )
        activity_button.grid(row=1, column=0, pady=15, padx=10, sticky='e')

        emotions_button = tk.Button(
            buttons_frame,
            text="Эмоции",
            font=('Arial', 14),
            bg='green',
            fg='white',
            width=18,
            height=2,
            command=self.app.show_emotion_frame
        )
        emotions_button.grid(row=1, column=1, pady=15, padx=10, sticky='w')

        result_button = tk.Button(
            self.frame,
            text="Результат",
            font=('Arial', 14, 'bold'),
            bg='orange',
            fg='white',
            width=25,
            height=2,
            command=self.app.show_result_frame
        )
        result_button.grid(row=4, column=0, columnspan=4, pady=30, sticky='n')
