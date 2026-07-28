import json
import os

MEMORY_FILE = "memory.json"


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)


def generate_response(user_input: str, memory: list) -> str:
    # TODO: Use PromptTemplate + LLM to generate a context-aware response
    # The `memory` list contains previous message dicts: {"role": "user|assistant", "text": "..."}
    return "This is a placeholder response. Replace with LLM call."


def main():
    memory = load_memory()
    print("Simple chat. Type 'exit' to quit.")
    while True:
        user = input("You: ")
        if user.strip().lower() in ("exit", "quit"):
            break
        memory.append({"role": "user", "text": user})
        reply = generate_response(user, memory)
        print("Bot:", reply)
        memory.append({"role": "assistant", "text": reply})
        save_memory(memory)


if __name__ == "__main__":
    main()
