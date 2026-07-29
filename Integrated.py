class IntegratedStressSystem:

    def __init__(self):
        sleep_weights = [0.35, 0.25, 0.20, 0.15, 0.05]
        sleep_power = sum(sleep_weights)

        food_k_values = [0.4, 0.5, 0.3, 0.2, 0.3, 0.6, 0.3, 0.2, 0.1, 0.1]
        food_power = sum(food_k_values)

        activity_k = [0.4, 0.35, 0.4, 0.008, 0.003]
        activity_power = sum(activity_k)

        emotion_k = [0.02, 0.035, 0.029, 0.03, 0.002813,0.003375]
        emotion_power = sum(emotion_k)

        total_power = sleep_power + food_power + activity_power + emotion_power

        self.base_weights = {
            'sleep': sleep_power / total_power,
            'food': food_power / total_power,
            'activity': activity_power / total_power,
            'emotion': emotion_power / total_power
        }

    def calculate_stress(self, sleep_score, food_score, activity_score, emotion_score):
        base_stress = (
                self.base_weights['sleep'] * sleep_score +
                self.base_weights['food'] * food_score +
                self.base_weights['activity'] * activity_score +
                self.base_weights['emotion'] * emotion_score
        )

        sleep_emotion_interaction = (
                self.base_weights['sleep'] * self.base_weights['emotion'] *
                (sleep_score * emotion_score / 100)
        )

        sleep_activity_interaction = (
                self.base_weights['sleep'] * self.base_weights['activity'] *
                (sleep_score * activity_score / 100)
        )

        activity_food_interaction = (
                self.base_weights['activity'] * self.base_weights['food'] *
                (activity_score * food_score / 100)
        )

        emotion_food_interaction = (
                self.base_weights['emotion'] * self.base_weights['food'] *
                (emotion_score * food_score / 100)
        )

        total_interaction = (
                sleep_emotion_interaction +
                sleep_activity_interaction +
                activity_food_interaction +
                emotion_food_interaction
        )

        final_stress = base_stress * (1 + min(total_interaction * 10, 0.3))

        return min(max(final_stress, 0), 10.0)

    def daily_stress(self, sleep_score, food_score, activity_score, emotion_score):
        return self.calculate_stress(sleep_score, food_score, activity_score, emotion_score)