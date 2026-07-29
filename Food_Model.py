class FoodModel:
    def __init__(self):
        self.k = {
            'quality': -0.4,
            'snacks': 0.5,
            'snack_quality': -0.3,
            'water': -0.2,
            'caffeine': 0.3,
            'alcohol': 0.6,
            'regularity': -0.3,
            'fermented': -0.2,
            'green_tea': -0.1,
            'magnesium': -0.1
        }
        self.max_vals = {
            'quality': 2,
            'snacks': 3,
            'snack_quality': 2,
            'water': 2,
            'caffeine': 3,
            'alcohol': 3,
            'regularity': 2
        }
        self.p = {
            'quality': 0.8,
            'snacks': 1.2,
            'snack_quality': 0.9,
            'water': 0.5,
            'caffeine': 1.1,
            'alcohol': 1.3,
            'regularity': 0.7
        }
        self.S_min = -11.0
        self.S_max = 10.0

    def _norm_pow(self, key, x):
        m = self.max_vals[key]
        v = max(0.0, min(x / m, 1.0))
        return v ** self.p[key]

    def _dampen_factor(self, water, regularity):
        f_water = self._norm_pow('water', water)
        f_regularity = self._norm_pow('regularity', regularity)
        return 1 - 0.15 * f_water - 0.1 * f_regularity

    def _synergy(self, quality, snacks):
        f_quality = self._norm_pow('quality', quality)
        f_snacks = self._norm_pow('snacks', snacks)
        return (1 - f_quality) * f_snacks * 0.1

    def daily_stress(self, d):
        S_protect = (
                self.k['quality'] * self._norm_pow('quality', d['quality']) +
                self.k['snack_quality'] * self._norm_pow('snack_quality', d['snack_quality']) +
                self.k['water'] * self._norm_pow('water', d['water']) +
                self.k['regularity'] * self._norm_pow('regularity', d['regularity'])
        )
        dampen = self._dampen_factor(d['water'], d['regularity'])
        synergy = self._synergy(d['quality'], d['snacks'])
        S_harmful = (
                            (self.k['snacks'] * self._norm_pow('snacks', d['snacks']) + synergy) +
                            self.k['caffeine'] * self._norm_pow('caffeine', d['caffeine']) +
                            self.k['alcohol'] * self._norm_pow('alcohol', d['alcohol'])
                    ) * dampen
        S_addit = 0.0
        for opt in ('fermented', 'green_tea', 'magnesium'):
            if d.get(opt, False):
                S_addit += self.k[opt]
        return S_protect + S_harmful + S_addit

    def periodic_stress(self, period_data):
        if len(period_data) < 1:
            raise ValueError("Нужно хотя бы 1 день.")
        n = len(period_data)
        total = sum(self.daily_stress(d) for d in period_data)
        S_min_adj = self.S_min * n / 7.0
        S_max_adj = self.S_max * n / 7.0
        norm = (total - S_min_adj) / (S_max_adj - S_min_adj)
        norm = max(0.0, min(norm, 1.0))
        return round(norm * 10.0, 1)