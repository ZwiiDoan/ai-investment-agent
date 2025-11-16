import uuid
from typing import TypedDict


class Message(TypedDict):
    role: str  # "user" | "ai"
    content: str


class ConversationMemory:
    """Simple in-memory conversation store. NOT persistent, for prototyping."""

    def __init__(self):
        self._store: dict[str, list[Message]] = {}

    def create_conversation(self) -> str:
        conversation_id = str(uuid.uuid4())
        self._store[conversation_id] = []
        return conversation_id

    def append(self, conversation_id: str, role: str, content: str) -> None:
        if conversation_id not in self._store:
            self._store[conversation_id] = []
        self._store[conversation_id].append({"role": role, "content": content})

    def get(self, conversation_id: str) -> list[Message]:
        return self._store.get(conversation_id, [])

    def last_n(self, conversation_id: str, n: int) -> list[Message]:
        return self.get(conversation_id)[-n:]


memory = ConversationMemory()
