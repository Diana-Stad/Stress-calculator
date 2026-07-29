import math


class ActivityModel:
    def __init__(self):
        self.k_work = 0.4
        self.p_work = 1.1
        self.m_work = 8
        self.k_psych = 0.35
        self.p_psych = 1.2
        self.m_psych = 10
        self.A_circ = 0.4
        self.alpha_circ = 12.0
        self.k_int = 0.008
        self.k_dur = 0.003
        self.threshold_intensity = 60

    def S_work_hours(self, H_w):
        normalized = H_w / self.m_work
        return self.k_work * (normalized ** self.p_work)

    def k_work_type(self, work_type):
        return {
            'office': 1.0,
            'physical': 0.7,
            'mixed': 0.85
        }.get(work_type, 1.0)

    def S_stress_psych(self, x):
        normalized = x / self.m_psych
        return self.k_psych * (normalized ** self.p_psych)

    def S_night_shift(self, t_work):
        angle = (2 * math.pi / 24) * (t_work - self.alpha_circ)
        return self.A_circ * (1 - math.cos(angle))

    def intensity_from_type(self, exercise_type):
        return {
            'none': 0,
            'low': 45,
            'moderate': 70,
            'high': 88
        }.get(exercise_type, 0)

    def delta_C_exercise(self, exercise_type, duration):
        I = self.intensity_from_type(exercise_type)
        if I < self.threshold_intensity:
            return -0.15
        else:
            return self.k_int * (I - self.threshold_intensity) + self.k_dur * duration

    def dampen_activity(self, delta_C_exercise):
        if delta_C_exercise < 0:
            return 1 - 0.25 * abs(delta_C_exercise) / 0.3
        else:
            return 1.0

    def daily_stress(self, d):
        S_work = self.S_work_hours(d['work_hours'])
        S_work *= self.k_work_type(d['work_type'])
        S_night = 0.0
        if d.get('work_night', False):
            t_work_start = d.get('work_start_hour', 22)
            S_night = self.S_night_shift(t_work_start)
        S_psych = self.S_stress_psych(d['work_stress'])
        delta_C = self.delta_C_exercise(d['exercise'], d.get('exercise_duration', 0))
        dampen = self.dampen_activity(delta_C)
        S_total = (S_work + S_night + S_psych) * dampen + delta_C
        return max(0, S_total)

    def periodic_stress(self, period_data):
        if len(period_data) < 1:
            raise ValueError("Требуется хотя бы 1 день")
        n = len(period_data)
        total = sum(self.daily_stress(d) for d in period_data)
        S_min = 0.0
        S_max = n * ( 0.856 + 0.8 + 0.35 + 0.5 )
        norm = (total - S_min) / (S_max - S_min) if S_max > S_min else 0
        norm = max(0.0, min(norm, 1.0))
        return round(norm * 10.0, 1)