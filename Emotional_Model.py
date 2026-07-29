class EmotionModel:
    def __init__(self):
        self.beta_sadness = 0.02
        self.beta_anxiety = 0.035
        self.beta_anger = 0.029
        self.p_emotion = 1.5
        self.beta_joy = 0.03
        self.k_social = (0.27 * 0.25) / 24
        self.k_isolation = (0.27 * 0.30) / 24

    def S_negative_emotions(self, sadness, anxiety, anger):
        sad_norm = sadness / 10.0
        anx_norm = anxiety / 10.0
        ang_norm = anger / 10.0
        sad_pow = self.beta_sadness * (sad_norm ** self.p_emotion)
        anx_pow = self.beta_anxiety * (anx_norm ** self.p_emotion)
        ang_pow = self.beta_anger * (ang_norm ** self.p_emotion)
        total_pow = sad_pow + anx_pow + ang_pow
        if total_pow == 0:
            return 0.0
        return total_pow

    def S_joy_protection(self, joy):
        joy_norm = joy / 10.0
        return -self.beta_joy * joy_norm

    def S_social_interaction(self, social_hours, isolation_hours):
        social_effect = self.k_social * social_hours
        isolation_effect = self.k_isolation * isolation_hours
        return social_effect + isolation_effect

    def daily_stress(self, d):
        S_neg = self.S_negative_emotions(
            d.get('sadness', 0),
            d.get('anxiety', 0),
            d.get('anger', 0)
        )
        S_joy = self.S_joy_protection(d.get('joy', 0))
        S_soc = self.S_social_interaction(
            d.get('social_hours', 0),
            d.get('isolation_hours', 0)
        )
        return S_neg + S_joy + S_soc

    def periodic_stress(self, period_data):
        if len(period_data) < 1:
            raise ValueError("Требуется хотя бы 1 день")
        n = len(period_data)
        total = sum(self.daily_stress(d) for d in period_data)
        S_min = -n * 0.1
        S_max = n * 0.27
        norm = (total - S_min) / (S_max - S_min) if (S_max - S_min) > 0 else 0
        norm = max(0.0, min(norm, 1.0))
        return round(norm * 10.0, 1)