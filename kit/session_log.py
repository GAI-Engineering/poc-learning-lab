"""Per-session logging to a plain dict row."""
import time
class SessionLog:
    def __init__(self, session_id):
        self.session_id = session_id
        self.start = time.time()
        self.turns = 0
        self.outcome = None
    def row(self):
        return {"session_id": self.session_id, "turns": self.turns,
                "elapsed_s": round(time.time() - self.start, 3), "outcome": self.outcome}
