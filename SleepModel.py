import math


class SleepModel:
    def __init__(self):
        self.opt_sleep = 7.75

    def time_to_hours(self, ts):
        h, mnt = map(int, ts.split(':'))
        return float(h) + float(mnt) / 60.0

    def daily_metrics(self, bed, wake):
        b = self.time_to_hours(bed)
        w = self.time_to_hours(wake)
        if w < b:
            w += 24
        duration = w - b
        deficit = max(0.0, self.opt_sleep - duration)
        mid = (b + w) / 2.0 % 24
        circ_align = min(abs(mid - 3.0), 24 - abs(mid - 3.0))
        return duration, deficit, mid, circ_align

    def periodic_stress(self, schedule):
        if len(schedule) < 1:
            raise ValueError("Требуется хотя бы 1 день.")
        n = len(schedule)
        deficits = []
        circs = []
        mids = []
        wd, we = [], []
        for i, (b, w) in enumerate(schedule):
            duration, deficit, mid, circ = self.daily_metrics(b, w)
            deficits.append(deficit)
            circs.append(circ)
            mids.append(mid)
            if i < n - 2:
                wd.append(mid)
            else:
                we.append(mid)
        debt = sum(deficits)
        avg_circ = sum(circs) / n
        corr = [(m - 24) if m > 12 else m for m in mids]
        avg_mid = sum(corr) / n
        var = math.sqrt(sum((x - avg_mid) ** 2 for x in corr) / n)
        if wd and we:
            jet = abs(sum(we) / len(we) - sum(wd) / len(wd))
        else:
            jet = 0.0
        day_def = sum(deficits) / n

        def norm(v, m):
            return min(v / m, 1.0)

        nm = {
            'debt': norm(debt, 10.0 * n),
            'circ': norm(avg_circ, 3.0),
            'var': norm(var, 2.0),
            'jet': norm(jet, 3.0),
            'day_def': norm(day_def, 2.0)
        }
        weights = {
            'debt': 0.35,
            'circ': 0.25,
            'var': 0.20,
            'jet': 0.15,
            'day_def': 0.05
        }
        score = sum(weights[k] * nm[k] for k in nm) * 10.0
        return {
            'stress_score': round(score, 1),
            'num_days': n,
            'metrics': {
                'debt': round(debt, 2),
                'circ': round(avg_circ, 2),
                'var': round(var, 2),
                'jet': round(jet, 2),
                'day_def': round(day_def, 2)
            },
            'normalized': nm
        }