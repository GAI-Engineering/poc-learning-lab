"""Transcript store: the transcript IS the state (POC 02 pattern)."""
import json
from pathlib import Path

class TranscriptStore:
    def __init__(self):
        self.messages = []
    def append(self, speaker, kind, content):
        msg = {"turn": len(self.messages) + 1, "speaker": speaker, "kind": kind, "content": content}
        self.messages.append(msg)
        return msg
    def save_jsonl(self, path):
        # newline="\n": the same bytes on every OS (Windows would otherwise write CRLF; .gitattributes keeps runs/ LF)
        Path(path).write_text("\n".join(json.dumps(m) for m in self.messages) + "\n", newline="\n")
    def __len__(self):
        return len(self.messages)
