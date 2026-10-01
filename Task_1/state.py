# Remembers what has happened in the conversation so far..

from dataclasses import dataclass, field
from Task_1 import config

@dataclass
class ConversationState:
    session_id: str  # Every chat has unique session_id.
    history: list = field(default_factory=list) # list of message
    negative_streak : int = 0 
    negative_since: object = None
    resolved: bool = False
    escalated: bool = False

    def add_message(self, role, content):  
        self.history.append({"role": role, "content": content})

    def update_with_analysis(self, analysis):
        sentiment = analysis["sentiment"]
        if sentiment in config.NEGATIVE_LABELS:
            self.negative_streak += 1
            self.resolved = False
            if self.negative_since is None:
                self.negative_since = config.get_now()
        elif sentiment == "positive":
            self.negative_streak = 0
            self.negative_since = None
            self.resolved = True
    
    def minute_negative(self):
        if self.negative_since is None:
            return 0
        return (config.get_now() - self.negative_since).total_seconds() / 60.0 