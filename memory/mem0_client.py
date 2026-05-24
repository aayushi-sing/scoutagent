'''import os
from mem0 import Memory


# Memory Configuration
config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "startup_memory",
            "path": "./memory_db"
        }
    }
}


# Initialise Memory
m = Memory.from_config(config)

USER_ID = "startup_scout_agent"


def save_research(topic: str, startups: list, summary: str):

    names = [s.get("name", "unknown") for s in startups]

    try:

        m.add(
            f"Researched topic: {topic}. "
            f"Startups found: {', '.join(names)}. "
            f"Summary: {summary[:300]}",
            user_id=USER_ID
        )

        return True

    except Exception as e:

        print(f"[Memory Save Error] {str(e)}")
        return False


def get_past_research(topic: str) -> str:

    try:

        results = m.search(
            topic,
            filters={"user_id": USER_ID},
            limit=5
        )

        if not results:
            return "No past research found."

        memories = []

        for r in results:

            memory_text = r.get("memory", "")

            if memory_text:
                memories.append(memory_text)

        return "PAST RESEARCH:\n" + "\n".join(memories)

    except Exception as e:

        return f"Memory error: {str(e)}"


def get_all_memories() -> list:

    try:

        return m.get_all(
            filters={"user_id": USER_ID}
        ) or []

    except Exception as e:

        print(f"[Get All Memories Error] {str(e)}")
        return []'''
import json
import os

MEMORY_FILE = "scout_memory.json"

def _load():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []

def _save(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def save_research(topic: str, startups: list, summary: str):
    try:
        memories = _load()
        names = [s.get("name", "unknown") for s in startups]
        memories.append({
            "topic": topic,
            "startups": names,
            "summary": summary[:300]
        })
        _save(memories)
    except Exception as e:
        print(f"[Memory Save Error] {str(e)}")

def get_past_research(topic: str) -> str:
    try:
        memories = _load()
        relevant = [m for m in memories if topic.lower() in m.get("topic", "").lower()]
        if not relevant:
            return "No past research found on this topic."
        lines = [f"Topic: {m['topic']} | Startups: {', '.join(m['startups'])}" for m in relevant[-3:]]
        return "PAST RESEARCH:\n" + "\n".join(lines)
    except Exception as e:
        return "No past research found."

def get_all_memories() -> list:
    try:
        return _load()
    except Exception as e:
        print(f"[Get All Memories Error] {str(e)}")
        return []