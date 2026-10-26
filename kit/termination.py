"""Termination caps and typed exits."""
class Termination:
    def __init__(self, max_turns=20, signal=None):
        self.max_turns = max_turns
        self.signal = signal
        self.turns = 0
    def check(self, text):
        self.turns += 1
        if self.signal and text.strip().endswith(self.signal):
            return "SIGNAL"
        if self.turns >= self.max_turns:
            return "CAP_TURNS"
        return None
