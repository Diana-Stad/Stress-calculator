import tkinter as tk
from matplotlib import gridspec
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import Patch

from Activity_Model import ActivityModel


class ActivityResultFrame:
    def __init__(self, parent, app):
        self.frame = tk.Frame(parent, bg='white')
        self.app = app
        self.results = None
        self.setup_ui()

    def setup_ui(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        for i in range(10):
            self.frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            self.frame.grid_columnconfigure(i, weight=1)

        title_label = tk.Label(
            self.frame,
            text="Результаты анализа активности",
            font=('Arial', 18, 'bold'),
            bg='white',
            fg='black'
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        button_frame = tk.Frame(self.frame, bg='white')
        button_frame.grid(row=1, column=0, columnspan=3, pady=5)

        back_button = tk.Button(
            button_frame,
            text="Назад к результатам",
            font=('Arial', 12),
            bg='grey',
            fg='white',
            width=20,
            height=1,
            command=self.go_back
        )
        back_button.pack(side=tk.LEFT, padx=5)

        self.content_frame = tk.Frame(self.frame, bg='white')
        self.content_frame.grid(row=2, column=0, columnspan=3, rowspan=12,
                                sticky='nsew', padx=10, pady=10)

        try:
            self.results = self.analyze_activity_data()
            self.show_graphs_view()
        except Exception as e:
            error_label = tk.Label(
                self.content_frame,
                text=f"Ошибка загрузки данных: {str(e)}",
                font=('Arial', 14),
                bg='white',
                fg='red'
            )
            error_label.pack(expand=True)

    def show_graphs_view(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.create_graphs(self.results)

    def create_graphs(self, results):
        fig = Figure(figsize=(14, 8), dpi=100)
        fig.patch.set_facecolor('white')

        gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.3)

        ax1 = fig.add_subplot(gs[0, 0])
        self.create_work_balance_chart(ax1, results['chart_data'])

        ax2 = fig.add_subplot(gs[0, 1])
        self.create_stress_timeline(ax2, results['chart_data'])

        ax3 = fig.add_subplot(gs[1, :])
        self.create_activity_types_chart(ax3, results['chart_data'])

        canvas = FigureCanvasTkAgg(fig, self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_work_balance_chart(self, ax, chart_data):
        total_work_hours = sum(d['work_hours'] for d in chart_data)
        total_exercise_hours = sum(d['exercise_duration'] for d in chart_data) / 60
        total_days = len(chart_data)

        total_awake_hours = total_days * 16
        rest_hours = total_awake_hours - total_work_hours - total_exercise_hours

        if total_awake_hours == 0:
            ax.text(0.5, 0.5, "Нет данных", ha='center', va='center', fontsize=14)
            ax.set_title('Баланс времени', fontsize=12, fontweight='bold')
            return

        sizes = [total_work_hours, total_exercise_hours, rest_hours]
        labels = [f'Работа\n{total_work_hours:.1f}ч',
                  f'Тренировки\n{total_exercise_hours:.1f}ч',
                  f'Отдых\n{rest_hours:.1f}ч']
        colors = ['#ff7f0e', '#2ca02c', '#1f77b4']

        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors,
                                          autopct='%1.1f%%', startangle=90)

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        ax.set_title('Баланс времени', fontsize=12, fontweight='bold')

    def create_stress_timeline(self, ax, chart_data):
        days = list(range(1, len(chart_data) + 1))
        stress_levels = [d['daily_stress'] for d in chart_data]
        work_hours = [d['work_hours'] for d in chart_data]

        ax.fill_between(days, stress_levels, alpha=0.3, color='#d62728')

        ax2 = ax.twinx()

        ax.set_xlabel('Дни')
        ax.set_ylabel('Стресс активности', color='#d62728')
        ax2.set_ylabel('Рабочие часы', color='#1f77b4')

        ax.tick_params(axis='y', labelcolor='#d62728')
        ax2.tick_params(axis='y', labelcolor='#1f77b4')

        ax.set_title('Стресс активности и рабочая нагрузка', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_xticks(days)
        ax.set_xticklabels([f'День {d}' for d in days])
        ax.set_ylim(0, max(stress_levels) + 0.5 if stress_levels else 1)
        ax2.set_ylim(0, max(work_hours) + 2 if work_hours else 10)

        ax.plot([], [], color='#d62728', label='Стресс активности')
        ax2.plot([], [], color='#1f77b4', label='Рабочие часы')
        ax.legend(loc='upper left')

    def create_activity_types_chart(self, ax, chart_data):
        work_types = {}
        exercise_types = {}

        for d in chart_data:
            work_type = d['work_type']
            work_types[work_type] = work_types.get(work_type, 0) + 1

            exercise = d['exercise']
            if exercise != 'none':
                exercise_types[exercise] = exercise_types.get(exercise, 0) + 1

        work_type_names = {
            'office': 'Офисная',
            'physical': 'Физическая',
            'mixed': 'Смешанная'
        }

        exercise_type_names = {
            'low': 'Легкие\nтренировки',
            'moderate': 'Средние\nтренировки',
            'high': 'Интенсивные\nтренировки'
        }

        if not work_types and not exercise_types:
            ax.text(0.5, 0.5, "Нет данных", ha='center', va='center', fontsize=14)
            ax.set_title('Типы активности', fontsize=12, fontweight='bold')
            return

        categories = []
        counts = []
        colors = []

        for work_type, count in work_types.items():
            categories.append(work_type_names[work_type])
            counts.append(count)
            colors.append('#ff7f0e')

        for exercise_type, count in exercise_types.items():
            categories.append(exercise_type_names[exercise_type])
            counts.append(count)
            colors.append('#2ca02c')

        x_pos = range(len(categories))
        bars = ax.bar(x_pos, counts, color=colors, alpha=0.7)

        ax.set_xlabel('Типы активности')
        ax.set_ylabel('Количество дней')
        ax.set_title('Распределение типов активности', fontsize=12, fontweight='bold')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(categories, ha='center')
        ax.grid(True, alpha=0.3, axis='y')

        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height + 0.1,
                    f'{int(count)}', ha='center', va='bottom', fontweight='bold')

        legend_elements = [
            Patch(facecolor='#ff7f0e', alpha=0.7, label='Работа'),
            Patch(facecolor='#2ca02c', alpha=0.7, label='Тренировки')
        ]
        ax.legend(handles=legend_elements, loc='upper right')

        max_count = max(counts) if counts else 1
        ax.set_ylim(0, max_count + 1)
        ax.set_yticks(range(0, int(max_count) + 2))

    def analyze_activity_data(self):
        if hasattr(self.app, 'activity_frame') and self.app.activity_frame:
            activity_data = self.app.activity_frame.activity_data
            valid_days = [day for day in activity_data if any(day.values())]

            if not valid_days:
                raise Exception("Нет данных об активности для анализа.")

            activity_model = ActivityModel()
            activity_score = activity_model.periodic_stress(valid_days)

            chart_data = []
            for day_data in valid_days:
                daily_stress = activity_model.daily_stress(day_data)
                chart_data.append({
                    'work_hours': day_data['work_hours'],
                    'work_stress': day_data['work_stress'],
                    'work_type': day_data['work_type'],
                    'exercise': day_data['exercise'],
                    'exercise_duration': day_data['exercise_duration'],
                    'daily_stress': daily_stress
                })

            return {
                'score': activity_score,
                'days_count': len(valid_days),
                'chart_data': chart_data
            }
        else:
            raise Exception("Данные активности не заполнены.")

    def go_back(self):
        self.app.show_result_frame()