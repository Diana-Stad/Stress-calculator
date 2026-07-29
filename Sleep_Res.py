import tkinter as tk
from matplotlib import gridspec
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from SleepModel import SleepModel


class SleepResultFrame:
    def __init__(self, parent, app):
        self.frame = tk.Frame(parent, bg='white')
        self.app = app
        self.current_view = "graphs"
        self.results = None

        self.setup_ui()

    def setup_ui(self):

        for widget in self.frame.winfo_children():
            widget.destroy()

        for i in range(15):
            self.frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            self.frame.grid_columnconfigure(i, weight=1)

        title_label = tk.Label(
            self.frame,
            text="Результаты анализа сна",
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
            self.results = self.analyze_sleep_data()
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
        self.current_view = "graphs"
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        if self.results:
            self.create_graphs(self.results)

    def create_graphs(self, results):
        fig = Figure(figsize=(14, 8), dpi=100)
        fig.patch.set_facecolor('white')

        gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.3)

        ax1 = fig.add_subplot(gs[0, :])
        self.create_sleep_duration_chart(ax1, results['chart_data'])

        ax2 = fig.add_subplot(gs[1, 0])
        self.create_sleep_metrics_chart(ax2, results['model_results'])

        ax3 = fig.add_subplot(gs[1, 1])
        self.create_stress_score_chart(ax3, results['model_results'])

        canvas = FigureCanvasTkAgg(fig, self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_sleep_duration_chart(self, ax, sleep_data):
        days = list(range(1, len(sleep_data) + 1))
        durations = [day['duration'] for day in sleep_data]
        deficits = [day['deficit'] for day in sleep_data]

        colors = ['red' if d < 7 else 'green' if d <= 9 else 'orange' for d in durations]
        bars = ax.bar(days, durations, color=colors, alpha=0.7, label='Продолжительность')

        ax.axhline(y=7.75, color='blue', linestyle='--', linewidth=2, label='Норма (7.75 ч)')

        for bar, duration in zip(bars, durations):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height + 0.1,
                    f'{duration:.1f}ч', ha='center', va='bottom', fontweight='bold')

        ax2 = ax.twinx()
        ax2.plot(days, deficits, 'ro-', linewidth=2, markersize=6, label='Дефицит')
        ax2.set_ylabel('Дефицит сна (часы)', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        ax.set_xlabel('Дни')
        ax.set_ylabel('Продолжительность сна (часы)')
        ax.set_title('Динамика продолжительности и дефицита сна')
        ax.legend(loc='upper left')
        ax2.legend(loc='upper right')
        ax.grid(True, alpha=0.3, axis='y')

        ax.set_xticks(days)
        ax.set_xticklabels([f'День {d}' for d in days])
        ax.set_ylim(0, max(durations) + 1 if durations else 10)

    def create_sleep_metrics_chart(self, ax, model_results):
        metrics = model_results['metrics']

        categories = ['Недосып (ч)', 'Стабильность \n засыпания', 'Колебания \n длительности', 'Сбой \n графика']
        values = [
            metrics['debt'],
            metrics['circ'],
            metrics['var'],
            metrics['jet']
        ]

        colors = []
        for i, value in enumerate(values):
            if i == 0:
                if value <= 5:
                    colors.append('#2ca02c')
                elif value <= 10:
                    colors.append('#ff7f0e')
                else:
                    colors.append('#d62728')
            else:
                if value <= 2:
                    colors.append('#2ca02c')
                elif value <= 4:
                    colors.append('#ff7f0e')
                else:
                    colors.append('#d62728')

        bars = ax.bar(categories, values, color=colors, alpha=0.7)

        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height + 0.05,
                    f'{value:.1f}', ha='center', va='bottom', fontweight='bold')

        ax.axhline(y=5, color='green', linestyle='--', alpha=0.5, label='Хорошо')
        ax.axhline(y=10, color='orange', linestyle='--', alpha=0.5, label='Средне')

        ax.set_ylabel('Значения')
        ax.set_title('Основные показатели сна\n(зеленый=хорошо, оранжевый=средне, красный=плохо)')
        ax.grid(True, alpha=0.3, axis='y')
        ax.legend()

    def create_stress_score_chart(self, ax, model_results):
        stress_score = model_results['stress_score']
        normalized = model_results['normalized']

        categories = ['Дефицит', 'Стабильность \n засыпания', 'Колебания \n длительности', 'Сбой \n графика']
        values = [
            normalized['debt'],
            normalized['circ'],
            normalized['var'],
            normalized['jet']
        ]

        values = [max(0, min(1, v)) for v in values]

        colors = ['red' if v > 0.7 else 'orange' if v > 0.4 else 'green' for v in values]
        bars = ax.bar(categories, values, color=colors, alpha=0.7)

        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height + 0.02,
                    f'{value:.2f}', ha='center', va='bottom', fontweight='bold')

        ax.axhline(y=stress_score / 10, color='blue', linestyle='--', linewidth=2,
                   label=f'Общий стресс: {stress_score:.1f}/10')

        ax.set_ylabel('Нормализованные значения')
        ax.set_title('Оценка стресса сна')
        ax.set_ylim(0, 1)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')

    def analyze_sleep_data(self):
        if hasattr(self.app, 'sleep_frame') and self.app.sleep_frame:
            sleep_schedule = self.app.sleep_frame.sleep_schedule
            valid_days = [day for day in sleep_schedule if day[0] and day[1]]

            if not valid_days:
                raise Exception("Нет данных о сне для анализа. Сначала заполните данные о сне.")

            sleep_model = SleepModel()
            analysis_results = sleep_model.periodic_stress(valid_days)

            chart_data = []
            for bed_time, wake_time in valid_days:
                duration, deficit, mid, circ_align = sleep_model.daily_metrics(bed_time, wake_time)
                chart_data.append({
                    'duration': duration,
                    'deficit': deficit,
                    'mid': mid,
                    'circ_align': circ_align
                })

            return {
                'model_results': analysis_results,
                'chart_data': chart_data,
                'days_count': len(valid_days),
                'raw_data': valid_days,
                'model': sleep_model
            }
        else:
            raise Exception("Данные сна не заполнены. Сначала заполните данные о сне.")

    def go_back(self):
        self.app.show_result_frame()






