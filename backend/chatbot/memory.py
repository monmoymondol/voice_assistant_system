# backend/chatbot/memory.py
class ConversationMemory:
    def __init__(self, max_turns=10):
        self.sessions = {}
        self.max_turns = max_turns

    def get_context(self, user_id: str):
        return self.sessions.get(user_id, [])

    def update(self, user_id: str, message: str, response: str):
        if user_id not in self.sessions:
            self.sessions[user_id] = []
        self.sessions[user_id].append({"user": message, "bot": response})
        if len(self.sessions[user_id]) > self.max_turns:
            self.sessions[user_id] = self.sessions[user_id][-self.max_turns:]
