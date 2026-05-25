

class BKTModel:
    def __init__(self, p_init: float = 0.2, T: float = 0.15, G: float = 0.2, S: float = 0.05):
        """
        :param p_init: Initial mastery
        :param T: Learning rate
        :param G: Guess probability
        :param S: Slip probability
        """
        self.p_init = p_init
        self.T = T
        self.G = G
        self.S = S

        self.p = self.p_init
        self.p_history = [self.p_init]

    def reset(self):
        """
        Sets p back to initial mastery and resets the history.
        """
        self.p = self.p_init
        self.p_history = [self.p_init]

    def observe(self, correct: bool) -> float:
        # 1) Bayes update with observation
        if correct:
            # P(L | correct)
            numerator = self.p * (1 - self.S)
            denom = numerator + (1 - self.p) * self.G
            posterior = numerator / denom if denom > 0 else 0.0
        else:
            # P(L | incorrect)
            numerator = self.p * self.S
            denom = numerator + (1 - self.p) * (1 - self.G)
            posterior = numerator / denom if denom > 0 else 0.0

        # 2) Transition (learning)
        p_next = posterior + (1 - posterior) * self.T
        self.p = p_next
        self.p_history += [self.p]
        return self.p

    def expected_correct(self) -> float:
        """
        Probability of a correct response at current state.
        """
        return self.p * (1 - self.S) + (1 - self.p) * self.G
