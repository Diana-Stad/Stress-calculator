import numpy as np
import tkinter as tk
from matplotlib import gridspec
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from Emotional_Model import EmotionModel


class EmotionResultFrame:
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
            text="Результаты анализа эмоционального состояния",
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
        self.content_frame.grid(row=2, column=0, columnspan=3, rowspan=17,
                                sticky='nsew', padx=10, pady=10)

        try:
            self.results = self.analyze_emotion_data()
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
        fig = Figure(figsize=(16, 10), dpi=80)
        fig.patch.set_facecolor('white')

        gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.3)

        ax1 = fig.add_subplot(gs[0, :2])
        self.create_emotion_timeline(ax1, results['chart_data'])

        ax2 = fig.add_subplot(gs[0, 2], projection='polar')
        self.create_emotion_compass(ax2, results['chart_data'])

        ax3 = fig.add_subplot(gs[1, 0])
        self.create_emotion_barchart(ax3, results['chart_data'])

        ax4 = fig.add_subplot(gs[1, 1:])
        self.create_social_activity_barchart(ax4, results['chart_data'])

        canvas = FigureCanvasTkAgg(fig, self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_emotion_barchart(self, ax, chart_data):
        emotions = ['Грусть', 'Тревога', 'Гнев', 'Радость']
        avg_values = [
            sum(d['sadness'] for d in chart_data) / len(chart_data),
            sum(d['anxiety'] for d in chart_data) / len(chart_data),
            sum(d['anger'] for d in chart_data) / len(chart_data),
            sum(d['joy'] for d in chart_data) / len(chart_data)
        ]

        colors = ['#1f77b4', '#ff7f0e', '#d62728', '#2ca02c']

        x_pos = np.arange(len(emotions))
        bars = ax.bar(x_pos, avg_values, color=colors, alpha=0.7)

        for bar, value in zip(bars, avg_values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height + 0.9,
                    f'{value:.1f}', ha='center', va='bottom',
                    fontweight='bold', fontsize=10)

        ax.set_ylabel('Средняя интенсивность', fontsize=11)
        ax.set_title('Средние значения эмоций', fontsize=14, fontweight='bold')
        ax.set_ylim(0, 13.5)
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(emotions, ha='center', fontsize=11)
        ax.tick_params(axis='y', labelsize=10)

    def create_social_activity_barchart(self, ax, chart_data):
        days = list(range(1, len(chart_data) + 1))
        social_hours = [d['social_hours'] for d in chart_data]
        isolation_hours = [d['isolation_hours'] for d in chart_data]

        bar_width = 0.35
        x_pos = np.arange(len(days))

        bars1 = ax.bar(x_pos - bar_width / 2, social_hours, bar_width,
                       label='Общение', color='#2ca02c', alpha=0.7)
        bars2 = ax.bar(x_pos + bar_width / 2, isolation_hours, bar_width,
                       label='Одиночество', color='#1f77b4', alpha=0.7)

        ax.set_xlabel('Дни')
        ax.set_ylabel('Часы')
        ax.set_title('Ежедневная социальная активность', fontsize=14, fontweight='bold')
        ax.set_xticks(x_pos)
        ax.set_xticklabels([f'День {d}' for d in days], ha='center')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')

        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width() / 2., height + 0.1,
                            f'{height:.1f}', ha='center', va='bottom',
                            fontsize=8, fontweight='bold')

        max_hours = max(max(social_hours), max(isolation_hours))
        ax.set_ylim(0, max_hours + 2)

    def create_emotion_timeline(self, ax, chart_data):
        days = list(range(1, len(chart_data) + 1))
        sadness = [d['sadness'] for d in chart_data]
        anxiety = [d['anxiety'] for d in chart_data]
        anger = [d['anger'] for d in chart_data]
        joy = [d['joy'] for d in chart_data]
        emotion_stress = [d['emotion_stress'] for d in chart_data]

        ax.plot(days, sadness, marker='o', linewidth=2, label='Грусть', color='#1f77b4')
        ax.plot(days, anxiety, marker='s', linewidth=2, label='Тревога', color='#ff7f0e')
        ax.plot(days, anger, marker='^', linewidth=2, label='Гнев', color='#d62728')
        ax.plot(days, joy, marker='D', linewidth=2, label='Радость', color='#2ca02c')
        ax.plot(days, emotion_stress, marker='*', linewidth=3, label='Стресс эмоций',
                color='#000000', linestyle='--', alpha=0.8)

        ax.set_xlabel('Дни')
        ax.set_ylabel('Интенсивность (1-10)')
        ax.set_title('Динамика эмоционального состояния', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 10)
        ax.set_xticks(days)
        ax.set_xticklabels([f'День {d}' for d in days], ha='center')

    def create_emotion_compass(self, ax, chart_data):
        emotions = ['Грусть', 'Тревога', 'Гнев', 'Радость']
        avg_values = [
            sum(d['sadness'] for d in chart_data) / len(chart_data),
            sum(d['anxiety'] for d in chart_data) / len(chart_data),
            sum(d['anger'] for d in chart_data) / len(chart_data),
            sum(d['joy'] for d in chart_data) / len(chart_data)
        ]

        angles = np.linspace(0, 2 * np.pi, len(emotions), endpoint=False).tolist()
        angles += angles[:1]
        avg_values += avg_values[:1]

        ax.plot(angles, avg_values, 'o-', linewidth=2, color='#9467bd')
        ax.fill(angles, avg_values, alpha=0.3, color='#9467bd')
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(emotions)
        ax.set_ylim(0, 10)
        ax.set_title('Эмоциональный компас\n(средние значения)', fontsize=14, fontweight='bold')

    def analyze_emotion_data(self):
        if hasattr(self.app, 'emotion_frame') and self.app.emotion_frame:
            emotion_data = self.app.emotion_frame.emotion_data
            valid_days = [day for day in emotion_data if any(day.values())]

            if not valid_days:
                raise Exception("Нет данных об эмоциях для анализа.")

            emotion_model = EmotionModel()
            emotion_score = emotion_model.periodic_stress(valid_days)

            chart_data = []
            for day_data in valid_days:
                daily_stress = emotion_model.daily_stress(day_data)

                chart_data.append({
                    'sadness': day_data['sadness'],
                    'anxiety': day_data['anxiety'],
                    'anger': day_data['anger'],
                    'joy': day_data['joy'],
                    'social_hours': day_data['social_hours'],
                    'isolation_hours': day_data['isolation_hours'],
                    'emotion_stress': daily_stress * 10
                })

            return {
                'score': emotion_score,
                'days_count': len(valid_days),
                'chart_data': chart_data
            }
        else:
            raise Exception("Данные эмоций не заполнены.")

    def go_back(self):
        self.app.show_result_frame()